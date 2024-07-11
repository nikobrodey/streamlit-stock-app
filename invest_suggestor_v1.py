import yfinance as yf
import pandas as pd
import numpy as np


ticker_data = ["PLTR", "TSLA", "MSFT", "META", "AAPL", "AMZN"] #, "KO", "NVDA", "SAP", "AZN", "SONY"]
start_date = "2023-01-01"
end_date = "2024-01-01"

data = yf.download(ticker_data, start=start_date, end=end_date)['Adj Close']

returns = data.pct_change()
moving_avg_10 = data.rolling(window=10).mean()
moving_avg_50 = data.rolling(window=50).mean()

data = data.join(returns, rsuffix='_daily_return')
data = data.join(moving_avg_10, rsuffix='_5day_MA')
data = data.join(moving_avg_50, rsuffix='_30day_MA')

def signal_rounded_ma_match(row):
    signals = {}
    for ticker in ticker_data:
        signal = 1 if round(row[ticker + '_5day_MA'], 0) == round(row[ticker + '_30day_MA'], 0) else 0
        signals[ticker + '_signal'] = signal
    return pd.Series(signals)

data = data.join(data.apply(signal_rounded_ma_match, axis=1))

def stock_return(data, invested):
    investments = {ticker: invested / len(ticker_data) for ticker in ticker_data}
    shares_held = {ticker: 0 for ticker in ticker_data}
    trades = 0
    # Iterate through each row in the DataFrame
    for index, row in data.iterrows():
        current_date = index.strftime('%Y-%m-%d')
       
        for ticker in ticker_data:
            if row[ticker + '_signal'] == 1:
                if row[ticker + '_daily_return'] > 0 and investments[ticker] > 0:  # Buying condition
                    trades += 1
                    buy_price = row[ticker]
                    shares_to_buy = investments[ticker] / buy_price
                    shares_held[ticker] += shares_to_buy
                    print(f"{current_date} - Buying: {shares_to_buy:.2f} shares of {ticker} at ${buy_price:.2f}, total spent: ${investments[ticker]:.2f}")
                    investments[ticker] = 0  # All money for ticker is invested

                elif row[ticker + '_daily_return'] < 0 and shares_held[ticker] > 0:  # Selling condition
                    trades += 1
                    sell_price = row[ticker]
                    investments[ticker] += shares_held[ticker] * sell_price
                    print(f"{current_date} - Selling: {shares_held[ticker]:.2f} shares of {ticker} at ${sell_price:.2f}, total retrieved: ${investments[ticker]:.2f}")
                    shares_held[ticker] = 0  # All shares sold

    # Calculate final value for each ticker
     # Print current position values
    for ticker in ticker_data:
        print(f"Current position for {ticker}: {shares_held[ticker]:.2f} shares held")
    
    final_values = [investments[ticker] + (shares_held[ticker] * data.iloc[-1][ticker]) for ticker in ticker_data]
    total_final_value = sum(final_values)
    return total_final_value, trades

# Calculate final portfolio value
initial_investment = 10000
final_portfolio_value, trades = stock_return(data, initial_investment)
print(f"\nPortfolio value: {round(final_portfolio_value,2)}")
print(f"profit: {round(final_portfolio_value- initial_investment,2)-trades}") 
print(f"roi: {round(((((final_portfolio_value-trades)/initial_investment)-1)*100),2)} % ")
print(f"after:  {trades} trades")


