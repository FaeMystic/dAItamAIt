from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf
import ta

app = FastAPI(title="dAItamAIt", version="0.8.0")


@app.get("/")
def home():
    return FileResponse("templates/index.html")


@app.get("/analyze")
def analyze(ticker: str):

    # Download daily data
    df = yf.download(
        ticker,
        period="6mo",
        interval="1d",
        auto_adjust=True,
        multi_level_index=False
    )

    # Download weekly data
    weekly = yf.download(
        ticker,
        period="2y",
        interval="1wk",
        auto_adjust=True,
        multi_level_index=False
    )

    # Download hourly data
    hourly = yf.download(
        ticker,
        period="3mo",
        interval="1h",
        auto_adjust=True,
        multi_level_index=False
    )

    if df.empty:
        return {"error": "Ticker not found"}

    close = df["Close"].squeeze()

    # Indicators
    df["EMA20"] = ta.trend.ema_indicator(close, window=20)
    df["EMA50"] = ta.trend.ema_indicator(close, window=50)
    df["RSI"] = ta.momentum.rsi(close, window=14)

    macd = ta.trend.MACD(close)
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    df["ATR"] = ta.volatility.average_true_range(
        df["High"],
        df["Low"],
        close,
        window=14
    )

    # Weekly EMA
    weekly["EMA20"] = ta.trend.ema_indicator(weekly["Close"], window=20)
    weekly["EMA50"] = ta.trend.ema_indicator(weekly["Close"], window=50)

    # Hourly EMA
    hourly["EMA20"] = ta.trend.ema_indicator(hourly["Close"], window=20)
    hourly["EMA50"] = ta.trend.ema_indicator(hourly["Close"], window=50)

    latest = df.iloc[-1]

    entry_price = float(latest["Close"])
    atr = float(latest["ATR"])

    stop_loss = entry_price - (2 * atr)
    take_profit = entry_price + (4 * atr)

    score = 50
    confidence = 50
    reasons = []

    if latest["EMA20"] > latest["EMA50"]:
        score += 20
        confidence += 15
        reasons.append("EMA trend is bullish")

    if latest["RSI"] > 55:
        score += 20
        confidence += 15
        reasons.append("RSI shows momentum")

    if latest["MACD"] > latest["MACD_SIGNAL"]:
        score += 15
        confidence += 20
        reasons.append("MACD crossover is bullish")

    confidence = min(confidence, 100)

    if score >= 100:
        signal = "STRONG BUY"
        trend = "Bullish"
    elif score >= 75:
        signal = "BUY"
        trend = "Bullish"
    elif score >= 55:
        signal = "HOLD"
        trend = "Neutral"
    else:
        signal = "SELL"
        trend = "Bearish"

    ema_status = "🟢 Bullish" if latest["EMA20"] > latest["EMA50"] else "🔴 Bearish"
    macd_status = "🟢 Bullish" if latest["MACD"] > latest["MACD_SIGNAL"] else "🔴 Bearish"

    if latest["RSI"] > 70:
        rsi_status = "🔴 Overbought"
    elif latest["RSI"] < 30:
        rsi_status = "🟢 Oversold"
    else:
        rsi_status = "🟡 Neutral"

    atr_status = "🔵 Normal"

    weekly_trend = "🟢 Bullish" if weekly.iloc[-1]["EMA20"] > weekly.iloc[-1]["EMA50"] else "🔴 Bearish"
    daily_trend = "🟢 Bullish" if latest["EMA20"] > latest["EMA50"] else "🔴 Bearish"
    hourly_trend = "🟢 Bullish" if hourly.iloc[-1]["EMA20"] > hourly.iloc[-1]["EMA50"] else "🔴 Bearish"

    alignment = sum([
        "Bullish" in weekly_trend,
        "Bullish" in daily_trend,
        "Bullish" in hourly_trend
    ])

    return {
        "ticker": ticker.upper(),
        "price": round(entry_price, 2),
        "entry_price": round(entry_price, 2),
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2),
        "risk_reward": "2 : 1",
        "EMA20": round(float(latest["EMA20"]), 2),
        "EMA50": round(float(latest["EMA50"]), 2),
        "RSI": round(float(latest["RSI"]), 2),
        "ATR": round(atr, 2),
        "MACD": round(float(latest["MACD"]), 2),
        "MACD_SIGNAL": round(float(latest["MACD_SIGNAL"]), 2),
        "trade_score": score,
        "confidence": f"{confidence}%",
        "trend": trend,
        "signal": signal,
        "reason": ", ".join(reasons),
        "ema_status": ema_status,
        "macd_status": macd_status,
        "rsi_status": rsi_status,
        "atr_status": atr_status,
        "weekly_trend": weekly_trend,
        "daily_trend": daily_trend,
        "hourly_trend": hourly_trend,
        "alignment_score": f"{alignment}/3"
    }
