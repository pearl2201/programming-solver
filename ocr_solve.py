import requests
import base64
from PIL import Image
import pytesseract
import cv2
import os
import numpy as np


session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0'}
uri = 'http://challenge01.root-me.org/programmation/ch8/'

r = session.get(uri,headers = headers)  

# Get Image data
start = r.text.find('img') 
end = r.text.find('form') 
img_data = r.text[start+9:end-13]  

# Separate the metadata from the image data
head, data = img_data.split(',', 1)

# Get the file extension (gif, jpeg, png)
file_ext = head.split(';')[0].split('/')[1]

# Decode the image data
plain_data = base64.b64decode(data)

# save image to disk
filename = './tmp/capcha.%s' %file_ext
f = open(filename,'wb')
f.write(plain_data)
f.close()

'''
use opencv to replace black noise by white
'''
# load the example image and convert it to grayscale
image = cv2.imread(filename)
shape = np.shape(image)
for i in range(shape[0]):
	for j in range(shape[1]):
		if image[i,j,0] == 0 and image[i,j,1] == 0 and image[i,j,2] == 0:
			image[i,j,0] = 255
			image[i,j,1] = 255
			image[i,j,2] = 255
cv2.imwrite(filename, image)

''' 
use tesseract to decode image
'''
text = pytesseract.image_to_string(Image.fromarray(image))
print (text)

'''
submit solution
'''
payload = {'cametu':text}
r1 = session.post(uri,headers = headers,data=payload)

# Get validation password
print (r1.text[:r1.text.find('img')])


#os.remove(filename)

