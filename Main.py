# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 13:31:44 2023
@authors: sadeghi.a, salehi.m
"""
import os
workingDir = r'D:\MultiRateScraper'
os.chdir(workingDir)
from funcs import *


from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import sqlalchemy as sa
import time

URL = "https://www.tgju.org/"
logPath = "D:\\rateScraper.txt"

hour = datetime.now().hour
if hour > 8 or hour < 22:
    try:
        page = sendRequest(URL)
    except requests.exceptions.SSLError:
        recordExceptionInLogs(logPath, "Could not read data from tgju")
    except Exception as errorMessage:
        recordExceptionInLogs(logPath, "Max tries exceeded" + " " + str(errorMessage))
        page = sendRequest(URL)
        time.sleep(180)
            
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        dollarRate = soup.select("#l-price_dollar_rl .info-price")[0].text.replace(',', '')
        dollarRateChangePercent, dollarRateChangeAmount = soup.select("#l-price_dollar_rl .info-change")[0].text.replace(',', '').replace('(', '').replace(')', '').replace('%', '').split()
        
        exchangeIndexRate = soup.select("#l-bourse .info-price")[0].text.replace(',', '')
        exchangeIndexChangePercent, exchangeIndexChangeAmount = soup.select("#l-bourse .info-change")[0].text.replace(',', '').replace('(', '').replace(')', '').replace('%', '').split()
        
        goldOZRate = soup.select("#l-ons .info-price")[0].text.replace(',', '')
        goldOZChangePercent, goldOZChangeAmount = soup.select("#l-ons .info-change")[0].text.replace(',', '').replace('(', '').replace(')', '').replace('%', '').split()
        
        BTCRate = soup.select("#l-crypto-bitcoin .info-price")[0].text.replace(',', '')
        BTCChangePercent, BTCChangeAmount = soup.select("#l-crypto-bitcoin .info-change")[0].text.replace(',', '').replace('(', '').replace(')', '').replace('%', '').split()
        
        USDTRate = soup.select("#l-crypto-tether-irr .info-price")[0].text.replace(',', '')
        USDTChangePercent, USDTChangeAmount = soup.select("#l-crypto-tether-irr .info-change")[0].text.replace(',', '').replace('(', '').replace(')', '').replace('%', '').split()
        
        goldGramsRate = soup.select("#l-geram18 .info-price")[0].text.replace(',', '')
        goldGramsChangePercent, goldGramsChangeAmount = soup.select("#l-geram18 .info-change")[0].text.replace(',', '').replace('(', '').replace(')', '').replace('%', '').split()
        
        brentOilRate = soup.select("#l-oil_brent .info-price")[0].text.replace(',', '')
        brentOilChangePercent, brentOilChangeAmount = soup.select("#l-oil_brent .info-change")[0].text.replace(',', '').replace('(', '').replace(')', '').replace('%', '').split()
        
        imamiCoinRate = soup.select("#l-sekee .info-price")[0].text.replace(',', '')
        imamiCoinChangePercent, imamiCoinChangeAmount = soup.select("#l-sekee .info-change")[0].text.replace(',', '').replace('(', '').replace(')', '').replace('%', '').split()
    
    except IndexError:        
        recordExceptionInLogs(logPath, "CSS has been changed")
            
    df = pd.DataFrame(columns = ["DateTime", "Rate", "ChangePercent", "ChangeAmount", "RateID"])
    df.loc[0] = [extractMomentDateTime(), dollarRate, dollarRateChangePercent, dollarRateChangeAmount, 1]
    df.loc[1] = [extractMomentDateTime(), exchangeIndexRate, exchangeIndexChangePercent, exchangeIndexChangeAmount, 2]
    df.loc[2] = [extractMomentDateTime(), goldOZRate, goldOZChangePercent, goldOZChangeAmount, 3]
    df.loc[3] = [extractMomentDateTime(), BTCRate, BTCChangePercent, BTCChangeAmount, 4]
    df.loc[4] = [extractMomentDateTime(), USDTRate, USDTChangePercent, USDTChangeAmount, 5]
    df.loc[5] = [extractMomentDateTime(), goldGramsRate, goldGramsChangePercent, goldGramsChangeAmount, 6]
    df.loc[6] = [extractMomentDateTime(), brentOilRate, brentOilChangePercent, brentOilChangeAmount, 7]
    df.loc[7] = [extractMomentDateTime(), imamiCoinRate, imamiCoinChangePercent, imamiCoinChangeAmount, 8]
    
    config = 'mssql+pyodbc://user:pass@server:port/database?driver=ODBC+Driver+18+for+SQL+Server&encrypt=no'
    engine = sa.create_engine(config)
    try:
        df.to_sql("RatesHistory", engine, if_exists="append", index=False, 
                  dtype=({"DateTime": sa.types.CHAR(length=19), "Rate": sa.types.FLOAT(), "ChangePercent": sa.types.FLOAT(), "ChangeAmount": sa.types.FLOAT(), "RateID": sa.types.INTEGER()}))
    except Exception as errorMessage:
        recordExceptionInLogs(logPath, "DB Related Error" + " " + str(errorMessage))
        
    print("recieved in", extractMomentDateTime())
else:
    print("out of specified time period")
