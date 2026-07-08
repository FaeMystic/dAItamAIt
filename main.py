from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf
import ta

app = FastAPI(title="dAItamAIt", version="0.1.0")


@app.get("/")
def home():
    return FileResponse("templates/index.html")


@app.get("/analyze")
def analyze(ticker: str):

    df = yf.download(
        ticker,
        period="6mo",
        interval="1d",
        auto_adjust=True,
        multi_level_index=False
    )

    if df.empty:
        return {"error": "Ticker not found"}

    close = df["Close"].squeeze()

    df["EMA20"] = ta.trend.ema_indicator(close, window=20)
    df["EMA50"] = ta.trend.ema_indicator(close, window=50)
    df["RSI"] = ta.momentum.rsi(close, window=14)

    latest = df.iloc[-1]

    score = 50

    if latest["EMA20"] > latest["EMA50"]:
        score += 20

    if latest["RSI"] > 55:
        score += 20

    if latest["RSI"] < 30:
        score -= 20

    if score >= 75:
        signal = "BUY"
    elif score >= 55:
        signal = "HOLD"
    else:
        signal = "SELL"

    return {
        "ticker": ticker.upper(),
        "price": round(float(latest["Close"]), 2),
        "EMA20": round(float(latest["EMA20"]), 2),
        "EMA50": round(float(latest["EMA50"]), 2),
        "RSI": round(float(latest["RSI"]), 2),
        "trade_score": score,
        "signal": signal
    }
