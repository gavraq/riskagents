---
# Process Metadata
process_id: MR-L4-008
process_name: VaR Backtesting
version: 1.1
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Reporting, Analysis & Validation (RAV)
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-001  # Market Risk Process Orchestration
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-003  # FRTB
  - REQ-L1-004  # Basel III/IV
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
l4_processes:
  - MR-L4-006   # Risk Engine Calculation (provides VaR)
  - MR-L4-007   # Market Risk Reporting and Sign-off (consumes backtest results)
l5_controls:
  - MR-L5-004   # Backtesting Exception Limits
l6_models:
  - MR-L6-001   # Historical Simulation VaR
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-012  # P&L ODS
---

# VaR Backtesting Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-008 |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Market Risk Process Orchestration (MR-L4-001) |
| **Owner** | Head of Reporting, Analysis & Validation (RAV) |

---

## 1. Purpose

The Backtesting process validates VaR model accuracy by comparing predicted risk measures to actual/hypothetical P&L outcomes. This process:

- **Monitors model performance** against regulatory standards (Basel traffic light system)
- **Identifies model deficiencies** that require remediation
- **Supports regulatory capital determination** (IMA multiplier)
- **Distinguishes genuine exceptions** from price source noise

Backtesting is a critical component of the Internal Models Approach (IMA) and directly impacts regulatory capital requirements.

---

## 2. Scope

### 2.1 Metrics Subject to Backtesting

| Metric | Confidence Level | Holding Period | Regulatory Requirement |
|--------|-----------------|----------------|------------------------|
| **VaR** | 99% | 1-day | CRR Article 366 |
| **SVaR** | 99% | 1-day | CRR Article 365 |
| **ES (FRTB)** | 97.5% | Varies by liquidity horizon | FRTB (future) |

### 2.2 P&L Measures Used

| P&L Type | Definition | Primary Use |
|----------|------------|-------------|
| **Hypothetical P&L** ("Clean") | P&L from market moves only, on static T-1 EOD positions | Primary regulatory backtest |
| **Actual P&L** ("Dirty") | Total P&L including new trades, fees, reserve changes | Supplementary backtest |

### 2.3 Backtesting Levels

| Level | Scope | Reporting |
|-------|-------|-----------|
| **Entity** | Legal entity (e.g., Meridian Bank UK) | Regulatory reporting |
| **Division** | Global Markets, Treasury | MLRC pack |
| **Desk** | Individual trading desks | Internal monitoring |

---

