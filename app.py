import streamlit as st
import pandas as pd
import datetime

# Asset list
assets = [
    "NVDA", "MSFT", "AAPL", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "AVGO", "COST",
    "AMD", "NFLX", "GOLD", "USTECH100", "SP500", "USOIL", "QQQ", "USDJPY", "EURUSD", "BTCUSD"
]

# Timeframe weighting presets (simulated)
timeframe_weights = {
    "M1": {"macro": 0.1, "options": 0.5, "geo": 0.4},
    "M5": {"macro": 0.15, "options": 0.5, "geo": 0.35},
    "M15": {"macro": 0.2, "options": 0.4, "geo": 0.4},
    "1H": {"macro": 0.3, "options": 0.35, "geo": 0.35},
    "4H": {"macro": 0.4, "options": 0.3, "geo": 0.3},
    "Daily": {"macro": 0.6, "options": 0.2, "geo": 0.2}
}

# Simulated scoring function
def score_asset(symbol, macro_us, macro_eu, macro_asia, options_bias, geo_risk, weights):
    today = datetime.date.today().toordinal()
    base = (hash(symbol) + today) % 9 - 4
    macro_score = base * (macro_us * 0.01 + macro_eu * 0.01 + macro_asia * 0.01)
    final_score = (
        macro_score * weights["macro"] +
        options_bias * weights["options"] +
        geo_risk * weights["geo"]
    )
    if final_score > 1:
        sentiment = "🟢 Bullish"
    elif final_score < -1:
        sentiment = "🔴 Bearish"
    else:
        sentiment = "🟡 Neutral"
    return round(final_score, 2), sentiment

# UI
st.set_page_config(page_title="AI EdgeFinder v3", layout="wide")
st.title("📊 AI EdgeFinder v3 – Timeframe-Aware Sentiment Dashboard")

# Timeframe Selector
timeframe = st.selectbox("Select Timeframe:", list(timeframe_weights.keys()), index=5)
weights = timeframe_weights[timeframe]

st.sidebar.header("🧠 Signal Inputs")
macro_us = st.sidebar.slider("US Macro Score", 0, 100, 40)
macro_eu = st.sidebar.slider("Eurozone Macro Score", 0, 100, 30)
macro_asia = st.sidebar.slider("Asia Macro Score", 0, 100, 30)
options_bias = st.sidebar.slider("Options Chain Bias (-3 to 3)", -3, 3, 0)
geo_risk = st.sidebar.slider("Geopolitical Risk (-3 to 3)", -3, 3, 0)

# Table
rows = []
for symbol in assets:
    score, sentiment = score_asset(symbol, macro_us, macro_eu, macro_asia, options_bias, geo_risk, weights)
    rows.append({"Symbol": symbol, "Score": score, "Sentiment": sentiment})

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, height=650)

st.caption(f"Bias calculated using weights for {timeframe}: Macro {weights['macro']*100:.0f}%, "
           f"Options {weights['options']*100:.0f}%, Geopolitics {weights['geo']*100:.0f}%")
