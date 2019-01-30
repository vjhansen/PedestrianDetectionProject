# dl-img-url.py 

import os, cv2
import urllib.request as urlreq
import numpy as np

img_urls = urlreq.urlopen('http://www.url..').read().decode()
img_num = 1
    
if not os.path.exists('datasett'):
    os.makedirs('datasett')

for i in img_urls.split('\n'):
    try:
        print(i)
        urlreq.urlretrieve(i, "datasett/"+str(img_num)+".jpg")
        img = cv2.imread("datasett/"+str(img_num)+".jpg",cv2.IMREAD_GRAYSCALE) #gjør bildene svart/hvit
        cv2.imwrite("datasett/"+str(img_num)+".jpg",img)
        print(img_num)
        img_num += 1
            
    except Exception as e:
            print(str(e))
