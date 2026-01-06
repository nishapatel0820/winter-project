past = data.loc["2016-01-01":"2020-12-31"].copy()
future = data.loc["2021-01-01":"2025-01-01"].copy()
def two_down_day_returns(df):
    P = df["Adj Close"]
    ret = (P - P.shift(1)) / P.shift(1)
    ret_tm1 = ret.shift(1)
    signal = (ret < 0) & (ret_tm1 < 0)
    fwd = (P.shift(-1) - P) / P
    return fwd[signal].dropna()
past_returns = two_down_day_returns(past)
future_returns = two_down_day_returns(future)

print("PAST (2016–2020)")
print("Trades:", len(past_returns))
print("Avg return:", past_returns.mean())

print("\nFUTURE (2021–2025)")
print("Trades:", len(future_returns))
print("Avg return:", future_returns.mean())

