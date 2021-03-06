#-*- coding: utf-8 -*-
from collections import Counter
from textblob import TextBlob as tb
import json
import pandas as pd
import re
import time
import numpy as np
from nltk import PorterStemmer

"""
PorterStemmer().stem_word('ate')
example_words = ["python","pythoner","pythoning","pythoned","pythonly"]
ps = PorterStemmer()

for w in example_words:
    print(ps.stem(w))
"""

"""
def tf(word, blob):
    return blob.words.count(word)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.word)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word,bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)
"""

document1 = """Python is a 2000 made-for-TV horror movie directed by Richard
Clabaugh. The film features several cult favorite actors, including William
Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy,
Keith Coogan, Robert Englund (best known for his role as Freddy Krueger in the
A Nightmare on Elm Street series of films), Dana Barron, David Bowe, and Sean
Whalen. The film concerns a genetically engineered snake, a python, that
escapes and unleashes itself on a small town. It includes the classic final
girl scenario evident in films like Friday the 13th. It was filmed in Los Angeles,
 California and Malibu, California. Python was followed by two sequels: Python
 II (2002) and Boa vs. Python (2004), both also made-for-TV films."""

document2 = """Python, from the Greek word (πύθων/πύθωνας), is a genus of
nonvenomous pythons[2] found in Africa and Asia. Currently, 7 species are
recognised.[2] A member of this genus, P. reticulatus, is among the longest
snakes known."""

document3 = """The Colt Python is a .357 Magnum caliber revolver formerly
manufactured by Colt's Manufacturing Company of Hartford, Connecticut.
It is sometimes referred to as a "Combat Magnum".[1] It was first introduced
in 1955, the same year as Smith &amp; Wesson's M29 .44 Magnum. The now discontinued
Colt Python targeted the premium revolver market segment. Some firearm
collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy
Thompson, Renee Smeets and Martin Dougherty have described the Python as the
finest production revolver ever made."""




def blob_maker(doc): #input as a string
    #sentences = re.split("[\.]",doc)
    sentences = tb(doc).sentences
    #blobs = list(map(lambda x: tb(x), sentences))
    blobs = list(sentences)
    return blobs

def blob_concat(docs): #input as a list
    blob_list = []
    for doc in docs:
        doc_l = doc.lower()
        blob_list.append(blob_maker(doc_l))
    return blob_list

""" #not needed anymore
document1 = document1.lower()
document2 = document2.lower()
document3 = document3.lower()
"""
test_v1 = blob_concat([document1,document2,document3])

"""
document1 = document1.lower()
document2 = document2.lower()
document3 = document3.lower()

Doc1 = re.split("[\.]",document1)
Doc2 = re.split("[\.]",document2)
Doc3 = re.split("[\.]",document3)

blob1 = list(map(lambda x: tb(x), Doc1)) #this is one blob list
blob2 = list(map(lambda x: tb(x), Doc2))
blob3 = list(map(lambda x: tb(x), Doc3))

Whole_doc = [blob1,blob2,blob3]
"""


ps = PorterStemmer()
#ps.stem('films')


def stemming(blob):
    i_list = []
    for i in range(len(blob)): # the whole_doc is a list of a list (double list)
        j_list =[]    
        for j in range(len(blob[i])):
            j_list.append(list(map(lambda x: ps.stem(x), blob[i][j].words)))
        i_list.append(j_list)
    return i_list

#stemming(test_v1)
stemmed_word = stemming(test_v1)
#stemmed_word[1][2].count('a')

