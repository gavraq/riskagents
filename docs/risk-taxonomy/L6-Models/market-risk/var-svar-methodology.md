---
# Model Metadata
model_id: MR-L6-001
model_name: Historical Simulation VaR and SVaR Methodology
version: 1.1
effective_date: 2025-01-16
next_review_date: 2026-01-15
owner: Head of Risk Methodology and Analytics (RMA)
approving_committee: Model Risk Committee / MLRC
model_tier: Tier 1 (Regulatory Capital)

# Taxonomy Linkages
parent_framework: MR-L3-003  # VaR Limit Framework
l1_requirements:
  - REQ-L1-001  # CRR (UK)
  - REQ-L1-003  # FRTB
  - REQ-L1-004  # Basel III/IV
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-003   # VaR Limit Framework
l4_processes:
  - MR-L4-001   # Market Risk Process Orchestration
  - MR-L4-006   # Risk Engine Calculation
  - MR-L4-008   # VaR Backtesting
l5_controls:
  - MR-L5-001   # VaR and SVaR Limits Controls
  - MR-L5-004   # Backtesting Controls
  - MR-L5-007   # ECAP Controls (extends VaR for Pillar 2)
related_models:
  - MR-L6-002   # ECAP Methodology (extends this model for economic capital)
l7_systems:
  - SYS-MR-003  # Risk Engine (FMDM)
  - SYS-MR-010  # Time Series ODS
  - SYS-MR-008  # Risk ODS
---

# Historical Simulation VaR and SVaR Methodology

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Model ID** | MR-L6-001 |
| **Version** | 1.1 |
| **Effective Date** | 16 January 2025 |
| **Parent Framework** | VaR Limit Framework (MR-L3-003) |
| **Owner** | Head of Risk Methodology and Analytics (RMA) |
| **Model Tier** | Tier 1 (Regulatory Capital) |

---

## 1. Executive Summary

### 1.1 Purpose

This document defines the methodology for calculating Value at Risk (VaR) and Stressed Value at Risk (SVaR) at Meridian Global Bank. Both metrics are calculated using the **Historical Simulation** approach, which is the bank's approved methodology for:

- Internal risk management and limit monitoring
- IMA (Internal Models Approach) regulatory capital
- Management reporting

### 1.2 VaR and SVaR: Same Model, Different Observation Periods

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  VaR AND SVaR: SAME MODEL, DIFFERENT OBSERVATION PERIODS                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│                        ┌─────────────────────────────────────────┐                      │
│                        │     HISTORICAL SIMULATION MODEL         │                      │
│                        │          (MR-L6-001)                    │                      │
│                        └──────────────────┬──────────────────────┘                      │
│                                           │                                             │
│                    ┌──────────────────────┴──────────────────────┐                      │
│                    │                                             │                      │
│                    ▼                                             ▼                      │
│         ┌─────────────────────┐                       ┌─────────────────────┐           │
│         │        VaR          │                       │       SVaR          │           │
│         │                     │                       │                     │           │
│         │  Observation:       │                       │  Observation:       │           │
│         │  Rolling 500 days   │                       │  Stressed period    │           │
│         │  (recent history)   │                       │  (2008-09 GFC)      │           │
│         │                     │                       │                     │           │
│         │  Purpose:           │                       │  Purpose:           │           │
│         │  Current risk under │                       │  Risk under severe  │           │
│         │  recent market      │                       │  market stress      │           │
│         │  conditions         │                       │  conditions         │           │
│         └─────────────────────┘                       └─────────────────────┘           │
│                                                                                         │
│  KEY PRINCIPLE: A methodology change to the model always affects BOTH VaR and SVaR      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Key Model Parameters

| Parameter | VaR | SVaR |
|-----------|-----|------|
| **Confidence Level** | 99% | 99% |
| **Holding Period (Internal)** | 1-day | 1-day |
| **Holding Period (Regulatory)** | 10-day | 10-day |
| **Observation Window** | Rolling 500 business days | Fixed 250-day stressed period |
| **Observation Period** | Most recent ~2 years | 15-Sep-2008 to 15-Sep-2009 (GFC) |
| **Calculation Method** | Historical Simulation | Historical Simulation |
| **Percentile Selection** | 5th worst out of 500 | 3rd worst out of 250 |

---

## 2. Regulatory Context

### 2.1 Applicable Regulations

| Regulation | Requirement | Compliance |
|------------|-------------|------------|
| **CRR Article 365** | IMA VaR requirements | HS VaR compliant |
| **CRR Article 365(2)** | SVaR calculation | Implemented |
| **Basel III** | VaR/SVaR capital multipliers | Applied in capital calc |
| **PRA SS13/13** | Model governance | Tier 1 model governance |
| **FRTB SA** | Fallback approach | Available if IMA revoked |

### 2.2 IMA Capital Calculation

VaR and SVaR feed into the IMA capital requirement:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        IMA CAPITAL CALCULATION                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Market Risk Capital = max(VaR_t-1, mc × VaR_avg) + max(SVaR_t-1, ms × SVaR_avg) + IRC  │
│                                                                                         │
│  Where:                                                                                 │
│  • VaR_t-1 = Previous day's VaR (10-day, 99%)                                           │
│  • VaR_avg = 60-day average VaR (10-day, 99%)                                           │
│  • mc = VaR multiplier (minimum 3, plus add-on for backtesting exceptions)              │
│  • SVaR_t-1 = Previous day's SVaR (10-day, 99%)                                         │
│  • SVaR_avg = 60-day average SVaR (10-day, 99%)                                         │
│  • ms = SVaR multiplier (minimum 3, plus add-on for backtesting exceptions)             │
│  • IRC = Incremental Risk Charge (credit positions)                                     │
│                                                                                         │
│  BACKTESTING MULTIPLIER SCHEDULE:                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐                    │
│  │  Exceptions (250 days)  │   Zone    │  Plus Factor │  mc / ms   │                    │
│  ├─────────────────────────┼───────────┼──────────────┼────────────┤                    │
│  │  0 - 4                  │   Green   │     0.00     │    3.00    │                    │
│  │  5                      │   Yellow  │     0.40     │    3.40    │                    │
│  │  6                      │   Yellow  │     0.50     │    3.50    │                    │
│  │  7                      │   Yellow  │     0.65     │    3.65    │                    │
│  │  8                      │   Yellow  │     0.75     │    3.75    │                    │
│  │  9                      │   Yellow  │     0.85     │    3.85    │                    │
│  │  10+                    │   Red     │     1.00     │    4.00    │                    │
│  └─────────────────────────┴───────────┴──────────────┴────────────┘                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Model Scope

