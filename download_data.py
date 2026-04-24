import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

end_date = datetime.today()
start_date = end_date - timedelta(days=5*365)

all_data = []

for stock in stocks:
    print(f"Downloading {stock}...")

    data = yf.download(stock, start=start_date, end=end_date)
    data["Stock"] = stock

    all_data.append(data)

df = pd.concat(all_data)

df.to_csv("data/stock_data_5y.csv")

print("Download completed!")