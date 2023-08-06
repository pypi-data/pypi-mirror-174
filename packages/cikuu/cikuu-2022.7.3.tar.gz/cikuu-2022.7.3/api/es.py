# 2022.9.10
import requests,os,re,itertools
import pandas as pd
from util import likelihood
if not 'eshost' in globals() :  eshost	= os.getenv('eshost', 'es.corpusly.com:9200')

iphrase = lambda hyb="_be in force", cp='en', field='postag': requests.post(f"http://{eshost}/{cp}/_search", json={   "query": {  "match_phrase": { field: hyb    }   } } ).json()['hits']['total']['value']
iterm  = lambda term="NOUN:force", cp='en', field='kps':requests.post(f"http://{eshost}/{cp}/_search", json={   "query": {  "term": { field: term    }   } } ).json()['hits']['total']['value']
sntsum = lambda cp='clec': requests.post(f"http://{eshost}/_sql", json={"query":f"select count(*) from {cp} where type='snt'"}).json()['rows'][0][0]
match_phrase = lambda hyb="_be in force", cp='en', field='postag': requests.post(f"http://{eshost}/{cp}/_search", json={   "query": {  "match_phrase": { field: hyb    }   } } ).json()
phrase_snt = lambda hyb="_be in force", cp='en', field='postag': [ ar['_source']['snt']  for ar in match_phrase(hyb,cp,field)['hits']['hits'] ]

esrows	= lambda query, fetch_size=1000: requests.post(f"http://{eshost}/_sql",json={"query": query,"fetch_size": fetch_size}).json().get('rows',[])
estables = lambda : [row[1] for row in esrows("show tables") if not row[1].startswith(".")]

rows	= lambda query, fetch_size=1000: requests.post(f"http://{eshost}/_sql",json={"query": query,"fetch_size": fetch_size}).json().get('rows',[]) #rows("select s,i from dic where s like 'dobj:VERB_open:NOUN_%'")
si		= lambda pattern, cp='en', sepa='_': [ (row[0].split(sepa)[-1], int(row[1]) )  for row in rows(f"select s,i from {cp} where s like '{pattern}' order by i desc")]
lemlex	= lambda lem, cp='en': [ (s.split(':')[-1],i) for s,i in rows(f"select s,i from {cp} where s like '_{lem}:%'")]
lempos	= lambda lem, cp='en': [ (s.split(':')[0], i) for s,i in rows(f"select s,i from {cp} where s in ('VERB:{lem}','NOUN:{lem}', 'ADJ:{lem}','ADV:{lem}')")]

terms	= lambda termlist='VERB,vtov,vvbg,VBD,dative', suffix='', sumkey=None, cp='en': rows(f"select s,i from {cp} where s in ('" + "','".join([ v.strip() + suffix for v in termlist.split(',')]) + f"', '{sumkey}')")
silist  = lambda vlist='vtov,vvbg,ccomp,dobj,nsubj', suffix=':VERB_consider', sumkey="VERB:consider", cp='en': rows(f"select s,i from {cp} where s in ('" + "','".join([ v + suffix for v in vlist.split(',')]) + f"', '{sumkey}')")

def keyness(si_src, si_tgt, sumkey:str=None): # keyness(lempos('sound','sino'),lempos('sound','en'))
	''' return (src, tgt, src_sum, tgt_sum, keyness) '''
	df = pd.DataFrame({'src': dict(si_src), 'tgt': dict(si_tgt)}).fillna(0)
	if sumkey is not None : df = df.drop(sumkey) 
	df['src_sum'] = sum([i for s,i in si_src]) if sumkey is None else dict(si_src)[sumkey]
	df['tgt_sum'] = sum([i for s,i in si_tgt]) if sumkey is None else dict(si_tgt)[sumkey]
	df['keyness'] = [ likelihood(row['src'],row['tgt'],row['src_sum'],row['tgt_sum']) for index, row in df.iterrows()] 
	return df.sort_values(df.columns[-1], ascending=True) 

def lemma_phrase_keyness(lemma:str='_force', phrase:list=["_be in force","_come into force","_go into force","_be forced to _VERB",'by force', '_VERB with force'], cps:str='sino', cpt:str='en'): 
	''' return: word  sino    en  sino_sum  en_sum  keyness '''
	sum_src = iphrase(lemma, cps)
	sum_tgt = iphrase(lemma, cpt)
	rows = [ (w, iphrase(w, cps), iphrase(w, cpt) ) for w in phrase]    
	return pd.DataFrame( [ (w, c1, c2, sum_src, sum_tgt, likelihood(c1,c2,sum_src, sum_tgt))  for w, c1,c2 in rows], columns=["word", cps, cpt, f"{cps}_sum", f"{cpt}_sum","keyness"])   

def cands_product(q='one two/ three/'):
    ''' {'one three', 'one two', 'one two three'} '''
    arr = [a.strip().split('/') for a in q.split()]
    res = [' '.join([a for a in ar if a]) for ar in itertools.product( * arr)]
    return set( [a.strip() for a in res if ' ' in a]) 

def compare(q="_discuss about/ the issue", cp='en'):
    cands = cands_product(q)
    return [ (cand, iphrase(cand, cp))  for cand in cands]

addpat	= lambda s : f"{s}_[^ ]*" if not s.startswith('_') else f"[^ ]*{s}[^ ]*"   # if the last one, add $ 
rehyb   = lambda hyb: ' '.join([ addpat(s) for s in hyb.split()])  #'the_[^ ]* [^ ]*_NNS_[^ ]* of_[^ ]*'
heads   = lambda chunk:  ' '.join([s.split('_')[0].lower() for s in chunk.split()])		#the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
def hybchunk(hyb:str='the _NNS of', index:str='en', size:int= -1, topk:int=10):
	''' the _NNS of -> {the books of: 13, the doors of: 7} , added 2021.10.13 '''
	from collections import Counter
	sql= { "query": {  "match_phrase": { "postag": hyb  } },  "_source": ["postag"], "size":  size}
	res = requests.post(f"http://{eshost}/{index}/_search/", json=sql).json()
	si = Counter()
	repat = rehyb(hyb)
	for ar in res['hits']['hits']: 
		postag =  ar["_source"]['postag']
		m= re.search(repat,postag) #the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
		if m : si.update({ heads(m.group()):1})
	return si.most_common(topk)

postag_snt = lambda postag='_^ the_the_DET_DT solution_solution_NOUN_NN is_be_AUX_VBZ':  ' '.join([  ar.split('_')[0] for ar in postag.strip().split()[1:] ])
def match_phrase(q:str="_take _NOUN into account", index:str='en', field:str='postag', size:int=10, keep_first:bool=True):
	''' '''
	sql= { "query": {  "match_phrase": { field: q  } },  "_source": [field], "size":  size}  #"track_total_hits": true
	res = requests.post(f"http://{eshost}/{index}/_search/", json=sql).json()
	total = res['hits']['total']['value']
	snts  = [ar['_source'][field] for ar in res['hits']['hits'] ]
	return [ postag_snt(snt) for snt in snts ] if keep_first else snts 

if __name__ == '__main__': 
	#eshost='wrask.com:9200'
	print (estables()) 
	#print (keyness(lempos('age','sino'),lempos('age'), 'NOUN'))
	#print ( match_phrase()) 

'''
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