### 3.1 In-Scope Products and Risk Factors

| Asset Class | Product Types | Risk Factors |
|-------------|---------------|--------------|
| **Interest Rates** | Swaps, Futures, Bonds, Swaptions | IR curves (tenor points), IR vol |
| **FX** | Spot, Forwards, Options | FX spot rates, FX vol |
| **Credit** | Bonds, CDS, TRS | Credit spreads, basis |
| **Equities** | Stocks, Futures, Options | Equity prices, equity vol |
| **Commodities** | Futures, Options | Commodity prices, commodity vol |
| **Inflation** | Inflation swaps, Linkers | Real rates, breakeven inflation |

### 3.2 Risk Factor Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        RISK FACTOR HIERARCHY                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  LEVEL 1: RISK CLASS                                                                    │
│  └── Interest Rates │ FX │ Credit │ Equities │ Commodities                              │
│                                                                                         │
│  LEVEL 2: RISK TYPE                                                                     │
│  ├── Interest Rates                                                                     │
│  │   ├── Yield Curve Risk                                                               │
│  │   ├── Basis Risk (OIS vs IBOR)                                                       │
│  │   └── Volatility Risk (Swaption vol, Cap vol)                                        │
│  ├── FX                                                                                 │
│  │   ├── Spot Rate Risk                                                                 │
│  │   └── FX Volatility Risk                                                             │
│  └── ...                                                                                │
│                                                                                         │
│  LEVEL 3: SPECIFIC RISK FACTOR                                                          │
│  ├── EUR-ESTER-1Y                                                                       │
│  ├── EUR-ESTER-2Y                                                                       │
│  ├── EUR-ESTER-5Y                                                                       │
│  ├── EUR-ESTER-10Y                                                                      │
│  ├── EUR-ESTER-30Y                                                                      │
│  ├── EURUSD-SPOT                                                                        │
│  ├── EURUSD-VOL-1M-ATM                                                                  │
│  └── ...                                                                                │
│                                                                                         │
│  Total Active Risk Factors: ~5,000                                                      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Out of Scope

| Exclusion | Reason | Alternative Treatment |
|-----------|--------|----------------------|
| **Banking book positions** | Not trading book | Separate IRRBB framework |
| **CVA risk** | Separate capital charge | CVA model (MR-L6-004) |
| **Operational risk events** | Non-market risk | Op Risk framework |
| **Liquidity risk** | Separate risk type | LCR/NSFR framework |

---

## 4. Methodology: Historical Simulation

### 4.1 Methodology Selection Rationale

Meridian Global Bank employs **Historical Simulation (HS)** as its primary VaR methodology. This section documents the rationale for selecting HS over alternative approaches.

#### 4.1.1 Alternative Methodologies Considered

| Methodology | Description | Pros | Cons |
|-------------|-------------|------|------|
| **Historical Simulation** | Uses actual historical returns | Distribution-free; captures fat tails; intuitive | Dependent on historical period; data intensive |
| **Parametric (Variance-Covariance)** | Assumes normal distribution | Computationally fast; simple | Fails with non-normal distributions; underestimates tail risk |
| **Monte Carlo Simulation** | Generates scenarios from fitted distributions | Flexible; can model complex dynamics | Model risk in distribution assumptions; computationally expensive |

#### 4.1.2 Justification for Historical Simulation

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        WHY HISTORICAL SIMULATION?                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  1. DISTRIBUTION-FREE APPROACH                                                          │
│     • Makes no assumptions about return distributions                                   │
│     • Captures actual fat tails observed in market data                                 │
│     • Accommodates non-normality (skewness, kurtosis) naturally                         │
│                                                                                         │
│  2. REGULATORY ACCEPTANCE                                                               │
│     • Approved methodology under CRR for IMA                                            │
│     • Well-established validation framework                                             │
│     • Transparent to regulators and auditors                                            │
│                                                                                         │
│  3. CORRELATION CAPTURE                                                                 │
│     • Historical returns implicitly capture contemporaneous correlations                │
│     • Correlation structure changes across market regimes are preserved                 │
│     • No need to estimate or model correlation matrices                                 │
│                                                                                         │
│  4. INTUITIVE INTERPRETATION                                                            │
│     • "What would have happened if history repeated?"                                   │
│     • P&L scenarios traceable to actual market dates                                    │
│     • Easy to explain to stakeholders and front office                                  │
│                                                                                         │
│  5. PRACTICAL CONSIDERATIONS                                                            │
│     • Established infrastructure and operational processes                              │
│     • Well-understood model risk profile                                                │
│     • Consistent approach across industry peers                                         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.1.3 Known Trade-offs

| Trade-off | Mitigation |
|-----------|------------|
| Cannot predict unprecedented events | Complementary stress testing (MR-L5-002) |
| Dependent on historical observation period | 500-day window balances stability and responsiveness |
| Equal weighting of all observations | Accepted; weighted schemes introduce model risk |
| Correlation breakdown in extreme stress | SVaR uses stress period correlations |

### 4.2 Fundamental Concept

Historical Simulation generates potential future portfolio values by applying actual historical market movements to today's portfolio. Unlike parametric VaR, it makes no assumptions about return distributions.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        HISTORICAL SIMULATION CONCEPT                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  PRINCIPLE:                                                                             │
│  "What would today's portfolio have gained or lost if historical market movements       │
│   occurred again?"                                                                      │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  TODAY'S PORTFOLIO              HISTORICAL MARKET MOVEMENTS                             │
│  ──────────────────             ───────────────────────────                             │
│                                                                                         │
│  Position 1: EUR 10Y Swap       Day 1 (15-Jan-2023): EUR 10Y +3bps, EURUSD -0.5%        │
│  Position 2: EUR/USD Forward    Day 2 (16-Jan-2023): EUR 10Y -5bps, EURUSD +0.3%        │
│  Position 3: Corp Bond          Day 3 (17-Jan-2023): EUR 10Y +1bp, EURUSD +0.1%         │
│  ...                            ...                                                     │
│                            →    Day 500: EUR 10Y +8bps, EURUSD -1.2%                    │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  RESULTING P&L DISTRIBUTION                                                             │
│  ─────────────────────────                                                              │
│                                                                                         │
│  Apply each day's returns to today's portfolio:                                         │
│                                                                                         │
│  Scenario 1 P&L = Σ (Sensitivity_i × Return_i for Day 1)  = -$120k                      │
│  Scenario 2 P&L = Σ (Sensitivity_i × Return_i for Day 2)  = +$85k                       │
│  Scenario 3 P&L = Σ (Sensitivity_i × Return_i for Day 3)  = -$15k                       │
│  ...                                                                                    │
│  Scenario 500 P&L = ...                                    = -$280k                     │
│                                                                                         │
│  VaR (99%) = 5th worst P&L out of 500 scenarios                                         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Return Calculation Methodology

