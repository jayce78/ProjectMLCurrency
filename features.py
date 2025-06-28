# ============================
# features.py
# ============================
def make_features(df):
    df['return'] = df['close'].pct_change()
    df['target'] = df['close'].shift(-3) / df['close'] - 1  # 3-period forward return
    df['target'] = df['target'].apply(lambda x: 1 if x > 0.001 else 0)
    df.dropna(inplace=True)
    X = df[['rsi', 'macd', 'bb_upper', 'bb_middle', 'bb_lower',
            'rsi_lag1', 'macd_lag2', 'bb_width', 'price_sma_diff', 'hour',
            'is_trending']]
    y = df['target']
    return X, y
