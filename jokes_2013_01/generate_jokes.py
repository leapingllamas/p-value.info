def indefinite_article(w):
    if w.lower().startswith("a ") or w.lower().startswith("an "): return ""
    return "an " if w.lower()[0] in list('aeiou') else "a "

def joke_type1(d1,d2,w1,w2):
    return "What do you call " + indefinite_article(d1) + d1 + " " + d2 + "? " + \
           indefinite_article(w1).upper() + w1 + " " + w2 + "."

def joke_type2(d1,d2,w1,w2):
    return "When is " + indefinite_article(d1)  + d1 + " like " + indefinite_article(d2) + d2 + "? " + \
           "When it is " + indefinite_article(w2)  + w2 + "."

data = open("processed_homonyms.txt","r").readlines()

for line in data:
     [w1,d1,pos1,w2,d2,pos2]=line.strip().split("\t")
     if pos1=='adjective' and pos2=='noun': 
         print joke_type1(d1,d2,w1,w2)
     elif pos1=='noun' and pos2=='adjective': 
         print joke_type1(d2,d1,w2,w1)
     elif pos1=='noun' and pos2=='noun': 
         print joke_type2(d1,d2,w1,w2)
         print joke_type2(d2,d1,w2,w1)