#### 4.3.1 Absolute vs Relative Returns

The choice between absolute and relative returns is determined by the nature of each risk factor. This is a fundamental model design decision with significant impact on VaR accuracy.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        ABSOLUTE vs RELATIVE RETURNS                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ABSOLUTE RETURNS: Change = Level(t) - Level(t-1)                                       │
│  Used when: Risk factor can be zero, negative, or near-zero                             │
│  Application: Today's level + historical absolute change                                │
│                                                                                         │
│  RELATIVE RETURNS: Change = ln(Level(t) / Level(t-1))                                   │
│  Used when: Risk factor is always positive and follows multiplicative process           │
│  Application: Today's level × exp(historical log return)                                │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Detailed Risk Factor Classification:**

| Risk Factor Type | Return Type | Formula | Rationale |
|------------------|-------------|---------|-----------|
| **Interest Rates (Nominal)** | Absolute | Δr = r(t) - r(t-1) | Rates can be zero or negative (EUR, CHF, JPY) |
| **Interest Rates (Real)** | Absolute | Δr = r(t) - r(t-1) | Real rates frequently negative |
| **Inflation Breakevens** | Absolute | Δb = b(t) - b(t-1) | Can be near zero |
| **FX Spot Rates** | Relative (Log) | ln(S(t)/S(t-1)) | Positive; multiplicative; prevents negative rates |
| **FX Volatility** | Relative (Log) | ln(σ(t)/σ(t-1)) | Always positive; proportional moves |
| **Equity Prices** | Relative (Log) | ln(P(t)/P(t-1)) | Positive; limited liability |
| **Equity Volatility** | Relative (Log) | ln(σ(t)/σ(t-1)) | Always positive |
| **Credit Spreads** | Absolute | Δcs = cs(t) - cs(t-1) | Can be very tight; allows widening |
| **Basis Spreads** | Absolute | Δbs = bs(t) - bs(t-1) | Can be positive or negative |
| **Commodity Prices** | Relative (Log) | ln(P(t)/P(t-1)) | Positive; prevents negative prices |
| **Commodity Volatility** | Relative (Log) | ln(σ(t)/σ(t-1)) | Always positive |

**Key Principles:**

1. **Consistency**: All tenors within a curve use the same return type
2. **Negative Rate Handling**: Absolute returns essential for currencies with historical/potential negative rates
3. **Basis Spreads**: Always absolute as spreads can flip sign
4. **Volatility**: Always relative as implied volatility is bounded below by zero

#### 4.3.2 Example: Interest Rate Return

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        INTEREST RATE RETURN EXAMPLE                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  RISK FACTOR: EUR-ESTER-10Y                                                             │
│                                                                                         │
│  Historical Observation:                                                                │
│  • Rate on 14-Jan-2024: 2.85%                                                           │
│  • Rate on 15-Jan-2024: 2.88%                                                           │
│  • Absolute Return: +3 basis points                                                     │
│                                                                                         │
│  Application to Today's Portfolio:                                                      │
│  • Today's EUR 10Y rate: 3.50%                                                          │
│  • Shocked rate: 3.50% + 0.03% = 3.53%                                                  │
│                                                                                         │
│  Position Impact:                                                                       │
│  • EUR 10Y Swap, €50M notional, DV01 = -€22,500/bp                                      │
│  • P&L = DV01 × Shock = -€22,500 × 3 = -€67,500                                         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Calculation Approaches

Two approaches are used based on product complexity:

#### 4.3.1 Sensitivity-Based Calculation (Linear Products)

For products with linear or near-linear payoffs:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        SENSITIVITY-BASED CALCULATION                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  P&L(scenario d) ≈ Σ [Sensitivity_i × Shock_i(d)]                                       │
│                   i=1 to n                                                              │
│                                                                                         │
│  Where:                                                                                 │
│  • Sensitivity_i = Position sensitivity to risk factor i (DV01, CS01, Delta, etc.)      │
│  • Shock_i(d) = Historical return of risk factor i on scenario date d                   │
│  • n = Number of risk factors affecting the position                                    │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  EXAMPLE: Corporate Bond Position                                                       │
│                                                                                         │
│  Sensitivities:                                                                         │
│  • DV01 (USD 10Y): -$50,000/bp                                                          │
│  • CS01 (Credit): -$20,000/bp                                                           │
│                                                                                         │
│  Scenario d = 15-Sep-2008 (Lehman):                                                     │
│  • USD 10Y rate: -25 bps (flight to quality)                                            │
│  • Credit spread: +150 bps (credit crisis)                                              │
│                                                                                         │
│  P&L = (-$50,000 × -25) + (-$20,000 × 150)                                              │
│      = +$1,250,000 + (-$3,000,000)                                                      │
│      = -$1,750,000                                                                      │
│                                                                                         │
│  USED FOR: Bonds, Swaps (vanilla), FX forwards, Linear derivatives                      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.3.2 Full Revaluation (Non-Linear Products)

