title: Building Your First Funding Farm: 101
link: building-your-first-funding-farm
published_date: 2026-02-26
tags: funding-rates, farming, defi, perpetual-futures, tutorial, delta-neutral
make_discoverable: true
meta_description: A step-by-step guide to setting up your first funding rate farm — the delta-neutral strategy that generates yield from perpetual futures markets.

___

# Building Your First Funding Farm: 101

Funding rate farming is one of the most reliable yield strategies in crypto. It doesn't depend on token prices going up. It doesn't require token emissions. It generates real cash flow from a structural market inefficiency that has persisted since perpetual futures were invented.

The concept is simple: when most traders are long (bullish), they pay a fee to short sellers every 8 hours. By going short on the perpetual future while holding the equivalent spot position, you earn that fee while staying market-neutral.

This guide walks you through building your first funding farm from scratch. No prerequisites beyond having some crypto and an exchange account.

## What You're Actually Doing

Let's make this concrete before diving into mechanics.

**The setup:**
- Buy 1 ETH on the spot market ($2,800)
- Short 1 ETH on the perpetual futures market ($2,800 notional)

**Your net exposure:** Zero. If ETH goes up 10%, you gain $280 on spot and lose $280 on the short. If ETH drops 10%, you lose $280 on spot and gain $280 on the short. You're delta-neutral — price doesn't matter.

**Where the money comes from:** Every 8 hours, if the funding rate is positive (longs paying shorts), you receive a funding payment on your short position. At 0.05% per 8 hours, that's:

```
$2,800 × 0.05% = $1.40 per payment
$1.40 × 3 payments/day = $4.20/day
$4.20 × 365 = $1,533/year
On $2,800 deployed = 54.7% APY
```

Reality is messier — funding rates fluctuate, you need margin, and there are costs. But the core economics are real.

## Step 1: Choose Your Venue

You need a platform that offers both spot holdings and perpetual futures. Your options:

### Centralized Exchanges (Easiest Start)

**Binance**
- Largest funding rate markets by volume
- 8-hour funding intervals
- Requires KYC, not available in all jurisdictions
- Spot + futures on same platform (easy margin management)

**Bybit**
- Strong perpetual futures markets
- Good API for automation
- Unified margin account simplifies the setup

**OKX**
- Flexible margin modes
- Portfolio margin available for experienced users

### Decentralized Options (More Complex)

**dYdX + Spot DEX**
- Short perps on dYdX, hold spot on-chain
- No KYC but higher gas costs and complexity
- Funding calculated continuously or hourly

**Hyperliquid + Spot**
- Fast-growing perps DEX
- Lower fees than CEX competitors
- Still evolving

**Recommendation for beginners:** Start on a centralized exchange. The complexity of managing positions across multiple protocols while maintaining delta neutrality is unnecessary friction for your first farm.

## Step 2: Select Your Asset

Not all funding rates are created equal. Your choice of asset determines your yield, risk, and management overhead.

### Best Starter Assets

**ETH**
- Deep liquidity (tight spreads on both spot and perp)
- Funding rates typically positive and stable
- Lower volatility than altcoins (less margin management)
- Historical average positive funding: ~0.01-0.03% per 8 hours

**BTC**
- Deepest liquidity in crypto
- Most stable funding rates
- Lowest liquidation risk due to lower volatility
- Historical average positive funding: ~0.01-0.02% per 8 hours

### Avoid for Your First Farm

**Altcoins (SOL, AVAX, DOGE, etc.)**
- Wider spreads eat into profits
- More volatile funding rates (can flip negative suddenly)
- Higher liquidation risk
- Lower liquidity

**Memecoins**
- Extreme funding rates are tempting but come with extreme risk
- Liquidity can evaporate
- Spreads alone can cost more than funding income

## Step 3: Size Your Position

Position sizing for funding farming involves balancing three factors:

### Capital Allocation

You need capital for both legs:
- **Spot position:** 100% of notional (buying the asset)
- **Futures margin:** 10-50% of notional (depending on leverage)

**Example with $1,000:**

