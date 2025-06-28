# ============================
# main.py
# ============================
from oanda_client import fetch_candles
from indicators import add_indicators
from features import make_features
from model import train_model
from backtest import backtest
import numpy as np

# Load and prepare data
df = fetch_candles("EUR_USD", granularity="H1", count=3000)
print("Fetched rows:", len(df))

# Add indicators
df = add_indicators(df)
print("After indicators:", len(df))

# Create features
X, y = make_features(df)
print("Features shape:", X.shape)
print("Target shape:", y.shape)

# Walk-forward validation
n_samples = len(X)
window = int(0.8 * n_samples)
step = 100
returns = []
accuracies = []

for start in range(0, n_samples - window, step):
    end = start + window
    X_train, y_train = X.iloc[start:end], y.iloc[start:end]
    X_test, y_test = X.iloc[end:end+step], y.iloc[end:end+step]

    if len(X_test) == 0:
        break

    model, y_pred, acc = train_model(X_train, y_train, X_test, y_test)
    final_return = backtest(df.iloc[end:end+step], y_pred)

    returns.append(final_return)
    accuracies.append(acc)

print(f"Average Accuracy: {np.mean(accuracies):.2f}")
print(f"Average Return: {np.mean(returns) * 100:.2f}%")