For products with non-linear payoffs:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        FULL REVALUATION CALCULATION                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  For each scenario d:                                                                   │
│                                                                                         │
│  1. Get today's market prices: P_today = {S, σ, r, ...}                                 │
│  2. Get historical returns from date d: R_d = {ΔS/S, Δσ, Δr, ...}                       │
│  3. Apply shocks: P_shocked = P_today × (1 + R_d)   [or P_today + R_d for absolute]     │
│  4. Revalue position: MTM_shocked = Pricing_Model(Position, P_shocked)                  │
│  5. Calculate P&L: P&L(d) = MTM_shocked - MTM_today                                     │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  EXAMPLE: EUR/USD Call Option                                                           │
│                                                                                         │
│  Option: EUR/USD Call, Strike 1.10, 3M expiry, €10M notional                            │
│                                                                                         │
│  Today's Market:                                                                        │
│  • EUR/USD Spot: 1.0850                                                                 │
│  • 3M Vol: 8.5%                                                                         │
│  • MTM_today: $125,000                                                                  │
│                                                                                         │
│  Scenario d = 20-Mar-2020 (COVID):                                                      │
│  • EUR/USD return: -3.5%                                                                │
│  • Vol return: +120%                                                                    │
│                                                                                         │
│  Shocked Market:                                                                        │
│  • EUR/USD Spot: 1.0850 × (1 - 0.035) = 1.0470                                          │
│  • 3M Vol: 8.5% × (1 + 1.20) = 18.7%                                                    │
│                                                                                         │
│  Full Revaluation:                                                                      │
│  • MTM_shocked = Black-Scholes(Option, 1.0470, 18.7%, ...) = $89,000                    │
│  • P&L = $89,000 - $125,000 = -$36,000                                                  │
│                                                                                         │
│  Note: Sensitivity-based would miss the convexity effects                               │
│                                                                                         │
│  USED FOR: Options, Swaptions, Structured products, Exotics                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.3.3 Product Classification Matrix

| Product Type | Calculation Method | Rationale |
|--------------|-------------------|-----------|
| Cash bonds | Sensitivity-based | Near-linear; DV01 + CS01 sufficient |
| Vanilla swaps | Sensitivity-based | Linear payoff; DV01 sufficient |
| FX spot/forwards | Sensitivity-based | Linear; Delta sufficient |
| FX options | Full revaluation | Significant gamma/vega |
| IR swaptions | Full revaluation | Vega-dominant risk |
| Equity options | Full revaluation | Gamma/vega significant |
| CDS | Sensitivity-based | Linear in spread; CS01 sufficient |
| Exotic derivatives | Full revaluation | Path-dependent features |
| Structured products | Full revaluation | Complex payoffs |

### 4.5 Data Floor Methodology

To prevent unrealistic shocked values (particularly for interest rates), market data floors are applied during scenario generation.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        DATA FLOOR METHODOLOGY                                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  PURPOSE:                                                                               │
│  Prevent historically large absolute moves from creating implausible shocked rates      │
│  when applied to current (potentially already low) rate environments.                   │
│                                                                                         │
│  EXAMPLE PROBLEM:                                                                       │
│  • Current EUR 5Y rate: 2.80%                                                           │
│  • Historical absolute move (2008): -150 bps                                            │
│  • Naive shocked rate: 2.80% - 1.50% = 1.30% ✓ (acceptable)                             │
│                                                                                         │
│  But:                                                                                   │
│  • Current EUR 5Y rate: 0.50%                                                           │
│  • Historical absolute move (2008): -150 bps                                            │
│  • Naive shocked rate: 0.50% - 1.50% = -1.00% ✗ (implausible for most markets)          │
│                                                                                         │
│  SOLUTION: Apply currency-specific floors                                               │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.5.1 Currency-Specific Rate Floors

| Currency | Floor Rate | Rationale |
|----------|------------|-----------|
| **EUR** | -0.75% | ECB deposit facility historical floor |
| **CHF** | -1.00% | SNB historical negative rate floor |
| **JPY** | -0.50% | BOJ negative rate policy |
| **GBP** | 0.00% | BoE has not implemented negative rates |
| **USD** | 0.00% | Fed has not implemented negative rates |
| **AUD, CAD, NZD** | 0.00% | No negative rate history |
| **CNY/CNH** | -2.00% | Conservative floor given capital controls |
| **EM Currencies** | 0.00% | Generally positive rate environments |

#### 4.5.2 Floor Application Logic

```
Shocked_Rate = max(Floor_Rate, Current_Rate + Historical_Shift)
```

**Example with Floor:**
- Current EUR 5Y rate: 0.50%
- Historical shift: -150 bps
- EUR floor: -0.75%
- Shocked rate = max(-0.75%, 0.50% - 1.50%) = max(-0.75%, -1.00%) = **-0.75%**

#### 4.5.3 Floor Governance

| Action | Frequency | Authority |
|--------|-----------|-----------|
| Review floor levels | Annual | RMA |
| Temporary floor adjustment | As needed | RMA Head + CRO |
| Add new currency floor | As needed | MLRC |
| Remove floor | Material change | Model Risk Committee |

**Documentation Requirement**: Any floor activation must be logged, including the scenario date, risk factor, pre-floor and post-floor values.

---

## 5. VaR Calculation: Detailed Steps

### 5.1 Three-Step Calculation Chain

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        VaR CALCULATION CHAIN                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  STEP 1: P&L STRIP CALCULATION                                                          │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  For each position × each scenario date (500):                                          │
│  → Calculate hypothetical P&L                                                           │
│  → Output: Matrix of position-level P&L strips                                          │
│                                                                                         │
│             │ Scenario 1 │ Scenario 2 │ ... │ Scenario 500 │                            │
│  Position 1 │   -$50k    │   +$125k   │ ... │    +$75k     │                            │
│  Position 2 │   +$10k    │   -$15k    │ ... │    -$40k     │                            │
│  ...        │    ...     │    ...     │ ... │     ...      │                            │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  STEP 2: HIERARCHY AGGREGATION                                                          │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  For each hierarchy level × each scenario date:                                         │
│  → Sum P&L strips of all positions within node                                          │
│  → Output: Aggregated P&L distribution at each hierarchy level                          │
│                                                                                         │
│  Position → Book → Desk → Business Unit → Division → Entity                             │
│                                                                                         │
│  Diversification benefit captured naturally through aggregation                         │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  STEP 3: PERCENTILE CALCULATION                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  For each hierarchy node:                                                               │
│  1. Sort aggregated P&L: [-$800k, -$750k, -$680k, ..., +$600k]                          │
│  2. Find 99th percentile loss (1% tail)                                                 │
│     → With 500 observations: 5th worst value                                            │
│  3. VaR (99%, 1-day) = |5th worst observation|                                          │
│                                                                                         │
│  Example:                                                                               │
│  Sorted P&L: [-$800k, -$750k, -$680k, -$620k, -$580k, ...]                              │
│  5th worst = -$580k                                                                     │
│  VaR (99%, 1-day) = $580k                                                               │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Percentile Calculation Details

