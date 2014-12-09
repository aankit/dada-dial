#download and conversion of mp3 to wav
from pydub import AudioSegment, silence
from urllib import URLopener
import re, os, math, numpy, requests, urllib
from urlparse import urlparse
from bs4 import BeautifulSoup
from scipy.io import wavfile
import pandas as pd
from dadasql.database import db_session
from dadasql.model import Line, Fundamental, DBFS, Duration, Poem
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

#file paths
final_audio = '/root/dada-dial/ubu/'
temp = '/root/dada-dial/temp/'

def fundamental_fft(filepath):
	sampFreq, snd = wavfile.read(filepath)
	snd = snd / (2.**15)
	timeArray = numpy.arange(0, snd.shape[0], 1)
	timeArray = timeArray / sampFreq
	timeArray = timeArray * 1000  #scale to milliseconds

	#ipython specific! maybe run with ipython?
	# get_ipython().magic(u'matplotlib inline')

	p = numpy.fft.fft(snd) #amplitude in frequency domains
	n = float(len(snd)) #number of samples, amplitude in the time domain

	nUniquePts = math.ceil((n+1)/2.0)
	#err....
	p = p[0:nUniquePts] 
	p = abs(p)
	p = p / n
	p = p**2
	if n % 2 > 0:
		p[1:len(p)] = p[1:len(p)] * 2
	else:
		p[1:len(p) -1] = p[1:len(p) - 1] * 2  
	
	freqArray = numpy.arange(0, nUniquePts, 1.0) * (sampFreq / n)
	df = pd.DataFrame(p, index=freqArray, columns=['power'])
	fundamental = df[df.power==df.power.max()].index[0]
	#hack to deal with telephony Hz range of 300-3400, ala missing fundamentals
	if fundamental < 300.0: #telephony cut-off
		multiplier = math.ceil(300.0/fundamental) #use harmonic above 300
		if multiplier <=1: multiplier = 2
		fundamental = fundamental * multiplier
		return fundamental
	else:
		return fundamental
	# harmonic_frequencies = numpy.arange(fundamental, 3400, fundamental) #telephony will not pick < 300Hz
	# harmonics = df[df.index.isin(harmonic_frequencies)]
	# return harmonics.itertuples()

def cutbySilence(audio, r=1):
	#using dBFS to normalize the silence across files
	silence_thresh = audio.dBFS - 4/r
	audio_splits = silence.split_on_silence(audio,
	 	min_silence_len=1000, 
	 	keep_silence=150, 
	 	silence_thresh=silence_thresh)
	#cuts that are still too long, maybe an area of higher overall dBFS
	long_splits = [split for split in audio_splits if math.floor(split.duration_seconds)>20]
	if r != 2:
		for split in long_splits:
			audio_splits.remove(split)
			#cut recursively
			new_splits = cutbySilence(split, r=r+1)
			for ns in new_splits:
				audio_splits.append(ns)
	#clean the cuts of anything too short
	audio_splits = [split for split in audio_splits if math.floor(split.duration_seconds)>.5]
	return audio_splits

def leadingZeros(num, r=1):
	leaders = '0'*(3-len(str(num)))
	str_num = '_' + leaders + str(num)
	return str_num


#just attacking ubuweb from now, maybe expanding from here
ubu_url = 'http://www.ubu.com/sound'
ubu_sound_html = requests.get(ubu_url)
ubu_sound = BeautifulSoup(ubu_sound_html.text)
links = ubu_sound.findAll('a')

#first link is home
for link in links[1:]:
	#the first character in the link refers to base url
	print link
	clean_link = link.get('href')[1:]
	print clean_link
	if clean_link[0] == '.':
		clean_link = clean_link[1:]
	req_link = ubu_url + clean_link
	print req_link
	r = requests.get(req_link)
	soup = BeautifulSoup(r.text)
	poemLinks = [a['href'] for a in soup.findAll('a',href=re.compile('http.*\.mp3'))]
	opener = URLopener()
	for poemLink in poemLinks: 
		try:
			pl = db_session.query(Poem).filter_by(poem=poemLink).one()
		except NoResultFound:
			p_obj = Poem(poem=poemLink)
			db_session.add(p_obj)
			print 'added poem %s' %poemLink
			db_session.commit()
			#download and save file to temp file
			#make sure its not massive
			d = urllib.urlopen(poemLink)
			if int(d.info()['Content-Length']) > 25000000: #arbitrary length, could be better
				continue
			filename = urlparse(poemLink).path.split('/')[-1]
			try:
				opener.retrieve(poemLink, temp + filename)
			except:
				continue
			#open and convert file to mono, 8000Hz
			poem = AudioSegment.from_mp3(temp + filename)
			poem = poem.set_channels(1)
			poem = poem.set_frame_rate(8000)
			#erase temp file
			os.remove(temp + filename)
			#cut the poem into lines based on silence
			lines = cutbySilence(poem)
			#number the lines
			line_num = 0
			for line in lines:
				if line.duration_seconds > 30:
					continue
				line_num += 1
				line_filename = filename[:-4] + leadingZeros(line_num) + '.wav'
				#save the lines...oh sweet golden, delicious lines
				wave = line.export(final_audio + line_filename, format='wav')
				#get the fundamental + harmonics info
				frequency  = fundamental_fft(final_audio + line_filename)
				if math.isnan(frequency):
					continue
				print frequency, line.dBFS, line.duration_seconds
				try:
					l = db_session.query(Line.filename).filter_by(filename=line_filename).one()
				except MultipleResultsFound:
					pass
				except NoResultFound:
					try:
						f_obj = db_session.query(Fundamental).filter_by(frequency=int(frequency)).one()
					except NoResultFound:
						f_obj = Fundamental(frequency=int(frequency))
						db_session.add(f_obj)
						db_session.commit()
					try:
						db_obj = db_session.query(DBFS).filter_by(dbfs=int(line.dBFS)).one()
					except NoResultFound:
						db_obj = DBFS(dbfs=int(line.dBFS))
						db_session.add(db_obj)
						db_session.commit()
					try:
						d_obj = db_session.query(Duration).filter_by(duration=int(line.duration_seconds)).one()
					except NoResultFound:
						d_obj = Duration(duration=int(line.duration_seconds))
						db_session.add(d_obj)
						db_session.commit()
					print 'attributes committed'
					try:
						l_obj = Line(filename=line_filename, 
							fundamental_id = f_obj.id,
							dbfs_id = db_obj.id,
							duration_id = d_obj.id
						)
						print l_obj.filename, l_obj.fundamental_id, l_obj.dbfs_id, l_obj.duration_id
						db_session.add(l_obj)
						db_session.commit()
						print 'success, line committed'
					except Exception,e:
						print str(e)
						print 'failed to add line'
						db_session.rollback()
				except Exception,e:
					print str(e)
					print 'failed to add audio objects'








