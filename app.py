import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.title('Stock Technical Indicators App')

# Input for stock ticker
ticker = st.text_input('Enter Stock Ticker', 'AAPL')

# Validate ticker input
if ticker:
    # Fetch data from Yahoo Finance
    data = yf.download(ticker, start="2020-01-01")

    if not data.empty:
        # Display raw data
        st.subheader('Raw Data')
        st.write(data.tail())

        # Calculate technical indicators using pandas_ta
        data['SMA'] = ta.sma(data['Close'], length=20)
        data['EMA'] = ta.ema(data['Close'], length=20)
        data['RSI'] = ta.rsi(data['Close'], length=14)

        # Display technical indicators
        st.subheader('Technical Indicators')
        st.write(data[['Close', 'SMA', 'EMA', 'RSI']].tail())

        # Plotting
        st.subheader('Stock Price and SMA/EMA')
        st.line_chart(data[['Close', 'SMA', 'EMA']])

        st.subheader('RSI')
        st.line_chart(data['RSI'])
    else:
        st.error('Invalid stock ticker or no data available. Please try again.')
else:
    st.warning('Please enter a stock ticker.')
