# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 11:58:35 2022

@author: ASUS
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_stock_codes():
    code_list = list()
    code_fletter_list = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
    for code_fletter in code_fletter_list:
        url = "https://eoddata.com/stocklist/NYSE/{}.htm".format(code_fletter)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        table = soup.find("table", {"class": "quotes"})
        rows = table.find_all("tr", {"class": "ro"}) + table.find_all("tr", {"class": "re"})
        for row in rows:
            code = row.find("td").text
            code_list.append(code)
        
    return code_list

def save_stock_codes(stock_code_list):
    df = pd.DataFrame(stock_code_list, columns=["Code"])
    df.to_csv("stock_code_list.csv")
            
if __name__ == "__main__":
    stock_code_list = get_stock_codes()
    save_stock_codes(stock_code_list)