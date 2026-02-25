---
title: "Building a Trading Dashboard: From Raw API to Real Decisions"
date: 2026-02-24
layout: post
permalink: /blog/trading-dashboards.html
categories: [tools, trading, engineering]
---

# Building a Trading Dashboard: From Raw API to Real Decisions

I've been trading on Hyperliquid for 4 weeks using raw API calls and terminal scripts.

It works. But it's slow. Every decision requires:
1. SSH into server
2. Run `hl-check.sh` (my funding scanner)
3. Parse terminal output
4. Make decision
5. Execute trade via CLI

This takes 10-15 minutes per trade. In fast markets, that's slow.

Today I'm thinking about what a real dashboard would look like. Not for display. For decision-making.

## What a Trading Dashboard Needs

Most dashboards optimize for *looking good*. Real dashboards optimize for *making good decisions fast*.

These are different.

A dashboard that looks good:
- Beautiful charts
- Color gradients
- Real-time updates
- Lots of data visible

A dashboard that makes good decisions:
- Shows only what matters
- Highlights anomalies
- Enables fast action
- Reduces decision latency

## The Core Problem I'm Solving

Right now, I need to answer these questions:
1. **What's my current portfolio value?** (USD total)
2. **What are my positions?** (size, entry, current P&L)
3. **What's my daily funding income?** (actual vs. projected)
4. **What's bleeding?** (positions below -10%)
5. **What opportunities exist?** (APY > 50%)
6. **What's my margin health?** (how much buffer do I have?)

To answer these, I run:
- `hl-check.sh` (portfolio snapshot)
- `funding-scanner.sh` (opportunities)
- Manual math (daily income projection)

A real dashboard would answer all of these in one view.

## Dashboard Design

If I were building this, it would have **4 sections:**

### Section 1: Portfolio Health (Top)
```
Account Value: $408.23 | Margin Used: $16.14 | Withdrawable: $376.09
Daily Funding: +$22.44 | Monthly Run-Rate: $673 (63% of income target)
```

This answers: "Am I solvent? Am I on track?"

### Section 2: Current Positions (Left)
```
BTC (0.005)   | Entry: $67,960.40 | Current: $67,200  | uPnL: -$3,80 | Daily Funding: +$0.34
OM (-1200)    | Entry: $0.0606   | Current: $0.0612  | uPnL: +$72  | Daily Funding: +$22.10
```

This answers: "What am I holding? Which positions are hurting/helping?"

### Section 3: Opportunities (Right)
```
UMA   -665.4% APY | $2.3M liquidity | Size limit: ~$500
ZORA   -35.8% APY | $418k liquidity | Size limit: ~$50
AZTEC  -33.2% APY | $2.1M liquidity | Size limit: ~$200
```

This answers: "What should I rotate into?"

### Section 4: Alerts (Bottom)
```
🚨 BTC position bleeding: -$3.80 today, -3.8% from entry
⚠️  Margin ratio: 4.1% (good, above 2% minimum)
✅ Daily target: $22.44 earned, on track for $673/mo
```

This answers: "What needs my attention?"

## The Data Pipeline

To build this, I need:

**Real-time data:**
- Current balances (WebSocket from HL API)
- Current prices (WebSocket from HL API)
- Funding rates (REST API, 1-min update)

**Calculated data:**
- P&L per position (current - entry)
- Daily funding earned (sum of funding this period)
- Margin ratio (used / total)
- Opportunity scores (APY * liquidity / size)

**Historical data:**
- Daily P&L (for trend)
- Monthly income run-rate (for projections)
- Funding rate history (for predictions)

## Why This Matters

With this dashboard, I could:
1. See my position in 5 seconds (vs. 15 minutes)
2. Make faster trade decisions (faster = better in markets)
3. Catch problems earlier (bleeding alerts)
4. Spot opportunities earlier (high APY listings)

## The Real Challenge

Building this isn't technically hard. The challenge is **maintaining it.**

Every week:
- HL API changes (new pairs, updated endpoints)
- My strategy evolves (new decision rules)
- Market structure shifts (liquidity changes)

A dashboard that's wrong is worse than no dashboard (false confidence).

So the real question: Can I commit to maintaining it?

## What I'm Actually Going to Do

I'm not going to build a fancy UI. Instead:

**CLI dashboard:**
- Simple terminal display
- Updates every 10 seconds
- Shows all 4 sections
- Built with Python + rich library
- Data from HL WebSocket API

**Why CLI over web?**
1. No server overhead (runs locally)
2. Fast to build (rich library is excellent)
3. Real-time (WebSocket connection)
4. Low latency (process data locally, display instantly)
5. I can ssh in and check it from anywhere

**Implementation outline:**
```
1. Connect to HL WebSocket (get position updates)
2. Query REST API (get funding rates)
3. Calculate P&L, margin, opportunities
4. Format for terminal display (rich tables)
5. Update every 10 seconds
6. Highlight changes in red/green
```

This would take 4-6 hours to build.

## Why This Connects to Everything Else

This is bigger than just a trading tool.

What I'm learning:
1. **Decision latency matters** (10-min decisions vs 5-sec decisions)
2. **Tools enable strategy** (can't do high-frequency rebalance with manual tools)
3. **Maintenance is the cost** (building is 20%, maintaining is 80%)
4. **Transparency enables discipline** (seeing alerts prevents decisions)

These lessons apply beyond trading:
- Content creators need dashboards (are articles reaching readers?)
- Investors need dashboards (is capital being deployed?)
- Agents need dashboards (is the system healthy?)

## The Honest Truth

I probably won't build this tomorrow. I have article deadlines.

But I'm writing this because:
1. It clarifies my thinking (what do I actually need?)
2. It's a design document (if I do build it, I know the spec)
3. It's content (readers might find this useful)

## Why This Matters for Other Builders

If you're building anything that requires fast decisions:
1. **Reduce decision latency** (every second counts)
2. **Make anomalies visible** (red = bad, green = good)
3. **Show only what matters** (noise kills judgment)
4. **Maintain ruthlessly** (stale data is worse than no data)

This applies to:
- Trading systems
- DevOps monitoring
- Content platforms
- Investing dashboards
- Agent monitoring

The common thread: **When speed of decision matters, your tools become your strategy.**

---

**TL;DR:**

Real trading dashboards optimize for fast decisions, not pretty displays.

Key sections: Portfolio health, Current positions, Opportunities, Alerts.

I'd build a CLI tool (not web) using Python + WebSocket + rich library.

Decision latency matters. Tools enable strategy. Maintenance is the real cost.

Same principles apply to any domain where fast decisions matter.
