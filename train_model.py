import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("features/stock_features.csv")

print("Rows loaded:", len(df))

# Target
df["Future_Close"] = df["Close"].shift(-5)
df["Target"] = (df["Future_Close"] > df["Close"]).astype(int)

# Features
features = [
    "RSI","MA20","MA50",
    "EMA9","EMA21","EMA200",
    "Volatility","Momentum","Return"
]

# Drop missing values
df = df.dropna(subset=features + ["Target"])

print("Rows after cleaning:", len(df))

X = df[features]
y = df["Target"]

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Prediction
pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("Model Accuracy:", round(accuracy, 3))

# Save model
joblib.dump(model, "models/stock_model.pkl")

print("Model saved successfully!")