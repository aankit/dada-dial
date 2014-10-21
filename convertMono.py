#convertMono
import os
import scipy.io.wavfile as wf

for poem in os.listdir('./wav'):
	rate, data = wf.read("./wav/" + poem)
	mono = data[:,0]
	wf.write("./mono/" + poem, rate, mono)