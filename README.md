# PedestrianDetectionProject - bachelor 19, automasjon, UiT

### 1) Oppsett - FloydHub
- Create Workspace
- Environment: TensorFlow 1.12, Machine: CPU (bytter til GPU senere)
- Åpne Terminal fra Launcher/Other

Installere Protobuf.
```
 cd /tmp/
 curl -OL https://github.com/google/protobuf/releases/download/v3.5.1/protoc-3.5.1-linux-x86_64.zip
 unzip protoc-3.5.1-linux-x86_64.zip -d protoc3
 mv protoc3/bin/* /usr/local/bin/
 mv protoc3/include/* /usr/local/include/
 chown `whoami` /usr/local/bin/protoc 
 chown -R `whoami` /usr/local/include/google
```
Klone modell fra TensorFlow.
```
cd /floyd/
git clone https://github.com/tensorflow/models.git

cd models/research && \
git reset --hard ea6d6aa && \
/usr/local/bin/protoc object_detection/protos/*.proto --python_out=. && \
cp -R object_detection /floyd/code && cp -R slim /floyd/code

rm -rf /floyd/code/models
export PYTHONPATH=$PYTHONPATH:/floyd/code/object_detection/:/floyd/code/slim
cd /floyd/code/ && python object_detection/builders/model_builder_test.py

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
