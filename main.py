#main program 

from textGrid import TextGrid

tg = TextGrid()

#data structures:
# - tg.annotations
# 	- tokens, including punctuation
#	- co-occurences
#	- ngrams
# - wav files
#	- path = ./finalAudio/filename.wav

structure = tg.generateText()

for line in structure:
	for interval in line:
		segment = (interval.start_time, interval.end_time)
		filename = tg.annotations[interval]
		

		
