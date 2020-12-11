#code to get json response for /v5/bibs/search
import requests
import base64
import PIL
import io
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict
import textwrap


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
syndetics=defaultdict(list)
for i in range(len(json_string['entries'])):
    for j in range(len(json_string['entries'][i]['bib']['varFields'])):
        if(json_string['entries'][i]['bib']['varFields'][j]['fieldTag']=='i'):
            for k in range(len(json_string['entries'][i]['bib']['varFields'][j]['subfields'])):
                syndetics[(json_string['entries'][i]['bib']['id'],json_string['entries'][i]['bib']['title'],json_string['entries'][i]['bib']['author'])].append(json_string['entries'][i]['bib']['varFields'][j]['subfields'][k]['content'])

for key,value in syndetics.items():
    count=0
    for i in range(len(value)):
        response = requests.get('http://www.syndetics.com/index.php?isbn='+str(value[i])+'/lc.jpg')
        if(bytes('large cover image', 'utf-8') in response.content):
            count+=1
        else:
            # print("yes cover")
            image_bytes = io.BytesIO(response.content)
            img = PIL.Image.open(image_bytes)
            img.show()
            break
        if(count==len(value)):
            # print("No cover Module")
            # print("No cover")
            W=200
            H=300
            msg="\n"+"Title: "+str(key[1])+"\n"+"Author: "+str(key[2])
            para = textwrap.wrap(msg, width=15)
            img = Image.new('RGB', (W, H), color = (73, 109, 137))       
            fnt = ImageFont.truetype('C:\\uc\\uclib\\isbn.txt\\arial.ttf', 26)
            d = ImageDraw.Draw(img)
            current_h, pad = 50, 10
            for line in para:
                w, h = d.textsize(line, font=fnt)
                d.text(((W - w) / 2, current_h), line, font=fnt)
                current_h += h + pad
            # w, h = d.textsize(para)
            # ((W-w)/2,(H-h)/2)
            # d.text((250,120), msg , font=fnt, fill=(255, 255, 0))
            img.show()
            
            
# for i in range(len(json_string['entries'])):
#     for j in range(len(json_string['entries'][i]['bib']['varFields'])):
#         if(json_string['entries'][i]['bib']['varFields'][j]['fieldTag']=='i'):
#             for k in range(len(json_string['entries'][i]['bib']['varFields'][j]['subfields'])):
#                 syndetics[json_string['entries'][i]['bib']['varFields'][j]['subfields'][k]['content']]=syndetics.get(json_string['entries'][i]['bib']['varFields'][j]['subfields'][k]['content'],0)+1
# arr=[]
# for key in syndetics:
#     if(key.isdigit()):
#         arr.append(key)

# with open('C:\\uc\\uclib\\isbn.txt', 'w') as txt_file:
#     for line in arr:
#         txt_file.write(line + "\n")
        
# for i in arr:
#     response = requests.get('http://www.syndetics.com/index.php?isbn='+str(i)+'/lc.jpg')
#     if(bytes('large cover image', 'utf-8') in response.content):
#         # print("No cover")
#         W=800
#         H=300
#         msg="Image Not Available"
#         img = Image.new('RGB', (W, H), color = (73, 109, 137))       
#         fnt = ImageFont.truetype('C:\\uc\\uclib\\isbn.txt\\arial.ttf', 30)
#         d = ImageDraw.Draw(img)
#         w, h = d.textsize(msg)
#         # ((W-w)/2,(H-h)/2)
#         d.text((250,120), msg , font=fnt, fill=(255, 255, 0))
#         img.show()
#     else:
#         # print("yes cover")
#         image_bytes = io.BytesIO(response.content)
#         img = PIL.Image.open(image_bytes)
#         img.show()
#print(r1)
#print(data1)