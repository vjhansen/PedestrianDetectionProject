# speiler bilder

import os, sys, cv2, numpy

img_num = 1
dir_src = "Datasets/"
dir_dst = "testing/"
src_files = os.listdir(dir_src)

if not os.path.exists(dir_dst):
	os.makedirs(dir_dst)

for file in src_files:
	if os.path.isfile(dir_src+file):
		try:
			a, b = os.path.splitext(dir_src + file)
			img = cv2.imread(str(a+b), 1)
			mirror_img = cv2.flip(img, 1)
			cv2.imwrite(dir_dst + 'mir'+ str(img_num) + ".jpg", mirror_img)
			print(img_num)
			img_num += 1
		
		except Exception as e:
			print(str(e))