## 3. Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     VaR BACKTESTING PROCESS FLOW                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │                         INPUTS (Daily - T+1 Morning)                                 │
    │                                                                                      │
    │  From Risk Engine (MR-L4-006):          From P&L ODS:                                │
    │  • VaR (T-1, 99%, 1-day)                • Hypothetical P&L (T-1)                     │
    │  • SVaR (T-1, 99%, 1-day)               • Actual P&L (T-1)                           │
    │                                                                                      │
    │  From Regional EOD (MR-L4-004):         From Price Source Monitoring:                │
    │  • Regional vs. Global P&L differences  • Internal price source differences          │
    └───────────────────────────────────────────────────────────────────────────┬──────────┘
                                                                                │
                                                                                ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │                         1. DAILY BACKTEST CALCULATION                                │
    │                                                                                      │
    │  For each backtesting level (Entity, Division, Desk):                                │
    │                                                                                      │
    │  IF |Hypothetical P&L (T-1)| > VaR (T-1) THEN                                        │
    │      Exception = TRUE (Hypothetical)                                                 │
    │                                                                                      │
    │  IF |Actual P&L (T-1)| > VaR (T-1) THEN                                              │
    │      Exception = TRUE (Actual)                                                       │
    │                                                                                      │
    │  Update rolling 250-day exception count                                              │
    └───────────────────────────────────────────┬──────────────────────────────────────────┘
                                                │
                            ┌───────────────────┴───────────────────┐
                            │                                       │
                            ▼                                       ▼
    ┌───────────────────────────────────────┐   ┌───────────────────────────────────────┐
    │         NO EXCEPTION                  │   │         EXCEPTION DETECTED            │
    │                                       │   │                                       │
    │  • Record result in backtest log      │   │  • Trigger exception analysis         │
    │  • Update zone status (likely GREEN)  │   │  • Proceed to price source analysis   │
    │  • Include in daily report            │   │  • Classify exception type            │
    └───────────────────────────────────────┘   └───────────────────────────────┬───────┘
                                                                                │
                                                                                ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │                         2. PRICE SOURCE ANALYSIS                                     │
    │                                                                                      │
    │  Calculate price source adjustments:                                                 │
    │  A. Regional snapshot difference (from Regional EOD process)                         │
    │  B. Internal price source difference (from Price Monitoring)                         │
    │                                                                                      │
    │  Adjusted P&L = Actual P&L - Price Source Noise                                      │
    └───────────────────────────────────────────────────────────────────────────┬──────────┘
                                                                                │
                                                                                ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │                         3. EXCEPTION CLASSIFICATION                                  │
    │                                                                                      │
    │  IF |Adjusted P&L| > VaR:                                                            │
    │      → GENUINE EXCEPTION (Model may be underpredicting risk)                         │
    │      → Full root cause analysis required                                             │
    │                                                                                      │
    │  IF |Adjusted P&L| ≤ VaR but |Actual P&L| > VaR:                                     │
    │      → PRICE SOURCE EXCEPTION (Not a model failure)                                  │
    │      → Document price drivers; consider proxy review if persistent                   │
    └───────────────────────────────────────────────────────────────────────────┬──────────┘
                                                                                │
                                                                                ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │                         4. ROOT CAUSE ANALYSIS (Genuine Exceptions)                  │
    │                                                                                      │
    │  • P&L Attribution: Which risk factors drove the loss?                               │
    │  • Market Move Analysis: How extreme were the moves vs. history?                     │
    │  • Scenario Coverage: Were similar moves in the VaR lookback window?                 │
    │  • Model Assessment: Is this a model limitation?                                     │
    │  • Documentation: Record findings for MLRC and regulator                             │
    └───────────────────────────────────────────────────────────────────────────┬──────────┘
                                                                                │
                                                                                ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │                         5. REPORTING AND GOVERNANCE                                  │
    │                                                                                      │
    │  • Update backtest report for VaR Reporting process (MR-L4-007)                      │
    │  • Update zone status and capital multiplier                                         │
    │  • Report to MLRC (weekly), RMA (monthly), PRA (quarterly)                           │
    └──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Backtesting Methodology

### 4.1 Daily Backtest Comparison

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     BACKTESTING METHODOLOGY                                              │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  DAILY BACKTEST:                                                                         │
│                                                                                          │
│  Compare T-1 P&L to T-1 VaR prediction:                                                  │
│                                                                                          │
│  If |P&L(T-1)| > VaR(T-1, 99%) → EXCEPTION                                               │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                     │ │
│  │  EXAMPLE:                                                                           │ │
│  │                                                                                     │ │
│  │  Date: 15-Jan-2025                                                                  │ │
│  │  VaR (14-Jan-2025, 99%, 1-day): $8.5M                                               │ │
│  │  Actual P&L (14-Jan-2025):      -$12.2M   ← LOSS EXCEEDS VaR                        │ │
│  │                                                                                     │ │
│  │  Result: BACKTESTING EXCEPTION                                                      │ │
│  │                                                                                     │ │
│  │  Required Analysis:                                                                 │ │
│  │  1. What market moves drove the loss?                                               │ │
│  │  2. Were these moves captured in VaR scenarios?                                     │ │
│  │  3. Is this a model limitation or extreme market event?                             │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Hypothetical vs. Actual P&L

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     P&L MEASURES FOR BACKTESTING                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  HYPOTHETICAL P&L ("Clean" P&L)                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Definition: P&L from market moves only, on static T-1 EOD positions                    │
│  Calculation: MTM(T-1 positions, T prices) - MTM(T-1 positions, T-1 prices)             │
│                                                                                         │
│  Use: PRIMARY regulatory backtest                                                       │
│       - Compares like-for-like with VaR (same positions, same prices)                   │
│       - Isolates market risk from trading activity                                      │
│       - Preferred by regulators for IMA validation                                      │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ACTUAL P&L ("Dirty" P&L)                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Definition: Total P&L including new trades, fees, reserve changes                      │
│  Calculation: Full P&L from trading sub-ledger                                          │
│                                                                                         │
│  Use: SUPPLEMENTARY backtest                                                            │
│       - Captures real-world performance including trading activity                      │
│       - May differ from hypothetical due to intraday hedging                            │
│       - Useful for understanding total risk management effectiveness                    │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  MERIDIAN APPROACH:                                                                     │
│  • Primary backtest: Hypothetical P&L (regulatory)                                      │
│  • Secondary backtest: Actual P&L (supplementary)                                       │
│  • Both monitored daily; only Hypothetical drives zone classification                   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Basel Traffic Light System

