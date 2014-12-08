import os
from scipy.io.wavfile import read
from numpy import sqrt, mean, log10

path = '/Users/Aankit/Documents/Redial/cutups/'

for chunk in os.listdir(path)[1:]:
	chunk = path+chunk
	samprate, wavdata = read(chunk)
	dbs = 20*log10( sqrt(mean(wavdata**2)) )
	max_val = max(wavdata)
	min_val = min(wavdata)
	print max_val
	print min_val