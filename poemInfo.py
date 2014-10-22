import pickle
class poemInfo(object):

	def __init__(self):
		f = open('poemInfo.p', 'rb')
		self.poemInfo = pickle.load(f)