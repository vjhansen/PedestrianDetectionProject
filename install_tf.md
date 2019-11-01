## Installere TensorFlow


### 1) Laste ned TensorFlow
Testet med Ubuntu 18.04 LTS og 18.10

```bash
cd Desktop

sudo apt install git && \
git clone https://github.com/tensorflow/models.git && \
sudo apt install python3-pip
```



### 2) Protobuf
```bash
sudo apt install protobuf-compiler && \
cd /models/research/ && \
protoc object_detection/protos/*.proto --python_out=. && \
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

```


### 3) Installere dependencies
```bash
cd /models/research/object_detection && \
git clone https://github.com/vjhansen/pdp-bachelor.git && \
cd /pdp-bachelor && \
pip3 install -r requirements.txt
```


### 4) Kjøre program
```bash
 python3 display_detections.py
```
