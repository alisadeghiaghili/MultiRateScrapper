import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

URL = "https://www.tgju.org/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
rate = soup.select("#l-sana_real_sell_usd .info-price")[0].text.replace(',', '')

path = r'D:\rate'
fileName = 'dollarRates.csv'
try:
    os.listdir(path)
except FileNotFoundError:
    os.mkdir(path)

string = ','.join([datetime.strftime(datetime.togitday(), '%Y-%m-%d'), rate])

try: 
    with open(path + r'\\' + fileName, 'a') as file:
        file.write(rate)
except FileNotFoundError:
    with open(path + r'\\' + fileName, 'w') as file:
        header = ','.join(['date', 'rate\n'])
        file.write(header)
        file.write(string)