def aspect_segment(blob, aspect): #input blob and dictionary
    sentence_aspect = {} #make dictionary to anotate by aspect
    for i in range(len(blob)): # the whole_doc is a list of a list (double list)
        for j in range(len(blob[i])): 
            hit_aspect = {} 
            for key, words in aspect.items():
                hit = Counter()
                for word in words:
                    #hit[word] = blob[i][j].words.count(word) #Count for words which is in aspect
                    hit[word] = stemmed_word[i][j].count(word)
                hit_aspect[key] = sum(hit.values()) #sum up the all word count by aspect and sentence 
            highest = max(hit_aspect.values())
            sentence_aspect[(i,j)] = [key for key, values in hit_aspect.items() if values == highest]
            #print(sentence_aspect[(i,j)],highest)  #does set recognize order?
    return sentence_aspect
    
test_v2 = aspect_segment(test_v1,aspects)

"""    
### match sentences in one document and assign sentence aspect
sentence_aspect = {} #make dictionary to anotate by aspect
for i in range(len(Whole_doc)): # the whole_doc is a list of a list (double list)
    for j in range(len(Whole_doc[i])): 
        hit_aspect = {} 
        for key, words in aspect.items():
            hit = Counter()
            for word in words:
                hit[word] = Whole_doc[i][j].words.count(word) #Count for words which is in aspect
            hit_aspect[key] = sum(hit.values()) #sum up the all word count by aspect and sentence 
        highest = max(hit_aspect.values())
        sentence_aspect[(i,j)] = [key for key, values in hit_aspect.items() if values == highest]
        print(sentence_aspect[(i,j)],highest)  #does set recognize order?
        
## test passed
"""
"".join(["dfsdfd","dfsdfsdf","dfsdfsdf"])

#total number of word Occurance C
#total_word = list(set(tb(document1 + document2 + document3).words))

stemmed_word[2][3]
len(stemmed_word[2])

def total_C(stem):
    total_doc =[]
    for i in range(len(stem)): # the whole_doc is a list of a list (double list)
        for j in range(len(stem[i])):
            total_doc += (stem[i][j])
    
    #conc_docs = " ".join(docs)
    #conc_docs = conc_docs.lower()
    #text_blob = tb(conc_docs)
    print(len(total_doc))
    stop_words = ['the', 'and', 'a','is','it','as','2','in',"'s",'was','on','by','of']
    stop_words = set(list(map(lambda x : ps.stem(x), stop_words)))
    use_words = set(total_doc)-stop_words
    #total_wscore = {word : text_blob.words.count(word) for word in use_words}
    total_wscore = {word : total_doc.count(word) for word in use_words}
    selected_word = dict(filter(lambda x: x[1] > 1, total_wscore.items()))
    C = sum(selected_word.values())
    return C, selected_word



"""
total_word = tb(document1+document2+document3)
total_wscore = {word : total_word.words.count(word) for word in total_word.words}
selected_word = dict(filter(lambda x: x[1] > 1, total_wscore.items()))
C = sum(selected_word.values())
"""

#여기서 문제가 있다!!

def calc_C1(stemmed, word, sent_asp, aspnum):
    aspect_loc = dict(filter(lambda x: aspnum in x[1], sent_asp.items()))
    sentences = []
    for loc in list(aspect_loc.keys()):
        sentences += stemmed[loc[0]][loc[1]]
    C1 = sentences.count(word)
    return C1

def calc_C4(stemmed, word, sent_asp, aspnum):
    aspect_loc = dict(filter(lambda x: aspnum not in x[1], sent_asp.items()))
    count = 0
    for loc in list(aspect_loc.keys()):
        sentences = stemmed[loc[0]][loc[1]]
        if word not in sentences:
            count += 1
        else:
            continue
    return count

def calc_C2(stemmed, word, sent_asp, aspnum):
    aspect_loc = dict(filter(lambda x: aspnum not in x[1], sent_asp.items()))
    sentences = []
    for loc in list(aspect_loc.keys()):
        sentences += stemmed[loc[0]][loc[1]]
    C2 = sentences.count(word)
    return C2

def calc_C3(stemmed, word, sent_asp, aspnum):
    aspect_loc = dict(filter(lambda x: aspnum in x[1], sent_asp.items()))
    count = 0
    for loc in list(aspect_loc.keys()):
        sentences = stemmed[loc[0]][loc[1]]
        if word not in sentences:
            count += 1
        else:
            continue
    return count


