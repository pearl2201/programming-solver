import requests
import base64
from pyzbar import pyzbar
from PIL import Image

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0'}

r = session.get('http://challenge01.root-me.org/programmation/ch7/',headers = headers)  

# Get Image data
start = r.text.find('img') 
end = r.text.find('form') 
img_data = r.text[start+9:end-15]  

# Separate the metadata from the image data
head, data = img_data.split(',', 1)

# Get the file extension (gif, jpeg, png)
file_ext = head.split(';')[0].split('/')[1]

# Decode the image data
plain_data = base64.b64decode(data)

# save image to disk
filename = 'background.%s' %file_ext
f = open(filename,'wb')
f.write(plain_data)
f.close()

# Gen qr code by add 3 corner image
foreground = Image.open('qrcode-top.png')
background = Image.open('background.png')
background.paste(foreground, (0, 0), foreground)
background.save('qrcode.png')

# Decode qr code
barcodes = pyzbar.decode(Image.open('D:/ret.png'))
code = barcodes[0].data.decode('utf-8')[11:]
print (code)

# Upload result
uri = 'http://challenge01.root-me.org/programmation/ch7/'
payload = {'metu':code}
r1 = session.post(uri,headers = headers,data=payload)

# Get validation password
print (r1.text[:r1.text.find('img')])

