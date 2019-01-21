import tensorflow as tf
import keras
from keras import Sequential
from keras.layers import Conv2D, Dense, Flatten, Activation, MaxPooling2D
import matplotlib.pyplot as plt
import numpy as np
import os

mnist = keras.datasets.fashion_mnist
save_dir = os.path.join(os.getcwd())
modell = 'min_modell.h5'

(train_imgs, train_lbls), (test_imgs, test_lbls) = mnist.load_data()

batch_size = 128
epochs = 20
num_classes = 10 # tall fra 0-9

train_imgs = train_imgs.reshape(train_imgs.shape[0], 28, 28, 1)
test_imgs = test_imgs.reshape(test_imgs.shape[0], 28, 28, 1)
train_lbls = keras.utils.to_categorical(train_lbls, num_classes)
test_lbls = keras.utils.to_categorical(test_lbls, num_classes)

# normaliserer data
train_imgs = keras.utils.normalize(train_imgs, axis = 1)
test_imgs = keras.utils.normalize(test_imgs, axis = 1)

# lineær modell: input --> hidden #1 --> hidden #2 --> output
model = Sequential()
model.add(Conv2D(32, (3,3), 
                input_shape = (28,28,1),
                activation = 'relu'))

model.add(Conv2D(32, (3,3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(32, (3,3), activation = 'relu'))
model.add(Conv2D(32, (3,3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Flatten())
model.add(Dense(10, activation = 'relu'))
model.add(Activation('softmax'))

optmzr = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

model.compile(loss = 'categorical_crossentropy',
             optimizer = optmzr,
             metrics=['accuracy'])

model.fit(train_imgs, train_lbls,
         batch_size = batch_size,
         epochs = epochs,
         validation_data = (test_imgs,test_lbls),
         shuffle=True)

# lagre modell
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
model_path = os.path.join(save_dir, modell)
model.save(model_path)
print('Saved trained model at %s ' % model_path)

# Score trained model.
scores = model.evaluate(test_imgs, test_lbls, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
