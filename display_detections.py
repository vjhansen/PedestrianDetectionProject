# PDP - Bachelor 19, Automasjon
# Fotgjengerdetektering med SSDLite + MobileNetV2

# Kode bygger på:
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

import numpy
import sys
import time
import os
import cv2    # - OpenCV
import tensorflow as TF

from datetime import datetime
from collections import defaultdict

sys.path.append("..")
# - Verktøy fra TensorFlow Object Detection API
from utils import label_map_util
from utils import visualization_utils as vis_util

### - VIDEO
cap = cv2.VideoCapture(0) # - usbkamera/webcam: forsøk (-1), (0) eller (1)
print ('[info]: Kamera tilkoblet')

# - For lagring av bilder
if not os.path.exists('detection_pics'):
  os.makedirs('detection_pics')
count = 0

### - MODELL
modell = 'pdp_v2'
# - Dette er modellen som brukes for detekteringen.
PATH_TO_CKPT = modell + '/frozen_inference_graph.pb'

# - ob-det.pbtxt inneholder label for 'person'.
label_path = os.path.join('training', 'ob-det.pbtxt')

# - Laster inn modellen vår
detection_graph = TF.Graph()
with detection_graph.as_default():
  od_graph_def = TF.GraphDef()
  with TF.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    TF.import_graph_def(od_graph_def, name = '')
print('[info]: Laster inn TensorFlow-modell')
     

# Når modellen predikerer verdien '1' så vet vi at dette er en 'person'. 
label_map = label_map_util.load_labelmap(label_path)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes = 1, use_display_name = True)
category_index = label_map_util.create_category_index(categories)

# - Starter detektering av fotgjengere
with detection_graph.as_default():
    with TF.Session(graph = detection_graph) as sess:
      while True:
        ret, frame = cap.read()
        timer = cv2.getTickCount()
        im_w = 1280
        im_h = 720
        frame = cv2.pyrUp(frame,frame)
        sttime = datetime.now().strftime('%d.%m.%Y - %H:%M:%S - ')
        
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # - Bruker expand_dims for å endre formen på frame fra (1080, 1920, 3) til (1, 1080, 1920, 3)
        frame_expanded = numpy.expand_dims(frame, axis = 0)

        # - Hver boks representerer en del av bildet der en fotgjenger ble detektert.
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # - Hver score representerer sannsynligheten for hvert detekterte objekt.
        # - En score vises på output-bildet sammen med label for klasse 'person'.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        
        # - her kjøres selve detekteringen
        (boxes, scores, classes, num) = sess.run(
          [detection_boxes, detection_scores, detection_classes, num_detections], 
          feed_dict = {image_tensor: frame_expanded})

        score_thresh = 0.5  # - nedre grense for prediction-score
        max_bbx = 5         # - maks. antall bounding boxes som skal tegnes

        # - Visualisering av detekteringen
        # - numpy.squeeze fjerner 1 dimensjonale oppføringer fra formen på input-array
        vis_util.visualize_boxes_and_labels_on_image_array(
              frame, 
              numpy.squeeze(boxes),
              numpy.squeeze(classes).astype(numpy.int32), 
              numpy.squeeze(scores),
              category_index,
              use_normalized_coordinates = True,
              max_boxes_to_draw = max_bbx, 
              min_score_thresh = score_thresh, 
              line_thickness = 4)

        # - Normaliserte bbx-koordinater (i forhold til størrelsen på input-frame)
        # - Koordinater er på formen [y_min, x_min, y_max, x_max]
        ymin = (boxes[0][0][0]) 
        xmin = (boxes[0][0][1])
        ymax = (boxes[0][0][2])
        xmax = (boxes[0][0][3])

        # - W (bredde) og H (høyde) endres med oppløsningen på film/kamera
        W = (frame.shape[1]) # - horisontal
        H = (frame.shape[0]) # - vertikal
       
        # - Tegner sirkel i sentrum av bounding box med høyeste score
        for i in range(min(max_bbx, boxes.shape[0])):
          if numpy.squeeze(scores)[i] > score_thresh:
              (bbx_ymin, bbx_xmin, bbx_ymax, bbx_xmax) = (int(ymin*H), int(xmin*W), int(ymax*H), int(xmax*W))
              xCenter = int((xmax + xmin)*W / 2.0)
              yCenter = int((ymax + ymin)*H / 2.0)
              # - Sirkel
              cv2.circle(frame, (xCenter, yCenter), 3, (0,0,255), -1)
              # - Tegner rektangel rundt fotgjenger (alternativ til visualize_boxes_and_labels_on_image_array)
              #cv2.rectangle(frame, (bbx_xmin, bbx_ymin), (bbx_xmax, bbx_ymax), (0,255,0), 4)
              # - Koordinater for sentrum av fotgjenger
              output_coords = 'X{0:d}Y{1:d}'.format(xCenter, yCenter)
              # - Lagrer bilder som inneholder et detektert objekt.
              cv2.imwrite('detection_pics/' + sttime + 'frame%d.jpg' % count, frame)
              count += 1   
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)        
        cv2.flip(frame, 0)
        # - Viser bildefrekvens på videostrømmen.
        score_view = numpy.squeeze(scores)[0]*100
        cv2.putText(frame, "FPS: " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (50, 170, 50), 2)
        cv2.putText(frame, "score: " + str(score_view), (500,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (50, 170, 50), 2)
        # - Videostrømming
        cv2.imshow('SSDLite + MobileNetV2', cv2.resize(frame, (im_w, im_h)))
        if cv2.waitKey(10) & 0xFF == ord('q'):
          break
cv2.destroyAllWindows()
cap.release()
