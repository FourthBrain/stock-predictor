import joblib
import datetime
import pandas as pd

import yfinance as yf

from neuralprophet import NeuralProphet

import argparse
from pathlib import Path


BASE_DIR = Path(__file__).resolve(strict=True).parent
TODAY = datetime.date.today()

def get_model_path(ticker:str):
    return Path(BASE_DIR).joinpath(f"{ticker}.joblib")

def get_data(ticker:str):
    # Load the data from yf
    data = yf.download(ticker, "2020-01-01", TODAY.strftime("%Y-%m-%d"))
    data.reset_index(inplace=True)
    data.rename(columns={"Date": "ds", "Adj Close": "y"}, inplace=True)
    data = data[["ds", "y"]]
    return data

def save_model(model, ticker):
    model.restore_trainer()  # avoid trainer being loaded into checkpoint 
    joblib.dump(model, get_model_path(ticker))

def train(ticker:str="MSFT"):
    # Get history stock data
    data = get_data(ticker=ticker)
    # Initiate model and fit the model
    model = NeuralProphet()
    model.fit(data, freq="D")
    # Save the model as a joblib object
    save_model(model, ticker)


def predict(ticker="MSFT", days=7):
    
    model_file = get_model_path(ticker)
    if not model_file.exists():
        # return False
        train(ticker=ticker)

    model = joblib.load(model_file)

    future_date = pd.bdate_range(start=TODAY, periods=days)[-1]
    dates = pd.bdate_range(start='2021-01-01', end=future_date.strftime("%Y-%m-%d"))

    future = pd.DataFrame({"ds": dates, "y": None})
    forecast = model.predict(future)

    model.plot(forecast)
    # model.plot_components(forecast).savefig(f"{ticker}_plot_components.png")

    return forecast.tail(days).to_dict("records")

def convert(prediction_list):
    output = {}
    for data in prediction_list:
        date = data["ds"].strftime("%m/%d/%Y")
        output[date] = data["trend"]
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict')
    parser.add_argument('--ticker', type=str, default='MSFT', help='Stock Ticker')
    parser.add_argument('--days', type=int, default=7, help='Number of days to predict')
    args = parser.parse_args()
    
    prediction_list = predict(ticker=args.ticker.upper(), days=args.days)
    output = convert(prediction_list)
    print(output)
    
