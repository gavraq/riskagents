---
# Control Metadata
control_id: MR-L5-005
control_name: Concentration Limits Controls
version: 1.2
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Market Risk
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-005  # Limit Monitoring
parent_framework: MR-L3-003  # VaR Limit Framework
l1_requirements:
  - REQ-L1-001  # CRR (UK)
  - REQ-L1-002  # Large Exposures
l2_risk_types:
  - MR-L2-001   # Market Risk
  - MR-L2-002   # Concentration Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-003   # VaR Limit Framework
l4_processes:
  - MR-L4-013   # Market Risk Limits Management
  - MR-L4-014   # Aged Inventory Monitoring
l6_models:
  - MR-L6-001   # Historical Simulation VaR
l7_systems:
  - SYS-MR-001  # Risk Engine (FMDM)
  - SYS-MR-003  # Murex (Front Office)
---

# Concentration Limits Controls

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Control ID** | MR-L5-005 |
| **Version** | 1.2 |
| **Effective Date** | 15 January 2025 |
| **Parent Framework** | VaR Limit Framework (MR-L3-003) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

This document defines the controls for monitoring and managing concentration limits in the trading book. Concentration limits prevent excessive exposure to single names, sectors, currencies, or other risk dimensions that may not be fully captured by VaR diversification assumptions.

---

## 2. Scope

### 2.1 Concentration Types Covered

| Concentration Type | Definition | Risk Concern |
|-------------------|------------|--------------|
| **Single Issuer** | Exposure to individual credit name | Default/downgrade of single issuer |
| **Single Currency** | FX exposure to single currency | Currency crash or intervention |
| **Single Curve** | Interest rate exposure to single curve | Curve-specific movement |
| **Liquidity** | Position size vs market liquidity | Exit difficulty in stress |
| **Sector** | Exposure to industry/geography | Sector-wide stress |
| **Maturity** | Exposure concentrated in specific tenors | Roll/refinancing risk |

### 2.2 Entity-Level Concentration Limits

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONCENTRATION LIMITS (Entity Level)                                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  TYPE                   │  METRIC                    │  LIMIT     │  WARNING            │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Single Issuer          │  % of Trading Book VaR     │    15%     │    12%              │
│  Single Currency        │  % of FX VaR               │    30%     │    24%              │
│  Single Curve           │  % of IR VaR               │    25%     │    20%              │
│  Position vs ADV        │  % of 30-day ADV           │    10%     │     8%              │
│  Single Sector          │  % of Credit VaR           │    25%     │    20%              │
│  Single Country (EM)    │  % of EM VaR               │    20%     │    16%              │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ADV = Average Daily Volume (market turnover)                                           │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Absolute Position Limits

| Asset Type | Metric | Limit |
|------------|--------|-------|
| **Single Corporate Bond** | Market Value | $50m |
| **Single Sovereign Bond (G10)** | Market Value | $200m |
| **Single Sovereign Bond (EM)** | Market Value | $30m |
| **Single Equity** | Market Value | $20m |
| **Single CDS Name** | Notional | $75m |

---

## 3. Risk Engine Integration

### 3.1 Data Source: Concentration VaR Decomposition