### 5.1 Exception Zone Classification

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     BACKTESTING EXCEPTION ZONES                                          │
│                     (Basel Framework - Rolling 250 Business Days)                        │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  Zone       │ Exceptions │ Interpretation         │ Capital Multiplier │ Action          │
│  ───────────────────────────────────────────────────────────────────────────────────     │
│  GREEN      │ 0-4        │ Model performing well  │ 3.0x (minimum)     │ Normal ops      │
│  YELLOW     │ 5-9        │ Possible model issues  │ 3.4x - 3.85x       │ Investigation   │
│  RED        │ ≥10        │ Model deficiency       │ 4.0x (maximum)     │ Remediation     │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                     │ │
│  │  REGULATORY EXPECTATION (99% VaR):                                                  │ │
│  │                                                                                     │ │
│  │  With 250 observations, expected exceptions = 250 × 1% = 2.5 per year               │ │
│  │                                                                                     │ │
│  │  Zone thresholds reflect statistical tolerance:                                     │ │
│  │  • 0-4 exceptions: Within 95% confidence that model is calibrated                   │ │
│  │  • 5-9 exceptions: Elevated but may be bad luck or unusual markets                  │ │
│  │  • ≥10 exceptions: Strong evidence of model underprediction                         │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Capital Multiplier Impact

| Zone | Exception Count | Base Multiplier | Plus-Factor | Total Multiplier |
|------|-----------------|-----------------|-------------|------------------|
| **GREEN** | 0-4 | 3.0 | 0.00 | 3.00 |
| **YELLOW** | 5 | 3.0 | 0.40 | 3.40 |
| **YELLOW** | 6 | 3.0 | 0.50 | 3.50 |
| **YELLOW** | 7 | 3.0 | 0.65 | 3.65 |
| **YELLOW** | 8 | 3.0 | 0.75 | 3.75 |
| **YELLOW** | 9 | 3.0 | 0.85 | 3.85 |
| **RED** | ≥10 | 3.0 | 1.00 | 4.00 |

### 5.3 Current Status Monitoring

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     MERIDIAN GLOBAL BANK - BACKTEST STATUS                              │
│                     As of: 15-Jan-2025                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ENTITY: Meridian Bank UK                                                               │
│                                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │  Metric                │ Exceptions (250d) │ Zone    │ Multiplier │ Status       │   │
│  │  ────────────────────────────────────────────────────────────────────────────────│   │
│  │  Hypothetical P&L      │ 3                 │ GREEN   │ 3.00x      │ ✓ Normal     │   │
│  │  Actual P&L            │ 4                 │ GREEN   │ N/A        │ ✓ Normal     │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
│  ROLLING 12-MONTH EXCEPTION TREND:                                                      │
│                                                                                         │
│  Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec                                        │
│   0   0   1   0   0   0   1   0   0   0   1   0  = 3 total                              │
│                                                                                         │
│  NEXT EXCEPTION WOULD: Remain in GREEN zone (4 exceptions still GREEN)                  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Price Source Alignment

### 6.1 The Price Source Challenge

