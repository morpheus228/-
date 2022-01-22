# importing of necessary libraries
import tensorflow as tf
import pandas as pd
import numpy as np
import random

# downloding of dataset and its normalizing to range of values (0, 1)
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
train_images = (train_images.astype('float32') / 255.)[..., None]
test_images = (test_images.astype('float32') / 255.)[..., None]

# creating of model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (5, 5), activation='relu', padding='same', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D((2, 2), (2, 2), padding='same'),
    tf.keras.layers.Conv2D(64, (5, 5), activation='relu', padding='same'),
    tf.keras.layers.MaxPooling2D((2, 2), (2, 2), padding='same'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax'),
])

# model's compiling 
model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              optimizer='Adam',
              metrics=['accuracy'])

# model's training
model.fit(x=train_images, y=train_labels, batch_size=64, epochs=5, validation_data=(test_images, test_labels))

# model's saving
model.save('model.hdf5')
