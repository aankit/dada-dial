#download and conversion of mp3 to wav
from pydub import AudioSegment, silence
import urllib, re, os, math
from urlparse import urlparse
from bs4 import BeautifulSoup
import requests

def cutbySilence(audio, r=1):
	silence_thresh = audio.dBFS - 4/r
	audio_splits = silence.split_on_silence(audio, min_silence_len=1000, silence_thresh=silence_thresh)
	long_splits = [split for split in audio_splits if math.floor(split.duration_seconds)>15]
	for split in long_splits:
		audio_splits.remove(split)
		#cut recursively
		new_splits = cutbySilence(split, r=r+1)
		for ns in new_splits:
			audio_splits.append(ns)
	audio_splits = [split for split in audio_splits if math.floor(split.duration_seconds)<.5]
	return audio_splits

def leadingZeros(num, r=1):
	leaders = '0'*(3-len(str(num)))
	str_num = leaders + str(num)
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
	opener = urllib.URLopener()
	for poemLink in poemLinks[:3]: 
		print poemLink
		#download and save file to temp file
		filename = urlparse(poemLink).path.split('/')[-1]
		opener.retrieve(poemLink, './temp/' + filename)
		#open and convert file to mono, 8000Hz
		poem = AudioSegment.from_mp3('./temp/' + filename)
		poem = poem.set_channels(1)
		poem = poem.set_frame_rate(8000)
		#erase temp file
		os.remove('./temp/' + filename)
		#cut the poem into lines based on silence
		lines = cutbySilence(poem)
		#number the lines
		line_num = 0
		poem_dict[filename] = []
		for line in lines:
			line_num += 1
			filename = filename[:-4] + leadingZeros(linenum) + '.wav'
			poem.export('./ubu/' + filename, format='wav')