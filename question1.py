######
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

data = yf.download("SPY", period="20y",auto_adjust=False)
data.head()
data['DayOfWeek'] = data.index.dayofweek
data['week'] = data.index.to_period('W-FRI')
data.head(10)
tuesday = data[data['DayOfWeek'] == 1][['Adj Close', 'week']]
friday  = data[data['DayOfWeek'] == 4][['Adj Close', 'week']]
trades = pd.merge(
    tuesday,
    friday,
    on='week',
    suffixes=('_Tue', '_Fri')
)
trades['return'] = trades['Adj Close_Fri'] / trades['Adj Close_Tue'] - 1
trades.head()

portfolio_returns = trades['return']
portfolio_value = (1 + portfolio_returns).cumprod()
portfolio_value.index = trades['week'].dt.to_timestamp()

start_price = data['Adj Close'].iloc[0]
end_price = data['Adj Close'].iloc[-1]
buy_hold_return = (end_price - start_price) / start_price

print("Number of trades:", len(trades))
print("Strategy total return (%):", round((portfolio_value.iloc[-1] - 1) * 100, 2))
print("Buy-and-hold total return (%):", round(buy_hold_return * 100, 2))

results_table = pd.DataFrame({
    'Metric': [
        'Number of trades',
        'Strategy total return (%)',
        'Buy-and-hold total return (%)'
    ],
    'Value': [
        len(trades),
        round((portfolio_value.iloc[-1] - 1) * 100, 2),
        round(float(buy_hold_return) * 100, 2)
    ]
})
results_table

buy_hold_portfolio = data['Adj Close'] / data['Adj Close'].iloc[0]
plt.figure(figsize=(10,6))

plt.plot(portfolio_value, label='Tuesday–Friday Strategy')
plt.plot(buy_hold_portfolio, label='Buy & Hold SPY')

plt.xlabel("Date")
plt.ylabel("Portfolio Value (Start = 1)")
plt.title("SPY Tuesday–Friday Strategy vs Buy-and-Hold")
plt.legend()

plt.show()
