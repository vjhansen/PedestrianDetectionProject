> - Outdated
> - Setup  (~15 minutes).
> - Training and evaluation (~4.5h for 14k steps of training).

### 1) Setup - https://www.floydhub.com/

- Open a Workspace
- Pick Environment: TensorFlow 1.12, Machine: GPU
- Open Terminal from Launcher/Other

```bash
sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade
```

Install Protobuf.

```bash
 cd /tmp/ && \
 curl -OL https://github.com/google/protobuf/releases/download/v3.5.1/protoc-3.5.1-linux-x86_64.zip && \
 unzip protoc-3.5.1-linux-x86_64.zip -d protoc3 && \
 mv protoc3/bin/* /usr/local/bin/ && \
 mv protoc3/include/* /usr/local/include/ && \
 chown `whoami` /usr/local/bin/protoc && \
 chown -R `whoami` /usr/local/include/google
```

Clone modell from TensorFlow.

```bash
cd /floyd/home && \
git clone https://github.com/tensorflow/models.git

mkdir PDP_folder && \
cd models/research && \
git reset --hard ea6d6aa && \
/usr/local/bin/protoc object_detection/protos/*.proto --python_out=. && \
cp -R object_detection /floyd/home/PDP_folder && cp -R slim /floyd/home/PDP_folder
```

> ^ run again if : 
> can't open file 'object_detection/builders/model_builder_test.py': [Errno 2] No such file or directory

* Using an earlier commit (git reset --hard ea6d6aa) of TensorFlow/Models/research*

```bash
rm -rf /floyd/home/PDP_folder/models && \
export PYTHONPATH=$PYTHONPATH:/floyd/home/PDP_folder/object_detection/:/floyd/home/PDP_folder/slim && \
cd /floyd/home/PDP_folder && python object_detection/builders/model_builder_test.py
```

Output: 

```bash
Ran 15 tests in 0.xxxs

OK
```

### 2) Download SSDLite+MobileNetV2 from Tensorflow detection model zoo.

```bash
 cd /floyd/home/PDP_folder && \
 wget http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz && \
 tar xf ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
```

### 3) Add files

```bash
git clone https://github.com/vjhansen/PedestrianDetectionProject

cd /floyd/home/PDP_folder/
```

Move everything from pdp-bachelor to `/floyd/home/PDP_folder/`.

##### Folder structure

```bash
PDP_folder
|--> data
|   |--> eval.record (generate file with TFrecord.py)
|   |--> train.record (generate file with TFrecord.py)
|   
|--> training
|   |--> ssdlite_mobilenet_v2_coco.config
|   |--> ob-det.pbtxt
```

### 4) Training

```bash
cd /floyd/home/ && \
pip install --upgrade pip && \
pip -q install pycocotools && \
mkdir tensorboard_data && \
cd /floyd/home/PDP_folder

python train.py --logtostderr --train_dir=/floyd/home/tensorboard_data --pipeline_config_path=training/ssdlite_mobilenet_v2_coco.config
```

**Tensorboard**
Visualization of training/evaluation.

```bash
cp -R training/ /floyd/home

tensorboard --logdir='floyd/home/tensorboard_data'
```

### 5) Testing/evaluation

Open a new Terminal-window in FloydHub.

```bash
cd /floyd/home/PDP_folder

python eval.py \
    --logtostderr \
    --pipeline_config_path=training/ssdlite_mobilenet_v2_coco.config \
    --checkpoint_dir=/floyd/home/tensorboard_data  \
    --eval_dir=eval/
```

 If you encounter some trouble:

```bash
export PYTHONPATH=$PYTHONPATH:/floyd/home/PDP_folder/object_detection/:/floyd/home/PDP_folder/slim
```

Finish training and evaluation with: ctrl+c or cmd+c

### 6) export inference graph

Do this when you're pleased with the training.  E.g. when Losses/TotalLoss < 1.5, and PascalBoxes_Precision/mAP@0.5IOU > 0.85.

```bash
cd PDP_folder

python3 export_inference_graph.py \
    --input_type image_tensor \
    --pipeline_config_path training/ssdlite_mobilenet_v2_coco.config \
    --trained_checkpoint_prefix /floyd/home/tensorboard_data/model.ckpt-xxx \
    --output_directory PDP_model

# pick model.ckpt-'highest nr.', e.g. model.ckpt-13983 (don't add .meta)
```

Download the folder: --> home --> PDP_folder --> PDP_model


