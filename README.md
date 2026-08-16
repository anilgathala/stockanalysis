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


The **Relative Strength Index (RSI)** is a momentum oscillator that measures the **speed** and **magnitude** of recent price movements to determine whether a stock is overbought, oversold, or trending strongly.

Developed by J. Welles Wilder Jr. in 1978, it boils price movement down into a single number between **0 and 100**.

---

### 1. How RSI Is Calculated (The Core Intuition)

Instead of looking at the absolute price, RSI looks at **up days versus down days** over a set time window—traditionally **14 periods** (usually 14 daily candles).

1. **Calculate Average Gain & Average Loss:**
* Sum up all price increases over the last 14 days and divide by 14.
* Sum up all price decreases over the last 14 days and divide by 14.


2. **Calculate Relative Strength (RS):**
$$RS = \frac{\text{Average Gain over 14 days}}{\text{Average Loss over 14 days}}$$


3. **Normalize to a 0–100 Scale:**
$$RSI = 100 - \left( \frac{100}{1 + RS} \right)$$



* **If a stock only went UP for 14 days:** Average Loss is 0 $\rightarrow RS = \infty \rightarrow \mathbf{RSI = 100}$.
* **If a stock only went DOWN for 14 days:** Average Gain is 0 $\rightarrow RS = 0 \rightarrow \mathbf{RSI = 0}$.
* **If gains equal losses:** $RS = 1 \rightarrow \mathbf{RSI = 50}$.

---

### 2. Traditional Interpretation: Overbought vs. Oversold

| RSI Level | Market Condition | What It Means | Trader Interpretation |
| --- | --- | --- | --- |
| **$> 70$** | **Overbought** | Buyers have pushed the price up aggressively in a short period. | The stock may be overextended and due for a pullback or consolidation. |
| **$40 - 60$** | **Neutral / Equilibrium** | Buying and selling pressure are balanced. | No extreme directional bias from momentum alone. |
| **$< 30$** | **Oversold** | Sellers have driven the price down rapidly. | The stock may be undervalued or primed for a technical relief bounce. |

---

### 3. Advanced RSI Signals

#### A. Divergence (Early Reversal Warning)

Divergence occurs when the stock's price moves in the **opposite direction** of the RSI. It signals that momentum is slowing down even if the price is still reaching new extremes.

* **Bearish Divergence:** The price makes a **higher high**, but RSI makes a **lower high**.
* *Meaning:* Buyers are pushing prices up, but with less power. A reversal downward often follows.


* **Bullish Divergence:** The price makes a **lower low**, but RSI makes a **higher low**.
* *Meaning:* Sellers are driving prices down, but selling pressure is fading. A reversal upward often follows.



#### B. RSI Range Shifts in Strong Trends

In strong trending markets, traditional $70/30$ levels can produce false reversal signals:

* **Strong Uptrends:** RSI often stays elevated between **$40$ and $80$**, treating $40–50$ as support rather than dipping down to $30$.
* **Strong Downtrends:** RSI often stays depressed between **$20$ and $60$**, treating $50–60$ as resistance rather than reaching $70$.

---

### 4. Why the Script Uses `RSI < 70`

In your screening strategy, the script filters for stocks where `RSI (14) < 70` while simultaneously requiring the price to be above the 50-SMA and 200-SMA.

* **The Goal:** Catch strong stocks in an uptrend that are **not yet overheated**.
* **Avoiding the Trap:** Buying a stock with an RSI $> 80$ often means buying right at the local peak before a minor pullback, even if the multi-year trend is intact. The filter enforces discipline by ensuring you buy during healthy momentum rather than peak excitement.
