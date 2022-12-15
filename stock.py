import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import tensorflow_estimator as tf
from datetime import date, timedelta
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.model_selection import train_test_split


class Stock():
    
    def __init__(self, chosen_stock, days):
        self.chosen_stock = chosen_stock
        self.days = days
        self.today = date.today().strftime("%Y-%m-%d")
        self.from_date = (date.today() - timedelta(days=self.days)).strftime("%Y-%m-%d")
        self.data = self.download_data()
        
    def download_data(self):
        data = yf.download(self.chosen_stock, start=self.from_date, end=self.today, progress=False)
        data["Date"] = self.data.index
        data = self.data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
        data.reset_index(drop=True, inplace=True)
            #print(stock_code, self.data.tail(5))
    
    def lstm_train_test(self):
        x = self.data[["Open","High","Low","Volume"]]
        x = x.to_numpy()
        
        y = self.data["Close"]
        y = y.to_numpy()
        
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.3, random_state=10) 
        
        model = Sequential()
        
        model.add(LSTM(128, return_sequences=True, input_shape= (xtrain.shape[1], 1)))
        model.add(LSTM(64, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))
        model.summary()
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(xtrain, ytrain, batch_size=1, epochs=30)
        
        #features = [Open, High, Low, Adj Close, Volume]
        features = np.array([self.data["Open"], self.data["High"], self.data["Low"], self.data["Volume"]])
        print(model.predict(features))
                
if __name__ == "__main__":
    days = 50
    chosen_stock = "AAL"
    callStock = Stock(chosen_stock,days)
    callStock.download_data()
    callStock.lstm_train_test()
    
        
        