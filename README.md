# 📈 AI Stock Market Predictor

A **machine learning-powered stock analysis dashboard** built with **Streamlit** that combines AI predictions, technical indicators, and sector intelligence into a single professional trading interface.

---

## 🚀 Features

### 🤖 AI Prediction Engine

* Predicts probability of stock price going up
* Confidence-based signals:

  * 🔥 Strong Buy
  * 📈 Buy
  * ⚠ Hold

---

### 📊 Interactive Stock Chart

* Candlestick chart (TradingView-style)
* Technical indicators:

  * EMA 9 (Short-term momentum)
  * EMA 21 (Swing trend)
  * EMA 200 (Long-term trend)
* Supports multiple timeframes (1M → 5Y)

---

### ⚡ Smart Trading Signals

* Custom EMA-based strategy:

  * Price near EMA zones
  * Trend alignment (EMA9 > EMA21 > EMA200)
* Combines:

  * AI prediction
  * Technical analysis
  * Trend confirmation

---

### 💰 Smart Money Detection

* Detects:

  * Volume spikes
  * Strong bullish candles
* Highlights institutional activity

---

### 📊 Sector Intelligence

* Dynamically calculates sector strength
* Ranks sectors based on AI probability
* Shows:

  * Sector strength %
  * Rank
  * Leading / Weak sectors

---

### 🔥 AI Heatmap

* Visual grid of top stocks
* Color-coded by probability:

  * 🟢 Strong bullish
  * 🟡 Neutral
  * 🔴 Weak

---

### 📊 Market Overview

* Live index tracking:

  * NIFTY 50
  * BANK NIFTY
  * FIN NIFTY
  * MIDCAP
  * SENSEX

---

### 📊 Stock Insights Panel

* All-time high / low
* Distance from ATH / ATL
* Volume analysis
* RSI (Overbought / Oversold)

---

## 🧠 Tech Stack

* **Python**
* **Streamlit**
* **Pandas**
* **yFinance**
* **Plotly**
* **Lightweight Charts**
* **TA (Technical Analysis)**

---

## 📁 Project Structure

```
AI_stock_predictor/
│
├── dashboard/
│   └── app.py                # Main Streamlit app
│
├── data/
│   └── stock_data_5y.csv
│
├── features/
│   └── stock_features.csv
│
├── stats/
│   ├── stocks_300.csv        # Stock + Sector mapping
│   └── nifty500.csv
│
├── scan_results.csv          # AI output
│
└── README.md
```

---

## ⚙️ Installation

```bash
# Clone repo
git clone https://github.com/your-username/AI_stock_predictor.git

cd AI_stock_predictor

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run dashboard/app.py
```

---

## 📌 Requirements

Create a `requirements.txt` file:

```
streamlit
pandas
yfinance
plotly
ta
streamlit-lightweight-charts
streamlit-autorefresh
```

---

## 🧠 How It Works

1. Collects stock data using yFinance
2. Generates technical indicators (EMA, RSI, Volume)
3. Runs ML model → outputs probability
4. Combines:

   * AI prediction
   * EMA strategy
   * Sector strength
5. Displays results in interactive dashboard

---

## ⚡ Strategy Logic

### ✅ Buy Signal Conditions

* Price:

  * 2–5% above EMA200
  * 1–3% above EMA21 & EMA9
* Trend:

  * EMA9 > EMA21 > EMA200
* AI Confidence:

  * High probability

---

## 📸 Screenshots

*(Add your app screenshots here)*

---

## ⚠ Disclaimer

This project is for **educational purposes only**.
Not financial advice. Always do your own research before investing.

---

## 🚀 Future Improvements

* 🔼 Buy/Sell signals on chart
* 📡 Real-time alerts
* 🧠 AI model improvements
* 📊 Backtesting engine
* 🌐 Deploy on cloud (Streamlit Cloud)

---
## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🍴 Fork it
* 📢 Share it

---
