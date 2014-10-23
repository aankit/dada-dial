#download and conversion of mp3 to wav
from pydub import AudioSegment
import wave, urllib, re
from urlparse import urlparse
from bs4 import BeautifulSoup

#functions
def stereo_to_mono(hex1, hex2):
    #average two hex string samples
    return hex((ord(hex1) + ord(hex2))/2)

urls = [
	'http://www.ubu.com/sound/dial.html'
]

soup = BeautifulSoup(urllib.urlopen(urls[0]).read())
poemLinks = [a['href'] for a in soup.findAll('a',href=re.compile('http.*\.mp3'))]
opener = urllib.URLopener()
for link in poemLinks[1:1]: 
	filename = urlparse(link).path.split('/')[-1]
	opener.retrieve(link, './mp3/' + filename)
	poem = AudioSegment.from_mp3("./mp3/" + filename)
	filename = filename[:-4] + '.wav'
	poem.export("./wav/" + filename, format="wav")
	rate, data = wf.read("./wav/" + filename)
	mono = data[:,0]
	wf.write(".mono/" + filename, rate, mono)
	
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