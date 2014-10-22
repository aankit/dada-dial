#!/usr/bin/env python

#Dada Dial
#ITP Redial Midterm
#by Aankit Patel

from textGrid import TextGrid
from audioSegmenter import AudioSegmenter
import sys, os
import pickle

path = '/home/abp225'

callerId = sys.argv[1]

f = open(path + '/asterisk_agi/poemInfo.p', 'rb')
poemInfo = pickle.load(f)
f.close()

# print poemInfo

tg = TextGrid(path)
segmenter = AudioSegmenter(path)

sounds_path = '/home/abp225/asterisk_sounds/'

structure = tg.generateText()

#create new wav file for our poem
attribution = ''
for line in structure:
	# print line
	for interval in line:
		filename = tg.annotations[interval.text][0]
		poet = [poem['poet'] for poem in poemInfo if poem['filename'][:-4]==filename]
		title = [poem['title'] for poem in poemInfo if poem['filename'][:-4]==filename]
		attribution += '%s by %s |' % (title, poet)
		segmenter.poem += segmenter.cut(filename, interval.start_time, interval.end_time)

filename = 'poem.wav'
segmenter.exportFile(sounds_path, filename)
os.system('/home/abp225/ruby/attributePoets.rb callerId attribution')