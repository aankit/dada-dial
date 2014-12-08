#download and conversion of mp3 to wav
from pydub import AudioSegment
import wave, urllib, re
from urlparse import urlparse
from bs4 import BeautifulSoup
import requests

ubu_url = 'http://www.ubu.com/sound'
ubu_sound_html = requests.get(ubu_url)
ubu_sound = BeautifulSoup(ubu_sound_html.text)
links = ubu_sound.findAll('a')
#first link is home
for link in links[1:2]:
	#the first character in the link refers to base url
	link = ubu_url + link.get('href')[1:]
	r = requests.get(link)
	soup = BeautifulSoup(r.text)
	poemLinks = [a['href'] for a in soup.findAll('a',href=re.compile('http.*\.mp3'))]
	opener = urllib.URLopener()
	for poemLink in poemLinks[:3]: 
		print poemLink
		filename = urlparse(poemLink).path.split('/')[-1]
		opener.retrieve(poemLink, './temp/' + filename)
		poem = AudioSegment.from_mp3('./temp/' + filename)
		poem = poem.set_channels(1)
		poem = poem.set_frame_rate(8000)
		filename = filename[:-4] + '.wav'
		poem.export('./ubu/' + filename, format='wav')
	# rate, data = wf.read("./wav/" + filename)
	# mono = data[:,0]
	# wf.write(".mono/" + filename, rate, mono)
	
	# average the two channels - didn't work for this audio
	# wr = wave.open('./wav/'+ filename,'r')
	# nchannels, sampwidth, framerate, nframes, comptype, compname =  wr.getparams()
	# filename = filename[:-4] + '_mono.wav'
	# ww = wave.open('./mono/' + filename,'wb')
	# ww.setparams((1,sampwidth,framerate,nframes,comptype,compname))
	# frames = wr.readframes(wr.getnframes()-1)
	# new_frames = ''
	# for s1 in frames[0::2],frames[1::2]):
	# 	new_frames += stereo_to_mono(s1,s2)[2:].zfill(2).decode('hex')
	# ww.writeframes(new_frames)