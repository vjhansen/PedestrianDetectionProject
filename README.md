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
cd /floyd/home
git clone https://github.com/tensorflow/models.git

cd models/research && \
git reset --hard ea6d6aa && \
/usr/local/bin/protoc object_detection/protos/*.proto --python_out=. && \
cp -R object_detection /floyd/home/code && cp -R slim /floyd/home/code

rm -rf /floyd/code/models
export PYTHONPATH=$PYTHONPATH:/floyd/home/code/object_detection/:/floyd/home/code/slim
cd /floyd/home/code/ && python object_detection/builders/model_builder_test.py

```
Output skal være: 
Ran 15 tests in 0.s

OK


### 2) Laste ned coco modell

```
 cd /floyd/home/code/object_detection
 wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2018_01_28.tar.gz
 tar xf ssd_mobilenet_v1_coco_2018_01_28.tar.gz
 
 #git clone https://github.com/vjhansen/pdp-bachelor.git (senere, privat nå)
 
```

### 3) legge til filer
```
mkdir training
```

```
object_detection
|--> data
|   |--> test.record
|   |--> train.record
|   
|--> training
|   |--> ssd_mobilenet_v1_coco.config
|   |--> training_ob-det.pbtxt

```

### 4) bytt til GPU-maskin
```
pip -q install pycocotools

python train.py --logtostderr --train_dir=training/ --pipeline_config_path=training/ssd_mobilenet_v1_coco.config

V
python model_main.py --logtostderr --train_dir=training/ --pipeline_config_path=training/ssd_mobilenet_v1_coco.config


Tensorboard
cp -R training/ /floyd/home
tensorboard --logdir='training'
eller trykk på TensorBoard-knappen nederst på skjermen (ved cpu-% osv)
```


### 5) eksportere inference graph
```
python3 export_inference_graph.py \
    --input_type image_tensor \
    --pipeline_config_path training/ssd_mobilenet_v1_coco.config \
    --trained_checkpoint_prefix training/model.ckpt-10856 \
    --output_directory pdp_alpha_inference_graph

# model.ckpt-'største nr' (meta)

```

