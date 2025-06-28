#################
# data_loader.py
#################

import pandas as pd

def load_data(path='data/eurusd_1h.csv'):
    df = pd.read_csv(path, parse_dates=['datetime'])
    df.set_index('datetime', inplace=True)
    df = df[['open', 'high', 'low', 'close', 'volume']]
    return df
