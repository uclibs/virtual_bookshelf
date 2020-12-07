#code to get json response for /v5/bibs/search
import requests
import base64
import PIL
import io


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

r1 = requests.get('https://uclid.uc.edu:443/iii/sierra-api/v5/bibs/search?fields=id%2Ctitle%2Cauthor%2CvarFields&text=PS3616.U%3F%3F%3F%3F', headers=headers1)
json_string = r1.json()
syndetics =dict()
for i in range(len(json_string['entries'])):
    for j in range(len(json_string['entries'][i]['bib']['varFields'])):
        if(json_string['entries'][i]['bib']['varFields'][j]['fieldTag']=='i'):
            for k in range(len(json_string['entries'][i]['bib']['varFields'][j]['subfields'])):
                syndetics[json_string['entries'][i]['bib']['varFields'][j]['subfields'][k]['content']]=syndetics.get(json_string['entries'][i]['bib']['varFields'][j]['subfields'][k]['content'],0)+1
arr=[]
for key in syndetics:
    if(key.isdigit()):
        arr.append(key)

for i in arr:
    response = requests.get('http://www.syndetics.com/index.php?isbn='+str(i)+'/lc.jpg')
    image_bytes = io.BytesIO(response.content)
    img = PIL.Image.open(image_bytes)
    img.show()
#print(r1)
#print(data1)
