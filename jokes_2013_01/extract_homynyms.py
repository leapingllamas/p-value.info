'''
 from http://www.cooper.com/alan/homonym_list.html, extract homonym information
 as homonym1, definition1, homonym2, defintion2 and then call google dictionary
 API to determine part of speech (noun, adjective etc) of each of the homonyms
'''
from bs4 import BeautifulSoup
import urllib2
from bs4 import Comment

filename="homonyms.html"
page = open(filename,"r").read()
# for speed of dev, I just downloaded the webpage and worked off that.
# Alterntively, you could do:
# url="http://www.cooper.com/alan/homonym_list.html"
# request = urllib2.Request(url)
# page = urllib2.urlopen(request)

import json
import urllib2
def get_part_of_speech(word):
    '''
     is this a noun, adjective etc. This API is unofficial but works.
    '''
    url="http://www.google.com/dictionary/json?callback=get_definition&q=" + word + "&sl=en&tl=en&restrict=pr%2Cde&client=te"
    s=urllib2.urlopen(url).read().replace("get_definition(","").replace(",200,null)","")
    try:
       return eval(s)['primaries'][0]['terms'][0]['labels'][0]['text']
    except: 
       return "unknown"

soup = BeautifulSoup(page)
results=[]
comments = soup.findAll(text=lambda text:isinstance(text, Comment))
for comment in comments:
    #for now, ignore the 3rd row of the 3 row homonyms
    try:
        word1=comment.next_sibling.next_sibling.find_all('td')[1].string.strip()
        def1=comment.next_sibling.next_sibling.find_all('td')[2].string.strip()
        pos1=get_part_of_speech(word1).lower()
        word2=comment.next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')[1].string.strip()
        def2=comment.next_sibling.next_sibling.next_sibling.next_sibling.find_all('td')[2].string.strip()
        pos2=get_part_of_speech(word2).lower()
        print "\t".join([word1,def1,pos1,word2,def2,pos2])
    except:
       pass
