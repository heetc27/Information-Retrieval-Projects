# -*- coding: utf-8 -*-

import json
# if you are using python 3, you should 
import requests
from textblob import TextBlob

#import urllib2

with open('test-queries.txt', encoding='UTF-8') as f:
    lines = f.readlines()
que=[]
for line in lines:
    q = line.replace(" ","%20")
    q = q.replace("\n","")
    que.append(q)
# change the url according to your own corename and query

qid = '001'
a="1"
for q in que:
    print(q)
    blob = TextBlob(q)
    s = blob.detect_language()
    if s == "de":
        q = blob.translate(to = "en")
        q = q.replace(" ","")
    inurl = 'http://18.188.221.217:8983/solr/VSM/query?q={}&q.op=OR&defType=dismax&wt=json&qf=text_en%20text_de%20text_ru&fl=id,score&wt=json&indent=true&rows=20'.format(q)

    # change query id and IRModel name accordingly
    outfn = a+'.txt'
    IRModel='vsm' #either bm25 or vsm
    outf = open(outfn, 'a+')
    #data = urllib2.urlopen(inurl)
    # if you're using python 3, you should use
    data_ = requests.get(inurl)
    data = data_.json()
    docs = data['response']['docs']
    # the ranking should start from 1 and increase
    rank = 1
    for doc in docs:
        outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
        rank += 1
    outf.close()
    qid = "00"+str(int(qid)+1)
    a = str(int(a)+1)
