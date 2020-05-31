# Used for downloading huge amounts of images from ImageNet via url.

import os, cv2
import urllib.request as urlreq
import numpy as np

# the URL below is probably outdated, its added as an example.
img_urls = urlreq.urlopen('http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n09629752').read().decode() 
img_num = 1
if not os.path.exists('datasett'):
    os.makedirs('datasett')
for i in img_urls.split('\n'):
    try:
        print(i)
        urlreq.urlretrieve(i, "datasett/"+str(img_num)+".jpg")
        img = cv2.imread("datasett/"+str(img_num)+".jpg") # use IMREAD_GRAYSCALE to make images black/white
        cv2.imwrite("datasett/"+str(img_num)+".jpg",img)
        print(img_num)
        img_num += 1
    except Exception as e:
            print(str(e))