The controls in this document rely on **Component VaR decomposition** outputs from the Risk Engine (MR-L4-006, Section 6.6). The Risk Engine calculates VaR attribution across multiple dimensions required for concentration monitoring.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  RISK ENGINE → CONCENTRATION CONTROLS DATA FLOW                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                         RISK ENGINE (MR-L4-006)                                 │    │
│  │                                                                                 │    │
│  │  During nightly VaR calculation, the Risk Engine produces:                      │    │
│  │                                                                                 │    │
│  │  1. Portfolio VaR / SVaR                                                        │    │
│  │  2. Component VaR decomposition by multiple dimensions:                         │    │
│  │     • By Issuer      → RISK_CONC_ISSUER table                                   │    │
│  │     • By Currency    → RISK_CONC_CURRENCY table                                 │    │
│  │     • By Curve       → RISK_CONC_CURVE table                                    │    │
│  │     • By Sector      → RISK_CONC_SECTOR table                                   │    │
│  │     • By Country     → RISK_CONC_COUNTRY table                                  │    │
│  │                                                                                 │    │
│  └──────────────────────────────────┬──────────────────────────────────────────────┘    │
│                                     │                                                   │
│                                     ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                            RISK ODS (SYS-MR-008)                                │    │
│  │                                                                                 │    │
│  │  RISK_CONC_ISSUER    │ issuer_id, component_var, pct_of_total, breach_flag      │    │
│  │  RISK_CONC_CURRENCY  │ currency_code, component_var, pct_of_fx_var, breach_flag │    │
│  │  RISK_CONC_CURVE     │ curve_id, component_var, pct_of_ir_var, breach_flag      │    │
│  │  RISK_CONC_SECTOR    │ gics_sector, component_var, pct_of_credit_var            │    │
│  │  RISK_CONC_COUNTRY   │ country_code, component_var, pct_of_em_var               │    │
│  │  RISK_CONC_SUMMARY   │ dimension, top_concentration, breach_flag                │    │
│  │                                                                                 │    │
│  └──────────────────────────────────┬──────────────────────────────────────────────┘    │
│                                     │                                                   │
│                                     ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                    CONCENTRATION CONTROLS (MR-L5-005)                           │    │
│  │                                                                                 │    │
│  │  CN-C01: Single Issuer Monitoring      ← RISK_CONC_ISSUER                       │    │
│  │  CN-C02: Single Currency Monitoring    ← RISK_CONC_CURRENCY                     │    │
│  │  CN-C03: Single Curve Monitoring       ← RISK_CONC_CURVE                        │    │
│  │  CN-C05: Sector Monitoring             ← RISK_CONC_SECTOR                       │    │
│  │  CN-C06: Country (EM) Monitoring       ← RISK_CONC_COUNTRY                      │    │
│  │  CN-C09: Top Exposures Report          ← RISK_CONC_SUMMARY                      │    │
│  │                                                                                 │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Component VaR vs Marginal VaR

The Risk Engine supports two VaR attribution methods:

| Method | Formula | Property | Use in Concentration Controls |
|--------|---------|----------|-------------------------------|
| **Component VaR** | ρ(i,P) × σ(i) × Position(i) / Portfolio_σ × VaR | Sums to portfolio VaR | **Primary method** - used for % of total calculations |
| **Marginal VaR** | VaR(Portfolio) - VaR(Portfolio excl. i) | Does NOT sum to VaR | Ad-hoc analysis; position sizing |

**Why Component VaR?**
- Component VaR sums exactly to total portfolio VaR, enabling meaningful % calculations
- Marginal VaR captures diversification benefit but cannot be used for % attribution
- Concentration limits are expressed as "% of VaR", requiring an additive decomposition

### 3.3 Data Refresh and SLA

| Source Table | Refresh Time | Data Available | Control Execution |
|--------------|--------------|----------------|-------------------|
| RISK_CONC_ISSUER | 04:00 GMT+1 | 04:30 GMT+1 | CN-C01 by 09:30 |
| RISK_CONC_CURRENCY | 04:00 GMT+1 | 04:30 GMT+1 | CN-C02 by 09:30 |
| RISK_CONC_CURVE | 04:00 GMT+1 | 04:30 GMT+1 | CN-C03 by 09:30 |
| RISK_CONC_SECTOR | 04:00 GMT+1 | 04:30 GMT+1 | CN-C05 weekly |
| RISK_CONC_COUNTRY | 04:00 GMT+1 | 04:30 GMT+1 | CN-C06 by 09:30 |

**Dependency**: If Risk Engine batch (MR-L4-006) is delayed, concentration controls are also delayed. Escalation per Risk Engine SLA.

---

## 4. Control Objectives

