# PedestrianDetectionProject - bachelor 19, automasjon, UiT

### 1) Oppsett - FloydHub
- Create Workspace
- Environment: TensorFlow 1.12, Machine: GPU
- Åpne Terminal fra Launcher/Other

```sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade```

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
cp -R object_detection /floyd/home/kode && cp -R slim /floyd/home/kode
```
^kjør denne på nytt hvis: 
can't open file 'object_detection/builders/model_builder_test.py': [Errno 2] No such file or directory

*Bruker en tidligere commit (git reset --hard ea6d6aa) av TensorFlow/Models/research*
```
rm -rf /floyd/home/kode/models
export PYTHONPATH=$PYTHONPATH:/floyd/home/kode/object_detection/:/floyd/home/kode/slim
cd /floyd/home/kode && python object_detection/builders/model_builder_test.py

```
Output skal være: 
```
Ran 15 tests in 0.xxxs

OK
```

### 2) Laste ned modell fra Tensorflow detection model zoo.

```
 cd /floyd/home/kode/object_detection
 # kan egentlig bare lagres i /kode
 wget http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
 tar xf ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz

# wget http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2018_01_28.tar.gz
# tar xf ssd_mobilenet_v1_coco_2018_01_28.tar.gz
# git clone https://github.com/vjhansen/pdp-bachelor.git (senere, privat nå)
```

### 3) legge til filer
(dette må gjøres manuelt..)
```
cd /floyd/home/kode/
mkdir training
```
```
kode
|--> data
|   |--> test.record (ligger på onedrive)
|   |--> train.record (ligger på onedrive)
|   
|--> training
|   |--> ssd_mobilenet_v1_coco.config
|   |--> training_ob-det.pbtxt

```

### 4) Trening
```
cd /floyd/home/
pip -q install pycocotools
mkdir tensorboard_data

cd /floyd/home/kode
python train.py --logtostderr --train_dir=/floyd/home/tensorboard_data --pipeline_config_path=training/ssd_mobilenet_v1_coco.config
```

**Tensorboard**
Visualisering av trening/evaluering.
Du kan evt. trykke på TensorBoard-knappen nederst på skjermen (ved cpu-% osv)
```
cp -R training/ /floyd/home
tensorboard --logdir='floyd/home/tensorboard_data'
```

### 5) Testing/evaluering
```
python eval.py \
    --logtostderr \
    --pipeline_config_path=training/ssd_mobilenet_v1_coco.config \
    --checkpoint_dir=/floyd/home/tensorboard_data  \
    --eval_dir=eval/
```

### 6) eksportere inference graph
```
cd kode
python3 export_inference_graph.py \
    --input_type image_tensor \
    --pipeline_config_path training/ssd_mobilenet_v1_coco.config \
    --trained_checkpoint_prefix /floyd/home/tensorboard_data/model.ckpt-xxx \
    --output_directory pdp_alpha_inference_graph

# velg model.ckpt-'største nr' (meta)
```
