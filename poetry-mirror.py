from sound_tools.pydubtools import PoemBuilder, Tools
from sound_tools.dadaFFT import dadaFFT
from dadasql.database import db_session
from dadasql.model import Line, Duration, Fundamental, DBFS

path = '/root/dada-dial/sounds/'
filename = 'user.wav'
#create pydub audio file
user_audio = Tools(path, filename)

user_splits = user_audio.cutbySilence()
split_durations = [int(s.duration_seconds) for s in user_splits]
split_dbfs = [int(s.dBFS) for s in user_splits]
split_fundamentals = []
for s in user_splits:
	s.export(path + 'temp.wav', format='wav')
	s_fft = dadaFFT(path+'temp.wav')
	fundamental, power = s_fft.get_fundamental()
	split_fundamentals.append(int(fundamental))
#got all the user input information, now we need to find lines that match
for duration in split_durations:
	duration_results = 