# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 15:37:53 2023

@author: ASUS
"""

import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date, timedelta
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler


class Stock():
    
    def __init__(self, chosen_stock, days):
        self.chosen_stock = chosen_stock
        self.days = days 
        self.today = date.today().strftime("%Y-%m-%d")
        self.from_date = (date.today() - timedelta(days=2000)).strftime("%Y-%m-%d")
        
    def download_data(self):
        self.data = yf.download(self.chosen_stock, start=self.from_date, end=self.today, progress=False)
        self.data["Date"] = self.data.index
        self.data = self.data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
        self.data.reset_index(drop=True, inplace=True)
        
    def stock_price_visualization(self):
        #print(self.data.head())
        #print(self.data.tail())
        
        last_index = self.data.index[-1]
        half_of_last = math.ceil(last_index/2)
        half_of_half = math.ceil(half_of_last/2)
        
        training_set = self.data.iloc[:half_of_last,1:2].values
        #test_set = self.data.iloc[half_of_last:,1:2].values
        
        #Feature Scaling
        scaler = MinMaxScaler(feature_range= (0, 1))
        training_set_scaled = scaler.fit_transform(training_set)
        
        #Creating a data structure with time-steps and 1 output
        X_train = []
        Y_train = []
        for i in range(half_of_half, half_of_last):
            X_train.append(training_set_scaled[i-half_of_half:i, 0])
            Y_train.append(training_set_scaled[i, 0])
        X_train, Y_train = np.array(X_train), np.array(Y_train)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        #print(X_train.shape)
    
        self.model = Sequential()
        #Adding the first LSTM layer and some Dropout regularisation
        self.model.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units = 50, return_sequences = True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units = 50, return_sequences = True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units = 50))
        self.model.add(Dropout(0.2))
        # Adding the output layer
        self.model.add(Dense(units = 1))

        # Compiling the RNN
        self.model.compile(optimizer = 'adam', loss = 'mean_squared_error')
        
        # Fitting the RNN to the Training set
        self.model.fit(X_train, Y_train, epochs = 100, batch_size = 32)
        
        # Reshape the test data
        dataset_train = self.data.iloc[:half_of_last, 1:2]
        dataset_test = self.data.iloc[half_of_last:, 1:2]
        dataset_total = pd.concat((dataset_train, dataset_test), axis = 0)
        inputs = dataset_total[len(dataset_total) - len(dataset_test) - half_of_half:].values
        inputs = inputs.reshape(-1,1)
        inputs = scaler.transform(inputs)
        #print(len(inputs))
        X_test = []
        for i in range(half_of_half, half_of_last+half_of_half):
            X_test.append(inputs[i-half_of_half:i, 0])
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        #print(X_test.shape)
        
        # Make Predictions using the test set
        predicted_stock_price = self.model.predict(X_test)
        predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
        
        # Visualizing the results
        plt.plot(self.data.loc[half_of_last:,"Date"],dataset_test.values, color = "red", label = "Real Stock Price")
        plt.plot(self.data.loc[half_of_last:,"Date"],predicted_stock_price, color = "blue", label = "Predicted Stock Price")
        plt.title('Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.show()
        
    def stock_price_prediction(self):
        # Prediction future price
        today_price_stock = self.data.iloc[-2:, 1:2].values
        print(today_price_stock.shape)
        #print(today_price_stock)
        scaler = MinMaxScaler(feature_range= (0, 1))
        prediction = list()
        
        for i in range(self.days):
            scaled_today_price_stock = scaler.fit_transform(np.reshape(today_price_stock, 
                                                                       (today_price_stock[0],
                                                                        today_price_stock[1], 1)))
            print(scaled_today_price_stock.shape)
            print(scaled_today_price_stock)
            input_tensor = np.expand_dims(scaled_today_price_stock[0], axis=0)
            predicted_tomorrow_stock_price = self.model.predict(input_tensor)
            prediction.append(predicted_tomorrow_stock_price)
            today_price_stock = predicted_tomorrow_stock_price
            
        print(prediction[0])
        
        
        
        
if __name__ == "__main__":
    days = 3
    chosen_stock = "ALL"
    call_stock = Stock(chosen_stock, days)
    call_stock.download_data()
    call_stock.stock_price_visualization()
    #call_stock.stock_price_prediction()