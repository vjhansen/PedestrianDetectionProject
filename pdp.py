# PDP - Bachelor 19, AUT, UiT
# update: 15.02, victor

# https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/

import numpy
import sys
import time
import os
import cv2
import tensorflow as tf
import serial # - kommunikasjon med Arduino

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from utils import label_map_util
from utils import visualization_utils as vis_util

#cap = cv2.VideoCapture(0) # - usbkamera/webcam: forsøk (-1), (0) eller (1)
cap = cv2.VideoCapture('vid_town.avi') # - teste video

# - laster inn ferdigtrent modell
modell = 'pdp-alpha-v1'

# - Frozen detection graph. Dette er modellen som brukes for detekteringen.
PATH_TO_CKPT = modell + '/frozen_inference_graph.pb'

# - List of the strings that is used to add correct label for each box.
label_path = os.path.join('training', 'training_ob-det.pbtxt')

# - Laster inn en (frozen) Tensorflow model
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name = '')

# - Load label map
# Når CNN predikerer verdien "1" så vet vi at dette er en "person". 
label_map = label_map_util.load_labelmap(label_path)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes = 1, use_display_name = True)
category_index = label_map_util.create_category_index(categories)

#ser = serial.Serial('/dev/tty.usbserial', 9600) # - Åpne serialport for komm. med Arduino

with detection_graph.as_default():
  with tf.Session(graph = detection_graph) as sess:
    while True:
      # - leser videokilde    
      ret, frame = cap.read()
      timer = cv2.getTickCount()
      # - størrelse på display-vindu
      im_w = 720
      im_h = 576
      cv2.resize(frame, (im_w, im_h))
      
      # - bruker expand_dims for å endre formen på frame fra (1080, 1920, 3) til (1, 1080, 1920, 3)
      frame_expanded = numpy.expand_dims(frame, axis = 0)
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      
      # - Each box represents a part of the image where a particular object was detected.
      boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      
      # - Each score represent how level of confidence for each of the objects.
      # - Score is shown on the result image, together with the class label.
      scores = detection_graph.get_tensor_by_name('detection_scores:0')
      #classes = detection_graph.get_tensor_by_name('detection_classes:0')
      #num_detections = detection_graph.get_tensor_by_name('num_detections:0')

      # - Actual detection.
      #(boxes, scores, classes, num_detections) = sess.run(
        #  [boxes, scores, classes, num_detections],
        #  feed_dict = {image_tensor: frame_expanded})

      (boxes, scores) = sess.run(
          [boxes, scores],
          feed_dict = {image_tensor: frame_expanded})
  
      score_thresh = 0.5 # - nedre grense for prediction-score
      max_bbx = 3 # - maks. antall bounding boxes som skal tegnes

      # - Visualisering av detekteringen
      # - numpy.squeeze fjerner 1 dimensjonale oppføringer fra formen på input-array
      ##vis_util.visualize_boxes_and_labels_on_image_array(
         ## frame,
         ## numpy.squeeze(boxes),
         ## numpy.squeeze(classes).astype(numpy.int),
         ## numpy.squeeze(scores),
         ## category_index,
         ## max_boxes_to_draw = max_bbx,
         ## min_score_thresh = score_thresh,
         ## line_thickness = 10)
      
      # - Normaliserte bbx-koordinater (i forhold til størrelsen på input-frame)
      # - koord. er på formen [y_min, x_min, y_max, x_max]
      ymin = (boxes[0][0][0]) 
      xmin = (boxes[0][0][1])
      ymax = (boxes[0][0][2])
      xmax = (boxes[0][0][3])

      # - W (bredde) og H (høyde) endres med oppløsningen på film/kamera
      # - ex. webcam på mac gir 1920x1080
      W = (frame.shape[1]) # - horisontal
      H = (frame.shape[0]) # - vertikal
      #print(W,H)
      
      # - Sentrum av bounding box
      xCenter = int((xmax + xmin)*W / 2.0)
      yCenter = int((ymax + ymin)*H / 2.0)

      n_ymin = int(ymin*H)
      n_xmin = int(xmin*W)
      n_ymax = int(ymax*H)
      n_xmax = int(xmax*W)
      # (left, right, top, bottom) = (xmin*W, xmax*W, ymax*H, ymin*H)
      
      # - Tegner sirkel i sentrum av bounding box med høyeste score
      for i in range(min(max_bbx, boxes.shape[0])):
        if numpy.squeeze(scores)[i] > score_thresh:
          cv2.circle(frame, (xCenter,yCenter), 10, (0,0,255), -1)
          #print(str(xCenter)+'x'+str(yCenter))
          #cv2.rectangle(frame, (n_xmin, n_ymin), (n_xmax, n_ymax), (0,0,255), 10)
          #ser.write(xCenter,yCenter) # - skriver koord. til Arduino

      fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
      cv2.putText(frame, "FPS: " +str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 1.75, (50,170,50), 2)
      cv2.imshow('Fotgjengerdetektering', cv2.resize(frame, (im_w, im_h))) # - viser detektering ++ i sanntid
      if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break
