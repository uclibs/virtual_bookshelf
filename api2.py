#code to get json response for /v5/bibs/{id}
import requests
import base64

f=open('C:\\uc\\uclib\\credentials.txt', 'r')
lines = f.readlines()

user=lines[0].replace('\n','')
pwd=lines[1].replace('\n','')
comb = user+':'+pwd
comb_enc = base64.b64encode(bytes(comb, 'utf-8')).decode("utf-8") 

headers = {
    #'authorization': "Basic "+(user+":"+pwd).base64.b64encode("base64"),
    #'authorization': "Basic "+base64.b64encode(bytes((user+":"+pwd),encoding='utf8')),
    #'authorization': "Basic NGRpRERaVzVlK2pFdjNLNE1yaFNLeGorNmUyejpwM21hOHBAVw==",
    'authorization': "Basic "+comb_enc,
    'content-type': "application/json",
}

r = requests.post('https://uclid.uc.edu:443/iii/sierra-api/v5/token', headers=headers)
data = r.json()
print(r)
print(data)

myToken = data['access_token']
print(myToken)

headers1 = {
    'authorization': 'Bearer '+str(myToken), 
    'content-type': "application/json",
}

r1 = requests.get('https://uclid.uc.edu:443/iii/sierra-api/v5/bibs/6973150', headers=headers1)
data1 = r1.json()
print(r1)
print(data1)

