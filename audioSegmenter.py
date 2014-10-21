from pydub import AudioSegment
from pydub.utils import db_to_float

	
class AudioSegmenter(object):
	
	def __init__(self):
		self.path = '../final_audio/'

	def cut(self, filename, interval):
		audio = AudioSegment.from_wav(self.path + filename)
		interval
		audio.



	def cutbySilence(self, filename):
		# Let's load up the audio we need...
		audio = AudioSegment.from_wav(self.path +filename)
		# Let's consider anything that is 30 decibels quieter than
		# the average volume of the podcast to be silence
		average_loudness = audio.rms
		silence_threshold = average_loudness

		# filter out the silence
		audio_parts = (ms for ms in audio if ms.rms > silence_threshold)

		# combine all the chunks back together
		audio = reduce(lambda a, b: a + b, audio_parts)

		# add on the bumpers
		# podcast = intro + podcast + outro

		# save the result
		audio.export(self.path + filename, format="wav")

if __name__ == '__main__':
	segmenter = AudioSegmenter()
	segmenter.cutbySilence('The-Dial-A-Poem-Poets_30_ginsberg.wav')