'''
This script works in two main phases: **screening** (which stocks qualify) and **ranking** (how they are ordered).

Here is the conceptual step-by-step breakdown of how the process operates:

### 1. Stock Selection (The Filter)

To be picked up by the script, a stock must pass three specific conditions simultaneously:

* **Long-Term Trend Alignment:** The stock’s price must be above its **200-SMA**. This ensures the script only looks at stocks currently in an overall long-term uptrend.
* **Medium-Term Trend Alignment:** The stock’s price must also be above its **50-SMA**. This confirms that the recent medium-term trend is positive as well.
* **Healthy Momentum (Not Overbought):** The **RSI (14)** must be below a certain ceiling (typically under 70). This filters out stocks that have run up too fast and might be due for an immediate cool-off or pullback.

Any stock failing even one of these criteria is eliminated from the list.

---

### 2. Ordering & Ranking (The Sorting)

Once the qualifying stocks are selected, the script orders them using a **momentum-to-risk ranking approach**:

* **Primary Rank (12M Return):** The list is primarily sorted in descending order by **12M Ret (%)**. The script prioritizes long-term momentum, putting the highest-performing stocks over the past year right at the top.
* **Secondary Ties & Risk Adjustments (Volatility):** To distinguish between stocks with similar returns, the script uses **3M Ann Vol (%)** and short-term returns (**1M / 3M Ret**).
* It favors stocks with strong 12-month performance that maintain **lower volatility** relative to their gains—seeking steady, sustained trends rather than erratic price swings.


'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

# ==========================================
# 1. PARAMETERS & UNIVERSE SETUP
# ==========================================
START_DATE = "2018-01-01"
END_DATE = "2026-08-01"
BENCHMARK = "SPY"

# Liquid megacap / tech stock universe
UNIVERSE = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
    "AVGO", "AMD", "QCOM", "TXN", "INTC", "MU", "AMAT", "LRCX"
]

TOP_N = 10  # Select top N momentum stocks

# ==========================================
# 2. DATA DOWNLOAD & PREPROCESSING
# ==========================================
print("Downloading historical data...")
tickers = list(set(UNIVERSE + [BENCHMARK]))

# Download raw data into memory
raw_data = yf.download(tickers, start=START_DATE, end=END_DATE, auto_adjust=True)

# Handle multi-level index column formats safely across yfinance versions
if isinstance(raw_data.columns, pd.MultiIndex):
    if "Close" in raw_data.columns.levels[0]:
        data = raw_data["Close"]
    elif "Adj Close" in raw_data.columns.levels[0]:
        data = raw_data["Adj Close"]
    elif "adj close" in raw_data.columns.levels[0]:
        data = raw_data["adj close"]
    elif "close" in raw_data.columns.levels[0]:
        data = raw_data["close"]
    else:
        data = raw_data.xs('Close', axis=1, level=1) if 'Close' in raw_data.columns.get_level_values(1) else raw_data.xs('Adj Close', axis=1, level=1)
else:
    data = raw_data

# Separate strategy universe from benchmark
price_df = data[UNIVERSE].dropna(axis=1, how="all")
spy_df = data[BENCHMARK].dropna()

# ==========================================
# 3. IDENTIFY TOP MOMENTUM STOCKS TODAY
# ==========================================
# Calculate 12-month momentum (~252 trading days)
momentum_12m = price_df.pct_change(252)

# Extract latest available trading day's momentum
latest_date = price_df.index[-1]
latest_momentum = momentum_12m.loc[latest_date]

# Rank and select top N stocks
top_stocks_series = latest_momentum.nlargest(TOP_N)
selected_tickers = top_stocks_series.index.tolist()

print("\n" + "=" * 55)
print(f" TOP {TOP_N} MOMENTUM STOCKS FOR {latest_date.strftime('%Y-%m-%d')}")
print("=" * 55)
for rank, (ticker, mom) in enumerate(top_stocks_series.items(), start=1):
    print(f" Rank {rank}: {ticker:<6} | 12-Month Return: {mom * 100:>7.2f}%")

# ==========================================
# 4. COMPUTE TECHNICAL INDICATORS
# ==========================================
def calculate_rsi(series, period=14):
    """Calculate Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Generate technical indicators table for selected stocks
indicator_summary = []

for ticker in selected_tickers:
    prices = price_df[ticker]
    
    # Latest Price
    current_price = prices.iloc[-1]
    
    # Moving Averages
    sma_50 = prices.rolling(window=50).mean().iloc[-1]
    sma_200 = prices.rolling(window=200).mean().iloc[-1]
    
    # Momentum Metrics
    mom_1m = prices.pct_change(21).iloc[-1] * 100   # ~1 month
    mom_3m = prices.pct_change(63).iloc[-1] * 100   # ~3 months
    mom_12m_val = latest_momentum[ticker] * 100     # 12 months
    
    # RSI (14-day)
    rsi_14 = calculate_rsi(prices, 14).iloc[-1]
    
    # Volatility (Annualized Daily Std Dev over 63 days)
    volatility_3m = (prices.pct_change().rolling(63).std().iloc[-1]) * np.sqrt(252) * 100
    
    indicator_summary.append({
        "Ticker": ticker,
        "Price ($)": round(current_price, 2),
        "50-SMA ($)": round(sma_50, 2),
        "200-SMA ($)": round(sma_200, 2),
        "RSI (14)": round(rsi_14, 2),
        "1M Ret (%)": round(mom_1m, 2),
        "3M Ret (%)": round(mom_3m, 2),
        "12M Ret (%)": round(mom_12m_val, 2),
        "3M Ann Vol (%)": round(volatility_3m, 2)
    })

indicator_df = pd.DataFrame(indicator_summary).set_index("Ticker")

print("\n" + "=" * 55)
print(" TECHNICAL INDICATORS SUMMARY FOR SELECTED STOCKS")
print("=" * 55)
print(indicator_df.to_string())

# ==========================================
# 5. BACKTEST HISTORICAL PERFORMANCE
# ==========================================
# Monthly price resampling for strategy backtest
monthly_prices = price_df.resample('ME').last()
monthly_returns = monthly_prices.pct_change()
momentum_lookback = monthly_prices.pct_change(12)

# Rebalance monthly based on top N 12-month momentum stocks
selected_history = momentum_lookback.shift(1).apply(
    lambda row: row.nlargest(TOP_N).index.tolist() if not row.isna().all() else [], axis=1
)

strategy_returns = []
for date, assets in selected_history.items():
    if isinstance(assets, list) and len(assets) > 0:
        period_ret = monthly_returns.loc[date, assets].mean()
        strategy_returns.append(period_ret)
    else:
        strategy_returns.append(0)

strategy_df = pd.DataFrame({'Strategy': strategy_returns}, index=monthly_prices.index)
strategy_df['Strategy_Equity'] = (1 + strategy_df['Strategy'].fillna(0)).cumprod()

# Benchmark performance
spy_monthly = spy_df.resample('ME').last().pct_change()
spy_equity = (1 + spy_monthly.fillna(0)).cumprod()

# Export results to CSV
indicator_df.to_csv("top_stocks_indicators.csv")
print("\nSaved technical summary to 'top_stocks_indicators.csv'")

# ==========================================
# 6. VISUALIZATION
# ==========================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), gridspec_kw={'height_ratios': [2, 1]})

# Chart 1: Normalized Price Normalized Performance of Selected Top Stocks
for ticker in selected_tickers:
    normalized_price = price_df[ticker] / price_df[ticker].iloc[0] * 100
    ax1.plot(normalized_price.index, normalized_price, label=f"{ticker} (Current Top Pick)", linewidth=1.8)

ax1.set_title(f"Price Performance History of Top {TOP_N} Selected Stocks (Base 100)", fontsize=12, fontweight='bold')
ax1.set_ylabel("Rebased Index Value")
ax1.legend(loc="upper left")
ax1.grid(True, linestyle="--", alpha=0.5)

# Chart 2: Strategy Backtest vs. SPY Benchmark
ax2.plot(strategy_df.index, strategy_df['Strategy_Equity'], label=f"Momentum Strategy (Top {TOP_N})", color="navy", linewidth=2)
ax2.plot(spy_equity.index, spy_equity, label="SPY Benchmark", color="gray", linestyle="--", linewidth=1.5)
ax2.set_title("Strategy Cumulative Equity Curve vs. SPY Benchmark", fontsize=12, fontweight='bold')
ax2.set_xlabel("Date")
ax2.set_ylabel("Growth of $1")
ax2.legend(loc="upper left")
ax2.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()