#### 5.2.1 Percentile Selection for Different Sample Sizes

| Sample Size | 99th Percentile Position | Formula |
|-------------|-------------------------|---------|
| 250 days (SVaR) | 3rd worst | ceil(250 × 0.01) = 3 |
| 500 days (VaR) | 5th worst | ceil(500 × 0.01) = 5 |
| 1000 days | 10th worst | ceil(1000 × 0.01) = 10 |

#### 5.2.2 Averaging Method for Percentile Stability

For improved stability and reduced sensitivity to single observations, Meridian Global Bank uses an **averaging approach** for percentile calculation:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        PERCENTILE AVERAGING METHOD                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  For 250 observations (SVaR):                                                           │
│  99th Percentile = Average of 2nd and 3rd worst observations                            │
│                  = (P&L_rank2 + P&L_rank3) / 2                                          │
│                                                                                         │
│  For 500 observations (VaR):                                                            │
│  99th Percentile = Average of 5th and 6th worst observations                            │
│                  = (P&L_rank5 + P&L_rank6) / 2                                          │
│                                                                                         │
│  RATIONALE:                                                                             │
│  • Reduces VaR sensitivity to individual extreme scenarios                              │
│  • Provides smoother day-to-day VaR progression                                         │
│  • Reduces noise in backtesting results                                                 │
│  • Consistent with industry practice                                                    │
│                                                                                         │
│  EXAMPLE (250 observations):                                                            │
│  Sorted losses: [-$1.2M, -$980k, -$920k, -$850k, ...]                                   │
│  99th percentile = (-$980k + -$920k) / 2 = -$950k                                       │
│  VaR (99%) = $950k                                                                      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 5.2.3 Interpolation Method

For cases where exact percentile positions result in non-integer values, linear interpolation is used:

```
If 99th percentile position = 5.0 (integer):
  VaR = |P&L at position 5|

If 99th percentile position = 4.75 (non-integer):
  VaR = 0.75 × |P&L at position 5| + 0.25 × |P&L at position 4|
```

### 5.3 10-Day VaR Calculation

Two methods are available for converting 1-day VaR to 10-day horizon:

#### 5.3.1 Square Root of Time Scaling (Regulatory Default)

```
VaR(10-day) = VaR(1-day) × √10 ≈ VaR(1-day) × 3.162
```

**Assumptions**:
- Returns are independently and identically distributed (i.i.d.)
- Volatility scales with square root of time

**Limitations**:
- Overstates risk if returns exhibit mean reversion
- Understates risk if returns exhibit autocorrelation

#### 5.3.2 Actual 10-Day Returns (Internal Risk Management)

Uses overlapping 10-day returns from historical time series:

```
Return_10day(t) = Price(t) / Price(t-10) - 1
```

**Advantages**:
- Captures actual return dynamics (autocorrelation, mean reversion)
- More accurate for assets with non-standard distributions

**Meridian Global Bank Approach**:

| Purpose | Method |
|---------|--------|
| Regulatory IMA capital | √10 scaling |
| Internal risk management | Actual 10-day returns |
| Limit monitoring | Actual 10-day returns |

### 5.4 Autocorrelation Study: Overlapping 10-Day Returns

The use of overlapping 10-day returns requires careful consideration of the statistical properties introduced by overlap.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        OVERLAPPING RETURN AUTOCORRELATION                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ISSUE:                                                                                 │
│  Overlapping 10-day returns share 9 out of 10 days with adjacent observations,          │
│  creating significant positive autocorrelation.                                         │
│                                                                                         │
│  Day 1:   [---------- 10 day return ----------]                                         │
│  Day 2:     [---------- 10 day return ----------]                                       │
│  Day 3:       [---------- 10 day return ----------]                                     │
│                                                                                         │
│  Adjacent returns share 9 days → Autocorrelation ≈ 0.81 for iid returns                 │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  MERIDIAN GLOBAL BANK ANALYSIS (conducted annually):                                    │
│                                                                                         │
│  Study Period: 2014-2024 (10 years)                                                     │
│                                                                                         │
│  Key Risk Factors Tested:                                                               │
│  ┌────────────────────────┬─────────────────────┬─────────────────────┐                 │
│  │ Risk Factor            │ Expected AC (iid)   │ Observed AC         │                 │
│  ├────────────────────────┼─────────────────────┼─────────────────────┤                 │
│  │ EUR 10Y Swap           │ 0.81                │ 0.78 - 0.85         │                 │
│  │ EURUSD Spot            │ 0.81                │ 0.79 - 0.84         │                 │
│  │ S&P 500                │ 0.81                │ 0.75 - 0.82         │                 │
│  │ EUR IG Credit Spreads  │ 0.81                │ 0.83 - 0.89         │                 │
│  └────────────────────────┴─────────────────────┴─────────────────────┘                 │
│                                                                                         │
│  CONCLUSION:                                                                            │
│  Observed autocorrelation is consistent with mechanical overlap effect.                 │
│  Credit spreads show slightly higher autocorrelation (momentum/trending behavior).      │
│  No adjustment required as overlap effect is expected and acceptable for VaR purposes.  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 5.4.1 Implications for VaR

| Consideration | Impact | Mitigation |
|---------------|--------|------------|
| Effective sample size | Reduced from 500 to ~50 independent observations | Accepted; provides parameter stability |
| P&L persistence | Large losses persist across adjacent scenarios | Natural behavior; reflects real liquidation periods |
| Statistical testing | Standard tests require adjustment | Use overlap-adjusted confidence intervals |
| Backtesting | Adjacent exceptions expected | Cluster-adjusted exception counting |

#### 5.4.2 Annual Validation

The autocorrelation study is updated annually as part of model validation. Key metrics:

- Ljung-Box test for residual autocorrelation
- Comparison of √10 scaling vs actual 10-day VaR
- Analysis of VaR prediction accuracy by horizon

---

## 6. SVaR: Stressed Value at Risk

### 6.1 Methodology

SVaR uses the identical Historical Simulation methodology as VaR, but applies returns from a **stressed market period** rather than recent history.

