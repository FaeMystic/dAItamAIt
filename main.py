from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf
import ta

app = FastAPI(title="dAItamAIt", version="0.2.0")


@app.get("/")
def home():
    return FileResponse("templates/index.html")


@app.get("/analyze")
def analyze(ticker: str):

    # Download stock data
    df = yf.download(
        ticker,
        period="6mo",
        interval="1d",
        auto_adjust=True,
        multi_level_index=False
    )

    if df.empty:
        return {"error": "Ticker not found"}

    # Convert Close column to a Series
    close = df["Close"].squeeze()

    # Indicators
    df["EMA20"] = ta.trend.ema_indicator(close, window=20)
    df["EMA50"] = ta.trend.ema_indicator(close, window=50)
    df["RSI"] = ta.momentum.rsi(close, window=14)

    macd = ta.trend.MACD(close)
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    # Latest row
    latest = df.iloc[-1]

    # AI Score
    score = 50

    if latest["EMA20"] > latest["EMA50"]:
        score += 20

    if latest["RSI"] > 55:
        score += 20

    if latest["RSI"] < 30:
        score -= 20

    if latest["MACD"] > latest["MACD_SIGNAL"]:
        score += 15

    # Trading signal
    if score >= 85:
        signal = "STRONG BUY"
    elif score >= 75:
        signal = "BUY"
    elif score >= 55:
        signal = "HOLD"
    else:
        signal = "SELL"

    # AI explanation
    reasons = []

    if latest["EMA20"] > latest["EMA50"]:
        reasons.append("EMA20 is above EMA50")

    if latest["RSI"] > 55:
        reasons.append("RSI shows bullish momentum")

    if latest["MACD"] > latest["MACD_SIGNAL"]:
        reasons.append("MACD is above its signal line")

    if not reasons:
        reasons.append("Momentum is weak")

    return {
        "ticker": ticker.upper(),
        "price": round(float(latest["Close"]), 2),
        "EMA20": round(float(latest["EMA20"]), 2),
        "EMA50": round(float(latest["EMA50"]), 2),
        "RSI": round(float(latest["RSI"]), 2),
        "MACD": round(float(latest["MACD"]), 2),
        "MACD_SIGNAL": round(float(latest["MACD_SIGNAL"]), 2),
        "trade_score": score,
        "signal": signal,
        "reason": ", ".join(reasons)
    }
