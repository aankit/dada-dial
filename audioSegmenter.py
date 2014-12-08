#!/usr/bin/env python

from pydub import AudioSegment, silence
import math
	
class AudioSegmenter(object):
	
	def __init__(self, path):
		self.path = path + '/final_audio/'
		self.poem = AudioSegment.from_wav(self.path + 'seedPoem.wav')
		print 'initialized'

	def cut(self, filename, start, end):
		audio = AudioSegment.from_wav(self.path + filename + '.wav')
		start = int(start*1000)
		end = int(end*1000)
		# curr = time.time()
		# audio[start:end].export(path + str(curr) + "file.wav", format="wav")
		return audio[start:end]

	def concatenate(self, first, second):
		return first + second

	def exportFile(self, sounds_path, filename):
		self.poem = self.poem.set_frame_rate(8000)
		self.poem.export(sounds_path + filename, format="wav")

if __name__ == '__main__':
	segmenter = AudioSegmenter()
	segmenter.cutbySilence('The-Dial-A-Poem-Poets_30_ginsberg.wav')