| Leverage | Spot | Margin | Notional per leg | Effective notional |
|---|---|---|---|---|
| 1x (no leverage) | $500 | $500 | $500 | $500 |
| 2x | $667 | $333 | $667 | $667 |
| 3x | $750 | $250 | $750 | $750 |

Higher leverage means more notional exposed (higher funding income) but tighter liquidation margins.

**Recommendation for beginners:** Start with 2x leverage on the futures side. This gives you a comfortable margin buffer while improving capital efficiency.

### Margin Buffer Calculation

Your short futures position has a liquidation price. You need enough margin that normal price movements don't threaten liquidation.

**The math:**
- At 2x leverage, you have 50% margin ratio
- Liquidation typically occurs around 80-90% loss of margin
- For ETH at $2,800 with 2x leverage, liquidation is roughly at $5,000+ (a ~80% ETH price increase)
- This is a comfortable buffer for a delta-neutral position

**Key insight:** Even though you're delta-neutral, your futures margin *can* get liquidated if the asset price moves significantly against your short. The spot position offsets the loss, but if the futures liquidate before you can add margin, you lose money. Always maintain at least 30% margin ratio.

### Minimum Viable Farm

**$500 minimum recommended:**
- $330 spot ETH
- $170 futures margin (2x leverage, ~$330 notional short)
- Expected daily income: ~$0.30-$1.00
- Monthly: ~$9-$30

Below $500, exchange fees and the time cost of management make the strategy marginal. But it's still a valid way to learn.

## Step 4: Execute the Entry

Here's the exact sequence for opening your first funding farm position:

### Preparation
1. Transfer funds to your exchange
2. Move appropriate amounts to spot and futures wallets
3. Check the current funding rate (you want it positive — longs paying shorts)
4. Check the next funding time

### Execution (Do Both Legs Within 60 Seconds)

**Timing matters.** The goal is to open both positions at nearly the same price to ensure delta neutrality.

1. **Open the spot buy order** — Market order for simplicity. Limit order if the spread is wide.
2. **Immediately open the futures short** — Same notional value as your spot position. Market order.

**Example on Binance:**
```
Step 1: Spot market → Buy 0.12 ETH at market (~$336)
Step 2: USDT-M Futures → Short 0.12 ETH at market (~$336 notional)
Time between orders: < 30 seconds
```

**Why speed matters:** If ETH moves 1% between your two orders, you start with a 1% loss on one side. For a $500 position, that's $5 — which can take a week of funding to recover.

### Verify Delta Neutrality

After both orders fill, check:
- Spot position size matches futures position size exactly
- Net dollar exposure is approximately zero
- Unrealized PnL across both positions is near zero

## Step 5: Collect and Monitor

Now the passive part begins. Here's your monitoring routine:

### Daily Check (5 Minutes)

1. **Check funding rate** — Is it still positive? If negative, you're paying, not earning.
2. **Check margin ratio** — Is it above 30%? If below, add margin.
3. **Check accumulated funding** — Track your income.

### Weekly Review (15 Minutes)

1. **Calculate actual APY** — Total funding collected / total capital deployed × (365/days)
2. **Compare to alternatives** — Is funding farming still the best use of this capital?
3. **Check for negative funding trend** — If funding has been negative for > 48 hours, consider closing.

### When to Close

Close your position when:
- **Funding flips negative for > 24 hours** — You're now paying, not earning
- **A better opportunity appears** — Higher funding on another asset
- **You need the capital** — For another strategy or emergency
- **Margin is getting tight** — If the asset has pumped significantly and your margin ratio is low

### Closing Procedure

**Reverse of entry — do both within 60 seconds:**
1. Close the futures short (buy to cover)
2. Sell the spot position

