import requests
import base64
from pyzbar import pyzbar
from PIL import Image

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0'}
r = session.get('http://challenge01.root-me.org/programmation/ch7/',headers = headers)  
start = r.text.find('img') 
end = r.text.find('form') 
img_data = r.text[start+9:end-15]  
# Separate the metadata from the image data
head, data = img_data.split(',', 1)

# Get the file extension (gif, jpeg, png)
file_ext = head.split(';')[0].split('/')[1]

# Decode the image data
plain_data = base64.b64decode(data)

filename = 'D:/qrcode.%s' %file_ext
f = open(filename,'wb')
f.write(plain_data)
f.close()

foreground = Image.open('qrcode-top.png')
background = Image.open('D:/qrcode.png')
background.paste(foreground, (0, 0), foreground)
background.save('D:/ret.png')

barcodes = pyzbar.decode(Image.open('D:/ret.png'))
print (barcodes)
print(barcodes[0].data.decode('utf-8')[11:])
code = barcodes[0].data.decode('utf-8')[11:]
print (code)
uri = 'http://challenge01.root-me.org/programmation/ch7/'
print (uri)
payload = {'metu':code}
r1 = session.post(uri,headers = headers,data=payload)
print (r1.headers)
print (r1.text[:r1.text.find('img')])