VaR calculations use **global London EOD snapshot** prices for consistency. However, this creates potential mismatches with trader P&L that can affect backtesting accuracy:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     PRICE SOURCE ALIGNMENT CHALLENGE                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  SCENARIO 1: REGIONAL SNAPSHOT DIFFERENCES                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  Regional traders value their books using LOCAL snapshots for P&L:                      │
│  • Asia traders use Asia snapshot (17:30 HKT)                                           │
│  • NY traders use NY snapshot (17:30 EST)                                               │
│                                                                                         │
│  But VaR uses GLOBAL (London) snapshot for all positions:                               │
│  • VaR calculation time: London EOD (17:30 GMT)                                         │
│                                                                                         │
│  Result: Regional P&L ≠ VaR-implied P&L due to timing differences                       │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  SCENARIO 2: INTERNAL VS. MARKET PRICE SOURCES                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  For some instruments, trader marks use "INTERNAL" price source:                        │
│  • Illiquid credit positions                                                            │
│  • Complex structured products                                                          │
│  • Emerging market instruments                                                          │
│  • Bespoke OTC derivatives                                                              │
│                                                                                         │
│  Trader EOD marks:    Based on internal valuation/model                                 │
│  VaR prices:          Based on market observable proxy (from Time Series)               │
│                                                                                         │
│  Result: Position valued differently for P&L vs. VaR → Backtesting noise                │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Impact on Backtesting

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     BACKTESTING NOISE FROM PRICE DIFFERENCES                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  IDEAL BACKTEST (No price source differences):                                          │
│                                                                                         │
│  Hypothetical P&L    = MTM(T, VaR prices) - MTM(T-1, VaR prices)                        │
│  VaR (T-1)           = 99th percentile from VaR model                                   │
│                                                                                         │
│  If |Hypothetical P&L| > VaR → Backtesting Exception (model issue)                      │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ACTUAL BACKTEST (With price source differences):                                       │
│                                                                                         │
│  Actual P&L          = MTM(T, trader prices) - MTM(T-1, trader prices)                  │
│  VaR (T-1)           = 99th percentile using VaR prices                                 │
│                                                                                         │
│  Price Noise         = P&L difference due to price source mismatch                      │
│                                                                                         │
│  Result: Backtesting exception may be driven by:                                        │
│  • Genuine model failure (real exception)                                               │
│  • Price source differences (noise - not a model issue)                                 │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │                                                                                     ││
│  │  EXAMPLE: Illiquid Credit Bond                                                      ││
│  │                                                                                     ││
│  │  Trader marks position at internal price (model-based): $102.50                     ││
│  │  VaR uses market proxy (similar liquid bond): $101.80                               ││
│  │  Price difference: $0.70 per $100 nominal                                           ││
│  │                                                                                     ││
│  │  For $50M position:                                                                 ││
│  │  P&L noise = $50M × 0.70% = $350,000                                                ││
│  │                                                                                     ││
│  │  This $350k could mask a genuine exception or create a false exception              ││
│  │                                                                                     ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Price Difference Monitoring

### 7.1 Check 1: Regional vs. Global Snapshot Differences

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     REGIONAL VS. GLOBAL P&L RECONCILIATION                               │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  CALCULATION:                                                                            │
│                                                                                          │
│  For each regional book:                                                                 │
│  Regional_P&L = MTM(positions, regional_snapshot) - MTM(positions, T-1_regional)         │
│  Global_P&L   = MTM(positions, London_snapshot) - MTM(positions, T-1_London)             │
│                                                                                          │
│  Snapshot_Timing_Difference = Regional_P&L - Global_P&L                                  │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  DAILY SNAPSHOT TIMING REPORT                                                       │ │
│  │  Date: 15-Jan-2025                                                                  │ │
│  │                                                                                     │ │
│  │  Region      │ Regional P&L │ Global P&L │ Difference │ Status                      │ │
│  │  ─────────────────────────────────────────────────────────────────────────────      │ │
│  │  Asia (HK)   │   +$1.2M     │   +$0.9M   │   +$300k   │ ⚠ Monitor (>$100k)          │ │
│  │  NY          │   -$0.5M     │   -$0.6M   │   +$100k   │ ✓ Within tolerance          │ │
│  │  London      │   +$2.1M     │   +$2.1M   │   $0       │ ✓ Same snapshot             │ │
│  │  ─────────────────────────────────────────────────────────────────────────────      │ │
│  │  TOTAL       │   +$2.8M     │   +$2.4M   │   +$400k   │                             │ │
│  │                                                                                     │ │
│  │  Note: Differences driven by USD/JPY move between Asia close and London close       │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  THRESHOLD: Material difference flagged if > $100k or > 5% of regional P&L               │
│  ACTION: Include in backtest analysis when investigating exceptions                      │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Check 2: Internal Price Source Differences

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     INTERNAL PRICE SOURCE RECONCILIATION                                 │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  SCOPE: Positions where price source = "INTERNAL" (not market observable)                │
│                                                                                          │
│  CALCULATION:                                                                            │
│                                                                                          │
│  For each internally-priced position:                                                    │
│  Trader_MTM  = Valuation using internal/model price                                      │
│  VaR_MTM     = Valuation using VaR time series proxy price                               │
│                                                                                          │
│  Price_Difference = |Trader_Price - VaR_Proxy_Price| / Trader_Price                      │
│  MTM_Difference   = Trader_MTM - VaR_MTM                                                 │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  INTERNAL PRICE SOURCE MONITORING REPORT                                            │ │
│  │  Date: 15-Jan-2025                                                                  │ │
│  │                                                                                     │ │
│  │  Position          │ Trader   │ VaR     │ Price    │ MTM        │ Status            │ │
│  │                    │ Price    │ Proxy   │ Diff %   │ Diff       │                   │ │
│  │  ─────────────────────────────────────────────────────────────────────────────      │ │
│  │  EM Credit Bond A  │ 98.50    │ 97.20   │ 1.3%     │ +$195k     │ ⚠ Material        │ │
│  │  Struct Prod XYZ   │ 102.30   │ 101.50  │ 0.8%     │ +$120k     │ ⚠ Material        │ │
│  │  Illiquid CDS      │ 145bp    │ 160bp   │ 10.3%    │ +$85k      │ ⚠ Review          │ │
│  │  Bespoke Swap      │ -$2.1M   │ -$2.3M  │ 9.5%     │ +$200k     │ ⚠ Material        │ │
│  │  ─────────────────────────────────────────────────────────────────────────────      │ │
│  │  TOTAL (24 positions with internal source)                │ +$850k   │              │ │
│  │                                                                                     │ │
│  │  SUMMARY:                                                                           │ │
│  │  • Positions with >5% price difference: 4                                           │ │
│  │  • Aggregate MTM difference: +$850k                                                 │ │
│  │  • Potential backtest noise: ±$850k                                                 │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  THRESHOLDS:                                                                             │
│  • Price difference > 5%: Flag for review                                                │
│  • MTM difference > $100k per position: Material - include in backtest analysis          │
│  • Aggregate MTM difference > $500k: Report to RAV/RMA                                   │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Exception Analysis Framework

