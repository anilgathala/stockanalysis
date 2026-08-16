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

Here are the definitions and interpretations for each metric generated in your technical indicators table:

* **50-SMA ($) [50-Day Simple Moving Average]**
The unweighted average closing price of the stock over the last 50 trading days (~10 weeks). It acts as a short-to-medium-term trend indicator and dynamic support/resistance level. A price above the 50-SMA generally signals short-term bullish momentum.
* **200-SMA ($) [200-Day Simple Moving Average]**
The unweighted average closing price over the last 200 trading days (~40 weeks or ~1 year). It is the standard technical indicator for long-term market trends. Stocks trading above their 200-SMA are considered in a long-term uptrend.
* **Golden Cross / Death Cross:** When the 50-SMA crosses above the 200-SMA, it forms a bullish "Golden Cross"; crossing below signals a bearish "Death Cross."


* **RSI (14) [Relative Strength Index (14-Period)]**
A momentum oscillator measured on a scale from 0 to 100 based on the speed and magnitude of recent price changes over the last 14 trading days.
* **$> 70$:** Overbought territory (stock may be overextended and prone to a pull-back).
* **$< 30$:** Oversold territory (stock may be undervalued or due for a technical bounce).


* **1M Ret (%) [1-Month Percentage Return]**
The total percentage price change over the last 21 trading days (~1 calendar month). Measures immediate short-term momentum.
* **3M Ret (%) [3-Month Percentage Return]**
The total percentage price change over the last 63 trading days (~1 calendar quarter). Useful for tracking medium-term quarterly momentum.
* **12M Ret (%) [12-Month Percentage Return]**
The total percentage price change over the last 252 trading days (~1 calendar year). This is the core ranking metric used in cross-sectional momentum strategies to identify top market performers.
* **3M Ann Vol (%) [3-Month Annualized Volatility]**
The annualized standard deviation of daily percentage returns computed over the trailing 63 trading days (multiplied by $\sqrt{252}$). It quantifies the price fluctuation risk of the asset—higher values indicate wider price swings and higher expected risk/reward variance.
