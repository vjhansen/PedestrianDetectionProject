# pdp-bachelor
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
 ``` $ protoc object_detection/protos/*.proto --python_out=. ```
