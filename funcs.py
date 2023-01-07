# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 13:51:15 2023
@author: sadeghi.a
"""
import requests
from datetime import datetime

def extractMomentDateTime():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

def sendRequest(url):
    return requests.get(url)

def recordExceptionInLogs(logPath, message):
    with open(logPath, "a") as file:
        file.write(extractMomentDateTime() + "  " + message + "\n")
    
