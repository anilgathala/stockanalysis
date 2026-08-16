import sys
import numpy as np
import pandas as pd
import ta
import yfinance as yf


def fetch_ticker_data(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """Downloads historical OHLCV data using yfinance for a given ticker symbol."""
    print(f"Fetching data for '{ticker}'...")
    data = yf.download(ticker, period=period, interval=interval, progress=False)

    if data.empty:
        raise ValueError(f"No market data found for ticker '{ticker}'. Please check the symbol.")

    # Flatten MultiIndex columns if present (yfinance return artifact)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Ensure required columns are clean and properly typed
    required_cols = ["Open", "High", "Low", "Close", "Volume"]
    for col in required_cols:
        if col not in data.columns:
            raise KeyError(f"Missing required column '{col}' in downloaded data.")

    return data[required_cols].copy()


def generate_exit_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates technical exit signals for short-term momentum expiry.

    Expects df with columns: ['Open', 'High', 'Low', 'Close', 'Volume']
    """
    df = df.copy()

    # ---------------------------------------------------------
    # Section 1: Moving Average Crossovers & MACD
    # ---------------------------------------------------------
    df["EMA_5"] = ta.trend.ema_indicator(df["Close"], window=5)
    df["EMA_20"] = ta.trend.ema_indicator(df["Close"], window=20)

    # MACD Calculation
    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_Signal"] = macd.macd_signal()
    df["MACD_Hist"] = macd.macd_diff()

    # Signal 1A: Price breaks below 20-day EMA
    df["Signal_EMA20_Break"] = df["Close"] < df["EMA_20"]

    # Signal 1B: MACD Bearish Crossover (Line drops below Signal Line)
    df["Signal_MACD_Cross_Under"] = (df["MACD"] < df["MACD_Signal"]) & (
        df["MACD"].shift(1) >= df["MACD_Signal"].shift(1)
    )

    # ---------------------------------------------------------
    # Section 2: Overbought & Divergence (RSI)
    # ---------------------------------------------------------
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)

    # Signal 2A: RSI Exit Overbought (Crosses below 70 from above)
    df["Signal_RSI_Exit_Overbought"] = (df["RSI"] < 70) & (
        df["RSI"].shift(1) >= 70
    )

    # Signal 2B: Bearish RSI Divergence (Price higher high, RSI lower high over 10 bars)
    df["Price_HH"] = df["Close"] > df["Close"].shift(10)
    df["RSI_LH"] = df["RSI"] < df["RSI"].shift(10)
    df["Signal_Bearish_RSI_Divergence"] = (
        df["Price_HH"] & df["RSI_LH"] & (df["RSI"] > 60)
    )

    # ---------------------------------------------------------
    # Section 3: Volume & Cashflow Exhaustion (OBV & VWAP)
    # ---------------------------------------------------------
    df["OBV"] = ta.volume.on_balance_volume(df["Close"], df["Volume"])
    df["OBV_EMA"] = ta.trend.ema_indicator(df["OBV"], window=10)

    # Signal 3A: On-Balance Volume Breaks below its 10-period EMA
    df["Signal_OBV_Distribution"] = df["OBV"] < df["OBV_EMA"]

    # ---------------------------------------------------------
    # Section 4: Volatility & Rejection (Bollinger Bands)
    # ---------------------------------------------------------
    bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)
    df["BB_Upper"] = bb.bollinger_hband()

    # Signal 4A: Rejection from Upper Bollinger Band (High touched BB, Close back inside)
    df["Signal_BB_Rejection"] = (df["High"].shift(1) >= df["BB_Upper"].shift(1)) & (
        df["Close"] < df["BB_Upper"]
    )

    # ---------------------------------------------------------
    # Composite Exit Score (0 to 5 Signals Active)
    # ---------------------------------------------------------
    signal_cols = [
        "Signal_EMA20_Break",
        "Signal_MACD_Cross_Under",
        "Signal_RSI_Exit_Overbought",
        "Signal_OBV_Distribution",
        "Signal_BB_Rejection",
    ]

    df["Exit_Signal_Count"] = df[signal_cols].sum(axis=1)
    df["Take_Profit_Cut_Loss_Trigger"] = df["Exit_Signal_Count"] >= 2

    return df


def analyze_ticker(ticker_symbol: str, period: str = "6mo") -> None:
    """Executes full pipeline: download, signal generation, and reporting."""
    df_raw = fetch_ticker_data(ticker_symbol, period=period)
    df_analyzed = generate_exit_signals(df_raw)

    latest = df_analyzed.iloc[-1]
    latest_date = df_analyzed.index[-1].strftime("%Y-%m-%d")

    print("\n" + "=" * 55)
    print(f" EXIT SIGNAL ANALYSIS SUMMARY: {ticker_symbol.upper()}")
    print(f" Date: {latest_date}")
    print("=" * 55)
    print(f" Close Price:                     ${latest['Close']:.2f}")
    print(f" 20-Day EMA:                      ${latest['EMA_20']:.2f}")
    print(f" RSI (14):                        {latest['RSI']:.2f}")
    print("-" * 55)
    print(" Active Individual Signals:")
    print(f"  - Price < EMA 20 Break:         {'[X]' if latest['Signal_EMA20_Break'] else '[ ]'}")
    print(f"  - MACD Bearish Cross-Under:     {'[X]' if latest['Signal_MACD_Cross_Under'] else '[ ]'}")
    print(f"  - RSI Overbought Exit (<70):    {'[X]' if latest['Signal_RSI_Exit_Overbought'] else '[ ]'}")
    print(f"  - OBV Distribution (<10 EMA):   {'[X]' if latest['Signal_OBV_Distribution'] else '[ ]'}")
    print(f"  - BB Upper Band Rejection:      {'[X]' if latest['Signal_BB_Rejection'] else '[ ]'}")
    print("-" * 55)
    print(f" Total Exit Signals Active:       {int(latest['Exit_Signal_Count'])} / 5")
    print(f" Action Required (Exit Trigger):  {latest['Take_Profit_Cut_Loss_Trigger']}")
    print("=" * 55 + "\n")

    # Show recent bars where 2+ exit signals triggered
    recent_triggers = df_analyzed[df_analyzed["Take_Profit_Cut_Loss_Trigger"]].tail(5)
    if not recent_triggers.empty:
        print("Recent Dates Triggering Action (Score >= 2):")
        summary_df = recent_triggers[["Close", "RSI", "Exit_Signal_Count"]]
        summary_df.index = summary_df.index.strftime("%Y-%m-%d")
        print(summary_df.to_string())
    else:
        print("No exit triggers (Score >= 2) in the analyzed period.")


if __name__ == "__main__":
    # Accept ticker symbol from CLI argument or prompt the user
    if len(sys.argv) > 1:
        target_symbol = sys.argv[1].upper()
    else:
        target_symbol = input("Enter ticker symbol (e.g. AAPL, NVDA, SPY): ").strip().upper()

    if target_symbol:
        analyze_ticker(target_symbol)
    else:
        print("No ticker symbol provided.")