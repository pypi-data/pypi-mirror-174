#2022.9.11
from uvirun import *
tat = lambda : requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/", data={"app_id":"cli_a390c187f1f9d00b", "app_secret":"sL6udKjwYarn3y8QKb4nyfO18OFqyp3F"}).json()['tenant_access_token']
print(tat())
geturl = lambda url: requests.get(url, headers = {"content-type":"application/json", "Authorization":f"Bearer {tat()}"}).json()

print( geturl("https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/shtcnyJFiHPwDkAeXGi0RdGVW3b/sheets/query"))

@app.get('/feishu/tat')
def feishu_tat(): return tat ()

@app.post('/flair/frame/snts')
def frame_snts(snts:list=["George returned to Berlin to return his hat.","He had a look at different hats."]):  
	''' ["George returned to Berlin to return his hat.","He had a look at different hats."]	'''
	return { snt: frame_snt(snt) for snt in snts }


if __name__ == '__main__': # read 'snt' from es,  parse , and submit back to ES, with type='frame' 
	import fire
	#fire.Fire({"walk":walk, "hello": frame_snt})
	pass