### 8.1 Adjusted Backtest Analysis

When a backtesting exception occurs, the price source analysis informs root cause determination:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     BACKTESTING EXCEPTION ROOT CAUSE FRAMEWORK                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  When |Actual P&L| > VaR:                                                               │
│                                                                                         │
│  STEP 1: Calculate Price Source Adjustments                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  A. Regional snapshot difference: +$400k (from Check 1)                                 │
│  B. Internal price source difference: +$850k (from Check 2)                             │
│  Total price noise: +$1,250k                                                            │
│                                                                                         │
│  STEP 2: Adjusted Backtest                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Actual P&L:           -$12.5M                                                          │
│  Less: Price noise:    +$1.25M                                                          │
│  Adjusted P&L:         -$11.25M                                                         │
│                                                                                         │
│  VaR (T-1):            $10.0M                                                           │
│                                                                                         │
│  STEP 3: Determine Exception Type                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                                  │   │
│  │  IF |Adjusted P&L| > VaR:                                                        │   │
│  │     → GENUINE EXCEPTION (Model may be underpredicting risk)                      │   │
│  │     → Investigate market moves, risk factor coverage, methodology                │   │
│  │                                                                                  │   │
│  │  IF |Adjusted P&L| ≤ VaR but |Actual P&L| > VaR:                                 │   │
│  │     → PRICE SOURCE EXCEPTION (Not a model failure)                               │   │
│  │     → Document price source drivers                                              │   │
│  │     → Consider for proxy/methodology review if persistent                        │   │
│  │                                                                                  │   │
│  │  In this example:                                                                │   │
│  │  |Adjusted P&L| = $11.25M > VaR = $10.0M → GENUINE EXCEPTION                     │   │
│  │  (But note: Price noise contributed $1.25M to total loss)                        │   │
│  │                                                                                  │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
│  DOCUMENTATION: All exceptions reported with:                                           │
│  • Unadjusted P&L and VaR                                                               │
│  • Price source adjustments                                                             │
│  • Adjusted comparison                                                                  │
│  • Root cause classification                                                            │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Root Cause Analysis Steps

| Step | Analysis | Output |
|------|----------|--------|
| **1. P&L Attribution** | Break down loss by risk factor | Which factors drove the loss |
| **2. Market Move Analysis** | Compare actual moves to historical distribution | How extreme were the moves |
| **3. Scenario Coverage** | Check if historical scenarios captured this type of event | Were similar moves in VaR lookback |
| **4. Price Source Review** | Calculate price source adjustments | Genuine vs. price-driven exception |
| **5. Model Assessment** | Determine if model limitation exists | Model adequacy conclusion |
| **6. Documentation** | Record findings for MLRC and regulator | Exception report |

### 8.3 Exception Classification

| Classification | Criteria | Action | Count Towards Zone |
|---------------|----------|--------|-------------------|
| **Genuine Exception** | Adjusted P&L > VaR | Full investigation; MLRC report | Yes |
| **Price Source Exception** | Only unadjusted P&L > VaR | Document; proxy review if persistent | Yes (regulatory) |
| **Data Error** | P&L or VaR calculation error | Fix data; rerun | No (corrected) |
| **Exceptional Event** | Major market dislocation | Document; regulatory discussion | Yes (but may be disregarded) |

