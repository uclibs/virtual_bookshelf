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

"""
There are two steps for getting a response using sierra API
        1) Authenticating with the Patron API
        2) Making a Sierra API call
"""
def load_client_key(file_path):
    #Step1
    #Loading Client key and secret key from the file
    f=open(file_path, 'r')
    lines = f.readlines()

    user=lines[0].replace('\n','')
    pwd=lines[1].replace('\n','')
    
    #Combining the API key and secret into a single string separated by a colon:
    return user+':'+pwd

def generate_encoded_key(combined_clientkey_secretkey):
    #Converting the combined key:secret string into a Base64 string
    return base64.b64encode(bytes(combined_clientkey_secretkey, 'utf-8')).decode("utf-8")

def authorize_api(combined_key_encrypted):
    #Setting the Header name field to authorization.
    #Setting the Header value field to Basic, and inserting the Base64-encoded credentials
    headers = {
        'authorization': "Basic "+combined_key_encrypted,
        'content-type': "application/json",
    }

    #Set the method to POST
    data = requests.post('https://uclid.uc.edu:443/iii/sierra-api/v5/token', headers=headers).json()

    #Here we will store the access_token in a variable named myToken
    return data['access_token']

def call_api_search(api_string, my_accessToken):
    #Step2
    #We will use the captured access token to make our API call
    #Setting the Header value field to Bearer, and inserting the access token
    headers1 = {
        'authorization': 'Bearer '+str(my_accessToken), 
        'content-type': "application/json",
    }

    #Set the method to GET and capture the json response into a variable
    return requests.get(api_string, headers=headers1).json()


def get_book_metadata(json_response):
    """
    Creating a hashmap named syndetics for our application where:
        key : (bib id, title of book, authors of book)
        value :  [Array of subfields parameter of the json response where fieldTag of a particular book is 'i']
        
    After creating an empty hash map we will loop through the json response obtained to fill the hashmap
    """
    syndetics=defaultdict(list)

    #Loading data into the syndetics hashmap
    for i in range(len(json_response['entries'])):
        for j in range(len(json_response['entries'][i]['bib']['varFields'])):
            if(json_response['entries'][i]['bib']['varFields'][j]['fieldTag']=='i'):
                for k in range(len(json_response['entries'][i]['bib']['varFields'][j]['subfields'])):
                    syndetics[(json_response['entries'][i]['bib']['id'],json_response['entries'][i]['bib']['title'],json_response['entries'][i]['bib']['author'])].append(json_response['entries'][i]['bib']['varFields'][j]['subfields'][k]['content'])

    return syndetics


def generate_book_covers(dictionary_response, font_path):
    """
    Here in the following code we will loop through value array of each key.
    Since ISBN numbers are stored in the value array, we will loop through them
    If we were able to get image for atleast one ISBN number in the array while traversing through the value array
    We will break there and store the [url, corresponding bib number] from which we are getting the image into an array named image_array
    
    If we had completed traversing the value array till end but still if we are unable to find the image for not even a single ISBN 
    number present in the value array that means there is no image existed in our database.
    In such case we are generating a manual image with title and author on the book cover.
    This condition is checked using a variable named count.
    If count is equal to the length of the value array which means we have looped through the entire value array
    but haven't found image for any of the ISBN's then we will enter into the second if statement.
    
    I have used a module named pillow in python for generating manual images.
    I have used a package named textwrap which fits the title and author names within the bounds of the book cover
    
    If we have manually generated an image, then the manually generated image is stored in a temporary location locally 
    and the [path, corresponding bib number] is appended into the image_array
    
    """
    image_array=[]
    for key,value in dictionary_response.items():
        count=0
        for i in range(len(value)):

            response = requests.get('http://www.syndetics.com/index.php?isbn='+str(value[i])+'/lc.jpg')
            if(bytes('large cover image', 'utf-8') in response.content):
                count+=1
            else:
                image_bytes = io.BytesIO(response.content)
                img = PIL.Image.open(image_bytes)
                image_array.append(['http://www.syndetics.com/index.php?isbn='+str(value[i])+'/lc.jpg',key[0]])
                break
            if(count==len(value)):
                W=200
                H=300
                msg="\n"+str(key[1])+"\n"+"by "+str(key[2])
                para = textwrap.wrap(msg, width=15)
                img = Image.new('RGB', (W, H), color = (73, 109, 137))       
                fnt = ImageFont.truetype(font_path, 26)
                d = ImageDraw.Draw(img)
                current_h, pad = 50, 10
                for line in para:
                    w, h = d.textsize(line, font=fnt)
                    d.text(((W - w) / 2, current_h), line, font=fnt)
                    current_h += h + pad
                arb="./"
                path=arb+str(json_string['entries'][i]['bib']['id'])+".png"
                img.save(path) 
                image_array.append([path,key[0]])
    return image_array
            
            
def gallery(url_path_arrary, limit, row_height='150px'):
    """Shows a set of images of the books that sits next to each other within the width of the notebook.
    
    Parameters
    ----------
    images: list of 
        URLs or path where the manual image is stored

    row_height: str
        CSS height value to assign to all images. Set to 'auto' by default to show images
        with their native dimensions. Set to a value like '150px' to make all rows
        in the gallery equal height.
       
    returning the HTML template
    """
    figures = []
    count=0
    for image in url_path_arrary:
        if(count<limit):
            reference="http://uclid.uc.edu.proxy.libraries.uc.edu/record=b"+str(image[1])+"~S39"
            src = image[0]
            figures.append(f'''
                <figure style="margin: 5px !important;">
                  <a href = '{reference}'>
                  <img src='{src}' style='height: {row_height}'></a>
                </figure>
            ''')
            count+=1
    return HTML(data=f'''
        <div style="display: flex; flex-flow: row wrap; text-align: center;">
        {''.join(figures)}
        </div>
    ''')

file_path = 'C:\\uc\\uclib\\credentials.txt'
font_path = 'C:\\uc\\uclib\\isbn.txt\\arial.ttf'
api_string = 'https://uclid.uc.edu:443/iii/sierra-api/v5/bibs/search?fields=id%2Ctitle%2Cauthor%2CvarFields&text=PS3616.U%3F%3F%3F%3F'
combined_clientkey_secretkey = load_client_key(file_path)
combined_key_encrypted = generate_encoded_key(combined_clientkey_secretkey)
my_accessToken = authorize_api(combined_key_encrypted)
json_response = call_api_search(api_string, my_accessToken)
dictionary_response = get_book_metadata(json_response)
url_path_arrary = generate_book_covers(dictionary_response, font_path)
number_of_images_to_display = 30
gallery(url_path_arrary, number_of_images_to_display, row_height='150px')
