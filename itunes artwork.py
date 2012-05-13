import urllib
from BeautifulSoup import BeautifulSoup
import re
import win32com.client
import sys
import eyeD3
import shelve, string, os
from fnmatch import fnmatch


def shelving():
	file1 = shelve.open('hashdata')
	path = iTunes.LibraryXMLPath
	file = open(self.path,'r')
	
	dom = xml.dom.minidom.parse(self.file)
	for dct in dom.getElementsByTagName('dict'):
		keys=dct.getElementsByTagName('key')
		vals=[key.nextSibling.firstChild for key in keys]
		keys=[key.firstChild.data for key in keys]
		vals=[val.data if val else None for val in vals]
		data=dict(zip(keys,vals))
		try :
			self.file1[data['Name'].encode('ascii','ignore')]= data['Location'].encode('ascii','ignore')
		except KeyError:
			continue
		print 'done'
	file1.close()
try:	
	if sys.argv[1] == '-r':
		shelving()
except IndexError:
	pass
try:	
	if sys.argv[1] == '-f':
		tag = eyeD3.Tag()
		
		print 'force'
		iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")

		cTrackName = iTunes.CurrentTrack.Name
		cArtist = iTunes.CurrentTrack.Artist
		cAlbum = iTunes.CurrentTrack.Album
		file = shelve.open('hashdata')
		locationfile = file[cTrackName.encode('ascii','ignore')]
		a = urllib.unquote(locationfile)
		b = a[17:len(a)]
		b = string.replace(b,'/','\\')
		c,v = os.path.split(b)
		def print_fnmatches(pattern, dir, files):
			for filename in files:
				if fnmatch(filename, pattern):
					name = os.path.join(dir, filename)
					tag.link(name)
					tag.removeImages()
					tag.update()
		os.path.walk(c,print_fnmatches,'*.mp3')
		
except IndexError:
	pass

iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")

cTrackName = iTunes.CurrentTrack.Name
cArtist = iTunes.CurrentTrack.Artist
cAlbum = iTunes.CurrentTrack.Album

print cAlbum + cArtist + cTrackName
url = 'http://www.last.fm/music/'+cArtist+'/'+cAlbum
albumPage = urllib.urlopen(url).read()
soup = BeautifulSoup(albumPage)
s =  soup.prettify()
z = re.compile('.*<img  width="174" src="(.*)" class="art"  id="albumCover" itemprop="image" class="albumCover coverMega"  />')
p = re.findall(z,s)
print p
pat = re.compile('http://cdn.*')
x = re.findall(pat,p[0])
if len(x) == 0 and len(p) > 0:
	urllib.urlretrieve(p[0],'a.png')
	a = urllib.quote('file://localhost/C:/Users/ArchAngel/Desktop/a.png')
	iTunes.CurrentTrack.AddArtworkFromFile(u'C:/Users/ArchAngel/Desktop/a.png')
else:
	print 'Cover Art not found'



"""a = urllib.urlopen('http://www.last.fm/music/Nickelback/All+The+Right+Reasons')
b = a.read()

soup = BeautifulSoup(b)
s =  soup.prettify()
z = re.compile('.*<img  width="174" src="(.*)" class="art"  id="albumCover" itemprop="image" class="albumCover coverMega"  />')
p = re.findall(z,s)

urllib.urlretrieve(p[0],'a.png')"""

