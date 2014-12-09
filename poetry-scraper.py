#download and conversion of mp3 to wav
from pydub import AudioSegment, silence
from urllib import URLopener
import re, os, math, numpy, requests
from urlparse import urlparse
from bs4 import BeautifulSoup
from scipy.io import wavfile
import pandas as pd
from dadasql.database import Base, db_session, engine
from dadasql.model import Line
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

#db setup


#file paths
final_audio = './ubu/'
temp = './temp/'

def fft_harmonics(filepath):
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
	harmonic_frequencies = numpy.arange(fundamental, 3400, fundamental) #telephony will not pick < 300Hz
	harmonics = df[df.index.isin(harmonic_frequencies)]
	return harmonics.itertuples()

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

#create a dict of poems or potentially a database, in the future
poem_dict = {}

#first link is home
for link in links[1:2]:
	#the first character in the link refers to base url
	link = ubu_url + link.get('href')[1:]
	r = requests.get(link)
	soup = BeautifulSoup(r.text)
	poemLinks = [a['href'] for a in soup.findAll('a',href=re.compile('http.*\.mp3'))]
	opener = URLopener()
	for poemLink in poemLinks[:6]: 
		print poemLink
		#download and save file to temp file
		filename = urlparse(poemLink).path.split('/')[-1]
		opener.retrieve(poemLink, temp + filename)
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
			line_num += 1
			line_filename = filename[:-4] + leadingZeros(line_num) + '.wav'
			print line_filename
			#save the lines...oh sweet golden, delicious lines
			wave = line.export(final_audio + line_filename, format='wav')
			#save the fundamental + harmonics info
			line_harmonics = fft_harmonics(final_audio + line_filename)
			try:
				l = db_session.query(Line.filename).filter_by(filename=line_filename).one()
			except MultipleResultsFound:
				pass
			except NoResultFound:
				for frequency, power in line_harmonics:
					l_obj = Line(filename=line_filename, 
						linenum= line_num, 
						frequency=round(frequency,4), 
						power=round(power, 4)
					)
					print l_obj
					db_session.add(l_obj)
					db_session.commit()
					print 'success'

				
print poem_dict









