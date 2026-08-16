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
