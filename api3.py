#code to get json response for /v5/bibs/search
import requests
import base64
import PIL
import io
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict
import textwrap
from IPython.display import HTML
from io import BytesIO
import struct

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

image_array=[]
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
            #img.show()
            image_array.append(['http://www.syndetics.com/index.php?isbn='+str(value[i])+'/lc.jpg',key[0]])
            #image_array.append(image_bytes)
            #image_array.append(img)
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
            #img.show()
            arb="./"
            path=arb+str(json_string['entries'][i]['bib']['id'])+".png"
            img.save(path) 
            image_array.append([path,key[0]])
            
# from IPython.display import Image as img_ipy     
# def _src_from_data(data):
    #str = base64.b64encode(imageFile.read())
#     data_uri = base64.b64encode(Image.fromarray(data)).decode('utf-8')
#     img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
#     return img_tag
#     """Base64 encodes image bytes for inclusion in an HTML img element"""
#     data=data.tobytes()
#     data_uri = base64.b64encode(Image.fromarray(data)).decode('utf-8')
#     img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
#     return img_tag
    #print(data)
    #print("\n")
    #print("**************************************************")
#     data=data.tobytes()
#     data_uri = data.read().encode('base64').replace('\n', '')
#     return f'<img src="data:image/png;base64,{0}" width="400" height="275">'.format(data_uri)
#     #print("\n")
#     #print(data)
#     def convert_string_to_bytes(string):
#         bytes = b''
#         for i in string:
#             bytes += struct.pack("B", ord(i))
#         return bytes
#     stream = BytesIO(convert_string_to_bytes(data))
#     image = Image.open(stream).convert("RGBA")
#     stream.close()
# #     image.show()
#     img_obj = img_ipy(data=data)
#     for bundle in img_obj._repr_mimebundle_():
#         for mimetype, b64value in bundle.items():
#             #if mimetype.startswith('image/'):
#             return f'data:{mimetype};base64,{b64value}'
#     data_uri = base64.b64encode(open(str(data), 'rb').read()).decode('utf-8')
#     img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
#     return img_tag
            
def gallery(images, row_height='150px'):
    """Shows a set of images in a gallery that flexes with the width of the notebook.
    
    Parameters
    ----------
    images: list of str or bytes
        URLs or bytes of images to display

    row_height: str
        CSS height value to assign to all images. Set to 'auto' by default to show images
        with their native dimensions. Set to a value like '250px' to make all rows
        in the gallery equal height.
    """
    figures = []
    for image1 in images:
        #image1.show()
        #print(type(image1))
        reference="http://uclid.uc.edu.proxy.libraries.uc.edu/record=b"+str(image1[1])+"~S39"
        if '.png' in image1[0]:
            #print("entered if")
            src = image1[0]
            #print(image1[1])
            #print(src)
        else:
            #print("entered else")
            src = image1[0]
        figures.append(f'''
            <figure style="margin: 5px !important;">
              <a href = '{reference}'>
              <img src='{src}' style='height: {row_height}'></a>
            </figure>
        ''')
    return HTML(data=f'''
        <div style="display: flex; flex-flow: row wrap; text-align: center;">
        {''.join(figures)}
        </div>
    ''')

gallery(image_array, row_height='150px')
