import joblib
import datetime
import pandas as pd

import yfinance as yf
from neuralprophet import NeuralProphet

import argparse
from pathlib import Path

import streamlit as st # add cache


BASE_DIR = Path(__file__).resolve(strict=True).parent
# check if now is the end of the day
if datetime.datetime.now().hour >= 16:
    TODAY = datetime.date.today() + datetime.timedelta(days=1)
else:
    TODAY = datetime.date.today()

def get_model_path(ticker:str):
    return Path(BASE_DIR).joinpath(f"{ticker}.joblib")

def get_data(ticker:str):
    """AI is creating summary for get_data

    Args:
        ticker (str): [description]

    Returns:
        [type]: [description]
    """
    data = yf.download(ticker, "2020-01-01", TODAY)
    data.reset_index(inplace=True)
    data.rename(columns={"Date": "ds", "Adj Close": "y"}, inplace=True)
    data = data[["ds", "y"]]
    return data

def save_model(model, ticker):
    """AI is creating summary for save_model

    Args:
        model ([type]): [description]
        ticker (str): stock ticker
    """
    model.restore_trainer()  # avoid trainer being loaded into checkpoint 
    joblib.dump(model, get_model_path(ticker))

def train(ticker:str="MSFT"):
    """AI is creating summary for train

    Args:
        ticker (str, optional): [description]. Defaults to "MSFT".
    """
    # Get history stock data
    data = get_data(ticker=ticker)
    # Initiate model and fit the model
    model = NeuralProphet(epochs=3)
    model.fit(data, freq="D")
    # Save the model as a joblib object
    save_model(model, ticker)

@st.cache_resource
def get_model(ticker:str="MSFT"):
    """AI is creating summary for get_model

    Args:
        ticker (str, optional): [description]. Defaults to "MSFT".

    Returns:
        [type]: [description]
    """
    model_file = get_model_path(ticker)
    if not model_file.exists():
        train(ticker=ticker)

    model = joblib.load(model_file)
    return model


def get_future_df(days:int) -> pd.DataFrame:
    future_date = pd.bdate_range(start=TODAY, periods=days)[-1]
    dates = pd.bdate_range(start='2021-01-01', end=future_date.strftime("%Y-%m-%d"))

    future = pd.DataFrame({"ds": dates, "y": None})
    return future


def predict(ticker="MSFT", days=7):
    """AI is creating summary for predict

    Args:
        ticker (str, optional): [description]. Defaults to "MSFT".
        days (int, optional): [description]. Defaults to 7.

    Returns:
        [type]: [description]
    """
    try:
        model = get_model(ticker)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    future = get_future_df(days)
    forecast = model.predict(future)

    return forecast.tail(days).to_dict("records")


def convert(predictions) -> dict:
    """AI is creating summary for convert

    Args:
        predictions ([type]): [description]
        
    Returns:
        dict: [description]
    """
    output = {}
    for data in predictions:
        date = data["ds"].strftime("%m/%d/%Y")
        output[date] = round(data["trend"], 2)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict')
    parser.add_argument('--ticker', type=str, default='MSFT', help='Stock Ticker')
    parser.add_argument('--days', type=int, default=7, help='Number of days to predict')
    args = parser.parse_args()
    
    prediction_list = predict(ticker=args.ticker.upper(), days=args.days)
    output = convert(prediction_list)
    print(output)
    
