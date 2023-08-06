# 2022.10.25  zset-like:  (key, name, value) 
import json, traceback,sys, time,  fileinput, os, en,fire
from collections import Counter,defaultdict
add = lambda *names: [fire.ssi[ name.split('|')[0] ].update({ name.split('|')[-1] : 1}) for name in names if  not '\t' in name and len(name) <= 80 ]

def walk(doc): 
	from dic.wordlist import wordlist 
	add( "#|sntnum")  
	[add( f"{t.lemma_}|{t.pos_}", f"{t.lemma_}:LEX|{t.text.lower()}", f"LEM|{t.lemma_.lower()}", f"LEX|{t.text.lower()}", f"{t.pos_}|{t.lemma_.lower()}"
		,f"{t.lemma_.lower()}:{t.pos_}|{t.tag_}",f"*:{t.pos_}|{t.tag_}") for t in doc if not t.pos_ in ('PROPN','X', 'PUNCT') and t.is_alpha  and t.lemma_.lower() in wordlist]
	for t in doc:
		add( "#|LEX", f"#|{t.pos_}", f"#|{t.tag_}",f"{t.pos_}|{t.tag_}",f"#|{t.dep_}",f"{t.pos_}|{t.dep_}") 
		if t.pos_ not in ("PROPN","PUNCT","SPACE") and t.is_alpha and t.head.is_alpha and t.lemma_.lower() in wordlist and t.head.lemma_.lower() in wordlist: #*:VERB:~punct:VERB:wink
			add(f"{t.head.lemma_}:{t.head.pos_}:{t.dep_}:{t.pos_}|{t.lemma_}", f"{t.head.lemma_}:{t.head.pos_}:{t.dep_}|{t.pos_}",f"{t.head.lemma_}:{t.head.pos_}|{t.dep_}", f"*:{t.head.pos_}|{t.dep_}")
			if t.dep_ not in ('ROOT'): 
				add(f"{t.lemma_}:{t.pos_}:~{t.dep_}:{t.head.pos_}|{t.head.lemma_}", f"{t.lemma_}:{t.pos_}:~{t.dep_}|{t.head.pos_}", f"{t.lemma_}:{t.pos_}|~{t.dep_}", f"*:{t.pos_}|~{t.dep_}")
			
	for sp in doc.noun_chunks: #book:NOUN:np:a book
		add(f"{sp.root.lemma_.lower()}:{sp.root.pos_}:np|{sp.text.lower()}", f"{sp.root.lemma_.lower()}:{sp.root.pos_}|np", f"*:{sp.root.pos_}|np", f"#|np",)

	# [('pp', 'on the brink', 2, 5), ('ap', 'very happy', 9, 11)]
	for lem, pos, type, chunk in en.kp_matcher(doc): #brink:NOUN:pp:on the brink
		add(f"{lem}:{pos}:{type}|{chunk}", f"{lem}:{pos}|{type}", f"*:{pos}|{type}", f"#|{type}")
	for trpx, row in en.dep_matcher(doc): #[('svx', [1, 0, 2])] ## consider:VERB:vnpn:**** 
		verbi = row[0] #consider:VERB:be_vbn_p:be considered as
		add(f"{doc[verbi].lemma_}:{doc[verbi].pos_}|{trpx}", f"*:{doc[verbi].pos_}|{trpx}", f"#|{trpx}") #consider:VERB:svx
		if trpx == 'sva' and doc[row[0]].lemma_ == 'be': # fate is sealed, added 2022.7.25
			add(f"{doc[row[1]].lemma_}:{doc[row[1]].pos_}:sbea:{doc[row[2]].pos_}|{doc[row[2]].lemma_}", f"{doc[row[1]].lemma_}:{doc[row[1]].pos_}|sbea", f"*:{doc[row[1]].pos_}|sbea")
			add(f"{doc[row[2]].lemma_}:{doc[row[2]].pos_}:~sbea:{doc[row[1]].pos_}|{doc[row[1]].lemma_}", f"{doc[row[2]].lemma_}:{doc[row[2]].pos_}|~sbea", f"*:{doc[row[2]].pos_}|~sbea")

	# last to be called, since NP is merged
	for row in en.verbnet_matcher(doc): #[(1, 0, 3, 'NP V S_ING')]
		if len(row) == 4: 
			verbi, ibeg, iend, chunk = row
			if doc[verbi].lemma_.isalpha() : 
				add(f"{doc[verbi].lemma_}:{doc[verbi].pos_}:verbnet|{chunk}") #consider:VERB:verbnet:NP V S_ING

	for name,ibeg,iend in en.post_np_matcher(doc): #added 2022.7.25
		if name in ('v_n_vbn','v_n_adj'): 
			add(f"{doc[ibeg].lemma_}:{doc[ibeg].pos_}:{name}|{doc[ibeg].lemma_} {doc[ibeg+1].lemma_} {doc[ibeg+2].text}", f"{doc[ibeg].lemma_}:{doc[ibeg].pos_}|{name}", f"*:{doc[ibeg].pos_}|{name}")

def run(infile, saveto:str='file'):
	''' saveto: mysql/file '''
	name = infile.split('.jsonlg')[0] #+ f".zset"
	start = time.time()
	fire.ssi = defaultdict(Counter)
	print ("started:", infile , saveto, flush=True)
	for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
		try:
			arr = json.loads(line.strip()) 
			doc = spacy.from_json(arr) 
			walk(doc)
		except Exception as e:
			print ("ex:", e, sid, line) 
	mysql(name, fire.ssi) if saveto == 'mysql' else tsv(name, fire.ssi) if saveto == 'file' else None 
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

def tsv(name, ssi):  
	outfile = name +".zset"
	with open( outfile, 'w') as fw:
		for k,si in ssi.items(): 
			for s,i in si.items(): 
				fw.write(f"{k}\t{s}\t{i}\n")		
	os.system(f"gzip {outfile}") #-f -9

def mysql(name, ssi, host='127.0.0.1', port=3307):  
	''' clec.spacybs -> mysql:kpsi/clec,clec_snt , 2022.7.20 '''
	import pymysql
	my_conn = pymysql.connect(host=host,port=port,user='root',password='cikuutest!',db='zset')
	with my_conn.cursor() as cursor: 
		cursor.execute(f"drop TABLE if exists {name}")
		cursor.execute(f"CREATE TABLE if not exists {name}(key varchar(64) COLLATE latin1_bin not null, name varchar(128) COLLATE latin1_bin not null, value int not null default 0, primary key(key,name) ) engine=myisam  DEFAULT CHARSET=latin1 COLLATE=latin1_bin") # not null default ''
		cursor.executemany(f"insert ignore into {name}(key, name, value) values(%s, %s, %s)",[(k,s,i) for k,si in ssi.items() for s,i in si.items() ]) 
		my_conn.commit()

if __name__	== '__main__':
	fire.Fire(run)