---

## 9. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| BT-C01 | Daily backtest performed for all entities | Detective | RAV |
| BT-C02 | Hypothetical P&L used for primary backtest | Preventive | RAV |
| BT-C03 | Rolling 250-day exception count maintained | Detective | RAV |
| BT-C04 | Exception triggers root cause analysis within 1 business day | Detective | RAV |
| BT-C05 | Price source adjustments calculated for all exceptions | Detective | RAV |
| BT-C06 | Zone status updated daily and reported to MLRC weekly | Detective | RAV |
| BT-C07 | Capital multiplier updated when zone changes | Preventive | RMA |
| BT-C08 | Regional vs. global P&L differences monitored daily | Detective | Product Control |
| BT-C09 | Internal price source positions monitored daily | Detective | RAV |
| BT-C10 | Aggregate MTM difference >$500k escalated to RMA | Detective | RAV |
| BT-C11 | Persistent price source exceptions trigger proxy review | Detective | RMA |
| BT-C12 | Annual backtest methodology review | Preventive | RMA |

---

## 10. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| Daily backtest complete | 05:30 GMT | 05:45 GMT | RAV Team Lead |
| Exception analysis complete | T+1 12:00 | T+1 17:00 | RAV Manager |
| Price source analysis | T+1 08:00 | T+1 10:00 | RAV |
| Zone status update | T+1 06:00 | T+1 07:00 | RAV |
| MLRC exception report | Weekly (Friday) | - | Head of RAV |

---

## 11. Governance and Reporting

### 11.1 Regular Reporting

| Report | Audience | Frequency | Content |
|--------|----------|-----------|---------|
| **Daily Backtest Report** | Market Risk, RAV | Daily | P&L vs. VaR comparison, exceptions |
| **Weekly Exception Summary** | MLRC | Weekly | Exception count, zone status, root cause |
| **Monthly Performance Review** | RMA | Monthly | Model performance trends, remediation |
| **Price Source Monitoring** | RAV, RMA | Daily | Positions with material price differences |
| **Proxy Alignment Review** | RMA | Quarterly | Systematic price source mismatches |

### 11.2 Regulatory Reporting

Backtesting results feed into the [Market Risk Regulatory Reporting Process (MR-L4-009)](./regulatory-reporting.md), which handles:

| Requirement | Regulatory Basis | Timing | Owner |
|-------------|------------------|--------|-------|
| **Immediate Exception Notification** | CRR Article 366(4) | ≤5 working days from exception | Regulatory Reporting |
| **Quarterly COREP Submission** | CRR Article 366(3), 430 | T+30 business days | Regulatory Reporting |
| **Zone Status and Multiplier** | CRR Article 366 | Quarterly assessment | RAV / Regulatory Reporting |

**Key Linkage**: The Backtesting process provides exception data and root cause analysis to Regulatory Reporting, which manages the formal PRA notification and COREP template submission (CAP24.03).

### 11.3 Escalation Path

| Trigger | Escalation | Timeline |
|---------|------------|----------|
| Single exception (GREEN zone) | RAV Team Lead → RAV Manager | T+1 |
| Exception moving to YELLOW zone | RAV Manager → Head of Market Risk → Regulatory Reporting | Immediate |
| Exception moving to RED zone | Head of Market Risk → CRO → PRA (via Regulatory Reporting) | Immediate |
| Persistent price source issues | RAV → RMA → MLRC | Quarterly review |

---

## 12. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [Risk Engine Calculation](./risk-engine-calculation.md) | Upstream - provides VaR |
| [Market Risk Reporting and Sign-off](./market-risk-reporting-signoff.md) | Downstream - uses backtest results |
| [Market Risk Regulatory Reporting](./regulatory-reporting.md) | Downstream - PRA notifications and COREP |
| [Regional EOD Management](./regional-eod-management.md) | Upstream - provides regional P&L |
| [Historical Simulation VaR Model](../L6-Models/var-methodology.md) | Model being backtested |
| [VaR Limit Framework](../L3-Governance/policies/var-limit-framework.md) | Governance - limit structure |

---

## 13. Document Control

### 13.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version - consolidated from Risk Engine (Price Source) and VaR Reporting (Backtesting) | MLRC |
| 1.1 | 2025-01-15 | Added Section 11.2 Regulatory Reporting with CRR Article 366 requirements and link to MR-L4-009 | MLRC |

---

*End of Document*
