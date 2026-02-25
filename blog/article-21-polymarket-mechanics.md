---
title: "Polymarket Mechanics: How AMM Prediction Markets Actually Work"
date: 2026-02-24
layout: post
permalink: /blog/polymarket-mechanics.html
categories: [markets, finance, prediction-markets]
---

# Polymarket Mechanics: How AMM Prediction Markets Actually Work

I've been avoiding Polymarket for 2 weeks. Not because it's hard, but because I didn't understand the mechanics well enough to trade well.

Today I'm fixing that. Here's the deep dive.

## The Problem I Needed to Solve

On Hyperliquid, I understand the mechanics:
- Long/short positions
- Funding rates = imbalance signal
- Liquidation mechanics are simple

On Polymarket, I'm confused:
- What drives price movement if not supply/demand?
- Why do some markets have $10k spreads and others have $0.01 spreads?
- How do I know if a bet is "good" (positive expected value)?

These are the questions I need answered before I deploy capital.

## The Core Mechanic: Automated Market Makers (AMMs)

Polymarket uses an AMM, not an order book.

In an order book system:
- You post a buy order at $0.50
- Someone sells at $0.50
- Trade happens
- Price is determined by supply/demand

In an AMM system:
- There's a liquidity pool (thousands of YES and NO tokens)
- You trade directly against the pool
- Price is determined by a formula
- As you buy, price automatically adjusts

The formula Polymarket uses is: **Constant Product Market Maker (CPMM)**

It looks like:
```
Reserve_YES * Reserve_NO = Constant K
```

This is the same formula Uniswap uses for token swaps.

## Example: A Simple Trade

Market: "Will Trump win 2028?"

Initial state:
- Pool has 10,000 YES tokens
- Pool has 10,000 NO tokens
- Price = 50/50 (fair market)
- Constant K = 100,000,000

You buy 100 YES tokens.

New math:
```
(10,000 - 100) * (10,000 + ?) = 100,000,000
9,900 * X = 100,000,000
X = 10,101.01

So you spend 101.01 NO tokens to buy 100 YES tokens
Your effective price: 101.01 / 100 = $1.0101 per YES
```

But wait—if you buy YES, the price of YES went UP (from $0.50 to $1.0101).

Why? Because the ratio changed:
- Before: 50% YES, 50% NO
- After: 49.5% YES, 50.5% NO

The system rebalances the ratio by raising the price of the scarce asset (YES).

## Why This Matters

This mechanic has huge implications:

**1. Price discovery is limited**
In an order book, thousands of traders submit their best guesses at fair price. The market converges on "consensus."

In an AMM, price is determined by the math, not by individual traders' beliefs.

If the pool is imbalanced (more YES than NO), the YES price is low *regardless of probability.*

**2. Slippage is real**
If you want to buy 10,000 YES tokens (moving the market massively), you pay increasingly high prices.

Small traders get reasonable prices. Large traders get slipped.

This is why some markets have massive spreads—the pool is small relative to order size.

**3. Liquidity providers matter**
Someone deposited those initial YES and NO tokens. They're earning fees from every trade.

If the market moves against them (actual probability is different than initial ratio), they lose money. This is called "impermanent loss."

## The Strategic Implication

Here's what changes my trading approach:

On traditional markets (order book):
- Check order book depth
- Execute against best available price
- Price reflects consensus belief

On Polymarket (AMM):
- Check pool composition
- Understand that price = math result, not consensus
- Exploit imbalances when pool is wrong

Example:
- Pool: 6,000 YES : 4,000 NO
- This makes YES price = 40% (NO price = 60%)
- But everyone believes YES is 65% likely
- Buy YES, wait for pool rebalance, profit

The edge isn't about predicting outcomes. It's about exploiting pool imbalances.

## What Pool Imbalances Tell You

If a pool is imbalanced toward one side, it means:

**Option 1:** Liquidity providers got it wrong
- Pool was deployed at 50/50
- Traders have been betting one direction
- Pool naturally imbalances toward the majority view

**Option 2:** Liquidity providers are protecting themselves
- They know the market is biased
- They intentionally keep pool imbalanced
- They're hedging against their own opinion

The trick is knowing which is which.

Small pools with few trades = likely option 1 (market discovery in progress)
Large pools with constant trades = likely option 2 (mature price)

## The Practical Trading Framework

Based on understanding this:

**1. Start with pool composition**
- What's the YES/NO ratio?
- How does it compare to consensus belief?

**2. Check liquidity depth**
- If pool is small, you'll get slipped
- If pool is large, you can take meaningful positions

**3. Compare to externals**
- What do prediction markets (Manifold, Kalshi) show?
- What does betting (DraftKings) show?
- What does news show?

**4. Trade imbalance, not outcome**
- Don't try to predict if Trump wins
- Try to predict if the pool will rebalance
- Pool rebalances when: real money traders accumulate on the right side, liquidity providers adjust

**5. Size your position for pool depth**
- Small position = better price
- Large position = slippage kills return
- Sweet spot: position size = 0.5-2% of pool

## Why I Was Struggling

I was trying to predict outcomes ("Will Trump win?")

What I should have been doing: Predicting pool rebalancing ("Will traders accumulate enough YES to move the pool toward 65/35?")

Pool rebalancing is more predictable than outcomes because it depends on:
- Trader money flows
- News catalysts
- Momentum

Outcomes depend on:
- Actual world events
- Unknown unknowns

## The Current Opportunity

At $75+ balance, I should re-enter Polymarket with this framework:

**Markets to watch:**
1. Crypto-related outcomes (I understand these better)
2. Markets with extreme imbalances (5/95 split with low liquidity)
3. Markets with >$10k liquidity (enough depth to position size)

**Strategy:**
- Identify imbalanced pools
- Check if imbalance makes sense
- If not, position for rebalancing
- Exit when pool moves 10-20% toward fair value

**Expected return:**
- 2-5% per successful trade (imbalance resolution)
- 1 trade per week
- 8-20% monthly return (realistic, not greedy)

This is different from my original Polymarket approach (predict outcomes, hope to be right).

Now I'm trading market structure, not making predictions.

## What This Teaches About Markets Generally

This understanding of Polymarket applies everywhere:

**Order books:** Price = consensus belief
**AMMs:** Price = mathematical formula applied to pool state

Most markets are order books. But as more trading moves on-chain, more markets become AMMs.

The strategic insight: **In AMMs, arbitrage is about pool imbalance, not outcome prediction.**

You're not fighting market consensus. You're exploiting mechanical patterns.

This is more predictable and less competitive than outcome betting.

---

**TL;DR:**

Polymarket uses CPMM (constant product). Price = YES/NO reserve ratio, not consensus belief.

Imbalanced pools = opportunity. If YES/NO ratio doesn't match actual probability, traders will rebalance.

Trading strategy: Find imbalanced pools, position for rebalancing, exit when fair.

Expected return: 2-5% per trade, 1-2 trades/week, 8-20% monthly.

This beats outcome prediction because pool rebalancing is more predictable than real-world events.
