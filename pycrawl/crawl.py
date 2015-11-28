import sys
import urllib2
from BeautifulSoup import BeautifulSoup as BS

url = sys.argv[2]
words = ''
if url[-4:] != '.txt':
    soup = BS(urllib2.urlopen(url).read())
    details = soup.findAll('div','details')
    words = str(details).split(' ')
else:
    words = open(url).read().split(' ')

forbid = ['#', '<', '>']
count = {}
for word in words:
    if word == '' or True in [x in word for x in forbid]: continue
    try: count[word] += 1
    except Exception,e: count[word] = 1

# right now skips the first couple (typically 'the', 'to', 'I', etc.)
print '\n'.join(sorted(count,key=count.get,reverse=True)[9:9+int(sys.argv[1])])
