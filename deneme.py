import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import date, timedelta
from sklearn.model_selection import train_test_split

class Stock():
    def __init__(self, days):
        self.days = days
        self.today = date.today().strftime("%Y-%m-%d")
        self.from_date = (date.today() - timedelta(days=self.days)).strftime("%Y-%m-%d")
        
    def download_data(self, stock_list):
        self.stock_list = stock_list
        for stock_code in self.stock_list:
            data = yf.download(stock_code, start=self.from_date, end=self.today, progress=False)
            data["Date"] = data.index
            data = data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
            data.reset_index(drop=True, inplace=True)
            print(stock_code, data.tail(5))
        
            
if __name__ == "__main__":
    stock_list = ["AAL","AAN","AAWW","ADTN"]
    callStock = Stock(100)
    print(callStock.download_data(stock_list))
    
        
        