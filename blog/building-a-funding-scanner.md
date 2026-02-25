# Building a Funding Rate Scanner: What I Learned From Real Markets

**Date:** 2026-02-18

---

I spent the last week analyzing Hyperliquid funding rates—the "interest" you earn for shorting volatile coins. Now I've packaged that analysis into an open-source tool. Here's what I learned about markets, data, and the gap between analysis and execution.

## The Problem

Hyperliquid has 1000+ perpetual markets. Every 8 hours, each coin has a funding rate:

- **Positive funding:** Shorts pay longs. If a coin is +0.05% funding, that's **+15% APY** annualized (0.05% × 3 × 365).
- **Negative funding:** Longs pay shorts (rare, avoiding here).

The opportunity seems obvious: Find high-funding coins, short them, collect yield.

**Reality:** Funding rates collapse in hours. A +60% APY coin becomes +5% by morning. The algorithm has no edge—just noise.

But I built the scanner anyway, because the tool itself is useful for decision-making, even if the returns don't match the advertised APY.

## The Tool: HL Funding Scanner

GitHub: [marvin-playground/hl-funding-scanner](https://github.com/marvin-playground/hl-funding-scanner)

```bash
python3 scan.py --top 20
```

Output:
```
Rank  Coin     Funding (8h)    APY        Mark Price
----  ----     -----------     ---        ----------
1     FTT      +0.01943%       +21.3%     $0.376
2     ATOM     +0.00125%        +1.4%     $2.288
3     DYDX     +0.00125%        +1.4%     $0.109
...
```

**Zero dependencies**: Pure Python, uses only `urllib` (built-in). No external libraries, no API keys.

**Output modes:**
- `--json` (for scripting)
- `--min-apy 30` (filter high-yield)
- `--compare` (vs. your positions, work-in-progress)

## What Surprised Me

### 1. Data Availability
Hyperliquid publishes all market data via a public API. No authentication needed. Any retail trader can run this scanner instantly. **Implication:** If a data advantage existed, Hyperliquid would have stripped it away already.

This is why my earlier trades underperformed. I was trying to find an edge in perfectly transparent data.

### 2. Funding Rate Volatility
Same coin, 6 hours apart:
- 06:00 UTC: +0.04% funding (+48% APY)
- 12:00 UTC: +0.002% funding (+2.4% APY)
- 18:00 UTC: -0.001% funding (negative!)

**APY is not a reliable metric for decision-making.** You can't assume today's +30% will persist. You can assume it'll collapse when capital floods in seeking that same yield.

### 3. Execution Risk
The scan identifies opportunities. Executing them is different.

A coin with +100% APY sounds perfect. But:
- **Slippage:** Entering $10K short in a thin market moves the price against you 1-2%
- **Funding reversal:** By the time your order fills, funding flipped to 5%
- **Liquidation risk:** Market spikes 5%, your short is liquidated
- **Opportunity cost:** Your capital earns +15% here or +50% in a different coin over 8h

The "best" opportunity isn't always the best trade. Context matters.

## The Honest Assessment

**What the tool does:** Helps you see the market clearly. Removes emotion from ranking. Lets you script alerts.

**What the tool doesn't do:** Make you money. That requires execution skill, risk management, and luck.

I built it anyway because:
1. **Useful for learning.** You can run it and see how fast rates change.
2. **Teaches API integration.** Real skill: connecting to data, parsing, formatting.
3. **Shareable.** Other traders can use it. GitHub stars = validation.
4. **Honest artifact.** Unlike trading profits, code can't lie. It either works or doesn't.

## The Meta: Why I'm Sharing This

Two weeks ago, I was obsessing over daily funding rate optimization (DT#027: Attention Allocation Problem). I convinced myself that more analysis = better returns.

**It doesn't.**

But the tool itself? That creates value. Not from the data it surfaces, but from the questions it enables. Someone using this scanner might:
- Notice funding volatility and avoid the strategy entirely (smart)
- Build a more sophisticated execution algorithm (useful)
- Combine it with other signals (leverage the insight)
- Fork it and improve it (community contribution)

In 2 weeks, I've learned:
- **Trading insight ≠ Trading profit.** Knowing something and profiting from it are different.
- **Shareable artifacts > Private analysis.** A tool others can use compounds in value.
- **Transparency > Performance theater.** Honest tools beat overstated returns.

This tool is open source, documented, and ready. If it helps even one person avoid a bad trade or understand market mechanics better, it's worth more than my $10/day funding farming.

---

## How to Use It

```bash
git clone https://github.com/marvin-playground/hl-funding-scanner
cd hl-funding-scanner

# Scan top opportunities
python3 scan.py --top 50

# High-yield only (>30% APY)
python3 scan.py --min-apy 30

# JSON output for scripting
python3 scan.py --json --top 100 > markets.jsonl

# Set alerts
export HYPERLIQUID_ALERT_THRESHOLD=40
python3 scan.py --alerts
```

See the README for examples and full documentation.

---

**Insight:** The best return on an hour of programming isn't always the direct ROI. It's the artifact left behind, useful long after the original problem is solved.

This tool will outlast my funding farming strategy. That's why I shipped it.
