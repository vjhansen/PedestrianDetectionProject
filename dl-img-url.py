# dl-img-url.py 

# http://www.image-net.org/about-overview

import urllib.request as urlreq
import cv2
import numpy as np
import os

img_urls = urlreq.urlopen('http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n04335209').read().decode()
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