# 30.01
# python3 pdp.py

import numpy as np
import sys, os, cv2, time
import tensorflow as tf
import zipfile, tarfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

#cap = cv2.VideoCapture(0) # webcam: prøv (-1,0,1)
cap = cv2.VideoCapture('vid2.mp4') # teste video
time.sleep(3.0)

sys.path.append("..")
# Import fra object detection module.
from utils import label_map_util
from utils import visualization_utils as vis_util

# Model preparation 
MODEL_NAME = 'pdp-alpha-v2'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('training', 'training_ob-det.pbtxt')

NUM_CLASSES = 1

# -- Load a (frozen) Tensorflow model into memory --

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# -- Loading label map --
# Label maps map indices to category names, so that when our convolution network predicts `5`, 
# we know that this corresponds to `airplane`.  
# Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def circle_draw(frame, x,y):
  cv2.circle(frame, (x,y), 10, (0,0,255), -1)

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    while True:
      ret, frame = cap.read()
      im_w = 720
      im_h = 576
      cv2.resize(frame, (im_w, im_h))
      stime = time.time()
      
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      frame_expanded = np.expand_dims(frame, axis=0)
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      
      # Each box represents a part of the image where a particular object was detected.
      boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      
      # Each score represent how level of confidence for each of the objects.
      # Score is shown on the result image, together with the class label.
      scores = detection_graph.get_tensor_by_name('detection_scores:0')
      classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')

      #Actual detection.
      (boxes, scores, classes, num_detections) = sess.run(
          [boxes, scores, classes, num_detections],
          feed_dict={image_tensor: frame_expanded})
      
      score_thresh = 0.6
      max_bbx = 2
      
      # Visualization of the results of a detection.
      vis_util.visualize_boxes_and_labels_on_image_array(
          frame,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          max_boxes_to_draw = max_bbx,
          min_score_thresh = score_thresh,
          line_thickness = 4)
      
      # getting normalized coordinates for bounding box
      # ymin og ymax bytter plass (pga. koordinatsystem i pyplot)
      ymax = (boxes[0][0][0]) 
      xmin = (boxes[0][0][1])
      ymin = (boxes[0][0][2])
      xmax = (boxes[0][0][3])

      cols = (frame.shape[1])
      rows = (frame.shape[0])
      
      # sentrum av rektangel
      xCenter = int((xmax + xmin)*cols / 2.0)
      yCenter = int((ymax + ymin)*rows / 2.0)

      (left, right, top, bottom) = (xmin*im_w, xmax*im_w, ymin*im_h, ymax*im_h)
      
      # openCV stuff....
      # print('FPS {:.1f}'.format(1/(time.time()-stime)))
      
      for i in range(min(max_bbx, boxes.shape[0])):
        if np.squeeze(scores)[i] > score_thresh:
          circle_draw(frame, xCenter, yCenter)
          print('target acquired')
      
      cv2.imshow('PDP', cv2.resize(frame, (im_w, im_h)))
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
