# ============================
# oanda_client.py
# ============================
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import pandas as pd
from config import OANDA_API_KEY

def fetch_candles(symbol="EUR_USD", granularity="H1", count=2000):
    client = oandapyV20.API(access_token=OANDA_API_KEY)
    params = {
        "granularity": granularity,
        "count": count,
        "price": "M"
    }
    r = instruments.InstrumentsCandles(instrument=symbol, params=params)
    client.request(r)
    candles = r.response['candles']

    df = pd.DataFrame([{
        'datetime': c['time'],
        'open': float(c['mid']['o']),
        'high': float(c['mid']['h']),
        'low': float(c['mid']['l']),
        'close': float(c['mid']['c']),
        'volume': c['volume']
    } for c in candles if c['complete']])

    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    return df
