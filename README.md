# PedestrianDetectionProject - bachelor 19, automasjon, UiT
Victor J. Hansen & Kato S. Karlsen.


### 1)
Testet med Ubuntu 18.04 LTS og 18.10

```
cd Skrivebord eller Desktop
sudo apt install git
git clone https://github.com/tensorflow/models.git
sudo apt install python3-pip
```

Legger *display_detections.py*, *pdp_17k_inference_graph (folder)**, *training (folder)* inn i /models/research/object_detection


### 2) Svært viktig steg
```
sudo apt install protobuf-compiler

cd /models/research/

protoc object_detection/protos/*.proto --python_out=.

export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

```


### 3) Installere
```
cd /models/research/object_detection
#git clone https://github.com/vjhansen/pdp-bachelor.git (privat)
pip3 install -r requirements.txt
```


### 4) Kjøre program
```
 python3 display_detections.py
```
