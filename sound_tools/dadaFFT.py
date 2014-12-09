from scipy.io import wavfile
import pandas as pd
import math, numpy

class dadaFFT(object):

	def __init__(self, filepath):
		self.sampFreq, self.snd = wavfile.read(filepath)
		self.fundamental_fft()

	def fundamental_fft(self):
		snd = self.snd / (2.**15)
		timeArray = numpy.arange(0, snd.shape[0], 1)
		timeArray = timeArray / self.sampFreq
		timeArray = timeArray * 1000  #scale to milliseconds

		#ipython specific! maybe run with ipython?
		# get_ipython().magic(u'matplotlib inline')

		p = numpy.fft.fft(snd) #amplitude in frequency domains
		n = float(len(snd)) #number of samples, amplitude in the time domain

		nUniquePts = math.ceil((n+1)/2.0)
		#err....
		p = p[0:nUniquePts] 
		p = abs(p)
		p = p / n
		p = p**2
		if n % 2 > 0:
			p[1:len(p)] = p[1:len(p)] * 2
		else:
			p[1:len(p) -1] = p[1:len(p) - 1] * 2  
		
		self.freqArray = numpy.arange(0, nUniquePts, 1.0) * (self.sampFreq / n)
		self.fft_data = pd.DataFrame(p, index=self.freqArray, columns=['power'])
		self.fundamental = self.fft_data[self.fft_data.power==self.fft_data.power.max()].index[0]
		self.harmonic_frequencies = numpy.arange(self.fundamental, 3400, self.fundamental) #telephony will not pick < 300Hz
		self.harmonics = self.fft_data[self.fft_data.index.isin(self.harmonic_frequencies)]


	def fundamental(self):
		return (self.fundamental, self.fft_data.get_value(self.fundamental, col='power'))

	def harmonics(self):
		return self.harmonics.itertuples()