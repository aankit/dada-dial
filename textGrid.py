import tgt, os
from markov import MarkovGenerator

class TextGrid(object):
 	
	def __init__(self):
		self.generator = MarkovGenerator(n=1, max=8)

		self.path = './textGrids'
		#let's get the text from the textGrids, save the annotations in a dict, key=filename
		self.annotations = dict()

		for tgFile in os.listdir(self.path):
			if tgFile[-9:] == '.TextGrid':
				#print tgFile
				tg = tgt.read_textgrid(self.path + '/' + tgFile)
				file_annotations = [i for t in tg.tiers for i in t]
				file_text = []
				for a, b in zip(file_annotations, file_annotations[1:]):
					filename = tgFile[:-9]
					self.annotations[a] = filename
					a.text = a.text.strip()
					b.text = b.text.strip()
					print "a:", a.text, a.start_time, a.end_time
					print "b:", b.text, b.start_time, b.end_time
					file_text += a.text
				text = " ".join(file_text)
				self.generator.feed(text)
			#startTime = int(a.start_time*1000)
			#endTime = int(a.end_time*1000)
			#duration = int(a.duration()*1000)
		

	def generateText(self):
		for i in range(14):
			self.generator.generate()

