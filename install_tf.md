## Install TensorFlow and run program

> outdated, tested with Ubuntu 18.04 LTS and 18.10.

### 1) Download TensorFlow

```bash
cd Desktop

sudo apt install git && \
git clone https://github.com/tensorflow/models.git && \
sudo apt install python3-pip
```

### 2) Get Protobuf

```bash
sudo apt install protobuf-compiler && \
cd /models/research/ && \
protoc object_detection/protos/*.proto --python_out=. && \
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```

### 3) Install dependencies

```bash
cd /models/research/object_detection && \
git clone https://github.com/vjhansen/pdp-bachelor.git && \
cd /pdp-bachelor && \
pip3 install -r requirements.txt
```

### 4) Run program

```bash
 python3 display_detections.py
```
