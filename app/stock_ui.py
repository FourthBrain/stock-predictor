import streamlit as st
import joblib
from model import train, convert, get_model_path, TODAY
import pandas as pd

@st.cache_data
def predict_ui(ticker="MSFT", days=7):
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

    future_date = pd.bdate_range(start=TODAY, periods=days)[-1]
    dates = pd.bdate_range(start='2021-01-01', end=future_date.strftime("%Y-%m-%d"))

    future = pd.DataFrame({"ds": dates, "y": None})
    forecast = model.predict(future)

    # TODO: plot should be allowed in streamlit app; currently it works in jupyter notebook
    # model.plot(forecast)
    # model.plot_components(forecast).savefig(f"{ticker}_plot_components.png")

    return forecast.tail(days).to_dict("records"), model, forecast

def main():
    st.title('Stock Predictor')
    
    ticker = st.text_input('Enter Stock Ticker', 'MSFT')
    days = st.number_input('Enter number of business days for prediction', min_value=1, value=7, step=1)
    
    if st.button('Predict'):
        prediction_list, model, forecast = predict_ui(ticker, days)
        predictions = convert(prediction_list)
        
        st.write(f'Forecast for {ticker} for the next {days} business days:')
        st.write(predictions)
        
        fig = model.plot(forecast)
        # st.write(type(fig))
        st.plotly_chart(fig)
        st.plotly_chart(model.plot_components(forecast))

if __name__ == "__main__":
    main()
