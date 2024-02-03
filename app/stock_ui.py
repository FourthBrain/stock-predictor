import joblib
import streamlit as st
from model import convert, get_model, TODAY, get_future_df
import pandas as pd
import yfinance as yf

def get_company_name(ticker:str) -> str:
    try:
        ticker = ticker.upper()
        stock = yf.Ticker(ticker)
        return stock.info['longName']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main():
    st.title('Stock Predictor')
    
    ticker = st.text_input('Enter Stock Ticker', 'MSFT')
    # check if ticker is valid
    if get_company_name(ticker) is None:
        st.error('Invalid ticker. Please enter a valid ticker.')
        return
    days = st.number_input('Enter number of business days for prediction', min_value=1, value=7, step=1)
    
    if st.button('Predict'):
        # prediction_list, model, forecast = predict_ui(ticker, days)
        model = get_model(ticker)
        # st.write(model)
        future = get_future_df(days)
        forecast = model.predict(future)

        # st.write(forecast, type(forecast))
        predictions = forecast.tail(days).to_dict("records")
        predictions = convert(predictions)
        
        st.write(f'Forecast for {get_company_name(ticker)} ({ticker.upper()}) for the next {days} business days:')
        st.dataframe(predictions)
        
        st.plotly_chart( model.plot(forecast))
        with st.expander('View forecast components'):
            st.plotly_chart(model.plot_components(forecast))

if __name__ == "__main__":
    st.set_page_config(page_title="Stock - NeuralProphet", page_icon="📈", layout="wide")
    main()