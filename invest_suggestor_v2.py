import yfinance as yf
import pandas as pd
import numpy as np

ticker_data = ["PLTR", "TSLA", "MSFT", "META", "AAPL", "AMZN"] 
start_date = "2023-01-01"
end_date = "2024-01-01"

data = yf.download(ticker_data, start=start_date, end=end_date)['Adj Close']

returns = data.pct_change().dropna()
data = data.join(returns, rsuffix='_daily_return')

std_devs = returns.std()

moving_avg_10 = data.rolling(window=10).mean()
data = data.join(moving_avg_10, rsuffix='_5day_MA')

moving_avg_50 = data.rolling(window=50).mean()
data = data.join(moving_avg_50, rsuffix='_30day_MA')


print(data)