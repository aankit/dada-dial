from sound_tools.pydubtools import PoemBuilder, Tools
from sound_tools.dadaFFT import dadaFFT
from dadasql.database import db_session
from dadasql.model import Line, Fundamental, DBFS, Duration
from sqlalchemy.orm.exc import NoResultFound
import random

path = '/root/dada-dial/sounds/'
filename = 'user.wav'
#create pydub audio file
user_audio = Tools(path, filename)

user_rests = user_audio.silenceLengths()
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
#match on duration
duration_results = []
for d in split_durations:
	try:
		duration_results.append([d[0] for d in db_session.query(Line.id).join(Duration.lines).filter(Duration.duration==d).all()])
	except NoResultFound:
		adjust = random.randint(1,d)
		duration_results.append([d[0] for d in db_session.query(Line.id).join(Duration.lines).filter(Duration.duration==adjust).all()])
#match on dbfs
dbfs_results = []
for d in split_dbfs:
	try:
		dbfs_results.append([db[0] for db in db_session.query(Line.id).join(DBFS.lines).filter(DBFS.dbfs==d).all()])
	except:
		adjust = random.randint(d,0)
		dbfs_results.append([db[0] for db in db_session.query(Line.id).join(DBFS.lines).filter(DBFS.dbfs==d).all()])
#match on fundamental
fundamental_results = []
for f in split_fundamentals:
	try:
		fundamental_results.append([fq[0] for fq in db_session.query(Line.id).join(Fundamental.lines).filter(Fundamental.frequency==f).all()])
	except:
		adjust = range(f-10, f+10)
		fundamental_results.append([fq[0] for fq in db_session.query(Line.id).join(Fundamental.lines).filter(Fundamental.frequency.in_(adjust)).all()])

poem = PoemBuilder('/root/dada-dial') 
for i in range(0, len(user_splits)):
	best = list(set(duration_results[i]) & set(dbfs_results[i]) & set(fundamental_results[i]))
	second_best = list(set(duration_results[i]) & set(dbfs_results[i]))
	if best:
		line = random.choice(best)
	else:
		line = random.choice(second_best)
	line_filename = db_session.query(Line.filename).filter_by(id=line).one()
	poem.addtoFile('/root/dada-dial/ubu/' + line_filename[0])


poem_filename = 'poem.wav'
poem.exportFile(path, poem_filename)