### 6.2 Stressed Period Selection

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        STRESSED PERIOD SELECTION                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  REGULATORY REQUIREMENT (CRR Article 365(2)):                                           │
│  The stressed period must represent a period of significant financial stress relevant   │
│  to the firm's portfolio. It should be a continuous 12-month (250 business day) period  │
│  that would produce maximum VaR for the current portfolio.                              │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  SELECTION METHODOLOGY:                                                                 │
│                                                                                         │
│  1. CANDIDATE PERIODS                                                                   │
│     Evaluate stressed periods relevant to current portfolio composition:                │
│     • Global Financial Crisis: Sep-2008 to Sep-2009                                     │
│     • European Sovereign Crisis: Jul-2011 to Jul-2012                                   │
│     • Taper Tantrum: May-2013 to May-2014                                               │
│     • COVID-19 Crisis: Mar-2020 to Mar-2021                                             │
│     • Rate Shock: Mar-2022 to Mar-2023                                                  │
│                                                                                         │
│  2. PORTFOLIO-SPECIFIC ASSESSMENT                                                       │
│     For each candidate period:                                                          │
│     • Calculate VaR using that period's returns                                         │
│     • Document stress relevance to current portfolio                                    │
│                                                                                         │
│  3. SELECTION CRITERIA                                                                  │
│     Select period that produces highest VaR for current portfolio                       │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  CURRENT STRESSED PERIOD:                                                               │
│                                                                                         │
│  Period: 15-Sep-2008 to 15-Sep-2009 (Global Financial Crisis)                           │
│                                                                                         │
│  Rationale:                                                                             │
│  • Extreme interest rate volatility (flight to quality)                                 │
│  • Credit spread widening (250bps+ on IG corporates)                                    │
│  • FX volatility spike                                                                  │
│  • Most severe stress for current rates/credit-dominated portfolio                      │
│                                                                                         │
│  Last Review: January 2025                                                              │
│  Next Review: April 2025 (quarterly)                                                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Stressed Period Review Process

| Trigger | Action | Authority |
|---------|--------|-----------|
| Quarterly review | Re-assess candidate periods | RMA |
| Significant portfolio change (>20% VaR impact) | Re-assess stressed period | RMA |
| Backtesting exception on SVaR | Investigate period appropriateness | RMA + MLRC |
| New stress event in markets | Evaluate as candidate | RMA |

### 6.4 SVaR/VaR Ratio Monitoring

The ratio of SVaR to VaR provides insight into portfolio stress sensitivity:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        SVaR/VaR RATIO INTERPRETATION                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  EXPECTED RANGE: 1.5x - 2.5x                                                            │
│                                                                                         │
│  LOW RATIO (<1.2x):                                                                     │
│  • Current market more stressed than "stressed" period                                  │
│  • May indicate stressed period no longer appropriate                                   │
│  • Action: Review stressed period selection                                             │
│                                                                                         │
│  HIGH RATIO (>3.0x):                                                                    │
│  • Large gap between current and stressed risk                                          │
│  • Portfolio may be highly sensitive to stress scenarios                                │
│  • Action: Investigate portfolio composition and risk concentration                     │
│                                                                                         │
│  MONITORING: Daily at entity level; weekly at division level                            │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Time Series Requirements

### 7.1 Observation Window

| Metric | Required History | Rationale |
|--------|-----------------|-----------|
| **VaR** | 500 business days (~2 years) | CRR minimum requirement |
| **SVaR** | 250 business days (stressed period) | CRR requirement |
| **Archive** | 5 years minimum | Backtesting analysis |

### 7.2 Data Quality Standards

| Requirement | Standard | Control |
|-------------|----------|---------|
| Completeness | 100% of days populated | Daily validation |
| Consistency | Same observation time daily | EOD snapshot |
| Accuracy | Reconciled to source | Weekly reconciliation |
| Proxying | <5% of risk factors proxied | Proxy governance |

### 7.3 Missing Data Treatment

See [Proxying Process (MR-L4-005f)](../../L4-Processes/processes/time-series-management/proxying-process.md) for detailed proxy methodology, including:
- Proxy Level Classification (Levels 1-4)
- Seven approved proxy functions (RFVB, NAR, LinIntrp, FECS, FEBS, Generic, CF)
- Approval workflow and governance
- History splicing and level adjustment techniques

| Gap Type | Treatment | Authority |
|----------|-----------|-----------|
| Single day gap | Linear interpolation | Automated |
| 2-5 day gap | Proxy from correlated series | RAV approval |
| >5 day gap | Synthetic proxy | RMA approval |
| New risk factor | Historical reconstruction | RMA approval + MLRC |

### 7.4 RNIV Framework (Risks Not in VaR)

Not all risk factors are adequately captured in the VaR model. The RNIV framework identifies, quantifies, and capitalizes these residual risks.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        RNIV FRAMEWORK                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  DEFINITION:                                                                            │
│  Risk Not in VaR (RNIV) refers to any market risk exposure where the VaR model does     │
│  not adequately capture the risk due to:                                                │
│  • Missing risk factors                                                                 │
│  • Insufficient time series history                                                     │
│  • Model limitations (e.g., linearization for non-linear products)                      │
│  • Data quality issues                                                                  │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  RNIV CATEGORIES:                                                                       │
│                                                                                         │
│  1. MISSING RISK FACTORS                                                                │
│     • Risk factors not in time series ODS                                               │
│     • Proxied risk factors with weak correlation                                        │
│     • New products pending risk factor mapping                                          │
│                                                                                         │
│  2. DATA LIMITATIONS                                                                    │
│     • Insufficient history (<500 days)                                                  │
│     • Stale or illiquid data sources                                                    │
│     • Time series with gaps >10%                                                        │
│                                                                                         │
│  3. MODEL LIMITATIONS                                                                   │
│     • Taylor series approximation for options (gamma/vega truncation)                   │
│     • Basis risks not explicitly modeled                                                │
│     • Cross-asset correlations not captured                                             │
│                                                                                         │
│  4. OPERATIONAL GAPS                                                                    │
│     • Intraday risk not captured by EOD VaR                                             │
│     • Event risk between calculation and reporting                                      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 7.4.1 RNIV Identification Process

