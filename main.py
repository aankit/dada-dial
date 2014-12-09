#!/usr/bin/env python

#Dada Dial
#ITP Redial Midterm
#by Aankit Patel

from textGrid import TextGrid
from pydubtools import PoemBuilder
import sys, os
import pickle

path = '/root/dada-dial'

f = open(path + '/poemInfo.p', 'rb')
poemInfo = pickle.load(f)

print poemInfo

tg = TextGrid(path)
segmenter = PoemBuilder(path)

sounds_path = path + '/sounds/'

structure = tg.generateText(4)

#create new wav file for our poem
attribution = ''
for line in structure:
	# print line
	for interval in line:
		filename = tg.annotations[interval.text][0]
		poet = [poem['poet'] for poem in poemInfo if poem['filename'][:-4]==filename]
		title = [poem['title'] for poem in poemInfo if poem['filename'][:-4]==filename]
		attribution += '%s by %s |' % (title, poet)
		segmenter.poem += segmenter.get_slice(filename, interval.start_time, interval.end_time)

filename = 'poem.wav'
segmenter.exportFile(sounds_path, filename)

# os.system('/home/abp225/ruby/attributePoets.rb callerId attribution')
