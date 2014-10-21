import tgt, os, pprint
from markov import MarkovGenerator

class TextGrid(object):
 	
	def __init__(self):
		self.pp = pprint.PrettyPrinter(indent=4)
		self.generator = MarkovGenerator(n=1, max=3)

		self.path = '../textGrids'
		#let's get the text from the textGrids, save the annotations in a dict, key=filename
		self.annotations = dict()

		for tgFile in os.listdir(self.path):
			if tgFile[-9:] == '.TextGrid':
				#print tgFile
				tg = tgt.read_textgrid(self.path + '/' + tgFile)
				file_annotations = [i for t in tg.tiers for i in t]
				for a1, a2 in zip(file_annotations, file_annotations[1:]):
					filename = tgFile[:-9]
					self.annotations[a1] = filename
					self.feedMarkov(a1,a2)

		# pp.pprint(self.generator.ngrams)
			#startTime = int(a.start_time*1000)
			#endTime = int(a.end_time*1000)
			#duration = int(a.duration()*1000)
		

	def generateText(self):
		output = list()
		for i in range(4):
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