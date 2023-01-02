import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import sqlalchemy as sa
import time

URL = "https://www.tgju.org/"

while True:
    try:
        page = requests.get(URL)
    except:
        with open("D:\\rateScraper.txt", "a+") as file:
            file.write(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') + "  Could not read data from tgju\n")
            
        page = requests.get(URL)
        time.sleep(2)
            
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        rate = soup.select("#l-price_dollar_rl .info-price")[0].text.replace(',', '')
    except IndexError:
        with open("D:\\rateScraper.txt", "a+") as file:
            file.write(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') + "  css has been changed\n")
            
    df = pd.DataFrame(columns = ["datetime", "rate"])
    df.loc[0] = [datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), rate]
    
    config = 'mssql+pyodbc://user:pass@server:port/database?driver=SQL+Server+Native+Client+11.0'
    engine = sa.create_engine(config)
    try:
        df.to_sql("DollarRate", engine, if_exists="append", index=False, dtype=({"datetime": sa.types.CHAR(length=19), "rate": sa.types.INTEGER()}))
    except:
        with open("D:\\rateScraper.txt", "a+") as file:
            file.write(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') + "  DB Related Error\n")
    
    time.sleep(3600)
