# ============================
# backtest.py
# ============================
def backtest(df, y_pred):
    df = df.iloc[-len(y_pred):].copy()
    df['signal'] = y_pred
    df['strategy_return'] = df['return'] * df['signal']
    cumulative = (1 + df['strategy_return']).cumprod()
    return cumulative.iloc[-1] - 1
