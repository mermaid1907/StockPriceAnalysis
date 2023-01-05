import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.graph_objects as go
import tensorflow_estimator as tf
from datetime import date, timedelta
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


class Stock():
    
    def __init__(self, chosen_stock, days):
        self.chosen_stock = chosen_stock
        self.days = days
        self.today = date.today().strftime("%Y-%m-%d")
        self.from_date = (date.today() - timedelta(days=1000)).strftime("%Y-%m-%d")
        
    def download_data(self):
        self.data = yf.download(self.chosen_stock, start=self.from_date, end=self.today, progress=False)
        self.data["Date"] = self.data.index
        self.data = self.data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
        self.data.reset_index(drop=True, inplace=True)
            #print(stock_code, self.data.tail(5))
    
    def lstm_train_test(self):
        x = self.data[["Open","High","Low", "Close", "Volume"]]
        x = x.to_numpy()
        
        y = self.data[["Open", "High", "Close"]]
        y = y.to_numpy()
        
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(y.reshape(-1,1))
        
        xtrain, xtest, ytrain, ytest = train_test_split(x[:-1*self.days,:], y[self.days:,:], test_size=0.3, random_state=10) 
        
        model = Sequential()
        
        model.add(LSTM(128, return_sequences=True, input_shape= (xtrain.shape[1], 1)))
        model.add(LSTM(64, return_sequences=False))
        model.add(Dense(3))
        model.summary()
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(xtrain, ytrain, batch_size=1, epochs=30)
        
        print("\n----------------------------------------------\n")
        predictions = model.predict(xtest)
        #denormalize the predicted stock prices
        predictions = scaler.inverse_transform(predictions)
        rmse = np.sqrt(np.mean(predictions - ytest)**2)
        
        print(rmse)
        
        print("\n----------------------------------------------\n")
        
        #features = [Open, High, Low, Close, Volume]
        features = np.array(x)
        prediction = model.predict(features)
        
        
        # Visualizing the results
        plt.plot(self.data["Date"],x[:,0], color = "red", label = "Real Stock Price")
        plt.plot(self.data["Date"],prediction[:,0], color = "blue", label = "Predicted Stock Price")
        frame = plt.gca()
        frame.axes.get_xaxis().set_visible(False)
        plt.title('Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.show()
        print(prediction[-1,:])
        return prediction[-1,:]
                
if __name__ == "__main__":
    days = 3
    chosen_stock = "AAL"
    callStock = Stock(chosen_stock,days)
    callStock.download_data()
    callStock.lstm_train_test()
    
        
        