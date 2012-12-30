'''
This is a very crude news aggregator
'''

#########################################
# define our feeds
#########################################
feeds = [
    'http://www.sfgate.com/rss/feed/Tech-News-449.php',
    'http://feeds.feedburner.com/TechCrunch/startups',
    'http://news.cnet.com/8300-1001_3-92.xml',
    'http://www.zdnet.com/news/rss.xml',
    'http://www.computerweekly.com/rss/Latest-IT-news.xml',
    'http://feeds.reuters.com/reuters/technologyNews',
    'http://www.tweaktown.com/news-feed/'
]

#########################################
# parse the feeds into a set of words per document
#########################################
import feedparser
import nltk
corpus = []
ct = -1
for feed in feeds:
    d = feedparser.parse(feed)
    for e in d['entries']:
       words = nltk.wordpunct_tokenize(nltk.clean_html(e['description']))
       words.extend(nltk.wordpunct_tokenize(e['title']))
       lowerwords=[x.lower() for x in words if len(x) > 1]
       ct += 1
       print ct, e['title']
       corpus.append(lowerwords)

#########################################
# tf-idf implementation
# from http://timtrueman.com/a-quick-foray-into-linear-algebra-and-python-tf-idf/
#########################################
import math
from operator import itemgetter
def freq(word, document): return document.count(word)
def wordCount(document): return len(document)
def numDocsContaining(word,documentList):
  count = 0
  for document in documentList:
    if freq(word,document) > 0:
      count += 1
  return count
def tf(word, document): return (freq(word,document) / float(wordCount(document)))
def idf(word, documentList): return math.log(len(documentList) / numDocsContaining(word,documentList))
def tfidf(word, document, documentList): return (tf(word,document) * idf(word,documentList))

#########################################
# extract top keywords from each doc.
# This defines features of our common feature vector
#########################################
import operator
def top_keywords(n,doc,corpus):
    d = {}
    for word in set(doc):
        d[word] = tfidf(word,doc,corpus)
    sorted_d = sorted(d.iteritems(), key=operator.itemgetter(1))
    sorted_d.reverse()
    return [w[0] for w in sorted_d[:n]]   

key_word_list=set()
nkeywords=20
[[key_word_list.add(x) for x in top_keywords(nkeywords,doc,corpus)] for doc in corpus]
   
ct=-1
for doc in corpus:
   ct+=1
   print ct,top_keywords(nkeywords,doc,corpus)

#########################################
# turn each doc into a feature vector using TF-IDF score
#########################################
feature_vectors=[]
n=len(corpus)

for document in corpus:
    vec=[]
    [vec.append(tfidf(word, document, corpus) if word in document else 0) for word in key_word_list]
    feature_vectors.append(vec)

#########################################
# now turn that into symmatrix matrix of 
# cosine similarities
#########################################
import numpy
mat = numpy.empty((n, n))
for i in xrange(0,n):
    for j in xrange(0,n):
       mat[i][j] = nltk.cluster.util.cosine_distance(feature_vectors[i],feature_vectors[j])
print mat

#########################################
# now hierarchically cluster mat
#########################################
from hcluster import linkage, dendrogram
Z = linkage(mat, 'single')
dendrogram(Z, color_threshold=0.75)

import pylab
pylab.savefig( "hcluster.png" ,dpi=800)
print Z