| Objective ID | Objective | Risk Mitigated |
|--------------|-----------|----------------|
| **CO-01** | Concentration limits monitored daily | Undetected concentrated exposures |
| **CO-02** | Single name exposures identified | Issuer-specific event impact |
| **CO-03** | Liquidity risk of positions assessed | Exit difficulty in stress |
| **CO-04** | Sector concentrations tracked | Sector-wide stress impact |
| **CO-05** | Breaches escalated appropriately | Delayed response to excess concentration |
| **CO-06** | VaR diversification assumptions validated | Over-reliance on diversification benefit |

---

## 4. Control Inventory

### 4.1 Control Summary

| Control ID | Control Name | Type | Frequency | Owner |
|------------|--------------|------|-----------|-------|
| CN-C01 | Single Issuer Concentration Monitoring | Detective | Daily | RAV |
| CN-C02 | Single Currency Concentration Monitoring | Detective | Daily | RAV |
| CN-C03 | Single Curve Concentration Monitoring | Detective | Daily | RAV |
| CN-C04 | Position vs ADV Monitoring | Detective | Daily | Market Risk |
| CN-C05 | Sector Concentration Monitoring | Detective | Weekly | Market Risk |
| CN-C06 | Country (EM) Concentration Monitoring | Detective | Daily | Market Risk |
| CN-C07 | Absolute Position Limit Monitoring | Detective | Daily | RAV |
| CN-C08 | Concentration Breach Escalation | Responsive | On breach | Market Risk |
| CN-C09 | Top Exposures Report | Detective | Daily | RAV |
| CN-C10 | Diversification Benefit Analysis | Detective | Monthly | Market Risk |
| CN-C11 | MLRC Concentration Dashboard | Detective | Weekly | MLRC |
| CN-C12 | Liquidity Stress Assessment | Detective | Weekly | Market Risk |
| CN-C13 | Aged Inventory Identification | Detective | Quarterly | Market Risk |
| CN-C14 | Aged Inventory ICAAP Contribution | Detective | Quarterly | Market Risk |

---

## 5. Control Details

### 5.1 CN-C01: Single Issuer Concentration Monitoring

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: CN-C01 - Single Issuer Concentration Monitoring                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Identify issuer-specific concentration that could cause                     │
│             disproportionate loss in default/downgrade event                            │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Daily (by 09:30)                                                            │
│  OWNER: RAV                                                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  DATA SOURCE: Risk Engine (MR-L4-006, Section 6.6)                                      │
│  TABLE: RISK_CONC_ISSUER                                                                │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CALCULATION METHOD (performed by Risk Engine):                                         │
│                                                                                         │
│  For each issuer 'i', Component VaR is calculated as:                                   │
│                                                                                         │
│  Component_VaR(i) = ρ(i, Portfolio) × σ(i) × Position(i)                                │
│                     ─────────────────────────────────────── × Portfolio_VaR             │
│                                Portfolio_σ                                              │
│                                                                                         │
│       Issuer Component VaR (i)                                                          │
│       ──────────────────────── × 100 = Issuer Concentration %                           │
│       Total Trading Book VaR                                                            │
│                                                                                         │
│  Note: Component VaR sums to portfolio VaR (unlike Marginal VaR)                        │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CONTROL ACTIVITIES:                                                                    │
│  1. Query RISK_CONC_ISSUER table from Risk ODS (available 04:30 GMT+1)                  │
│  2. Extract pre-calculated concentration % (pct_of_total column)                        │
│  3. Filter for issuers with material exposure (>1% of VaR)                              │
│  4. Apply thresholds:                                                                   │
│     • Warning (12%): Amber status                                                       │
│     • Limit (15%): Red status - breach (breach_flag = 'Y')                              │
│  5. Include top 10 issuer concentrations in daily report                                │
│                                                                                         │
│  EXAMPLE (from Risk ODS):                                                               │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  issuer_id      │ component_var │ pct_of_total │ breach_flag │ warning_flag        │ │
│  ├─────────────────┼───────────────┼──────────────┼─────────────┼─────────────────────┤ │
│  │  UK_GOVT        │   $2.4M       │    12.0%     │     N       │      Y              │ │
│  │  DEUTSCHE_BANK  │   $2.0M       │    10.0%     │     N       │      N              │ │
│  │  VODAFONE       │   $1.8M       │     9.0%     │     N       │      N              │ │
│  └────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Daily Concentration Report (generated from RISK_CONC_ISSUER)                         │
│  • Issuer concentration heat map                                                        │
│  • Breach notification emails (auto-generated on breach_flag = 'Y')                     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 CN-C02: Single Currency Concentration Monitoring

