# 2022.9.7
import requests,os,re,itertools
import pandas as pd
c4host	= os.getenv('c4host', 'wrask.com:9200')

iphrase = lambda hyb="_be in force", cp='en', field='postag': requests.post(f"http://{eshost}/{cp}/_search", json={   "query": {  "match_phrase": { field: hyb    }   } } ).json()['hits']['total']['value']
iterm  = lambda term="NOUN:force", cp='en', field='kps':requests.post(f"http://{eshost}/{cp}/_search", json={   "query": {  "term": { field: term    }   } } ).json()['hits']['total']['value']
sntsum = lambda cp='clec': requests.post(f"http://{eshost}/_sql", json={"query":f"select count(*) from {cp} where type='snt'"}).json()['rows'][0][0]
match_phrase = lambda hyb="_be in force", cp='en', field='postag': requests.post(f"http://{eshost}/{cp}/_search", json={   "query": {  "match_phrase": { field: hyb    }   } } ).json()
phrase_snt = lambda hyb="_be in force", cp='en', field='postag': [ ar['_source']['snt']  for ar in match_phrase(hyb,cp,field)['hits']['hits'] ]

rows	= lambda query, fetch_size=1000: requests.post(f"http://{eshost}/_sql",json={"query": query,"fetch_size": fetch_size}).json().get('rows',[]) #rows("select s,i from dic where s like 'dobj:VERB_open:NOUN_%'")
si		= lambda pattern, cp='en', sepa='_': [ (row[0].split(sepa)[-1], int(row[1]) )  for row in rows(f"select s,i from {cp} where s like '{pattern}' order by i desc")]
lemlex	= lambda lem, cp='en': [ (s.split(':')[-1],i) for s,i in rows(f"select s,i from {cp} where s like '_{lem}:%'")]
lempos	= lambda lem, cp='en': [ (s.split(':')[0], i) for s,i in rows(f"select s,i from {cp} where s in ('VERB:{lem}','NOUN:{lem}', 'ADJ:{lem}','ADV:{lem}')")]

addpat	= lambda s : f"{s}_[^ ]*" if not s.startswith('_') else f"[^ ]*{s}[^ ]*"   # if the last one, add $ 
rehyb   = lambda hyb: ' '.join([ addpat(s) for s in hyb.split()])  #'the_[^ ]* [^ ]*_NNS_[^ ]* of_[^ ]*'
heads   = lambda chunk:  ' '.join([s.split('_')[0].lower() for s in chunk.split()])		#the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
def hyb(hyb:str='the _NNS of', index:str='c4-1', size:int= -1, topk:int=10):
	''' the _NNS of -> {the books of: 13, the doors of: 7} , added 2021.10.13 '''
	from collections import Counter
	sql= { "query": {  "match_phrase": { "postag": hyb  } },  "_source": ["postag"], "size":  size}
	res = requests.post(f"http://{c4host}/{index}/_search/", json=sql).json()
	si = Counter()
	repat = rehyb(hyb)
	for ar in res['hits']['hits']: 
		postag =  ar["_source"]['postag']
		m= re.search(repat,postag) #the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
		if m : si.update({ heads(m.group()):1})
	return si.most_common(topk)

postag_snt = lambda postag='_^ the_the_DET_DT solution_solution_NOUN_NN is_be_AUX_VBZ':  ' '.join([  ar.split('_')[0] for ar in postag.strip().split()[1:] ])
def match_phrase(q:str="_take _NOUN into account", index:str='c4-1', field:str='postag', size:int=10, keep_first:bool=True):
	''' '''
	sql= { "query": {  "match_phrase": { field: q  } },  "_source": [field,'did'], "size":  size}  #"track_total_hits": true
	res = requests.post(f"http://{c4host}/{index}/_search/", json=sql).json()
	total = res['hits']['total']['value']
	snts_dids = [ ( postag_snt(ar['_source'][field]), ar['_source']['did'])  for ar in res['hits']['hits'] ]

	did_res = requests.post(f"http://{c4host}/{index}/_search/", json={"query": {
        "ids" : {
            "type" : "_doc",
            "values" : [did for snt, did in snts_dids]
			}
		}
	}).json()
	did_v = { ar['_id']: ar['_source']  for ar in did_res['hits']['hits']}
	return [ dict(did_v.get(did,{}), **{'snt':snt}) for snt, did in snts_dids]
	# snts  = [ar['_source'][field] for ar in res['hits']['hits'] ]
	# return [ postag_snt(snt) for snt in snts ] if keep_first else snts 

if __name__ == '__main__': 
	print ( match_phrase()) 

'''

GET /c4-1/_search
{ 
    "query": {
        "ids" : {
            "type" : "_doc",
            "values" : ["bc343eab29888c137904ebf8f3ee47cc"]
			}
		}
	}


POST /c4-1/_search
{
  "query": {
    "match_phrase": {
      "postag":"as soon as _ADV possible"
    }
  }
}


GET /clec/_search
{
  "query": { "match": {"type": "snt"}   }, 
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": "kps",
         "include": "dobj:have_VERB:NOUN_dream"
      },
    "aggs" : {
                "snt" : {
                    "top_hits": { "_source": {"includes":"snt" }, "size":5
                    }
                }
            }

    }
  }
}

GET /dic/_search
{
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": "kps",
         "include": "VERB:sound|ADJ:sound|ADV:sound|NOUN:sound"
      }
    }
  }
}

GET /dic/_search
{
  "size":0,
  "aggs": {
    "myagg": {
      "terms": {
        "field": "kps",
         "include": "VERB:.*",
         "size":10000
      }
    }
  }
}
'''