| Step | Action | Frequency | Owner |
|------|--------|-----------|-------|
| 1 | New product risk factor review | Per new product | Risk Architecture |
| 2 | Proxy correlation analysis | Monthly | RAV |
| 3 | Time series completeness review | Daily | Risk Engine Ops |
| 4 | Model limitation assessment | Quarterly | RMA |
| 5 | RNIV inventory update | Quarterly | RMA |

#### 7.4.2 RNIV Capitalization

RNIV items are capitalized through one of the following methods:

| Method | Application | Calculation |
|--------|-------------|-------------|
| **Stress Scenario** | Missing risk factors | Apply worst historical stress |
| **Conservative Proxy** | Weak correlation | Apply volatility premium to proxy |
| **Standalone Add-on** | Model limitations | Calculated separately, added to VaR |
| **Qualitative Buffer** | Operational gaps | Management judgment overlay |

#### 7.4.3 RNIV Governance

| Item | Requirement |
|------|-------------|
| **RNIV Inventory** | Maintained by RMA; reviewed quarterly by MLRC |
| **Materiality Threshold** | RNIV item >$1M capital impact requires formal documentation |
| **Remediation Plan** | Each RNIV item must have documented remediation plan and timeline |
| **Regulatory Disclosure** | Material RNIV items disclosed in IMA application documentation |

### 7.5 Proxy Governance Framework

When a risk factor lacks sufficient historical data, a proxy risk factor may be used. This section documents the governance framework for proxy approvals.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        PROXY GOVERNANCE FRAMEWORK                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  PROXY TYPES:                                                                           │
│                                                                                         │
│  1. EXACT PROXY                                                                         │
│     • Same risk factor, different source                                                │
│     • Example: EUR 5Y swap rate from Bloomberg vs Reuters                               │
│     • Approval: Automated                                                               │
│                                                                                         │
│  2. CORRELATED PROXY                                                                    │
│     • Different risk factor with high correlation (>0.85)                               │
│     • Example: 9Y swap proxied by average of 7Y and 10Y                                 │
│     • Approval: RAV                                                                     │
│                                                                                         │
│  3. SECTOR PROXY                                                                        │
│     • Sector/region index used for specific issuer                                      │
│     • Example: Single name CDS proxied by iTraxx sector                                 │
│     • Approval: RMA                                                                     │
│                                                                                         │
│  4. SYNTHETIC PROXY                                                                     │
│     • Constructed time series from multiple sources                                     │
│     • Example: New EM currency proxied by basket of similar EM FX                       │
│     • Approval: RMA + MLRC (if material)                                                │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 7.5.1 Proxy Approval Matrix

| Proxy Type | Correlation Required | Maximum Duration | Approving Authority |
|------------|---------------------|------------------|---------------------|
| Exact | N/A | Unlimited | Automated |
| Correlated | ≥0.85 | 6 months | RAV |
| Sector | ≥0.70 | 3 months | RMA |
| Synthetic | Documented | 1 month (renewable) | RMA + MLRC |

#### 7.5.2 Proxy Documentation Requirements

Each proxy must be documented with:
- Target risk factor and proxy risk factor identification
- Correlation analysis (minimum 250-day sample)
- Volatility comparison
- Basis risk assessment
- Remediation plan to eliminate proxy
- RNIV charge calculation (if correlation <0.85)

#### 7.5.3 Proxy Monitoring

| Metric | Threshold | Action |
|--------|-----------|--------|
| Proxy count | <5% of total risk factors | Report to MLRC if exceeded |
| Proxy correlation drift | Falls below approval threshold | Escalate to RMA for re-approval |
| Proxy duration | Exceeds approved duration | Automatic escalation |
| VaR contribution from proxied factors | >10% of total VaR | Remediation plan required |

---

## 8. Model Limitations

### 8.1 Known Limitations

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        MODEL LIMITATIONS                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  1. HISTORICAL DEPENDENCE                                                               │
│     Limitation: VaR cannot predict losses from scenarios not observed in history        │
│     Mitigation: Complementary stress testing (MR-L5-002); scenario analysis             │
│                                                                                         │
│  2. PROCYCLICALITY                                                                      │
│     Limitation: VaR decreases during calm periods, increases after volatility events    │
│     Mitigation: SVaR provides floor based on stressed period; qualitative buffer        │
│                                                                                         │
│  3. LIQUIDITY ASSUMPTION                                                                │
│     Limitation: Assumes positions can be liquidated at observed prices                  │
│     Mitigation: Concentration limits (MR-L5-005); liquidity-adjusted holding periods    │
│                                                                                         │
│  4. TAIL RISK UNDERESTIMATION                                                           │
│     Limitation: 99% VaR ignores worst 1% of outcomes                                    │
│     Mitigation: Expected Shortfall analysis; stress testing                             │
│                                                                                         │
│  5. STATIC PORTFOLIO ASSUMPTION                                                         │
│     Limitation: Assumes portfolio unchanged during holding period                       │
│     Mitigation: Daily recalculation; 1-day holding period for internal use              │
│                                                                                         │
│  6. CORRELATION BREAKDOWN                                                               │
│     Limitation: Historical correlations may not hold during stress                      │
│     Mitigation: SVaR captures stress correlations; scenario stress testing              │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Complementary Risk Measures

VaR/SVaR limitations are addressed through complementary measures:

| Limitation | Complementary Measure | Reference |
|------------|----------------------|-----------|
| Historical dependence | Scenario stress testing | MR-L5-002 |
| Tail risk | Expected Shortfall (internal) | Future enhancement |
| Concentration | Concentration limits | MR-L5-005 |
| Liquidity | Stop-loss limits | MR-L5-006 |
| Model accuracy | Backtesting | MR-L5-004 |

---

## 9. Model Validation

### 9.1 Validation Framework

| Validation Type | Frequency | Responsibility |
|-----------------|-----------|----------------|
| **Backtesting** | Daily | RAV |
| **Methodology review** | Annual | Model Risk |
| **Independent validation** | Annual | Model Risk |
| **Parameter review** | Quarterly | RMA |
| **Benchmark comparison** | Semi-annual | RMA |

### 9.2 Backtesting