| Attribute | Value |
|-----------|-------|
| **Control ID** | CN-C02 |
| **Objective** | Identify currency-specific concentration in FX portfolio |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | RAV |

**Control Activities**:
1. Extract FX VaR decomposition by currency from Risk Engine
2. Calculate concentration % for each currency:
   - Currency VaR Contribution / Total FX VaR × 100
3. Flag currencies exceeding:
   - Warning (24%): Amber
   - Limit (30%): Red - breach
4. Include top 5 currency concentrations in daily report

**Evidence**:
- Daily FX Concentration Report
- Currency concentration dashboard

### 5.3 CN-C03: Single Curve Concentration Monitoring

| Attribute | Value |
|-----------|-------|
| **Control ID** | CN-C03 |
| **Objective** | Identify curve-specific concentration in rates portfolio |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | RAV |

**Control Activities**:
1. Extract IR VaR decomposition by curve from Risk Engine
2. Calculate concentration % for each curve:
   - Curve VaR Contribution / Total IR VaR × 100
3. Flag curves exceeding:
   - Warning (20%): Amber
   - Limit (25%): Red - breach
4. Include top 5 curve concentrations in daily report

**Evidence**:
- Daily IR Concentration Report
- Curve concentration dashboard

### 5.4 CN-C04: Position vs ADV Monitoring

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: CN-C04 - Position vs ADV Monitoring                                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Identify positions that are large relative to market liquidity              │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Daily                                                                       │
│  OWNER: Market Risk                                                                     │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CALCULATION METHOD:                                                                    │
│                                                                                         │
│       Position Market Value                                                             │
│       ─────────────────────── × 100 = Position/ADV %                                    │
│       30-day Average Daily Volume                                                       │
│                                                                                         │
│  ADV Sources:                                                                           │
│  • Equities: Exchange-reported volume × price                                           │
│  • Bonds: Dealer volume estimates (e.g., MarketAxess, TradeWeb)                         │
│  • FX: BIS triennial survey data / dealer estimates                                     │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CONTROL ACTIVITIES:                                                                    │
│  1. Obtain ADV data from market data providers                                          │
│  2. Calculate Position/ADV % for all positions > $1m                                    │
│  3. Flag positions exceeding:                                                           │
│     • Warning (8%): Amber - potential liquidity concern                                 │
│     • Limit (10%): Red - breach; significant exit difficulty                            │
│  4. Estimate liquidation timeframe for large positions                                  │
│  5. Report to MLRC weekly                                                               │
│                                                                                         │
│  LIQUIDATION TIME ESTIMATE:                                                             │
│  • If Position/ADV = 10%, assume 10+ days to exit without market impact                 │
│  • Stress assumption: 50% ADV decline, doubling exit time                               │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Daily Position/ADV Report                                                            │
│  • Liquidity concentration heat map                                                     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.5 CN-C05: Sector Concentration Monitoring

| Attribute | Value |
|-----------|-------|
| **Control ID** | CN-C05 |
| **Objective** | Identify sector-specific concentration in credit portfolio |
| **Type** | Detective |
| **Frequency** | Weekly |
| **Owner** | Market Risk |

**Control Activities**:
1. Classify all credit exposures by GICS sector
2. Calculate sector VaR contribution:
   - Sector VaR Contribution / Total Credit VaR × 100
