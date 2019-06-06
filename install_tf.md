## Installere TensorFlow


### 1)
Testet med Ubuntu 18.04 LTS og 18.10

```
cd Desktop

sudo apt install git && \
git clone https://github.com/tensorflow/models.git && \
sudo apt install python3-pip
```

Flytt *display_detections.py*, *pdp_v2 (folder)*, og *training (folder)* til */models/research/object_detection*


### 2) Svært viktig steg
```
sudo apt install protobuf-compiler && \
cd /models/research/ && \
protoc object_detection/protos/*.proto --python_out=. && \
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

```


### 3) Installere
```
cd /models/research/object_detection
git clone https://github.com/vjhansen/pdp-bachelor.git
cd /pdp-bachelor
pip3 install -r requirements.txt
```


### 4) Kjøre program
```
 python3 display_detections.py
```
