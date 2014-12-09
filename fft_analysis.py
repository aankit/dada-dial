import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy, math
import pandas as pd

class harmonics(object):
	
	def __init__(self, file_obj):
		sampFreq, snd = wavfile.read('/Users/Aankit/Documents/Redial/cutups/The-Dial-A-Poem-Poets_12_kandel034.wav')
		snd = snd / (2.**15)

		timeArray = numpy.arange(0, snd.shape[0], 1)
		timeArray = timeArray / sampFreq
		timeArray = timeArray * 1000  #scale to milliseconds

		#ipython specific! maybe run with ipython?
		# get_ipython().magic(u'matplotlib inline')

		p = numpy.fft.fft(snd) #the FFT transform...how to speed this up? FFTW will do this in C
		n = float(len(snd)) #number of samples?

		nUniquePts = math.ceil((n+1)/2.0)
		p = p[0:nUniquePts] #what does this part do?
		p = abs(p)
		p = p / n
		p = p**2

		if n % 2 > 0:
		    p[1:len(p)] = p[1:len(p)] * 2
		else:
		    p[1:len(p) -1] = p[1:len(p) - 1] * 2  
		freqArray = numpy.arange(0, nUniquePts, 1.0) * (sampFreq / n)
		df = pd.DataFrame(p, index=freqArray, columns=['power'])
		fundamental = df[df.power==df.power.max()].index[0]
		harmonic_frequencies = numpy.arange(fundamental, 1500, fundamental)
		harmonics = df[df.index.isin(harmonic_frequencies)]




notes = {
'F': 87.31,
'F#': 92.50,
'G': 98.00,
'G#': 103.8,
'A':110.0,
'Bb': 116.5,
'B': 123.5,
'C':130.8,
'C#': 138.6,
'D':146.8,
'Eb' :155.6,
'E':164.8,
'F': 174.6,
'F#': 185.0,
'G':196.0,
'G#':207.7,
'A':220.0,
'Bb':233.1,
'B':246.9
}
