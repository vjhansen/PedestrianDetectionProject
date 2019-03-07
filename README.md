# PedestrianDetectionProject - bachelor 19, automasjon, UiT
Victor J. Hansen & Kato S. Karlsen.


### 1)
Krever GNU/Linux eller macOS.

```
cd til skrivebord
sudo apt install git
git clone https://github.com/tensorflow/models.git
sudo apt install python3-pip
```

Legger *display_detections.py*, *pdp_final_model (folder)**, *training (folder)* og en .mp4-fil inn i /models/research/object_detection
* last heller ned pdp_17k_inference_graph, og legg den inn i /models/research/object_detection


### 2) Svært viktig steg
```
sudo apt install protobuf-compiler

cd /models/research/

protoc object_detection/protos/*.proto --python_out=.

export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim


```


### 3) Installere Python-pakker
```
pip3 install -r requirements.txt

```
evt. sjekk hva du ikke har fra før av som er i requirements.txt



### 4) Kjøre program
```
 cd /models/research/object_detection
 python3 display_detections.py
```