3. Flag sectors exceeding:
   - Warning (20%): Amber
   - Limit (25%): Red - breach
4. Present sector breakdown to MLRC weekly

**Sector Classification**:
- Energy
- Materials
- Industrials
- Consumer Discretionary
- Consumer Staples
- Health Care
- Financials
- Information Technology
- Communication Services
- Utilities
- Real Estate

**Evidence**:
- Weekly Sector Concentration Report
- MLRC presentation

### 5.6 CN-C06: Country (EM) Concentration Monitoring

| Attribute | Value |
|-----------|-------|
| **Control ID** | CN-C06 |
| **Objective** | Identify country-specific concentration in EM exposures |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | Market Risk |

**Control Activities**:
1. Aggregate all EM exposures by country:
   - Bonds, FX, derivatives, loans
2. Calculate country VaR contribution:
   - Country VaR Contribution / Total EM VaR × 100
3. Flag countries exceeding:
   - Warning (16%): Amber
   - Limit (20%): Red - breach
4. Include top 5 EM country concentrations in daily report
5. Cross-reference with country risk ratings

**Evidence**:
- Daily EM Concentration Report
- Country concentration dashboard

### 5.7 CN-C07: Absolute Position Limit Monitoring

| Attribute | Value |
|-----------|-------|
| **Control ID** | CN-C07 |
| **Objective** | Monitor absolute position sizes against hard limits |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | RAV |

**Control Activities**:
1. Extract all positions by instrument type
2. Compare against absolute position limits:
   - Single Corporate Bond: $50m
   - Single Sovereign Bond (G10): $200m
   - Single Sovereign Bond (EM): $30m
   - Single Equity: $20m
   - Single CDS Name: $75m notional
3. Flag positions exceeding limits
4. Generate breach notifications

**Evidence**:
- Daily Absolute Position Report
- Breach notifications

### 5.8 CN-C08: Concentration Breach Escalation

| Attribute | Value |
|-----------|-------|
| **Control ID** | CN-C08 |
| **Objective** | Escalate concentration limit breaches appropriately |
| **Type** | Responsive |
| **Frequency** | On breach |
| **Owner** | Market Risk |

**Escalation Matrix**:

| Breach Type | Escalate To | Timeline | Action Required |
|-------------|-------------|----------|-----------------|
| Single Name | Desk Head + Market Risk | Same day | Position reduction plan |
| Currency/Curve | BU Head + MLRC Chair | Same day | Risk reduction or hedge |
| Liquidity (ADV) | MLRC + CRO | Immediate | Exit strategy; potential trading restriction |
| Sector/Country | MLRC | Weekly meeting | Portfolio rebalancing plan |

**Evidence**:
- Escalation notification
- Breach Register entry
- Reduction plan documentation

### 5.9 CN-C09: Top Exposures Report

| Attribute | Value |
|-----------|-------|
| **Control ID** | CN-C09 |
| **Objective** | Provide visibility of largest concentrations |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | RAV |

**Report Contents**:
1. Top 10 issuer concentrations (by VaR contribution)
2. Top 5 currency concentrations
3. Top 5 curve concentrations
4. Top 10 positions by ADV %
5. Top 5 sector concentrations
6. Top 5 EM country concentrations
7. Day-on-day changes
8. Positions approaching limits

**Distribution**: Market Risk, Trading Heads, MLRC members

**Evidence**:
- Daily Top Exposures Report

### 5.10 CN-C10: Diversification Benefit Analysis

| Attribute | Value |
|-----------|-------|
| **Control ID** | CN-C10 |
| **Objective** | Validate VaR diversification assumptions |
| **Type** | Detective |
| **Frequency** | Monthly |
| **Owner** | Market Risk |

**Control Activities**:
1. Calculate sum of standalone VaRs (undiversified)
2. Compare to total portfolio VaR (diversified)
3. Calculate diversification benefit:
   - (Undiversified VaR - Diversified VaR) / Undiversified VaR
