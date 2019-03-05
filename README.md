# PedestrianDetectionProject - bachelor 19, automasjon, UiT
Victor J. Hansen & Kato S. Karlsen.


### 1)
Krever GNU/Linux eller macOS.

```
sudo apt install git
git clone https://github.com/tensorflow/models.git
sudo apt install python3-pip
```

Legger *display_detections.py*, *pdp_final_model (folder)*, *training (folder)* og en .mp4-fil inn i /models/research/object_detection


### 2)
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



### 4) Kjøre program
```
 cd /models/research/object_detection
 python3 display_detections.py
```
