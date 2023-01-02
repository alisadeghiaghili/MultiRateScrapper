import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import pandas as pd

URL = "https://www.tgju.org/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
rate = soup.select("#l-price_dollar_rl .info-price")[0].text.replace(',', '')

path = r'D:\rate'
fileName = 'dollarRates.csv'
try:
    os.listdir(path)
except FileNotFoundError:
    os.mkdir(path)
    
    
dfNew = pd.DataFrame(columns = ["datetime", "rate"])
dfNew.loc[0] = [datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), rate]
try: 
    dfOld = pd.read_csv(path + r'\\' + fileName)
    dfAll = pd.concat([dfOld, dfNew])
    dfAll.to_csv(path + r'\\' + fileName, index=False)
except FileNotFoundError:
    dfNew.to_csv(path + r'\\' + fileName, index=False)