4. Monitor diversification benefit over time
5. Flag if benefit is unusually high (>40%) - may indicate model issue or correlation breakdown risk
6. Report to MLRC

**Evidence**:
- Monthly Diversification Analysis
- MLRC presentation

### 5.11 CN-C11: MLRC Concentration Dashboard

| Attribute | Value |
|-----------|-------|
| **Control ID** | CN-C11 |
| **Objective** | Governance oversight of concentration risk |
| **Type** | Detective |
| **Frequency** | Weekly |
| **Owner** | MLRC |

**Control Activities**:
1. Market Risk presents concentration dashboard to MLRC
2. Dashboard includes:
   - All concentration limits with utilisation
   - Breaches in period
   - Top exposures
   - Trend analysis
   - Liquidity assessment
   - Diversification benefit analysis
3. MLRC challenges and approves actions
4. Decisions minuted

**Evidence**:
- MLRC agenda and pack
- MLRC minutes

### 5.12 CN-C12: Liquidity Stress Assessment

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: CN-C12 - Liquidity Stress Assessment                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Assess portfolio liquidation under stress market conditions                 │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Weekly                                                                      │
│  OWNER: Market Risk                                                                     │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  STRESS SCENARIOS:                                                                      │
│                                                                                         │
│  ┌────────────────────────────────────────────────────────────────────────────────┐     │
│  │  SCENARIO 1: NORMAL STRESS                                                     │     │
│  │  • ADV declines by 30%                                                         │     │
│  │  • Bid-ask spreads widen by 2x                                                 │     │
│  │  • Estimate exit cost and timeframe                                            │     │
│  └────────────────────────────────────────────────────────────────────────────────┘     │
│                                                                                         │
│  ┌────────────────────────────────────────────────────────────────────────────────┐     │
│  │  SCENARIO 2: SEVERE STRESS (GFC-like)                                          │     │
│  │  • ADV declines by 60%                                                         │     │
│  │  • Bid-ask spreads widen by 5x                                                 │     │
│  │  • Some markets effectively closed                                             │     │
│  │  • Estimate exit cost and timeframe                                            │     │
│  └────────────────────────────────────────────────────────────────────────────────┘     │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CONTROL ACTIVITIES:                                                                    │
│  1. Apply stress haircuts to ADV estimates                                              │
│  2. Estimate liquidation timeframe for each position                                    │
│  3. Estimate liquidation cost (market impact + spread)                                  │
│  4. Aggregate to portfolio level                                                        │
│  5. Compare to VaR liquidity horizon assumptions                                        │
│  6. Report to MLRC                                                                      │
│                                                                                         │
│  OUTPUT METRICS:                                                                        │
│  • Liquidity-at-Risk: Expected cost to exit portfolio in stress                         │
│  • Days to Liquidate: Time to exit if limited to 10% ADV/day                            │
│  • Illiquid Positions: Positions requiring >5 days to exit                              │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Weekly Liquidity Stress Report                                                       │
│  • MLRC presentation                                                                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.13 CN-C13: Aged Inventory Identification

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: CN-C13 - Aged Inventory Identification                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Identify positions that have become illiquid due to age and low turnover    │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Quarterly                                                                   │
│  OWNER: Market Risk                                                                     │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  LINKAGE: This control implements MR-L4-014 Aged Inventory Monitoring                   │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  AGED INVENTORY CRITERIA (per MR-L4-014):                                               │
│  Position qualifies as "Aged Inventory" if BOTH criteria met:                           │
│  1. Position held for > 6 months (180 calendar days)                                    │
│  2. Turnover < 10% of position size in trailing 90 days                                 │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CONTROL ACTIVITIES:                                                                    │
│  1. Extract all positions with holding period > 180 days                                │
│  2. Calculate 90-day turnover for each position:                                        │
│     Turnover % = (Buy Volume + Sell Volume) / Average Position × 100                    │
│  3. Identify positions meeting aged inventory criteria                                  │
│  4. Classify by severity:                                                               │
│     • Watch List: 6-9 months, turnover 5-10%                                            │
│     • Aged: 9-12 months, turnover <5%                                                   │
│     • Stale: >12 months, turnover <2%                                                   │
│  5. Assess exit feasibility:                                                            │
│     • Current market depth                                                              │
│     • Estimated liquidation cost                                                        │
│     • Estimated liquidation timeframe                                                   │
│  6. Document business rationale for holding (if strategic)                              │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ESCALATION:                                                                            │
│  • "Stale" positions (>12 months, <2% turnover): Escalate to MLRC for action plan       │
│  • >$5m aggregate aged inventory: Escalate to ALCO                                      │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Quarterly Aged Inventory Report (per MR-L4-014)                                      │
│  • Position-level analysis with turnover calculations                                   │
│  • Exit feasibility assessments                                                         │
│  • MLRC/ALCO presentations                                                              │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.14 CN-C14: Aged Inventory ICAAP Contribution

