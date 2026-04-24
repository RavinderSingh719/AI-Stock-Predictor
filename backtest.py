import yfinance as yf
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

model = joblib.load("models/stock_model.pkl")

stock = "RELIANCE.NS"

df = yf.download(stock, period="5y")

# Indicators
df["MA20"] = df["Close"].rolling(20).mean()
df["MA50"] = df["Close"].rolling(50).mean()

df["Volatility"] = df["Close"].pct_change().rolling(10).std()

# Momentum
df["Momentum"] = df["Close"] - df["Close"].shift(10)

# Return
df["Return"] = df["Close"].pct_change(5)

# RSI
delta = df["Close"].diff()

gain = delta.clip(lower=0).rolling(14).mean()
loss = (-delta.clip(upper=0)).rolling(14).mean()

rs = gain / loss
df["RSI"] = 100 - (100 / (1 + rs))

# Features used by model
features = [
    "RSI","MA20","MA50",
    "EMA9","EMA21","EMA200",
    "Volatility","Momentum","Return"
]

df = df.dropna()

correct = 0
total = 0

for i in range(len(df)-5):

    row = df[features].iloc[i:i+1]

    prob = model.predict_proba(row)[0][1]

    price_today = df["Close"].iloc[i].item()
    price_future = df["Close"].iloc[i+5].item()

    if prob > 0.6:
        total += 1

        if price_future > price_today:
            correct += 1

if total > 0:
    accuracy = correct / total
else:
    accuracy = 0

print("Predictions:", total)
print("Correct:", correct)
print("Accuracy:", round(accuracy,2))