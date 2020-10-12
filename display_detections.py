# Pedestrian Detection using SSDLite + MobileNetV2

# Code is based on:
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

import numpy
import sys
import time
import os
import cv2

import tensorflow.compat.v1 as TF
TF.disable_v2_behavior()

from datetime import datetime
from collections import defaultdict

sys.path.append("..")
# - Tools from TensorFlow Object Detection API
from utils import label_map_util
from utils import visualization_utils as vis_util

### - VIDEO
cap = cv2.VideoCapture(0) # - usb-cam/webcam: try (-1), (0) or (1)
print ('[info]: Kamera tilkoblet')

# - storing of images
if not os.path.exists('detection_pics'):
  os.makedirs('detection_pics')
count = 0

### - MODEL
modell = 'pdp_v2'
# - model used for detection
PATH_TO_CKPT = modell + '/frozen_inference_graph.pb'

# ob-det.pbtxt contains label for 'person'.
label_path = os.path.join('training', 'ob-det.pbtxt')

# - Load model
detection_graph = TF.Graph()
with detection_graph.as_default():
  od_graph_def = TF.GraphDef()
  with TF.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    TF.import_graph_def(od_graph_def, name = '')
print('[info]: Laster inn TensorFlow-modell')
     

# When our model predicts the value '1', then we know that this is a 'person'. 
label_map = label_map_util.load_labelmap(label_path)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes = 1, use_display_name = True)
category_index = label_map_util.create_category_index(categories)

# - Start pedestrian detection
with detection_graph.as_default():
    with TF.Session(graph = detection_graph) as sess:
      while True:
        ret, frame = cap.read()
        timer = cv2.getTickCount()
        im_w = 1280
        im_h = 720
        sttime = datetime.now().strftime('%d.%m.%Y - %H:%M:%S - ')
        
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # - using expand_dims to change frame shape from (1080, 1920, 3) to (1, 1080, 1920, 3)
        frame_expanded = numpy.expand_dims(frame, axis = 0)

        # - each box represents a piece of the image-frame where a pedestrian was detected.
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # - each score represents the probability for each detected object.
        # - a score is shown on the output image-frame with the label 'person'
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        
        # - running the actual detection
        (boxes, scores, classes, num) = sess.run(
          [detection_boxes, detection_scores, detection_classes, num_detections], 
          feed_dict = {image_tensor: frame_expanded})

        score_thresh = 0.5  # - lower threshold of prediction score 
        max_bbx = 5         # - max. number of bounding boxes to be drawn

        # - Visualization of the detection
        # - numpy.squeeze removes the 1-D entries in the input array's shape
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

        # - Normalize bbx-coordinates (relative to the input-frame's size)
        # - coordinates: [y_min, x_min, y_max, x_max]
        ymin = (boxes[0][0][0]) 
        xmin = (boxes[0][0][1])
        ymax = (boxes[0][0][2])
        xmax = (boxes[0][0][3])

        # - W (width) and H (height) varies according to the resolution of the video-input.
        W = (frame.shape[1]) # - horizontal
        H = (frame.shape[0]) # - vertical
       
        # - Draw a small circle in the centre of the bounding box with the highest score
        for i in range(min(max_bbx, boxes.shape[0])):
          if numpy.squeeze(scores)[i] > score_thresh:
              (bbx_ymin, bbx_xmin, bbx_ymax, bbx_xmax) = (int(ymin*H), int(xmin*W), int(ymax*H), int(xmax*W))
              xCenter = int((xmax + xmin)*W / 2.0)
              yCenter = int((ymax + ymin)*H / 2.0)
              cv2.circle(frame, (xCenter, yCenter), 3, (0,0,255), -1)
              # - coordinates for centre of detected object
              output_coords = 'X{0:d}Y{1:d}'.format(xCenter, yCenter)
              # - save images containing detected objects
              cv2.imwrite('detection_pics/' + sttime + 'frame%d.jpg' % count, frame)
              count += 1   
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)        
        cv2.flip(frame, 0)
        score_view = numpy.squeeze(scores)[0]*100
        cv2.putText(frame, "FPS: " + str(int(fps)), (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
        cv2.putText(frame, "Person: " + str(int(score_view)) + '%', (300,60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
        # - Video stream
        cv2.imshow('SSDLite + MobileNetV2', cv2.resize(frame, (im_w, im_h)))
        if cv2.waitKey(10) & 0xFF == ord('q'):
          break
cv2.destroyAllWindows()
cap.release()
