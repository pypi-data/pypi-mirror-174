# 2022.9.2
import requests ,os
coshost		= os.getenv('coshost', 'json-1257827020.cos.ap-shanghai.myqcloud.com')
cos_json	= lambda filename='230537': requests.get(f"https://{coshost}/{filename}.json").json() #essays	= lambda : requests.get(f"https://{coshost}/230537.json").json()
cos_tsv		= lambda filename='verb_mf': [ row.split("\t") for row in requests.get("https://tsv-1257827020.cos.ap-nanjing.myqcloud.com/verb_mf.tsv").text.strip().split("\n")]
cos_tsv_dic = lambda filename='verb_mf': dict(cos_tsv(filename))

from api.dm import * 
from api.wget import * 
from api.es import * 
from api.chunk import * 

def walk():
	import os
	for root, dirs, files in os.walk(".",topdown=False):
		for file in files: 
			if file.endswith(".py") and not file.startswith("_"): 
				file = file.split(".")[0]
				__import__(file, fromlist=['*']) #			importlib. 

if __name__	== '__main__': 
	print (cos_tsv_dic()) 
