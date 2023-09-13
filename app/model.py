import joblib
import datetime
import pandas as pd

import yfinance as yf
from neuralprophet import NeuralProphet

import argparse
from pathlib import Path


BASE_DIR = Path(__file__).resolve(strict=True).parent
# check if now is the end of the day
if datetime.datetime.now().hour >= 16:
    TOMORROW = datetime.date.today() + datetime.timedelta(days=1)
else:
    TOMORROW = datetime.date.today()

def get_model_path(ticker:str):
    #TODO: should we keep in tmp?
    return Path(BASE_DIR).joinpath(f"{ticker}.joblib")

def get_data(ticker:str):
    """AI is creating summary for get_data

    Args:
        ticker (str): [description]

    Returns:
        [type]: [description]
    """
    data = yf.download(ticker, "2020-01-01", TOMORROW)
    data.reset_index(inplace=True)
    data.rename(columns={"Date": "ds", "Adj Close": "y"}, inplace=True)
    data = data[["ds", "y"]]
    return data

def save_model(model, ticker):
    """AI is creating summary for save_model

    Args:
        model ([type]): [description]
        ticker ([type]): [description]
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
    model = NeuralProphet()
    model.fit(data, freq="D")
    # Save the model as a joblib object
    save_model(model, ticker)


def predict(ticker="MSFT", days=7):
    """AI is creating summary for predict

    Args:
        ticker (str, optional): [description]. Defaults to "MSFT".
        days (int, optional): [description]. Defaults to 7.

    Returns:
        [type]: [description]
    """
    model_file = get_model_path(ticker)
    if not model_file.exists():
        train(ticker=ticker)

    model = joblib.load(model_file)

    future_date = pd.bdate_range(start=TOMORROW, periods=days)[-1]
    dates = pd.bdate_range(start='2021-01-01', end=future_date.strftime("%Y-%m-%d"))

    future = pd.DataFrame({"ds": dates, "y": None})
    forecast = model.predict(future)

    # TODO: plot should be allowed in streamlit app; currently it works in jupyter notebook
    # model.plot(forecast)
    # model.plot_components(forecast).savefig(f"{ticker}_plot_components.png")

    return forecast.tail(days).to_dict("records")

def convert(prediction_list) -> dict:
    """AI is creating summary for convert

    Args:
        prediction_list ([type]): [description]
        
    Returns:
        dict: [description]
    """
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
    
