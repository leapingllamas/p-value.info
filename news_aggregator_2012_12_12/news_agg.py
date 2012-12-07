import feedparser
import nltk

#########################################
# define our feeds
#########################################
feeds = [
    'http://www.sfgate.com/rss/feed/Tech-News-449.php',
#    'http://feeds.feedburner.com/TechCrunch/startups'
]

#########################################
# parse the feeds into a set of words per document
#########################################
docs=[]
data=[]
for feed in feeds:
    d = feedparser.parse(feed)
    for e in d['entries']:
       words = nltk.wordpunct_tokenize(nltk.clean_html(e['description']))
       words.extend(nltk.wordpunct_tokenize(e['title']))
       docs.append(words)
       data.append(nltk.Text(words))

#d=feedparser.parse(feeds[0])
#print d['entries'][0]['description']

#########################################
# this collection will enable us to 
# read off TF-IDF easily
#########################################
col = nltk.TextCollection(data)

import operator

#########################################
# get the top n keywords for a doc
#########################################
def top_key_words(n,doc,data):
    d={}
    for word in set(doc):
        d[word] = col.tf_idf(word,data)
    sorted_d = sorted(d.iteritems(), key=operator.itemgetter(1))
    sorted_d.reverse()
    keywords = [w[0] for w in sorted_d[:10]]
    return keywords

#d={}
#for word in set(docs[0]):
#    d[word] = col.tf_idf(word,data[0])
#
#sorted_d = sorted(d.iteritems(), key=operator.itemgetter(1))
#sorted_d.reverse()
#keywords = [w[0] for w in sorted_d[:10]]
#print keywords

#########################################
# output top keywords for 12 docs 
#########################################
for i in xrange(0,12):
   print top_key_words(10,docs[i],data[i])
