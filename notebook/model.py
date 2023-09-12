import joblib
import datetime
import pandas as pd

import yfinance as yf

from neuralprophet import NeuralProphet

import argparse
from pathlib import Path 
TRADING_DAYS_IN_ONE_YEAR = 252
TODAY = datetime.date.today()
START = datetime.date.today() - datetime.timedelta(days=365*3)
def get_data(ticker:str='MSFT'):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    data.rename(columns={"Date": "ds", "Adj Close": "y"}, inplace=True)
    data = data[["ds", "y"]]
    return data