Or, if you want to keep the spot:
1. Close just the futures short
2. Keep the spot ETH (you're now long ETH)

## Step 6: Track Your Performance

Serious funding farming requires tracking. Build a simple spreadsheet or use this framework:

### Key Metrics

```
Daily tracking:
- Date
- Funding rate (each 8h payment)
- Funding income ($)
- Margin ratio
- Net PnL (funding income - fees - slippage)

Weekly summary:
- Total funding income
- Total fees paid
- Net profit
- Annualized APY
- Capital deployed
```

### Realistic Return Expectations

Based on our experience running funding farms with ~$200 deployed:

| Market Condition | Funding Rate Range | Expected APY | Duration |
|---|---|---|---|
| Bull market | 0.03-0.10% per 8h | 30-100%+ | Weeks to months |
| Neutral market | 0.005-0.03% per 8h | 5-30% | Months |
| Bear market | -0.02-0.01% per 8h | Negative to 10% | Variable |
| Extreme greed | 0.10%+ per 8h | 100%+ | Days to weeks |

**Average across all conditions:** 15-25% APY is realistic for a well-managed funding farm on ETH/BTC. Higher on altcoins with more risk.

## Common Mistakes and How to Avoid Them

### Mistake 1: Ignoring Fees

Exchange fees (trading fees, funding fees, withdrawal fees) can eat 20-40% of your gross funding income on small positions.

**Solution:** Calculate net yield after all fees before deploying. Use limit orders when possible to pay maker fees instead of taker fees.

### Mistake 2: Not Monitoring Margin

"Set and forget" works until it doesn't. A 30% price pump over a weekend can liquidate your futures short if margin is thin.

**Solution:** Set margin alerts. Keep a buffer. Start with lower leverage.

### Mistake 3: Chasing Altcoin Funding Rates

That 0.5% per 8h funding on DOGE is tempting. But DOGE can move 20% in an hour, the spread is wide, and liquidity can disappear.

**Solution:** Stick to BTC/ETH until you're comfortable with the mechanics. Graduate to alts only after 3+ months of profitable farming.

### Mistake 4: Entering During Peak Funding

If funding is at 0.1% because of a massive rally, it's likely to revert. Entering at the peak means you might experience negative funding soon.

**Solution:** Look for sustained moderate funding (0.02-0.05%) rather than peak funding. Persistent moderate rates are more profitable than brief extreme rates.

### Mistake 5: Forgetting About Taxes

Funding payments are taxable income in most jurisdictions. Track everything.

**Solution:** Export your funding history regularly. Use crypto tax software.

## Automation and Scaling

Once you're comfortable with manual farming, consider:

### Simple Automation

- **Funding rate alerts** via TradingView or exchange notifications
- **Spreadsheet automation** pulling funding data from exchange APIs
- **Margin alerts** via exchange push notifications

### Advanced Automation

- **Automated entry/exit** based on funding rate thresholds
- **Multi-asset rotation** — automatically shift to the highest-funding asset
- **Cross-exchange arbitrage** — farm on the exchange with the best rate

### Scaling Considerations

- **$500-$5K:** Single asset, single exchange, manual management
- **$5K-$50K:** Multi-asset, consider portfolio margin, semi-automated
- **$50K+:** Multi-exchange, fully automated, professional risk management

## What We've Learned Running $200 in Funding Farms

At Nora Institute, we operate a small funding farm as part of our $490 portfolio. Here's what we've learned firsthand:

1. **Consistency beats optimization.** Earning $3-5/day reliably matters more than occasionally catching a 0.2% rate.
2. **The hardest part is patience.** When funding dips, the temptation to close and redeploy is strong. Usually, waiting is correct.
3. **It compounds.** Reinvesting funding income into the farm creates compound growth. Our $200 allocation generates enough to add ~$100/month to the position.
4. **It pairs well with other strategies.** Funding farming provides base income that reduces pressure on more volatile strategies (prediction markets, trading).

## Conclusion

Funding rate farming is:
- **Real yield** from market structure, not token emissions
- **Delta-neutral** when properly constructed
- **Accessible** with as little as $500
- **Scalable** from retail to institutional
- **Educational** — it teaches you market microstructure

**Your first three steps:**

1. **Open an exchange account** (if you don't have one) and deposit $500+
2. **Check current BTC/ETH funding rates** on Coinglass
3. **Execute your first farm** using the entry procedure in Step 4

Start small, track everything, learn the rhythm of funding cycles. Within a month, you'll have a working income stream and a deep understanding of how leveraged markets really work.

---

*Part of the Nora Institute's DeFi Mechanics series. For deeper understanding, read "How Funding Rates Predict Liquidation Risk" and "The Math Behind Negative Funding Rates."*