Backtesting compares VaR predictions against actual P&L outcomes:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        BACKTESTING FRAMEWORK                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  PRINCIPLE:                                                                             │
│  If VaR is accurate, actual losses should exceed VaR only 1% of the time                │
│  For 250 trading days: expect 2.5 exceptions on average                                 │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  EXCEPTION IDENTIFICATION:                                                              │
│  If |Actual P&L| > VaR(99%)  →  Exception recorded                                      │
│                                                                                         │
│  P&L TYPES USED:                                                                        │
│  • Hypothetical P&L: Same positions valued at T and T-1 prices (preferred)              │
│  • Actual P&L: With intraday trading effect                                             │
│                                                                                         │
│  BASEL TRAFFIC LIGHT:                                                                   │
│  ┌──────────────────────────────────────────────────────────────────┐                   │
│  │  Exceptions (250 days)  │   Zone    │  Regulatory Consequence    │                   │
│  ├─────────────────────────┼───────────┼────────────────────────────┤                   │
│  │  0 - 4                  │   Green   │  Model performing well     │                   │
│  │  5 - 9                  │   Yellow  │  Model under review        │                   │
│  │  10+                    │   Red     │  Model potentially flawed  │                   │
│  └─────────────────────────┴───────────┴────────────────────────────┘                   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

See [Backtesting Controls (MR-L5-004)](../../L5-Controls/market-risk/backtesting-controls.md) for detailed control procedures.

### 9.3 Key Performance Indicators

| KPI | Target | Threshold | Escalation |
|-----|--------|-----------|------------|
| Backtesting exceptions (rolling 250d) | <5 | <10 | MLRC |
| Model stability (VaR change vs portfolio change) | <20% unexplained | <30% | RMA |
| SVaR/VaR ratio | 1.5x - 2.5x | 1.2x - 3.0x | RMA |
| Coverage ratio | 98-100% | 95-105% | MLRC |

---

## 10. Model Change Governance

### 10.1 Change Categories

| Category | Examples | Approval Authority |
|----------|----------|-------------------|
| **Material** | Calculation methodology; confidence level; observation window | Model Risk Committee + MLRC + PRA notification |
| **Significant** | Stressed period selection; new product coverage | MLRC |
| **Minor** | Risk factor mapping; proxy methodology | RMA Head |
| **Calibration** | Parameter updates within approved ranges | RMA |

### 10.2 Parallel Run Requirement

For material and significant changes:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        PARALLEL RUN REQUIREMENTS                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  REQUIREMENT:                                                                           │
│  Run both old and new methodologies in parallel before cutover                          │
│                                                                                         │
│  MINIMUM DURATION:                                                                      │
│  • Material changes: 15 business days minimum                                           │
│  • Significant changes: 5 business days minimum                                         │
│                                                                                         │
│  ANALYSIS REQUIREMENTS:                                                                 │
│  • Compare VaR/SVaR under both methodologies                                            │
│  • Assess impact on capital                                                             │
│  • Backtest both methodologies                                                          │
│  • Document differences and rationale                                                   │
│                                                                                         │
│  APPROVAL:                                                                              │
│  • Parallel run results reviewed by RMA                                                 │
│  • Sign-off by Model Risk                                                               │
│  • MLRC approval for cutover                                                            │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. System Implementation

### 11.1 System Architecture

| System | Role | Reference |
|--------|------|-----------|
| **Risk Engine (FMDM)** | VaR/SVaR calculation engine | SYS-MR-003 |
| **Time Series ODS** | Historical data storage | SYS-MR-010 |
| **Valuations ODS** | Position valuations and sensitivities | SYS-MR-007 |
| **Hierarchy ODS** | Book structure | SYS-MR-011 |
| **Risk ODS** | VaR output storage | SYS-MR-008 |

### 11.2 Calculation Schedule

| Step | Start Time | Duration | SLA |
|------|------------|----------|-----|
| Input validation | 22:00 GMT | 15 min | 22:15 GMT |
| P&L strip calculation | 22:15 GMT | 2h 45m | 01:00 GMT+1 |
| Hierarchy aggregation | 01:00 GMT+1 | 1h 30m | 02:30 GMT+1 |
| Percentile calculation | 02:30 GMT+1 | 1h | 03:30 GMT+1 |
| Output validation | 03:30 GMT+1 | 30 min | **04:00 GMT+1** |

---

## 12. Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| **RMA (Owner)** | Methodology ownership; model documentation; parameter review |
| **Model Risk** | Independent validation; model approval; ongoing monitoring |
| **RAV** | Daily calculation oversight; backtesting; exception investigation |
| **Risk Engine Ops** | System operation; batch execution; technical issues |
| **MLRC** | Governance oversight; approval of significant changes |
| **Model Risk Committee** | Approval of material changes; model tier classification |

---

## 13. Related Documents

| Document | Relationship |
|----------|--------------|
| [VaR Limit Framework](../../L3-Governance/policies/var-limit-framework.md) | Governance framework |
| [VaR and SVaR Limits Controls](../../L5-Controls/market-risk/var-limits-controls.md) | L5 Controls |
| [Market Risk Process Orchestration](../../L4-Processes/processes/market-risk-process-orchestration.md) | Orchestration process |
| [Risk Engine Calculation](../../L4-Processes/processes/risk-engine-calculation.md) | Calculation process |
| [Backtesting Controls](../../L5-Controls/market-risk/backtesting-controls.md) | Model validation |
| [Time Series Management](../../L4-Processes/processes/time-series-management/time-series-overview.md) | Data management |
| [Proxying Process](../../L4-Processes/processes/time-series-management/proxying-process.md) | Proxy functions, approval, governance |
| [Scenario Stress Limits Controls](../../L5-Controls/market-risk/stress-limits-controls.md) | Complementary risk measure |

---

## 14. Document Control

### 14.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | Model Risk Committee / MLRC |
| 1.1 | 2025-01-16 | Enhanced methodology documentation: Added methodology selection rationale (Section 4.1), detailed absolute vs relative shift specifications (Section 4.3.1), data floor methodology (Section 4.5), percentile averaging method (Section 5.2.2), autocorrelation study (Section 5.4), RNIV framework (Section 7.4), and proxy governance framework (Section 7.5) | RMA |

### 14.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full methodology review | Annual | January 2026 |
| Parameter review | Quarterly | April 2025 |
| Stressed period review | Quarterly | April 2025 |
| Independent validation | Annual | January 2026 |

### 14.3 Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Head of RMA | [Name] | | |
| Head of Model Risk | [Name] | | |
| CRO | [Name] | | |
| MLRC Chair | [Name] | | |

---

*End of Document*
