import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from streamlit_lightweight_charts import renderLightweightCharts
from streamlit_autorefresh import st_autorefresh


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Stock Predictor",
    layout="wide",
    page_icon="📈"
)

# ---------------------------------------------------
# AUTO REFRESH
# ---------------------------------------------------

st_autorefresh(interval=60000, key="refresh")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("📈 AI Stock Market Predictor")
st.caption("Machine Learning Based Market Scanner")

# ---------------------------------------------------
# MARKET OVERVIEW
# ---------------------------------------------------

st.subheader("📊 Market Overview")

indices = {
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "FIN NIFTY": "NIFTY_FIN_SERVICE.NS",
    "MIDCAP": "NIFTY_MIDCAP_100.NS",
    "SENSEX": "^BSESN"
}

cols = st.columns(len(indices))

def get_index(symbol):
    try:
        data = yf.Ticker(symbol).history(period="2d")
        if data.empty or len(data) < 2:
            return None, None

        price = data["Close"].iloc[-1]
        prev = data["Close"].iloc[-2]
        change = ((price - prev) / prev) * 100
        return price, change
    except:
        return None, None

for i, (name, sym) in enumerate(indices.items()):
    price, change = get_index(sym)

    with cols[i]:
        if price is None:
            st.metric(name, "N/A")
        else:
            st.metric(
                name,
                f"{price:.0f}",
                f"{change:.2f}%",
                delta_color="normal" if change > 0 else "inverse"
            )

st.divider()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

try:
    df = pd.read_csv("scan_results.csv")
except:
    st.error("scan_results.csv not found")
    st.stop()

df["Probability_%"] = (df["Probability_Up"] * 100).round(2)
df = df.sort_values("Probability_Up", ascending=False)

# ---------------------------------------------------
# LAYOUT
# ---------------------------------------------------

left, center, right = st.columns([1.2, 2.7, 1.1])

# ---------------------------------------------------
# LEFT PANEL
# ---------------------------------------------------

with left:
    st.subheader("🏆 Top AI Picks")

    for _, row in df.head(5).iterrows():
        st.write(f"**{row['Stock']}**")
        st.progress(row["Probability_%"] / 100)
        st.caption(f"{row['Probability_%']}%")

    st.divider()
    st.subheader("Ranking")

    st.dataframe(
        df[["Stock", "Probability_%"]],
        use_container_width=True,
        height=350
    )

# ---------------------------------------------------
# CENTER PANEL (CHART + INSIGHTS)
# ---------------------------------------------------

