# ============================
# indicators.py
# ============================
import pandas as pd
import numpy as np

def add_indicators(df):
    # RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    df['rsi'] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26

    # Bollinger Bands
    sma = df['close'].rolling(window=20).mean()
    std = df['close'].rolling(window=20).std()
    df['bb_upper'] = sma + (2 * std)
    df['bb_middle'] = sma
    df['bb_lower'] = sma - (2 * std)

    # Additional indicators
    df['rsi_lag1'] = df['rsi'].shift(1)
    df['macd_lag2'] = df['macd'].shift(2)
    df['bb_width'] = df['bb_upper'] - df['bb_lower']
    df['price_sma_diff'] = df['close'] - df['bb_middle']
    df['hour'] = df.index.hour

    # Trend regime (simple proxy)
    df['ma_slope'] = df['bb_middle'].diff()
    df['is_trending'] = (df['ma_slope'].abs() > df['ma_slope'].std()).astype(int)

    df = df.dropna(subset=['rsi', 'macd', 'bb_upper', 'bb_middle', 'bb_lower'])
    return df
