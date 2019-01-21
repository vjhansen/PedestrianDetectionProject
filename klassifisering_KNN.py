import tensorflow as tf
import matplotlib.pyplot as plt


#dataset = ---
(x_train, y_train),(x_test, y_test) = dataset.load_data()


# lineær modell: input --> hidden #1 --> hidden #2 --> output
model = Sequential()
model.add(Dense(32, input_shape=(500,)))


