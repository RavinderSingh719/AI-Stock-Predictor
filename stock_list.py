import pandas as pd
import os

# ---------------------------------------------------
# BASE PATH
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# ---------------------------------------------------
# DOWNLOAD NIFTY 500 LIST
# ---------------------------------------------------
url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"

try:
    df = pd.read_csv(url)
    print("✅ Loaded from NSE website")
except:
    file_path = os.path.join(BASE_DIR, "stats", "nifty500.csv")
    df = pd.read_csv(file_path)
    print("⚠️ Loaded from local file")

# ---------------------------------------------------
# CHECK COLUMNS
# ---------------------------------------------------
print("Columns:", df.columns)

# ---------------------------------------------------
# SELECT REQUIRED DATA
# ---------------------------------------------------
df = df[["Symbol", "Industry"]].dropna()

df.rename(columns={
    "Symbol": "Stock",
    "Industry": "Sector"
}, inplace=True)

# ---------------------------------------------------
# 🔥 CLEAN SECTOR NAMES (VERY IMPORTANT)
# ---------------------------------------------------
def clean_sector(sector):
    sector = str(sector).lower()

    if "bank" in sector:
        return "Banking"
    elif "it" in sector or "software" in sector or "tech" in sector:
        return "IT"
    elif "pharma" in sector or "health" in sector:
        return "Pharma"
    elif "auto" in sector:
        return "Auto"
    elif "fmcg" in sector or "consumer" in sector:
        return "FMCG"
    elif "metal" in sector:
        return "Metals"
    elif "energy" in sector or "oil" in sector or "gas" in sector:
        return "Energy"
    elif "infra" in sector or "construction" in sector:
        return "Infrastructure"
    elif "cement" in sector:
        return "Cement"
    elif "power" in sector:
        return "Power"
    else:
        return "Other"

# Apply cleaning
df["Sector"] = df["Sector"].apply(clean_sector)

# ---------------------------------------------------
# CONVERT TO YAHOO FORMAT
# ---------------------------------------------------
df["Stock"] = df["Stock"] + ".NS"

# ---------------------------------------------------
# LIMIT TO 300 STOCKS
# ---------------------------------------------------
df = df.head(300)

print("Total stocks:", len(df))
print(df.head())

# ---------------------------------------------------
# SAVE FILE
# ---------------------------------------------------
save_path = os.path.join(BASE_DIR, "stats", "stocks_300.csv")
df.to_csv(save_path, index=False)

print("✅ Saved with sectors:", save_path)

# ---------------------------------------------------
# DEBUG (OPTIONAL)
# ---------------------------------------------------
print("\nSector Distribution:\n")
print(df["Sector"].value_counts())