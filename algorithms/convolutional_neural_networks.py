# -*- coding: utf-8 -*-
"""redes_neurais_convolucionais.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qSUC3Qj0zKwIYOteQsUtdU9w6H6dZqwe
"""

import tensorflow as tf
import pandas as pd
import numpy as np
import math
import time
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error,median_absolute_error,r2_score
from datetime import datetime

def prediction_cnn(df, metrics):
  
  #separates 80% of this data
  training_data_len = math.floor(len(df)*.8)

  numerical_i = tf.keras.layers.Input((48,1))
  numerical = tf.keras.layers.Conv1D(20,4)(numerical_i)
  numerical = tf.keras.layers.Flatten()(numerical)
  dense = tf.keras.layers.Dense(300,'relu')(numerical)
  out=tf.keras.layers.Dense(48,'relu')(dense)

  #creating a training dataset
  train = pd.DataFrame(df[0:training_data_len]['timestamp'])
  train[metrics] = df[0:training_data_len][metrics]
  train.set_index('timestamp',inplace = True)

  l=48
  h=48

  X=[]
  Y=[]

  for i in range(l,train.shape[0]-h):
    f=train.iloc[i-l:i][metrics].values
    y=train.iloc[i:i+h][metrics].values

    X.append(f)
    Y.append(y)

  X=np.array(X)
  Y=np.array(Y)

  #creating the test base
  test = pd.DataFrame(df[training_data_len:]['timestamp'])
  test[metrics] = df[training_data_len:][metrics]
  test.set_index('timestamp',inplace = True)

  Xv=[]
  Yv=[]

  for i in range(l, test.shape[0]-h):
    f=test.iloc[i-l:i][metrics].values
    y=test.iloc[i:i+h][metrics].values

    Xv.append(f)
    Yv.append(y)

  Xv=np.array(Xv)
  Yv=np.array(Yv)

  model=tf.keras.Model(numerical_i,out)
  model.compile('adam','mae')   

  #Treinamento: 10 épocas para treinamento do modelo.
  model.fit(X,Y,batch_size=1,shuffle=True,epochs=10)  

  #Gerando as previsões do modelo
  predictions=model.predict(Xv)

  return predictions, Yv