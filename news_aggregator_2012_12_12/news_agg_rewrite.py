import feedparser
import nltk

#########################################
# define our feeds
#########################################
feeds = [
    'http://www.sfgate.com/rss/feed/Tech-News-449.php',
    'http://feeds.feedburner.com/TechCrunch/startups'
]

#########################################
# parse the feeds into a set of words per document
#########################################
corpus = []
all_words=set()
ndocs=5
gct=-1
for feed in feeds:
    gct+=1
    d = feedparser.parse(feed)
    ct=-1
    for e in d['entries']:
       ct+=1
       if ct < ndocs:
           words = nltk.wordpunct_tokenize(nltk.clean_html(e['description']))
           words.extend(nltk.wordpunct_tokenize(e['title']))
           lowerwords=[x.lower() for x in words if len(x) > 1]
           print gct*ndocs+ct,e['title']
           [all_words.add(w) for w in lowerwords]
           corpus.append(lowerwords)

#########################################
# tf idf implementation
# from http://timtrueman.com/a-quick-foray-into-linear-algebra-and-python-tf-idf/
#########################################
import math
from operator import itemgetter

def freq(word, document):
  return document.count(word)

def wordCount(document):
  return len(document)

def numDocsContaining(word,documentList):
  count = 0
  for document in documentList:
    if freq(word,document) > 0:
      count += 1
  return count

def tf(word, document):
  return (freq(word,document) / float(wordCount(document)))

def idf(word, documentList):
  return math.log(len(documentList) / numDocsContaining(word,documentList))

def tfidf(word, document, documentList):
  return (tf(word,document) * idf(word,documentList))

feature_vectors=[]
n=len(corpus)

for i in xrange(0,n):
    document=corpus[i]
    vec=[]
    for word in all_words:
       if word in document:
           vec.append(tfidf(word, document, corpus))
       else:
          vec.append(0)
    feature_vectors.append(vec)

import numpy
mat = numpy.empty((n, n))

for i in xrange(0,n):
    for j in xrange(0,n):
        #if i > j:
        mat[i][j] = nltk.cluster.util.cosine_distance(feature_vectors[i],feature_vectors[j])
        if mat[i][j] < 0.0000001:
           mat[i][j] = 0

#print mat

#print n
for i in xrange(0,n):
    s=""
    for j in xrange(0,n):
       s+= str(round(mat[i][j],5)) + "\t"
#    print s

from hcluster import pdist, linkage, dendrogram
#Y = pdist(feature_vectors)
#print "Y=", Y

Z = linkage(feature_vectors)
print "Z=", Z
import matplotlib
print "dendro=",dendrogram(Z)

dendrogram(Z)