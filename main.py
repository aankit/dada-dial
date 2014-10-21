#Dada Dial
#ITP Redial Midterm
#by Aankit Patel

from textGrid import TextGrid
from audioSegmenter import AudioSegmenter
import time

tg = TextGrid()
segmenter = AudioSegmenter()


structure = tg.generateText()

#create new wav file for our poem

for line in structure:
	print line
	for interval in line:
		filename = tg.annotations[interval.text][0]
		segmenter.poem += segmenter.cut(filename, interval.start_time, interval.end_time)

currentTime = time.time()
filename = str(currentTime) + 'poem.wav'
segmenter.exportFile(filename)
# print filename



		
