import pandas as pd
import joblib
import os

# -----------------------------
# Load trained model
# -----------------------------
model = joblib.load("models/stock_model.pkl")

# -----------------------------
# Load stock data
# -----------------------------
data_path = os.path.join("data", "stock_data_5y.csv")
df = pd.read_csv(data_path)

print("\nColumns in dataset:")
print(df.columns)

# -----------------------------
# Convert columns to numeric
# -----------------------------
numeric_cols = ["Open", "High", "Low", "Close", "Volume"]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# Create indicators
# -----------------------------
df["MA20"] = df["Close"].rolling(20).mean()
df["MA50"] = df["Close"].rolling(50).mean()

df["Volatility"] = df["Close"].pct_change(fill_method=None).rolling(10).std()

# RSI
delta = df["Close"].diff()
gain = delta.clip(lower=0).rolling(14).mean()
loss = (-delta.clip(upper=0)).rolling(14).mean()

rs = gain / loss
df["RSI"] = 100 - (100 / (1 + rs))

# ✅ ADD THESE (FIX)
df["Momentum"] = df["Close"] - df["Close"].shift(10)
df["Return"] = df["Close"].pct_change()

# -----------------------------
# Features for model
# -----------------------------
features = [
    "RSI","MA20","MA50",
    "EMA9","EMA21","EMA200",
    "Volatility","Momentum","Return"
]

# Drop missing values
df = df.dropna(subset=features)

X = df[features]

# -----------------------------
# Run prediction
# -----------------------------
predictions = model.predict(X)
probabilities = model.predict_proba(X)[:, 1]

df["Prediction"] = predictions
df["Probability"] = probabilities

# -----------------------------
# Show results
# -----------------------------
print("\nAI Prediction Results:\n")
print(df[["Close", "Prediction", "Probability"]].tail(10))