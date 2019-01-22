# Victor Hansen
# 15.01.19
# python3

# skalerer alle bilder i folder, brukes også for å rename bilder.

import cv2, os, sys
import numpy as np

src_folder = "folder/"
dst_folder = "resized_folder/"

files_in_dir = os.listdir(src_folder)
img_num = 1
if not os.path.exists(dst_folder):
	os.makedirs(dst_folder)
	
for item in files_in_dir:
	if os.path.isfile(src_folder+item):
		try:
			f ,e = os.path.splitext(src_folder+item)
			print(img_num)
			img = cv2.imread(str(f+e), 1) # 0 = grayscale, 1 = RGB
			resized_img = cv2.resize(img, (512, 512))
			cv2.imwrite(dst_folder+str(img_num)+".jpg",resized_img)
			img_num+=1

		except Exception as ex:
			print(str(ex))
			
print("Resized %d pics" % (img_num))
