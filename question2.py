import yfinance as yf
import pandas as pd
import numpy as np


ticker = "SPY"
start = "2005-01-01"
end = "2025-01-01"

data = yf.download(ticker, start=start, end=end, auto_adjust=False)


P = data["Adj Close"]


data["Return_t"] = (P - P.shift(1)) / P.shift(1)

# R_{t-1}
data["Return_t_minus_1"] = data["Return_t"].shift(1)

buy_signal = (
    (data["Return_t"] < 0) &
    (data["Return_t_minus_1"] < 0)
).fillna(False)


data["Return_t_plus_1"] = (P.shift(-1) - P) / P


trade_returns = data.loc[buy_signal, "Return_t_plus_1"].dropna()


avg_return_per_trade = trade_returns.mean() * 100
total_trades = len(trade_returns)
cumulative_return_percent = ((1 + trade_returns).prod() - 1) * 100


print(f"Strategy Performance for {ticker} (2005-01-01 to 2025-01-01):")
print(f"Total Trades: {total_trades}")
print(f"Average Return per Trade: {avg_return_per_trade:.4f}%")
print(f"Total Cumulative Return: {cumulative_return_percent:.4f}%")

