# PedestrianDetectionProject - bachelor 19, automasjon, UiT

### 1) Oppsett - FloydHub
- Create Workspace
- Environment: TensorFlow 1.12, Machine: CPU (bytter til GPU senere)
- Åpne Terminal fra Launcher/Other
```
 cd /tmp/
 curl -OL https://github.com/google/protobuf/releases/download/v3.5.1/protoc-3.5.1-linux-x86_64.zip
 unzip protoc-3.5.1-linux-x86_64.zip -d protoc3
 mv protoc3/bin/* /usr/local/bin/
 mv protoc3/include/* /usr/local/include/
 chown `whoami` /usr/local/bin/protoc 
 chown -R `whoami` /usr/local/include/google
```


```
$ git clone https://github.com/tensorflow/models.git
$ wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2018_01_28.tar.gz
$ tar xf ssd_mobilenet_v1_coco_2018_01_28.tar.gz
```

Krever:
- pycocotools
- protobuf-compiler: https://github.com/protocolbuffers/protobuf/releases
``` 
$ wget https://github.com/protocolbuffers/protobuf/releases/download/v3.6.1/protobuf-python-3.6.1.tar.gz
$ tar xf protobuf-python-3.6.1.tar.gz
$ cd protobuf-python-3.6.1
$ sudo ./configure
$ sudo make check
$ sudo make install
```
models/research 
 ``` 
 $ protoc object_detection/protos/*.proto --python_out=. 
 $ export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
 ```