with center:
    st.subheader("📊 Stock Chart")

    stock = st.selectbox("Select Stock", df["Stock"])

    timeframe_map = {
        "1M": ("1mo", "1d"),
        "3M": ("3mo", "1d"),
        "6M": ("6mo", "1d"),
        "1Y": ("1y", "1d"),
        "5Y": ("5y", "1wk")
    }

    tf = st.selectbox("Timeframe", list(timeframe_map.keys()), index=3)
    period, interval = timeframe_map[tf]

    data = yf.download(stock, period=period, interval=interval, progress=False, auto_adjust=True)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    if data.empty or len(data) < 20:
        st.warning("Not enough data")
        st.stop()

    if "Volume" not in data.columns:
        data["Volume"] = 0

    # --------------------
    # INDICATORS
    # --------------------

    data = data.copy().reset_index(drop=True)

    data["MA20"] = data["Close"].rolling(20, min_periods=1).mean()
    data["MA50"] = data["Close"].rolling(50, min_periods=1).mean()
     
     # EMA (FIX - REQUIRED)
    data["EMA9"] = data["Close"].ewm(span=9, adjust=False).mean()
    data["EMA21"] = data["Close"].ewm(span=21, adjust=False).mean()
    data["EMA200"] = data["Close"].ewm(span=200, adjust=False).mean()

    data["Volume"] = data["Volume"].astype(float)
    data["AvgVol"] = data["Volume"].rolling(20, min_periods=1).mean()
    data["VolumeSpike"] = data["Volume"] > (data["AvgVol"] * 2)

    data["CandleMove"] = (data["Close"] - data["Open"]) / data["Open"]
    data["SmartMoney"] = data["VolumeSpike"] & (data["CandleMove"] > 0.02)

    latest_smart = data["SmartMoney"].iloc[-1]
    latest_vol = data["VolumeSpike"].iloc[-1]
    
   # Distance from EMAs (in %)
    data["Dist_EMA200"] = ((data["Close"] - data["EMA200"]) / data["EMA200"]) * 100
    data["Dist_EMA21"] = ((data["Close"] - data["EMA21"]) / data["EMA21"]) * 100
    data["Dist_EMA9"] = ((data["Close"] - data["EMA9"]) / data["EMA9"]) * 100

    # --------------------
    # EXTRA METRICS (NEW)
    # --------------------

    ath = data["High"].max()
    atl = data["Low"].min()
    current_price = data["Close"].iloc[-1]

    dist_high = ((current_price - ath) / ath) * 100
    dist_low = ((current_price - atl) / atl) * 100

    today_volume = int(data["Volume"].iloc[-1])

    # RSI
    delta = data["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14, min_periods=1).mean()
    avg_loss = loss.rolling(14, min_periods=1).mean()

    rs = avg_gain / avg_loss.replace(0, 1e-10)
    rsi = 100 - (100 / (1 + rs))
    latest_rsi = rsi.iloc[-1]

    # --------------------
    # CHART DATA
    # --------------------

    chart_data = [
        {
            "time": str(row["Date"].date()),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"])
        }
        for _, row in data.tail(300).iterrows()
    ]

    ema9_data = [
    {"time": str(row["Date"].date()), "value": float(row["EMA9"])}
    for _, row in data.tail(300).iterrows()
    if not pd.isna(row["EMA9"])
    ]

    ema21_data = [
    {"time": str(row["Date"].date()), "value": float(row["EMA21"])}
    for _, row in data.tail(300).iterrows()
    if not pd.isna(row["EMA21"])
    ]

    ema200_data = [
    {"time": str(row["Date"].date()), "value": float(row["EMA200"])}
    for _, row in data.tail(300).iterrows()
    if not pd.isna(row["EMA200"])
    ]

    # Theme
    theme = st.get_option("theme.base")

    if theme == "dark":
        bg_color = "#0b1220"
        text_color = "white"
        grid_color = "#1f2937"
    else:
        bg_color = "white"
        text_color = "black"
        grid_color = "#e5e7eb"

    chart = {
        "chart": {
            "height": 500,
            "layout": {
                "background": {"type": "solid", "color": bg_color},
                "textColor": text_color
            },
            "grid": {
                "vertLines": {"color": grid_color},
                "horzLines": {"color": grid_color}
            }
        },
        "series": [
    {"type": "Candlestick", "data": chart_data},

    {
        "type": "Line",
        "data": ema9_data,
        "options": {"color": "#facc15", "lineWidth": 2}   # Yellow
    },
    {
        "type": "Line",
        "data": ema21_data,
        "options": {"color": "#3b82f6", "lineWidth": 2}   # Blue
    },
    {
        "type": "Line",
        "data": ema200_data,
        "options": {"color": "#ef4444", "lineWidth": 3}   # Red
    }
    ]
    }

    renderLightweightCharts([chart], key="chart")

    # --------------------
    # 📊 STOCK INSIGHTS PANEL (NEW)
    # --------------------

    st.markdown("### 📊 Stock Insights")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("ATH", f"{ath:.2f}")
        st.metric("ATL", f"{atl:.2f}")

    with c2:
        st.metric("From ATH", f"{dist_high:.2f}%")
        st.metric("From ATL", f"{dist_low:.2f}%")

    with c3:
        st.metric("Volume", f"{today_volume:,}")

    with c4:
        rsi_status = "Overbought" if latest_rsi > 70 else "Oversold" if latest_rsi < 30 else "Neutral"
        st.metric("RSI (14)", f"{latest_rsi:.2f}")
        st.caption(rsi_status)
        
    stocks_info = pd.read_csv("stats/stocks_300.csv")
    df = df.merge(stocks_info, on="Stock", how="left")
    
    
# ---------------------------------------------------
# RIGHT PANEL
# ---------------------------------------------------
with right:
    st.subheader("🤖 AI Prediction")

    selected = df[df["Stock"] == stock].iloc[0]
    prob = selected["Probability_%"]
    sector = selected.get("Sector", "Unknown")

    st.metric("Confidence", f"{prob}%")

    # -------------------------
    # BASIC AI SIGNAL
    # -------------------------
    if prob > 70:
        st.success("STRONG BUY")
    elif prob > 55:
        st.info("BUY")
    else:
        st.warning("HOLD")

    st.divider()

    # -------------------------
    # EMA DISTANCE LOGIC (YOUR STRATEGY)
    # -------------------------
    dist_ema200 = ((data["Close"].iloc[-1] - data["EMA200"].iloc[-1]) / data["EMA200"].iloc[-1]) * 100
    dist_ema21 = ((data["Close"].iloc[-1] - data["EMA21"].iloc[-1]) / data["EMA21"].iloc[-1]) * 100
    dist_ema9 = ((data["Close"].iloc[-1] - data["EMA9"].iloc[-1]) / data["EMA9"].iloc[-1]) * 100

    buy_signal = (
        (2 < dist_ema200 < 5) and
        (1 < dist_ema21 < 3) and
        (1 < dist_ema9 < 3)
    )

    # -------------------------
    # TREND CONFIRMATION
    # -------------------------
    trend_ok = (
        data["EMA9"].iloc[-1] > data["EMA21"].iloc[-1] > data["EMA200"].iloc[-1]
    )

    # -------------------------
    # FINAL DECISION ENGINE
    # -------------------------
    st.subheader("⚡ Smart Signal")

    if prob > 70 and buy_signal and trend_ok:
        st.success("🚀 STRONG BUY (AI + EMA + Trend)")
    elif buy_signal and trend_ok:
        st.success("📈 BUY (EMA Strategy)")
    elif prob > 70:
        st.info("AI Bullish, but no technical confirmation")
    else:
        st.warning("No Strong Setup")

    st.divider()

    # -------------------------
    # SHOW DISTANCES (DEBUG / PRO INFO)
    # -------------------------
    st.subheader("📊 EMA Distance")

    st.metric("EMA200 Distance", f"{dist_ema200:.2f}%")
    st.metric("EMA21 Distance", f"{dist_ema21:.2f}%")
    st.metric("EMA9 Distance", f"{dist_ema9:.2f}%")

    st.divider()

    # -------------------------
    # SMART MONEY
    # -------------------------
    if latest_smart:
        st.success("Smart Money Detected")
    elif latest_vol:
        st.info("High Volume Activity")
    else:
        st.warning("Normal Activity")

    st.divider()

    # -------------------------
    # TREND
    # -------------------------
    if data["Close"].iloc[-1] > data["MA50"].iloc[-1]:
        st.success("Bullish Trend")
    else:
        st.warning("Weak Trend")

    st.divider()

    # -------------------------
    # 🔥 SECTOR STRENGTH (FINAL FIX)
    # -------------------------
    st.subheader("📊 Sector Strength")

    if "Sector" in df.columns:
        sector_perf = df.groupby("Sector")["Probability_Up"].mean().sort_values(ascending=False)

        # Current stock sector rank
        if sector in sector_perf.index:
            rank = list(sector_perf.index).index(sector) + 1
            strength = sector_perf[sector] * 100

            st.metric("Sector", sector)
            st.metric("Sector Strength", f"{strength:.2f}%")
            st.caption(f"Rank: #{rank} / {len(sector_perf)}")

            # Status
            if rank <= 3:
                st.success("🔥 Leading Sector")
            elif rank <= 6:
                st.info("Moderate Sector")
            else:
                st.warning("Weak Sector")

        # Small visual
        st.bar_chart(sector_perf)

    else:
        st.warning("Sector data not available")

    

  
# ---------------------------------------------------
# 🔥 PRO AI HEATMAP (CARD STYLE)
# ---------------------------------------------------



st.divider()
st.subheader("🔥 AI Market Heatmap")

# 🔥 create same layout proportions
h_left, h_center, h_right = st.columns([1.2, 2.7, 1.1])

with h_center:   # 👈 IMPORTANT (align under center panel)
    
    heat = df.head(20)

    cols_per_row = 4
    rows = (len(heat) + cols_per_row - 1) // cols_per_row

    def get_color(p):
        if p >= 80: return "#16a34a"
        elif p >= 65: return "#22c55e"
        elif p >= 50: return "#facc15"
        elif p >= 35: return "#f97316"
        else: return "#dc2626"

    for i in range(rows):
        cols = st.columns(cols_per_row, gap="medium")

        for j in range(cols_per_row):
            idx = i * cols_per_row + j

            if idx < len(heat):
                stock = heat.iloc[idx]["Stock"]
                prob = heat.iloc[idx]["Probability_%"]

                cols[j].markdown(f"""
                <div style="
                    height:110px;
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    align-items:center;
                    background:{get_color(prob)};
                    border-radius:12px;
                    color:white;
                    font-weight:600;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                ">
                    <div style="font-size:13px;">{stock}</div>
                    <div style="font-size:18px;">{prob:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.caption("⚠️ Not financial advice")