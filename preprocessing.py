import pandas as pd
import numpy as np
import tqdm
import csv
import nltk
nltk.download('punkt')
from urllib.request import urlopen
from bs4 import BeautifulSoup
import math
import json

data = pd.read_csv("docdatabse.csv")
# print(data.head())


Docs = []
docID =[]

for line in tqdm.tqdm(data.Doc.values):
  Docs.append(line)

for id in tqdm.tqdm(data.Docid.values):
  docID.append(id)


# print(docID)
# print(Docs)

symbols = ['!','[',']',';','@','//','/','.','>','<','*','`','(',')','#','%','-',',','?','&','...','.','"','``',]
stopwords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

def checkKey(dict, key):
  if key in dict.keys():
    return 1
  else:
    return 0

index = {}

docid = 1


for d in Docs:
  url = d
  html = urlopen(url).read()
  soup = BeautifulSoup(html, features="html.parser")
  for script in soup(["script","style"]):
    script.extract()   

  text = soup.get_text()
  doctext = nltk.word_tokenize(text)
  for a in range(len(doctext)):
    doctext[a] = doctext[a].lower()
  
  for b in symbols: 
    for items in doctext:
        if items == b:
            doctext.remove(items)

  for x in stopwords: 
    for item in doctext:
        if item == x:
            doctext.remove(item)

  for w in doctext:
    c = doctext.count(w)

    s = checkKey(index,w)
  # print(s)
    if s == 0:
      index[w] = {}
  # print(c)
      index[w][docid] = c
  

    else:
      if docid in index[w]:
        v =2;
      else:
        index[w][docid] = c

  #   index[w][str(docid)] = c
 


  docid = docid + 1

# print(index)

words_vocabulary = list(index.keys())

for word in words_vocabulary:
  l = list(index[word].keys())
  k = len(l)
  idf1 = math.log((len(Docs)+1)/k,2)
  index[word]['IDF'] = idf1

with open("InvertedIndex.json", "w") as outfile: 
    json.dump(index, outfile)

queries = {1:"current state of the world economy or global economy",
           2:"Understanding microeconomics and macroeconomics",
           3:"android development for beginners",
           4:"how many versions of android are released till date",
           5:"what is the origin of SARS-CoV-2 or covid-19",
           6:"what is covax?",
           7:"how does bitcoin mining work",
           8:"ethereum and bitcoin",
           9:"best players in the history of football",
           10:"are the basic rules of football and american football same?"}

with open("Queries.json", "w") as outfile: 
    json.dump(queries, outfile)


rqueries = {1:[2,4,6,7],
            2:[5,8,9,10],
            3:[12,13,14,16,17],
            4:[11,12,14,20],
            5:[21,26,30],
            6:[22,23],
            7:[31,32,35,38,40],
            8:[31,33,38],
            9:[42,45,49,50],
            10:[41,43,48]}

with open("QueryRelevancies.json", "w") as outfile: 
    json.dump(rqueries, outfile)