# -*- coding: utf-8 -*-
"""RNN_on_sine_wave.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q5moKFZrCbAV_H6IR8ro9-FENuYMPXcl
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,50,501)
y = np.sin(x)
plt.plot(x,y)

df = pd.DataFrame(data=y,index=x,columns=['sine'])

test_percent = 0.1
len(df)*test_percent
test_point = np.round(len(df)*test_percent)
test_ind = int( len(df) - test_point )

train = df.iloc[:test_ind]
test = df.iloc[test_ind:]
len(train)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

scaler.fit(train)
scaled_train = scaler.transform(train)
scaled_test  = scaler.transform(test)

from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator

length = 50 #length of generator[0], length of output sequences in a number of time steps
batch_size = 1 #how many time-series samples are returned in each batch
generator = TimeseriesGenerator(scaled_train,scaled_train,length=length,batch_size=batch_size)

len(scaled_train)

len(generator)

X,y =generator[0]

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, LSTM

n_features = 1

model = Sequential()

model.add(SimpleRNN(50,input_shape=(length,n_features)))
model.add(Dense(1))
model.compile(optimizer='adam',loss='mse')

model.summary()

model.fit(generator,epochs=5)

losses = pd.DataFrame(model.history.history)
losses.plot()

first_eval_batch = scaled_train[-length:]
first_eval_batch = first_eval_patch.reshape(1,length,n_features)

model.predict(first_eval_batch)

scaled_test[0]

test_predictions = []
first_eval_batch = scaled_train[-length:]
current_batch = first_eval_patch.reshape(1,length,n_features)

for i in range(len(test)):
  current_pred = model.predict(current_batch)[0]
  test_predictions.append(current_pred)
  current_batch = np.append(current_batch[:,1:],[[current_pred]],axis=1)

true_predictions = scaler.inverse_transform(test_predictions)
test['Predictions'] = true_predictions

test.plot(figsize=(12,8))

from tensorflow.keras.callbacks import EarlyStopping
early_stop = EarlyStopping(monitor='val_loss', patience=2)

length = 49
generator = TimeseriesGenerator(scaled_train,scaled_train,
                               length=length,batch_size=1)


validation_generator = TimeseriesGenerator(scaled_test,scaled_test,
                                          length=length,batch_size=1)

model = Sequential()
model.add(LSTM(50,input_shape=(length,n_features)))
model.add(Dense(1))
model.compile(optimizer='adam',loss='mse')

model.fit_generator(generator,epochs=20,
                    validation_data=validation_generator,
                    callbacks=[early_stop])

test_predictions = []

first_eval_batch = scaled_train[-length:]
current_batch = first_eval_batch.reshape((1, length, n_features))

for i in range(len(test)):
  current_pred = model.predict(current_batch)[0]
  test_predictions.append(current_pred)
  current_batch = np.append(current_batch[:,1:],[[current_pred]],axis=1)

true_predictions = scaler.inverse_transform(test_predictions)
test['LSTM Predictions'] = true_predictions
test.plot(figsize=(12,8))

full_scaler = MinMaxScaler()
scaled_full_data = full_scaler.fit_transform(df)

length = 50 # Length of the output sequences (in number of timesteps)
generator = TimeseriesGenerator(scaled_full_data, scaled_full_data, length=length, batch_size=1)

model = Sequential()
model.add(LSTM(50, input_shape=(length, n_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
model.fit_generator(generator,epochs=6)

forecast = []

first_eval_batch = scaled_full_data[-length:]
current_batch = first_eval_batch.reshape((1, length, n_features))

for i in range(len(test)):
    
    # get prediction 1 time stamp ahead ([0] is for grabbing just the number instead of [array])
    current_pred = model.predict(current_batch)[0]
    
    # store prediction
    forecast.append(current_pred) 
    
    # update batch to now include prediction and drop first value
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

forecast = scaler.inverse_transform(forecast)

forecast_index = np.arange(50.1,55.1,step=0.1)

df.head()

plt.plot(df.index,df['sine'])
plt.plot(forecast_index,forecast)