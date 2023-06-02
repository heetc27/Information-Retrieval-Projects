# -*- coding: utf-8 -*-
import json
import urllib.request
from urllib.parse import quote
import urllib

# change query id, core name and IRModel name accordingly
IRModel='BM25'
lines = [line.rstrip('\n') for line in open('test-queries.txt',encoding='utf-8')]
x=1
for line in lines:
    qid,q = line.split(maxsplit=1)
    q = q.replace(':','\:')
    q = q.replace(' ','%20')
    q = quote(q)

    # change the url according to your own corename and query
    inurl = 'http://35.245.193.88:8983/solr/BM25/select?defType=dismax&fl=id,%20score&indent=on&q='+str(q)+'&qf=tweet_hashtags^3%20text_en^6%20text_ru^6%20text_de^6%20text_en_copy%20text_de_copy%20text_ru_copy&rows=20&wt=json'
    outfn = str(x)+'.txt'
    outf = open(outfn, 'w')

    # if you're using python 3, you should use
    #data = urllib2.urlopen(inurl)
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']
    # the ranking should start from 1 and increase
    rank = 1
    for doc in docs:
        outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
        rank += 1
    outf.close()
    x=x+1