| Attribute | Value |
|-----------|-------|
| **Control ID** | CN-C14 |
| **Objective** | Ensure aged inventory illiquidity is reflected in ICAAP capital |
| **Type** | Detective |
| **Frequency** | Quarterly |
| **Owner** | Market Risk |

**Control Activities**:
1. Take aged inventory list from CN-C13
2. For each aged position, calculate illiquidity adjustment:
   - Assess if standard ECAP liquidity horizon is sufficient
   - If not, calculate extended horizon ECAP
   - Illiquidity add-on = Extended ECAP - Standard ECAP
3. Aggregate illiquidity add-ons by desk and entity
4. Include in quarterly ICAAP submission (via MR-L5-007 EC-C05)
5. Present to ALCO as part of capital adequacy review

**Illiquidity Horizon Extension Guidelines**:

| Position Category | Standard Horizon | Extended Horizon | Add-on Multiplier |
|-------------------|------------------|------------------|-------------------|
| Watch List (6-9 months) | Asset class default | +5 days | ~1.2x |
| Aged (9-12 months) | Asset class default | +10 days | ~1.4x |
| Stale (>12 months) | Asset class default | +20 days | ~1.7x |

**Integration Points**:

| Process | Input/Output |
|---------|--------------|
| MR-L4-014 Aged Inventory Monitoring | Source: Aged inventory list |
| MR-L5-007 ECAP Controls (EC-C05) | Output: Illiquidity add-on |
| ICAAP | Output: Pillar 2 illiquidity capital |

**Evidence**:
- Quarterly Illiquidity Adjustment Calculation
- ECAP reconciliation including aged inventory add-on
- ALCO presentation
- ICAAP submission documentation

---

## 6. Concentration Heat Map

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        CONCENTRATION HEAT MAP (Example)                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ISSUER CONCENTRATIONS (Top 10)                                                         │
│  ───────────────────────────────                                                        │
│  Issuer               │ VaR Contrib │  %   │ Status │ ADV %                             │
│  ─────────────────────┼─────────────┼──────┼────────┼───────                            │
│  UK Government        │   $2.2m     │ 11%  │  🟢    │  <1%                              │
│  Deutsche Bank        │   $2.0m     │ 10%  │  🟢    │   2%                              │
│  Vodafone             │   $1.8m     │  9%  │  🟢    │   4%                              │
│  BP                   │   $1.5m     │  8%  │  🟢    │   3%                              │
│  HSBC                 │   $1.4m     │  7%  │  🟢    │   2%                              │
│  Shell                │   $1.3m     │  7%  │  🟢    │   2%                              │
│  Barclays             │   $1.1m     │  6%  │  🟢    │   3%                              │
│  GlaxoSmithKline      │   $1.0m     │  5%  │  🟢    │   2%                              │
│  Rio Tinto            │   $0.9m     │  5%  │  🟢    │   4%                              │
│  BT Group             │   $0.8m     │  4%  │  🟢    │   5%                              │
│                                                                                         │
│  FX CONCENTRATIONS                      SECTOR CONCENTRATIONS                           │
│  ─────────────────────                  ─────────────────────                           │
│  USD: 28% 🟡                            Financials: 22% 🟢                              │
│  EUR: 25% 🟡                            Energy: 18% 🟢                                  │
│  JPY: 15% 🟢                            Industrials: 15% 🟢                             │
│  GBP: 12% 🟢                            Healthcare: 12% 🟢                              │
│  AUD:  8% 🟢                            Technology: 11% 🟢                              │
│                                                                                         │
│  🟢 = Green (within limit)  🟡 = Amber (warning)  🔴 = Red (breach)                     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Control Testing Schedule

