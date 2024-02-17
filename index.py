import pandas as pd
import numpy as np
import tqdm
import csv
import nltk
nltk.download('punkt')

import math
import json

data = pd.read_csv("docdatabse.csv")
# print(data.head())

symbols = ['!','[',']',';','@','//','/','.','>','<','*','`','(',')','#','%','-',',','?','&','...','.','"','``',]
stopwords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

Docs = []
docID =[]
# print("x1")
for line in tqdm.tqdm(data.Doc.values):
  Docs.append(line)

for id in tqdm.tqdm(data.Docid.values):
  docID.append(id)

# print(Docs)

with open('InvertedIndex.json') as json_file:
    index = json.load(json_file)

with open('QueryRelevancies.json') as json_file:
    r_queries = json.load(json_file)

# print(r_queries['1'])

with open('Queries.json') as json_file:
    q = json.load(json_file)
    queries = list(q.values())
# print(queries)


def TFvalue(dict,word,d):
    if word in dict:
        l = []
        for n in dict[word]:
            l.append(n)
        if d in l:
            return dict[word][d]
        else:
            return 0
    else:
        return 0
        
def IDFvalue(dict,w):
    return dict[w]["IDF"]

def PR(r,i,q):
    ret =[]
    precision=[]
    recall =[]
    relevants = q[i]
    # print(relevants)
    total = len(relevants)
    # print(total)
    rcount = 0
    print(" ")
    print("Step wise Precision and Recall Calculation")
    print("Sno.", "Precision", "Recall")
    for h in range(len(r)):
  
        if r[h] in relevants:
            rcount = rcount +1
            p = rcount/(h+1)
            precision.append(p)
            recall.append(rcount/total)
            print((h+1),"   ",p,"     ",(rcount/total))
        else:
            
            precision.append(0)
            recall.append(rcount/total)
            print((h+1),"   ",'0',"     ",(rcount/total))
            # rcount = rcount +1
    ret.append(precision)
    ret.append(recall)
    return ret

m_avp = []
r =1
while r > 0:
    print("1 : Start TR System")
    print("2 : Exit")

    choice = input("Enter Choice: ")
    # print(choice)
    if int(choice) == 1:
        # print("x")
        for num in range(len(queries)):
            print("  ", (num+1),"  ",queries[num])
        print("     0 for Others")    

        qchoice = input("Choose Query: ")
        
        if int(qchoice) != 0:
            Q = queries[int(qchoice)-1]
            print(" ")
            print(" ")
            print("You have Chosen the Query: ", " ", Q)
            # print(Q)
            print(" ")
            print(" ")


            qtext = nltk.word_tokenize(Q)
            # print(qtext)

            for e in range(len(qtext)):
                qtext[e] = qtext[e].lower()

            queryt = []
            # print(queryt)

            for t in qtext:
                if queryt.count(t) == 0:
                    queryt.append(t)
                
            
            for b in symbols: 
                for items in queryt:
                    if items == b:
                        queryt.remove(items)

            for x in stopwords: 
                for item in queryt:
                    if item == x:
                        queryt.remove(item)

            # print(queryt)
            # print(qtext)
            scores= []
            for i in range(len(Docs)):
                acc = 0
                for w in queryt:
                    # print(w)
                    a = qtext.count(w)
                # print(a)
                    j = i+1
                    j = str(j)
                    b = TFvalue(index,w,j)
                    # print(b)
                    c = IDFvalue(index,w)
                    # print(c)
                    acc = acc + (a*b*c)
                scores.append(acc)

                # print(scores)
            scores1 = []
            for z in range(len(scores)):
                scores1.append(scores[z])
            
            retrieved = []

            def ranked(arr):
                while max(arr) != 0:
                
                    x = arr.index(max(arr)) + 1
                    retrieved.append(x)
                    print("Document",x)
                
                    arr[arr.index(max(arr))] = 0
            print(" ")
            print("Relevant Document Ranking:")
            print(" ")
            print(ranked(scores))

            
            # while max(scores1) != 0:
            #     x1 = scores1.index(max(scores1))
            #     retrieved.append(x1+1)
            #     scores1.remove(scores1[x1])
            # print(retrieved)
            rett = PR(retrieved,qchoice,r_queries)
            # print(rett)
            avg_p = 0
            for n in rett[0]:
                avg_p = avg_p + n
                g = len(r_queries[qchoice])
            avg_p = avg_p / g      
            # print(rett)
            print(" ")
            print("Average Precision"," ",avg_p)
            print(" ")
            m_avp.append(avg_p)

            mavp = 0
            for o in range(len(m_avp)):
                mavp = mavp + m_avp[o]
            
            print(" ")
            print("Mean Avg P is :")
            print(mavp/(len(m_avp)))
            print(" ")

        else:
            c_query = input("Enter Query:")
            Q = c_query
            print("You have Chosen the Query: ", " ", Q)



            qtext = nltk.word_tokenize(Q)
            # print(qtext)

            for e in range(len(qtext)):
                qtext[e] = qtext[e].lower()

            queryt = []

            for t in qtext:
                if queryt.count(t) == 0:
                    queryt.append(t)
                
            
            for b in symbols: 
                for items in queryt:
                    if items == b:
                        queryt.remove(items)

            for x in stopwords: 
                for item in queryt:
                    if item == x:
                        queryt.remove(item)

            # print(queryt)
            # print(qtext)
            scores= []
            for i in range(len(Docs)):
                acc = 0
                for w in queryt:
                # print(w)
                    a = qtext.count(w)
                # print(a)
                    j = i+1
                    j = str(j)
                    b = TFvalue(index,w,j)
                # print(b)
                    c = IDFvalue(index,w)
                # print(c)
                    acc = acc + (a*b*c)
                scores.append(acc)

                # print(scores)
            scores1 = []
            for z in range(len(scores)):
                scores1.append(scores[z])

            def ranked(arr):
                while max(arr) != 0:
                
                    x = arr.index(max(arr)) + 1
                    print("Document",x)
                
                    arr[arr.index(max(arr))] = 0

            print(" ")
            print("Relevant Document Ranking:")
            print(" ")
            print(ranked(scores))









    elif int(choice) ==2:
        r = 0