# PDP - Bachelor 19, AUT, UiT
# Fotgjengerdetektering med SSDLite + MobileNetV2

# Kode bygger på:
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

import numpy
import sys
import time
import os
import cv2    # - OpenCV
import tensorflow as TF
import serial   # - kommunikasjon med Arduino
import struct   # trengs ikke?

from datetime import datetime
from collections import defaultdict

sys.path.append("..")
# verktøy fra TensorFlow Object Detection API
from utils import label_map_util
from utils import visualization_utils as vis_util

### - Video/Webcam
cap = cv2.VideoCapture(0) # - usbkamera/webcam: forsøk (-1), (0) eller (1)
print ('[info]: Kamera tilkoblet')
#cap = cv2.VideoCapture('a1.mp4') # - teste video

# For lagring av video
#output_vid  = cv2.VideoWriter('test_out.mp4', 0x7634706d, 24, (1920,1080), True)

### - SERIELL KOMMUNIKASJON
arduino = serial.Serial(port = '/dev/tty.usbmodem14101', baudrate = 9600, timeout=1) # - Åpne serialport for komm. med Arduino
time.sleep(2)
arduino.flush()
print ('[info]: Oppretter seriell kommunikasjon med Arduino')

# For lagring av bilder
if not os.path.exists('detection_pics'):
  os.makedirs('detection_pics')
count = 0

### - MODELL
# - laster inn ferdigtrent modell
modell = 'pdp_17k_inference_graph'

# - Frozen detection graph. Dette er modellen som brukes for detekteringen.
PATH_TO_CKPT = modell + '/frozen_inference_graph.pb'

# - List of the strings that is used to add correct label for each box.
label_path = os.path.join('training', 'ob-det.pbtxt')

# - Laster inn en (frozen) Tensorflow modell
detection_graph = TF.Graph()
with detection_graph.as_default():
  od_graph_def = TF.GraphDef()
  with TF.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    TF.import_graph_def(od_graph_def, name = '')
print('[info]: Laster inn Tensorflow-modell')
     
# - Load label map
# Når modellen predikerer verdien "1" så vet vi at dette er en "person". 
label_map = label_map_util.load_labelmap(label_path)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes = 1, use_display_name = True)
category_index = label_map_util.create_category_index(categories)

with detection_graph.as_default():
    with TF.Session(graph = detection_graph) as sess:
      while True:
        ret, frame = cap.read()
        timer = cv2.getTickCount()
        im_w = 480
        im_h = 320

        sttime = datetime.now().strftime('%d.%m.%Y - %H:%M:%S - ')
        #cv2.resize(frame, (im_w,im_h))
        #output_vid.open('test_out.mp4', fourcc,20, (1280,720), True)

        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        
        # - bruker expand_dims for å endre formen på frame fra (1080, 1920, 3) til (1, 1080, 1920, 3)
        frame_expanded = numpy.expand_dims(frame, axis = 0)

        # - hver box representerer en del av bildet der et objekt ble detektert.
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

        # - hver score representerer level of confidence for each of the objects.
        # - Score vises på output-bildet sammen med klasse-label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        (boxes, scores, classes, num) = sess.run(
          [detection_boxes, detection_scores, detection_classes, num_detections], 
          feed_dict = {image_tensor: frame_expanded})

        score_thresh = 0.5  # - nedre grense for prediction-score
        max_bbx = 1        # - maks. antall bounding boxes som skal tegnes

        # - Visualisering av detekteringen
        # - numpy.squeeze fjerner 1 dimensjonale oppføringer fra formen på input-array
        vis_util.visualize_boxes_and_labels_on_image_array(
              frame, 
              numpy.squeeze(boxes),
              numpy.squeeze(classes).astype(numpy.int32), 
              numpy.squeeze(scores),
              category_index,
              use_normalized_coordinates=True
              max_boxes_to_draw = max_bbx, 
              min_score_thresh = score_thresh, 
              line_thickness = 5)

        # - Normaliserte bbx-koordinater (i forhold til størrelsen på input-frame)
        # - koord. er på formen [y_min, x_min, y_max, x_max]
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
              cv2.circle(frame, (xCenter,yCenter), 5, (0,0,255), -1)
              output_coords = 'X{0:d}Y{1:d}'.format(xCenter, yCenter)
              txt_detect = 'Detected pedestrian'
              print(output_coords)
              log = 'log.txt'
              arduino.write(output_coords.encode()) # - skriver koord. til Arduino      
              with open(os.path.join('/Users/victor/Desktop/pdp_local/logging',log),'w') as logfile:
                logfile.write(sttime + txt_detect + '\n')
              cv2.imwrite('detection_pics/'+sttime+'frame%d.jpg' % count, frame) # lagrer bilder som inneholder detektering
              cv2.imwrite("frame.jpg", frame)     # nyeste bilde for html     
              count += 1
              
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)        
        cv2.flip(frame,0)
        cv2.putText(frame, "FPS: " +str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (50,170,50), 2)
        cv2.imshow('SSDLite + MobileNetV2', cv2.resize(frame,(im_w, im_h)))
        #output_vid.write(frame)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
          break
          
cv2.destroyAllWindows()
cap.release()
#output_vid.release()
arduino.close()
