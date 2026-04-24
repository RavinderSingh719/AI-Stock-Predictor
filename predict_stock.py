import pandas as pd
import joblib

# Load model
model = joblib.load("models/stock_model.pkl")

# Load latest data
df = pd.read_csv("features/stock_features.csv")

# Select last row (latest market data)
latest = df.iloc[-1]

features = [
    "RSI","MA20","MA50",
    "EMA9","EMA21","EMA200",
    "Volatility","Momentum","Return"
]

X = latest[features].values.reshape(1, -1)

prediction = model.predict(X)[0]

probability = model.predict_proba(X)[0]

print("Prediction:", "UP" if prediction == 1 else "DOWN")
print("UP Probability:", probability[1])
print("DOWN Probability:", probability[0])