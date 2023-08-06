# 2022.10.25 
import json, traceback,sys, time, fire,os,traceback,fileinput,en, pymysql

def run(infile, host:str='172.17.0.1', port:int=3307, db:str='zset'):
	'''  '''
	name = infile.split('.jsonlg')[0] 
	start = time.time()
	print ("started:", infile , flush=True)
	my_conn = pymysql.connect(host=host,port=port,user='root',password='cikuutest!',db=db)
	with my_conn.cursor() as cursor: 
		cursor.execute(f"drop TABLE if exists {name}_snt")
		cursor.execute(f"CREATE TABLE if not exists {name}_snt(sid int primary key, snt text not null, kps text not null, fulltext key `snt`(`snt`), fulltext key `kps`(`kps`) ) engine=myisam  DEFAULT CHARSET=latin1 COLLATE=latin1_bin")
		for did, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)):  #for rowid, snt, doc in tqdm(Spacybs(dbfile).docs()) :
			try:
				arr = json.loads(line.strip()) 
				tdoc = spacy.from_json(arr) 
				for sid, sp in enumerate(tdoc.sents):
					doc = sp.as_doc()
					cursor.execute(f"insert ignore into {name}_snt(sid, snt, kps) values(%s, %s, %s)", (did * 10000 + sid,sp.text.strip(), 
					" ".join([ f"{t.lemma_}_{t.pos_}" for t in doc  if t.pos_ not in ('PUNCT')] 
					+ [ f"{t.lemma_}_{t.pos_}_{t.tag_}_{t.text.lower()}" for t in doc  if t.pos_ not in ('PUNCT')] # consider:VERB:VBG:considering
					+ [ f"{t.head.lemma_}_{t.head.pos_}_{t.dep_}_{t.pos_}_{t.lemma_}" for t in doc if t.pos_ not in ('PRON','PUNCT') and t.dep_ in ('dobj','nsubj','advmod','acomp','amod','compound','xcomp','ccomp','oprd')]) ))

			except Exception as e: 
				print ("ex:", e, did,line)
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	fire.Fire(run)