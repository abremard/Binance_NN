"""
    Author :
        Alexandre Bremard
    Version Control :
        1.0 - 09/26/2020 : train()
    Todo :
        - Separate train and test and predict
        - Comment
"""

import tensorflow as tf
from tensorflow import keras

def train(x_array=None, y_array=None):
    model = keras.Sequential()
    model.add(keras.layers.LSTM(50, return_sequences = True))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(1))
    model.compile(keras.optimizers.Adam(), loss='mean_squared_error')

    model.fit(x_array[0:8000], y_array[0:8000], epochs=10, batch_size=32)
    model.evaluate(x_array[8000:9950], y_array[8000:9950])
    predictions = model.predict(x_array)
