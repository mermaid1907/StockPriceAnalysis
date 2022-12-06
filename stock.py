import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import date, timedelta
from sklearn.model_selection import train_test_split

today = date.today().strftime("%Y-%m-%d")
end_date = today
from_date = date.today() - timedelta(days=100)
from_date = from_date.strftime("%Y-%m-%d")
start_date = from_date

stock_list = ["AAL","AAN","AAWW","ADTN"]

for stock_code in stock_list:
    data = yf.download(f"{stock_code}", start=start_date, end=end_date, progress=False)
    data["Date"] = data.index
    data = data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    data.reset_index(drop=True, inplace=True)
    #print(stock_code, data.tail(5))
    correlation = data.corr()
    #print(stock_code, "Correlation of Close: \n", correlation["Close"].sort_values(ascending=False))
    
    x = data[["Open","High","Low","Volume"]]
    x = x.to_numpy()
    
    y = data["Close"]
    y = y.to_numpy()
    
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.3, random_state=10) 
    
    
    
    
    