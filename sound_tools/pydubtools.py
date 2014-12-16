#!/usr/bin/env python

from pydub import AudioSegment, silence
import math
	
class PoemBuilder(object):
	
	def __init__(self, path):
		self.path = path + '/final_audio/'
		self.poem = AudioSegment.from_wav(self.path + 'seedPoem.wav')
		print 'initialized'

	def get_slice(self, filename, start, end):
		audio = AudioSegment.from_wav(self.path + filename + '.wav')
		start = int(start*1000)
		end = int(end*1000)
		# curr = time.time()
		# audio[start:end].export(path + str(curr) + "file.wav", format="wav")
		return audio[start:end]

	def concatenate(self, first, second):
		return first + second

	def addtoFile(self, path_to_file):
		new_audio = AudioSegment.from_wav(path_to_file)
		print new_audio.duration_seconds
		self.poem += new_audio

	def exportFile(self, sounds_path, filename):
		self.poem = self.poem.set_frame_rate(8000)
		self.poem.export(sounds_path + filename, format="wav")

class Tools(object):

	def __init__(self, sounds_path, filename):
		self.path = sounds_path
		self.filename = filename
		self.audio = AudioSegment.from_wav(self.path + self.filename)

	def cutbySilence(self, min_silence_len=1000, r=1):
		#using dBFS to normalize the silence across files
		silence_thresh = self.audio.dBFS - 5/r
		audio_splits = silence.split_on_silence(self.audio,
		 	min_silence_len=min_silence_len, 
		 	keep_silence=150, 
		 	silence_thresh=-16)
		#cuts that are still too long, maybe an area of higher overall dBFS
		long_splits = [split for split in audio_splits if math.floor(split.duration_seconds)>20]
		if r != 2:
			for split in long_splits:
				audio_splits.remove(split)
				#cut recursively
				new_splits = self.cutbySilence(split, r=r+1)
				for ns in new_splits:
					audio_splits.append(ns)
		#clean the cuts of anything too short
		audio_splits = [split for split in audio_splits if math.floor(split.duration_seconds)>.5]
		return audio_splits

	def silenceLengths(self, r=1):
		silence_thresh = self.audio.dBFS - 4/r
		silence_ranges = silence.detect_silence(self.audio,
			min_silence_len=1000,
			keep_silence=150,
			silence_thresh=silence_thresh)
		silence_lengths = []
		for sr in silence_ranges:
			silence_lengths.append(sr[1]-sr[0])
		return silence_lengths

if __name__ == '__main__':
	segmenter = Tools('./sounds/', 'The-Dial-A-Poem-Poets_01_ginsberg.wav')
	segmenter.cutbySilence()
