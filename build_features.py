import pandas as pd
import ta

# Load data
df = pd.read_csv("data/stock_data_5y.csv")

print("Rows before processing:", len(df))

# Ensure Close is numeric
df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

# -----------------------
# INDICATORS
# -----------------------

df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()

df["MA20"] = df["Close"].rolling(20).mean()
df["MA50"] = df["Close"].rolling(50).mean()

# ✅ REAL EMA (FIXED)
df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
df["EMA21"] = df["Close"].ewm(span=21, adjust=False).mean()
df["EMA200"] = df["Close"].ewm(span=200, adjust=False).mean()

# -----------------------
# OTHER FEATURES
# -----------------------

df["Daily_Return"] = df["Close"].pct_change()
df["Volatility"] = df["Daily_Return"].rolling(20).std()

df["Momentum"] = df["Close"] - df["Close"].shift(10)
df["Return"] = df["Close"].pct_change(5)

# -----------------------
# CLEAN DATA
# -----------------------

features = [
    "RSI","MA20","MA50",
    "EMA9","EMA21","EMA200",
    "Volatility","Momentum","Return"
]

df = df.dropna(subset=features)

print("Rows after feature engineering:", len(df))

# Save
df.to_csv("features/stock_features.csv", index=False)

print("✅ Feature engineering completed!")