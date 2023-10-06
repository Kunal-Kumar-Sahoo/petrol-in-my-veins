import csv
import numpy as np
import os

from  tensorflow import keras
from tensorflow.keras import layers
from  tensorflow import math

def get_model(x=700):
    p1_=keras.Input(shape=(x,), name='p1')
    p2_=keras.Input(shape=(x,), name='p2')
    t2_=keras.Input(shape=(x,), name='t2')
    sc_=keras.Input(shape=(3,), name='sc')

    sc_00=layers.Reshape((1,3))(sc_)
    sc_00=layers.UpSampling1D(size=int(x/35))(sc_00)

    p1_00=layers.Reshape((x,1))(p1_)
    p2_00=layers.Reshape((x,1))(p2_)
    t2_00=layers.Reshape((x,1))(t2_)

    p1_0=layers.MaxPooling1D(pool_size=35,strides=None)(p1_00)
    p2_0=layers.MaxPooling1D(pool_size=35,strides=None)(p2_00)
    t2_0=layers.MaxPooling1D(pool_size=35,strides=None)(t2_00)

    p1_1=layers.AveragePooling1D(pool_size=35,strides=None)(p1_00)
    p2_1=layers.AveragePooling1D(pool_size=35,strides=None)(p2_00)
    t2_1=layers.AveragePooling1D(pool_size=35,strides=None)(t2_00)

    pt=layers.concatenate([p1_0,p1_1,p2_0,p2_1,t2_0,t2_1,sc_00],axis=2)

    pt =layers.Conv1D(
        64,
        3,
        strides=1,
        padding="valid",
        activation='relu',
        use_bias=True,
        kernel_initializer="glorot_uniform",
        bias_initializer="zeros",
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        )(pt)

    pt =layers.MaxPooling1D(pool_size=3,strides=3)(pt)

    pt =layers.LSTM(
        30,
        activation="tanh",
        recurrent_activation="sigmoid",
        use_bias=True,
        kernel_initializer="glorot_uniform",
        recurrent_initializer="orthogonal",
        bias_initializer="zeros",
        unit_forget_bias=True,
        kernel_regularizer=None,
        recurrent_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        recurrent_constraint=None,
        bias_constraint=None,
        dropout=0.6,
        recurrent_dropout=0.0,
        return_sequences=False,
        return_state=False,
        go_backwards=False,
        stateful=False,
        time_major=False,
        unroll=False,)(pt)

    pt =layers.Dense(27,activation="relu", use_bias=True)(pt)
    catN=layers.Dense(9,activation="softmax", use_bias=False, name='output')(pt)

    model = keras.Model(inputs=[p1_,p2_,t2_,sc_], outputs=catN)
    model.summary()
    opt = keras.optimizers.Adam(learning_rate=0.001)
    model.compile(loss='sparse_categorical_crossentropy', 
                optimizer=opt,  metrics=[keras.metrics.SparseCategoricalAccuracy()])

    return model

def predict_(model, inputs):
    preds = model.predict(inputs)
    return [np.argmax(preds, axis=1), preds]


if __name__ == '__main__':
    # unit testing code here
    model = keras.models.load_model('backend/iteration1.keras')
    # print(model.summary())
    dataset=[]
    with open(r'data/2.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            dataset.append(row)
    dataset = np.array(dataset, dtype=np.float32)

    # print('Dataset:', dataset.shape)

    vs = 0.5
    x = 700
    label,p1,ts1,p2,ts2,t2,ts3,interlabel=np.hsplit(dataset, [1,x+1,x+2,2*x+2,2*x+3,3*x+3,3*x+4])
    # interlabel is a sample’s parameter showing its position in the time window. This parameter equals to 1,2,3, or 4 and is isolated from the NN’s input
    label=label.flatten()
    sc=np.concatenate([ts1,ts2,ts3], axis=1)


   

