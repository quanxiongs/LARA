# -*- coding: utf-8 -*-

import json
import pandas as pd
import re
from nltk import word_tokenize
from nltk import download
download()

import string

data = []

with open("reviews_Electronics_5.json","r") as json_data:
    for lines in json_data:
        data.append(json.loads(lines))

#not correct because it just take dictionary as an element, don't care any key value
#data_series = pd.Series(data)

data_series = list(map(lambda x: pd.Series(x), data))
data_frame = pd.DataFrame(data_series)

#access to reviews outside python
with open("summary.txt","w") as handle:
    for line in data_frame["reviewText"][0:10]:
        handle.writelines( "%s\n\n\n" % line)

#use only 10 text        
train_set = data_frame["reviewText"][0:10]
train_set = list(map(lambda x: x.lower(), train_set))
 

#split into sentences, the first document
D1 = re.split("[\.,]",train_set[0])

#remove punctuation and tokenize
punctuations = list(string.punctuation)
D1 = list(map(lambda x: word_tokenize(x), D1))
word_tokenize


#strip space
D1 = [item.strip() for item in D1]

#remove empty line
D1 = list(filter(None, D1))

#split into words
D1 = list(map(lambda x: x.split(" "), D1))



    
"""
import ijson
with open("reviews_Electronics_5.json","r") as json_data:
    parser = ijson.parse(json_data)
    for ids,asin, user, text in parser:
        print (ids)
        
#, asin, user, texts, rating, summary, _, time

"""

"dfsAAD ffdfsdSS".lower()