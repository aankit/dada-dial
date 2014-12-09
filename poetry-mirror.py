from sound_tools.pydubtools import PoemBuilder, Tools
from sound_tools.dadaFFT import dadaFFT

path = '/root/dada-dial/sounds/'
filename = 'user.wav'
#create pydub audio file
user_audio = Tools(path, filename)

user_splits = user_audio.cutbySilence()
split_durations = [s.duration_seconds for s in user_splits]
split_dbfs = [s.dBFS for s in user_splits]
split_fundamentals = []
for s in user_splits:
	s.export(path + 'temp.wav', format='wav')
	s_fft = dadaFFT(path+'temp.wav')
	fundamental = s_fft.fundamental()
	split_fundamentals.append(fundamental)

print split_fundamentals
print split_dbfs
print split_durations




