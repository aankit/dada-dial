#let's create  dictionary of the poems

#first we need filenames
import urllib, re
from urlparse import urlparse
from bs4 import BeautifulSoup
import pickle
#just one url for now - the dial-a-poem poets, but I could potentially run this on the entire ubu web site
urls = [
	'http://www.ubu.com/sound/dial.html'
]

soup = BeautifulSoup(urllib.urlopen(urls[0]).read())
poems = []
for a in soup.findAll('a',href=re.compile('http.*\.mp3')):
	poem = {
	'filename' : urlparse(a['href']).path.split('/')[-1],
	'poet' : re.search('[A-Z]\w+\s([A-Z]\w+|[A-Z]\'\w+)', a.contents[0].split('|')[0] ).group(0),
	'title' : a.contents[0].split('|')[1]
	}
	poems.append(poem)

f = open('poemInfo.p', 'wr')
pickle.dump(poems, f)
f.close()

#used the dictionary above, might need different models for each site
#poets = [a.contents[0].split('|')[0] for a in soup.findAll('a', href=re.compile('http.*\.mp3'))]
#poets = [re.search('[A-Z]\w+\s([A-Z]\w+|[A-Z]\'\w+)', p).group() for p in poets]
#titles = [a.contents[0].split('|')[1] for a in soup.findAll('a', href=re.compile('http.*\.mp3'))]


