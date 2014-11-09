#!/usr/bin/env python

import tgt, os, pprint
from markov import MarkovGenerator

class TextGrid(object):
 	
	def __init__(self, path):
		# pp = pprint.PrettyPrinter(indent=4)
		self.generator = MarkovGenerator(n=1, max=3)

		self.path = path + '/textGrids/'
		#let's get the text from the textGrids, save the annotations in a dict, key=filename
		self.annotations = dict()

		for tgFile in os.listdir(self.path):
			if tgFile[-9:] == '.TextGrid':
				#print tgFile
				tg = tgt.read_textgrid(self.path + tgFile)
				file_annotations = [i for t in tg.tiers for i in t]
				for i in range(len(file_annotations)):
					a1 = file_annotations[i]
					filename = tgFile[:-9]
					self.annotations[a1.text] = (filename, a1)
					if i == len(file_annotations)-1:
						continue
					else:
						a2 = file_annotations[i+1]
						self.feedMarkov(a1,a2)

		# pp.pprint(self.annotations)
		

	def generateText(self, numLines):
		output = list()
		for i in range(numLines):
			 output.append(self.generator.generate())
		return output

	def feedMarkov(self, a1, a2):
		a1.text = a1.text.strip()
		a2.text = a2.text.strip()
		endFirst = a1.text[-1]
		startSecond = a2.text[0]
		first = (endFirst, a1)
		second = (startSecond, a2)
		self.generator.feed(first, second)
