import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE SETUP
# -------------------------
st.set_page_config(page_title="AI Stock Predictor", layout="wide")

st.title("📈 AI Stock Market Predictor")
st.caption("Powered by Machine Learning")

# -------------------------
# LOAD DATA
# -------------------------
try:
    heat = pd.read_csv("scan_results.csv")
except:
    st.error("❌ scan_results.csv not found. Run scanner first.")
    st.stop()

# Clean columns
heat.columns = heat.columns.str.strip()

# -------------------------
# VALIDATE DATA
# -------------------------
if "Stock" not in heat.columns or "Probability_Up" not in heat.columns:
    st.error("❌ Required columns missing in CSV")
    st.write("Columns found:", heat.columns)
    st.stop()

# Convert to numeric
heat["Probability_Up"] = pd.to_numeric(heat["Probability_Up"], errors="coerce")

# Drop bad rows
heat = heat.dropna(subset=["Stock", "Probability_Up"])

if heat.empty:
    st.warning("⚠ No valid data available")
    st.stop()

# -------------------------
# MARKET OVERVIEW
# -------------------------
st.subheader("📊 Market Overview")

# Top 20 stocks
top = heat.sort_values(by="Probability_Up", ascending=False).head(20)

# Create chart
fig = px.scatter(
    top,
    x="Stock",
    y="Probability_Up",
    color="Probability_Up",
    size="Probability_Up",
    color_continuous_scale="RdYlGn",
    title="Top AI Picks"
)

fig.update_layout(height=400)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# TABLE VIEW
# -------------------------
st.subheader("📋 Top Stocks")

top["Probability %"] = (top["Probability_Up"] * 100).round(2)

st.dataframe(top[["Stock", "Probability %"]], use_container_width=True)

# -------------------------
# FOOTER
# -------------------------
st.divider()
st.caption("⚠ This is an AI probability tool, not financial advice.")