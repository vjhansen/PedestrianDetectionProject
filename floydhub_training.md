- Oppsett (~15 minutter).
- Trening og Evaluering (~4.5 timer for 14k steg trening).

### 1) Oppsett - FloydHub 
- Åpne en Workspace
- Velg Environment: TensorFlow 1.12, Machine: GPU
- Åpne Terminal fra Launcher/Other

```sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade```

Installere Protobuf.
```
 cd /tmp/ && \
 curl -OL https://github.com/google/protobuf/releases/download/v3.5.1/protoc-3.5.1-linux-x86_64.zip && \
 unzip protoc-3.5.1-linux-x86_64.zip -d protoc3 && \
 mv protoc3/bin/* /usr/local/bin/ && \
 mv protoc3/include/* /usr/local/include/ && \
 chown `whoami` /usr/local/bin/protoc && \
 chown -R `whoami` /usr/local/include/google
```
Klone modell fra TensorFlow.
```
cd /floyd/home && \
git clone https://github.com/tensorflow/models.git

mkdir PDP_folder && \
cd models/research && \
git reset --hard ea6d6aa && \
/usr/local/bin/protoc object_detection/protos/*.proto --python_out=. && \
cp -R object_detection /floyd/home/PDP_folder && cp -R slim /floyd/home/PDP_folder
```
^kjør denne på nytt hvis: 
can't open file 'object_detection/builders/model_builder_test.py': [Errno 2] No such file or directory

*Bruker en tidligere commit (git reset --hard ea6d6aa) av TensorFlow/Models/research*
```
rm -rf /floyd/home/PDP_folder/models && \
export PYTHONPATH=$PYTHONPATH:/floyd/home/PDP_folder/object_detection/:/floyd/home/PDP_folder/slim && \
cd /floyd/home/PDP_folder && python object_detection/builders/model_builder_test.py

```
Output skal være: 
```
Ran 15 tests in 0.xxxs

OK
```

### 2) Laste ned modellen SSDLite+MobileNetV2 fra Tensorflow detection model zoo.

```
 cd /floyd/home/PDP_folder && \
 wget http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz && \
 tar xf ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
```

### 3) Legge til filer
```
git clone https://github.com/vjhansen/pdp-bachelor.git 

cd /floyd/home/PDP_folder/
```
Flytt alt fra pdp-bachelor til /floyd/home/PDP_folder/.
Struktur
```
PDP_folder
|--> data
|   |--> eval.record (ligger på onedrive)
|   |--> train.record (ligger på onedrive)
|   
|--> training
|   |--> ssdlite_mobilenet_v2_coco.config
|   |--> ob-det.pbtxt

```

### 4) Trening
```
cd /floyd/home/ && \
pip install --upgrade pip && \
pip -q install pycocotools && \
mkdir tensorboard_data && \
cd /floyd/home/PDP_folder

python train.py --logtostderr --train_dir=/floyd/home/tensorboard_data --pipeline_config_path=training/ssdlite_mobilenet_v2_coco.config
```

**Tensorboard**
Visualisering av trening/evaluering.
Du kan evt. trykke på TensorBoard-knappen nederst på skjermen (ved cpu-% osv)
```
cp -R training/ /floyd/home

tensorboard --logdir='floyd/home/tensorboard_data'
```

### 5) Testing/evaluering
Kan kjøres samtidig som treningen i steg 4 starter. Vi venter til TotalLoss er rundt 2.0. 
Bare åpne et nytt terminal-vindu inne på FloydHub.
```
cd /floyd/home/PDP_folder

python eval.py \
    --logtostderr \
    --pipeline_config_path=training/ssdlite_mobilenet_v2_coco.config \
    --checkpoint_dir=/floyd/home/tensorboard_data  \
    --eval_dir=eval/
```
Hvis du får trøbbel:
```
export PYTHONPATH=$PYTHONPATH:/floyd/home/PDP_folder/object_detection/:/floyd/home/PDP_folder/slim
```
Avslutt trening og evaluering med: CTRL+C


### 6) eksportere inference graph
Gjør dette når du er fornøyd med treningen. F.eks. når Losses/TotalLoss < 1.5, og PascalBoxes_Precision/mAP@0.5IOU > 0.85. (følg med på utviklingen inne på TensorBoard)
```
cd PDP_folder

python3 export_inference_graph.py \
    --input_type image_tensor \
    --pipeline_config_path training/ssdlite_mobilenet_v2_coco.config \
    --trained_checkpoint_prefix /floyd/home/tensorboard_data/model.ckpt-xxx \
    --output_directory PDP_model

# velg model.ckpt-'største nr', f.eks. model.ckpt-13983 (ikke ta med .meta)
```
Last ned mappen: --> home --> PDP_folder --> PDP_model