c1 = calc_C1(test_v1,'films',test_v2,1)
c2 = calc_C2(test_v1,'films',test_v2,1)
c3 = calc_C3(test_v1,'films',test_v2,1)
c4 = calc_C4(test_v1,'films',test_v2,1)
c = total_C([document1,document2,document3])

c1 = calc_C1(test_v1,'film',test_v2,1)
c2 = calc_C2(test_v1,'film',test_v2,1)
c3 = calc_C3(test_v1,'film',test_v2,1)
c4 = calc_C4(test_v1,'film',test_v2,1)
c = total_C([document1,document2,document3])


(c*(c1*c4-c2*c3)) / (c1+c3) * (c2+c4) * (c1+c2) * (c3+c4)

##Vectorized implementation
c,words = total_C(stemmed_word)

def c_list(stemmed, wordlist, sent_asp, aspnum):
    c1 = np.array([],dtype = np.float32)
    c2 = np.array([],dtype = np.float32)
    c3 = np.array([],dtype = np.float32)
    c4 = np.array([],dtype = np.float32)
    for word in wordlist:
        c1 = np.append(c1, calc_C1(stemmed,word,sent_asp,aspnum)) 
        c2 = np.append(c2, calc_C2(stemmed,word,sent_asp,aspnum))
        c3 = np.append(c3, calc_C3(stemmed,word,sent_asp,aspnum))
        c4 = np.append(c4, calc_C4(stemmed,word,sent_asp,aspnum))
    return c1,c2,c3,c4

[ps.stem('revolver'),ps.stem('films')]
#repeat until 10 iteration
#must use stemmed aspectword
aspects = {1 : list(map(lambda x : ps.stem(x), ["movie","films","made-for-tv"])), 2 : list(map(lambda x : ps.stem(x), ["greek","genus","member"])),3 : list(map(lambda x : ps.stem(x), ["product","revolver","colt"])) } #initial
Xscore=np.array([])
test_v2 = aspect_segment(stemmed_word,aspects)

for aspect in aspects.keys():
    c1,c2,c3,c4 = c_list(stemmed_word,words,test_v2, aspect)
    temp = (c*((c1*c4-c2*c3)**2)) / ((c1+c3) * (c2+c4) * (c1+c2) * (c3+c4))
    Xscore = np.hstack((Xscore,temp))
Xscore = Xscore.reshape(len(aspects),len(words))


#find the word with high Xsquare values and assign it to aspects dictionary
for i in range(len(aspects)):
    temp=Xscore.argsort(axis=1)[i,-3:]
    print([list(words.keys())[x] for x in temp ])
    aspects[i+1] = [list(words.keys())[i] for i in temp ]


#수렴하지 않는다..... ㅆㅂ..... 데이터를 정제해서 다시 해보자


"""
starttime = time.time()
calc_C1(test_v1,'film',test_v2,1)
print(time.time() - starttime)
"""

"""
#number of times w occurs in sentence belonging to aspect Ai
for i in aspect.keys():
    aspect_loc = dict(filter(lambda x: i in x[1], sentence_aspect.items()))
    sentences = []
    for loc in list(aspect_loc.keys()):
        sentences += Whole_doc[loc[0]][loc[1]].words
    C1 = sentences.count()
"""


"""old version      
### match sentences in one document and assign sentence aspect
sentence_aspect = {}
for num, sentence in enumerate(doc1):
    hit_aspect = {}
    for key, words in aspect.items():
        hit = Counter()
        for word in words:
            hit[word] = sentence.count(word)
        hit_aspect[key] = sum(hit.values())
    highest = max(hit_aspect.values())
    sentence_aspect[num] = [key for key, values in hit_aspect.items() if values == highest] 
###
"""





