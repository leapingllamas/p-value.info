##########################################################
# simple sentiment analysis
# Author: Carl Anderson
##########################################################

'''
   for a given document, extract the features of interest.
   Here, unique, lower case words with more than 2 characters
'''
def extract_features(document):
    features={}
    for word in set(document.split()):
        if len(word) > 2:
            features['contains(%s)' % word.lower()] = True
    return features

#########################################
# read documents into a list of tuples
#########################################
documents=[]
f = open("uniq_training.txt","r")
for document in f.readlines():
    parts= document.strip().split("\t")
    documents.append((parts[1],bool(int(parts[0]))))

#########################################
# randomize the list in a reproducible fashion
#########################################
import random
random.seed(1234) #so that you can reproduce my results if you wish
random.shuffle(documents)

#########################################
# split our data into a training (80%) and test set (20%)
# and extract the features
#########################################
import nltk
n_train = int(0.8*len(documents))
training_set = nltk.classify.apply_features(extract_features,documents[:n_train])
test_set = nltk.classify.apply_features(extract_features,documents[n_train:])

#########################################
# train our classifier
#########################################
classifier = nltk.NaiveBayesClassifier.train(training_set)

#########################################
# metrics...
# accuracy
#########################################
print "accuracy = ", nltk.classify.accuracy(classifier, test_set)

#########################################
# number positive and number negative in our training set
#########################################
ct_pos=0
for d in training_set:
    if d[1]==True: ct_pos+=1

print '#pos=', ct_pos, ' #neg=',len(training_set)-ct_pos

#########################################
# use the classifier
#########################################
print "that movie was awful = ", classifier.classify(extract_features("that movie was awful"))
print "that movie was great = ", classifier.classify(extract_features("that movie was great"))

#########################################
# show the most informative features
#########################################
classifier.show_most_informative_features(16)

#########################################
# compute precision, recall and F scores
#########################################
import collections
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
for i, (feats, label) in enumerate(test_set):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)

print 'pos precision: %2.3f' % nltk.metrics.precision(refsets[True], testsets[True])
print 'pos recall: %2.3f' % nltk.metrics.recall(refsets[True], testsets[True])
print 'pos F-measure: %2.3f' % nltk.metrics.f_measure(refsets[True], testsets[True])
print 'neg precision: %2.3f' % nltk.metrics.precision(refsets[False], testsets[False])
print 'neg recall: %2.3f' % nltk.metrics.recall(refsets[False], testsets[False])
print 'neg F-measure: %2.3f' % nltk.metrics.f_measure(refsets[False], testsets[False])

#########################################
# confusion matrix
#########################################
observed=[]
actual=[]
for i, (feats, label) in enumerate(test_set):
    actual.append(label)
    observed.append(classifier.classify(feats))

print nltk.ConfusionMatrix(actual,observed)