| Control | Test Frequency | Test Type | Tester |
|---------|---------------|-----------|--------|
| CN-C01 | Monthly | Sample testing | Internal Audit |
| CN-C02 | Monthly | Sample testing | Internal Audit |
| CN-C03 | Monthly | Sample testing | Internal Audit |
| CN-C04 | Quarterly | Data validation | Market Risk |
| CN-C05 | Quarterly | Sector mapping review | Market Risk |
| CN-C06 | Quarterly | Country classification review | Market Risk |
| CN-C07 | Monthly | Full reconciliation | RAV |
| CN-C08 | Semi-annually | Scenario testing | Operational Risk |
| CN-C09 | Monthly | Report review | Market Risk |
| CN-C10 | Quarterly | Methodology review | Model Risk |
| CN-C11 | Ongoing | Attendance/minutes | MLRC Secretary |
| CN-C12 | Quarterly | Methodology review | Market Risk |
| CN-C13 | Quarterly | Sample testing | Internal Audit |
| CN-C14 | Quarterly | ICAAP reconciliation | Finance |

---

## 8. Key Risk Indicators (KRIs)

| KRI ID | Indicator | Threshold | Escalation |
|--------|-----------|-----------|------------|
| KRI-CN-01 | Number of concentration breaches per month | >3 | MLRC |
| KRI-CN-02 | Single issuer at >10% concentration | Any | Market Risk |
| KRI-CN-03 | Positions at >8% ADV | >5 | MLRC |
| KRI-CN-04 | Diversification benefit | >40% | Model Risk |
| KRI-CN-05 | Sector at >20% concentration | Any | MLRC |
| KRI-CN-06 | EM country at >15% concentration | Any | Market Risk |
| KRI-CN-07 | Aged inventory (>6 months, <10% turnover) | >$5m aggregate | ALCO |
| KRI-CN-08 | Stale positions (>12 months, <2% turnover) | Any | MLRC |

---

## 9. Related Controls

| Control ID | Control Name | Relationship |
|------------|--------------|--------------|
| MR-L5-001 | VaR Limits Controls | Complementary - VaR captures aggregate risk |
| MR-L5-002 | Stress Limits Controls | Complementary - stress captures tail |
| MR-L5-003 | Sensitivity Limits Controls | Related - granular risk factor limits |
| MR-L5-007 | ECAP Controls | Related - aged inventory feeds ECAP illiquidity add-on |
| MR-L4-014 | Aged Inventory Monitoring | Upstream process - source for CN-C13/CN-C14 |
| CR-L5-001 | Credit Concentration Controls | Related - credit-specific concentration |

---

## 10. Document Control

### 10.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |
| 1.1 | 2025-01-15 | Added Section 3: Risk Engine Integration - explicit linkage to MR-L4-006 Section 6.6 concentration outputs, Component VaR methodology, and data flow from RISK_CONC_* tables | MLRC |
| 1.2 | 2025-01-16 | Added CN-C13 (Aged Inventory Identification) and CN-C14 (Aged Inventory ICAAP Contribution) controls; linked to MR-L4-014 and MR-L5-007 | MLRC |

### 10.2 Review Schedule

- Full review: Annually (January)
- Limit calibration: Annually or on material portfolio change
- ADV data sources: Quarterly review

---

*End of Document*
