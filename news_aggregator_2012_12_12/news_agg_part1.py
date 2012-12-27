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
docs = []
data = []
for feed in feeds:
    d = feedparser.parse(feed)
    for e in d['entries']:
       words = nltk.wordpunct_tokenize(nltk.clean_html(e['description']))
       words.extend(nltk.wordpunct_tokenize(e['title']))
       docs.append(words)
       data.append(nltk.Text(words))

#########################################
# this collection will enable us to 
# read off TF-IDF easily
#########################################
col = nltk.TextCollection(data)

#########################################
# get the top n keywords for a doc
#########################################
import operator
def top_key_words(n,doc,data):
    d = {}
    for word in set(doc):
        d[word] = col.tf_idf(word,data)
    sorted_d = sorted(d.iteritems(), key=operator.itemgetter(1))
    sorted_d.reverse()
    return [w[0] for w in sorted_d[:10]]

#########################################
# output top 10 keywords for 12 docs 
#########################################
number_keywords = 10
number_documents = 12
for i in xrange(0,number_documents):
   print top_key_words(number_keywords,docs[i],data[i])
