---
# Process Metadata
process_id: MR-L4-005f
process_name: Proxying Process
version: 1.1
effective_date: 2025-01-16
next_review_date: 2026-01-15
owner: Head of Market Risk (analysis) / Head of RMA (approval) / Head of RAV (implementation)
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-005  # Time Series Management
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-003  # FRTB
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-002   # MLRC Terms of Reference
l7_systems:
  - SYS-MR-010  # Time Series Service
  - SYS-MR-012  # Proxy Tracking Tool (Jira)
---

# Proxying Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-005f |
| **Version** | 1.1 |
| **Effective Date** | 16 January 2025 |
| **Parent Process** | Time Series Management (MR-L4-005) |
| **Owner** | Head of Market Risk (analysis) / Head of RMA (approval) / Head of RAV (implementation) |

---

## 1. Purpose

The Proxying Process fills gaps in historical time series data when complete pricing data is not available for a risk factor. Proxies substitute missing data points with values derived from related risk factors, enabling:

- Complete time series for VaR calculation (500+ days)
- Coverage for new instruments without sufficient history
- Handling of data gaps from source failures or market closures

Without effective proxying, VaR calculations would be incomplete or impossible for instruments with limited price history.

---

## 2. When is Proxying Required?

### 2.1 Primary Triggers

| Trigger | Description | Example |
|---------|-------------|---------|
| **New instrument** | Instrument traded for first time with no history | New corporate bond issue |
| **New curve/surface** | Risk factor created without historical observations | New emerging market currency curve |
| **Data gaps** | Missing observations due to source failure or market closure | Bloomberg outage |
| **Insufficient history** | Risk factor exists but lacks required 500+ day history | Recently created tenor point |
| **FRTB modellability** | Risk factor fails MRF test (< 24 observations in 12 months) | Illiquid credit name |

### 2.2 Identification Methods

| Method | Description | Owner |
|--------|-------------|-------|
| **Automated detection** | Daily check for risk factors with gaps | Time Series Service |
| **New instrument workflow** | Triggered by Instrument Setup process | Operations/MDC |
| **Ultimate proxy report** | Daily review of auto-proxied risk factors | RAV |
| **Backtesting failures** | VaR backtest identifies missing data | RMA |

---

## 3. Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              PROXYING PROCESS                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         1. GAP IDENTIFICATION                                            │
│                                                                                          │
│  • Daily automated scan of all risk factors                                              │
│  • Flag risk factors with:                                                               │
│    - Missing history (< 500 days)                                                        │
│    - Missing leading edge (no current observation)                                       │
│    - Gaps in historical sequence                                                         │
│  • Generate gap report for RAV review                                                    │
│                                                                                          │
│  Owner: RAV (automated) → RAV/Market Risk (review)                                       │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         2. AUTO-PROXY SUGGESTION                                         │
│                                                                                          │
│  System suggests potential proxy candidates based on:                                    │
│  • Same asset class / risk type                                                          │
│  • Same currency / geography                                                             │
│  • Similar issuer characteristics (for credit)                                           │
│  • Historical correlation (where available)                                              │
│  • Country/issuer match                                                                  │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  Example: New EUR Corporate Bond (BBB rated, 5Y maturity)                           │ │
│  │                                                                                     │ │
│  │  Suggested proxies (ranked by relevance):                                           │ │
│  │  1. EUR IG BBB Corporate Curve (5Y point) - Same rating, currency, tenor            │ │
│  │  2. EUR IG A Corporate Curve (5Y point) - Adjacent rating bucket                    │ │
│  │  3. Same issuer existing bonds - Same issuer, different tenor                       │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  Owner: System (automated suggestion) → Market Risk (selection)                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         3. PROXY ANALYSIS                                                │
│                                                                                          │
│  Market Risk performs analysis to evaluate proxy quality:                                │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  QUANTITATIVE METRICS                                                               │ │
│  │                                                                                     │ │
│  │  • Correlation analysis: Proxy vs. proxied (including returns)                      │ │
│  │  • Volatility comparison: Relative volatility levels                                │ │
│  │  • Tracking error: Basis and its volatility (rolling annual)                        │ │
│  │  • Information ratio: (Proxy - Proxied) / StdDev of difference                      │ │
│  │                                                                                     │ │
│  │  Note: No strict numerical thresholds - reasonable judgement applied                │ │
│  │  Poor metrics may still be acceptable if no viable alternatives exist               │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  Owner: Market Risk                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         4. PROXY METHODOLOGY SELECTION                                   │
│                                                                                          │
│  Based on analysis, select appropriate proxy function (see Section 4):                   │
│                                                                                          │
│  • PF1 - Risk Factor with Variable/Fixed Basis (RFVB)                                    │
│  • PF2 - Linear Interpolation                                                            │
│  • PF3 - Flat Extrapolation on Calendar Spread (FECS)                                    │
│  • PF4 - Flat Extrapolation on Basis Spread (FEBS)                                       │
│  • PF5 - No Arbitrage Return (NAR)                                                       │
│  • Generic - Default fallback                                                            │
│  • Copy Forward - Last available value                                                   │
│                                                                                          │
│  For historical backfill, may also use:                                                  │
│  • Linear regression models                                                              │
│  • Brownian Bridge techniques                                                            │
│                                                                                          │
│  Owner: Market Risk (recommendation) → RMA (methodology approval)                        │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         5. APPROVAL                                                      │
│                                                                                          │
│  Joint approval required from:                                                           │
│  • Head of RMA - Methodology soundness                                                   │
│  • Head of Market Risk - Business appropriateness                                        │
│                                                                                          │
│  Approval documented in Proxy Tracking Tool (Jira) with:                                 │
│  • Analysis results                                                                      │
│  • Methodology selected                                                                  │
│  • Rationale for selection                                                               │
│  • Any monitoring exclusions                                                             │
│                                                                                          │
│  Owner: RMA + Market Risk                                                                │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         6. IMPLEMENTATION                                                │
│                                                                                          │
│  RAV implements approved proxy configuration:                                            │
│  • Configure proxy function in Time Series Service                                       │
│  • Backfill historical data (if required)                                                │
│  • Validate proxy generates expected values                                              │
│  • Enable for production                                                                 │
│                                                                                          │
│  Owner: RAV                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         7. MONITORING                                                    │
│                                                                                          │
│  Ongoing monitoring of proxy performance:                                                │
│  • Daily: Proxy values generated without error                                           │
│  • Monthly: Proxy & RniV Forum reviews proxy inventory                                   │
│  • Quarterly: Performance analysis (tracking error vs. actuals when available)           │
│                                                                                          │
│  Owner: RAV (daily) / RMA (periodic review)                                              │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Proxy Level Classification

### 4.1 Proxy Level Waterfall

Each time series observation is assigned a **Proxy Level** indicating the data quality and source. The system applies a waterfall logic, starting from Level 1 and progressing through levels until a valid observation is obtained.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           PROXY LEVEL WATERFALL                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  LEVEL 1: ACTUAL DATA                                                           │    │
│  │  ─────────────────────                                                          │    │
│  │  • Observation sourced directly from configured primary source                  │    │
│  │  • Passed all validation checks (stale, spike, zero)                            │    │
│  │  • No proxy applied                                                             │    │
│  │                                                                                 │    │
│  │  Label: proxy_level = "1", proxy_applied = FALSE                                │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                    │                                                    │
│                                    │ If Level 1 not available                           │
│                                    ▼                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  LEVEL 2: SPECIFIC PROXY                                                        │    │
│  │  ─────────────────────────                                                      │    │
│  │  • Proxy from closely related, pre-approved risk factor                         │    │
│  │  • Functions: RFVB (Risk Factor with Variable Basis), NAR (No Arbitrage)        │    │
│  │  • Requires specific proxy configuration in system                              │    │
│  │                                                                                 │    │
│  │  Label: proxy_level = "2", proxy_function = "RFVB" or "NAR"                     │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                    │                                                    │
│                                    │ If Level 2 not configured                          │
│                                    ▼                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  LEVEL 3: CURVE/SURFACE PROXY                                                   │    │
│  │  ────────────────────────────                                                   │    │
│  │  • Proxy derived from same curve/surface using mathematical techniques          │    │
│  │  • Functions: LinIntrp (Interpolation), FECS, FEBS (Extrapolation)              │    │
│  │  • Uses adjacent tenors/points from same risk factor                            │    │
│  │                                                                                 │    │
│  │  Label: proxy_level = "3", proxy_function = "LinIntrp", "FECS", or "FEBS"       │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                    │                                                    │
│                                    │ If Level 3 not applicable                          │
│                                    ▼                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  LEVEL 4: GENERIC / FALLBACK PROXY                                              │    │
│  │  ─────────────────────────────────                                              │    │
│  │  • Default proxy based on generic mapping rules                                 │    │
│  │  • Functions: Generic (mapping table), Copy Forward (last value)                │    │
│  │  • Least preferred option; triggers monitoring alert                            │    │
│  │                                                                                 │    │
│  │  Label: proxy_level = "4", proxy_function = "Generic" or "CF"                   │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Proxy Level Summary

| Level | Name | Quality | Functions | Approval | Monitoring |
|-------|------|---------|-----------|----------|------------|
| **1** | Actual Data | Highest | N/A | Automated | Standard |
| **2** | Specific Proxy | High | RFVB, NAR | Joint (RMA + MR) | Monthly review |
| **3** | Curve/Surface Proxy | Medium | LinIntrp, FECS, FEBS | Joint (RMA + MR) | Monthly review |
| **4** | Generic/Fallback | Low | Generic, CF | Joint (RMA + MR) | Daily alert; escalation |

### 4.3 Proxy Level Usage Targets

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| Level 1 (Actual) | >95% | >90% | MLRC if below threshold |
| Level 2 (Specific) | <3% | <5% | Monthly review |
| Level 3 (Curve/Surface) | <2% | <4% | Monthly review |
| Level 4 (Generic/Fallback) | <0.5% | <1% | Daily escalation |

---

## 5. Approved Proxy Functions

### 5.1 Function Overview

| Function | Code | Level | Description | Primary Use Cases |
|----------|------|-------|-------------|-------------------|
| **Risk Factor with Variable/Fixed Basis** | PF1 / RFVB | 2 | Set equal to another risk factor with optional basis adjustment | Short/long end curves; volatility surfaces |
| **No Arbitrage Return** | PF5 / NAR | 2 | Use no-arbitrage relationships | IR, FX, Commodities |
| **Linear Interpolation** | PF2 / LinIntrp | 3 | Interpolate between available data points | Curves and volatility surfaces (most versatile) |
| **Flat Extrapolation - Calendar Spread** | PF3 / FECS | 3 | Extrapolate using calendar spread assumptions | Short/long end curves and surfaces |
| **Flat Extrapolation - Basis Spread** | PF4 / FEBS | 3 | Extrapolate using basis spread assumptions | Primarily curves |
| **Generic** | Generic | 4 | Default fallback proxy | When no better alternative exists |
| **Copy Forward** | CF | 4 | Forward copy last available value | Fallback when no other proxy applies |

### 5.2 Function Details

#### PF1 - Risk Factor with Variable/Fixed Basis (RFVB)

**Methodology**: Set proxied risk factor equal to source risk factor plus/minus a basis adjustment.

```
Proxied_Value = Source_Value + Basis

Where Basis can be:
- Fixed: Constant spread (e.g., +50 bps)
- Variable: Calculated from historical relationship
```

**Use Cases**:
- Proxying short-end curve tenors from longer tenors
- Proxying illiquid credit names from index
- Proxying off-the-run bonds from benchmark

#### PF2 - Linear Interpolation (LinIntrp)

**Methodology**: Interpolate linearly between two known points.

```
Proxied_Value = Value_1 + (Value_2 - Value_1) × (T - T_1) / (T_2 - T_1)

Where:
T_1, T_2 = Known tenor points
T = Target tenor
```

**Use Cases**:
- Filling intermediate curve tenors
- Volatility surface tenor interpolation
- Most flexible proxy function

#### PF3 - Flat Extrapolation on Calendar Spread (FECS)

**Methodology**: Extrapolate using the assumption that calendar spread is flat beyond last known point.

```
Proxied_Value = Last_Known_Value + (Calendar_Spread × Time_Extension)
```

**Use Cases**:
- Long-end curve extrapolation
- Extending volatility surfaces beyond observed expiries

#### PF4 - Flat Extrapolation on Basis Spread (FEBS)

**Methodology**: Extrapolate using constant basis spread assumption.

```
Proxied_Value = Reference_Curve_Value + Fixed_Basis_Spread
```

**Use Cases**:
- Extending basis curves
- Currency-specific curve extensions

#### PF5 - No Arbitrage Return (NAR)

**Methodology**: Use no-arbitrage relationships between related risk factors.

```
Example: FX Forward = Spot × exp[(r_d - r_f) × T]
```

**Use Cases**:
- FX forward curves
- Interest rate parity relationships
- Commodity forward curves

---

## 6. Non-Approved Techniques (Historical Backfill Only)

For historical data upload where approved functions are unsuitable, other techniques may be used with proper analysis and approval:

### 6.1 Linear Regression

**Methodology**: Regress proxied risk factor on explanatory variables with sufficient history.

```
Proxied_Value = α + β × Explanatory_Variable + ε

Where coefficients calibrated on periods where both exist
```

**Requirements**:
- R² and coefficient stability analysis
- Out-of-sample validation
- RMA approval

### 6.2 Brownian Bridge

**Methodology**: Monte Carlo simulation to generate missing data points between known values.

```
Simulated path constrained to match:
- Known start point
- Known end point
- Volatility from comparable period
```

**Requirements**:
- Statistical validation of simulated paths
- RMA approval

---

## 7. Approval Workflow (Jira-Based)

### 7.1 Workflow Statuses

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           PROXY APPROVAL WORKFLOW                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────┐    ┌─────────────────┐    ┌───────────────────┐    ┌───────────────────┐   │
│  │ TO DO   │───▶│ MARKET RISK     │───▶│ READY FOR RMA     │───▶│ RAV               │   │
│  │         │    │ ANALYSIS        │    │ REVIEW            │    │ IMPLEMENTATION    │   │
│  └─────────┘    └─────────────────┘    └───────────────────┘    └───────────────────┘   │
│                                                                           │             │
│                                                                           ▼             │
│                                                                    ┌─────────┐          │
│                                                                    │ DONE    │          │
│                                                                    └─────────┘          │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

Status Descriptions:
• TO DO: Proxy need identified; Jira created by RAV or Market Risk
• MARKET RISK ANALYSIS: Analyst performing proxy selection analysis
• READY FOR RMA REVIEW: Analysis complete; awaiting RMA approval
• RAV IMPLEMENTATION: RMA approved; RAV implementing in system
• DONE: Proxy live in production; sign-off from all parties
```

### 7.2 Required Documentation

| Workflow Stage | Required Documentation |
|----------------|------------------------|
| **TO DO** | Risk factor ID, gap description, urgency |
| **MARKET RISK ANALYSIS** | Auto-proxy suggestions reviewed; analysis underway |
| **READY FOR RMA REVIEW** | Correlation analysis, proxy function recommendation, rationale |
| **RAV IMPLEMENTATION** | RMA approval email/comment, implementation plan |
| **DONE** | Validation results, production confirmation |

### 7.3 Exceptional Circumstances

Market Risk Managers may implement proxies **without pre-approval** under exceptional circumstances:

| Requirement | Description |
|-------------|-------------|
| **Same-day notification** | Inform RMA and Market Risk on implementation day |
| **Written justification** | Document reason for bypassing approval |
| **Post-implementation approval** | Obtain formal approval by Day 2 |

---

## 8. Asset-Class Specific Guidelines

### 8.1 FX & Rate Proxies

- Use same-currency proxies where possible
- Basis adjustments calibrated to recent spread history
- Cross-currency proxies require additional justification

### 8.2 Bond & CDS Proxies

- Same rating bucket preferred
- Same sector/industry considered
- Issuer-specific factors documented

### 8.3 Commodity Proxies

- Same commodity complex preferred
- Geographic basis considered
- Seasonal factors documented

---

## 9. History Splicing and Level Adjustment

When constructing time series history, discontinuities can arise from joining different data sources or from instrument roll events. These discontinuities create artificial "jumps" that would distort VaR calculations. This section describes techniques to ensure smooth, continuous time series.

### 9.1 The Discontinuity Problem

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    HISTORY SPLICING DISCONTINUITY                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Price                                                                                  │
│    │                                                                                    │
│    │                                          ┌─────── Real Data (new)                  │
│    │                                         /                                          │
│    │                              Jump ──▶  X                                           │
│    │                                       /                                            │
│    │  ─────────────────────────────────── X                                             │
│    │  Proxy/Old Data                       \                                            │
│    │                                        Transition Date                             │
│    │                                                                                    │
│    └──────────────────────────────────────────────────────────────────────────▶ Time    │
│                                                                                         │
│  Problem: The "jump" at transition creates an artificial return that will               │
│  distort VaR calculations and cause spurious backtesting exceptions.                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Scenarios Requiring Level Adjustment

| Scenario | Description | Typical Occurrence |
|----------|-------------|-------------------|
| **Proxy History Backfill** | New risk factor uses proxy for historical data; transition to real data when available | New instruments, new curves |
| **CDS Index Roll** | New on-the-run series replaces old series; level difference at roll | Semi-annual (March/September) |
| **Bond Roll** | Benchmark bond changes (e.g., new 10Y issue replaces old) | When new benchmark issued |
| **Source Change** | Time series switches from one data vendor to another | Ad-hoc |
| **Methodology Change** | Curve construction methodology updated | Rare; requires model approval |

### 9.3 Level Adjustment Techniques

#### 9.3.1 Constant Shift Adjustment (Standard Method)

The most common approach for handling discontinuities:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    CONSTANT SHIFT ADJUSTMENT                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Step 1: Calculate the level difference at transition date (T)                          │
│                                                                                         │
│          Δ = Real_Value(T) - Proxy_Value(T)                                             │
│                                                                                         │
│  Step 2: Apply adjustment to all historical proxy values                                │
│                                                                                         │
│          Adjusted_Proxy(t) = Proxy_Value(t) + Δ    for all t < T                        │
│                                                                                         │
│  Result: Continuous time series with no artificial jump at transition                   │
│                                                                                         │
│  Price                                                                                  │
│    │                                                                                    │
│    │                                          ┌─────── Real Data (unchanged)            │
│    │                                         /                                          │
│    │  ─────────────────────────────────────X─────── Smooth transition                   │
│    │  Adjusted Proxy (shifted up by Δ)                                                  │
│    │                                                                                    │
│    └──────────────────────────────────────────────────────────────────────────▶ Time    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Characteristics:**
- Simple to implement and explain
- Preserves historical return patterns from proxy
- Appropriate when proxy and real data have similar volatility dynamics

#### 9.3.2 Ratio Adjustment (Multiplicative Method)

For data where proportional relationships are more appropriate:

```
Adjustment_Ratio = Real_Value(T) / Proxy_Value(T)

Adjusted_Proxy(t) = Proxy_Value(t) × Adjustment_Ratio    for all t < T
```

**Use Cases:**
- Equity prices (stock splits, index rebalancing)
- FX rates
- Data where percentage moves are more meaningful than absolute moves

#### 9.3.3 Regression-Based Adjustment (Advanced Method)

For cases where the relationship between proxy and real data is more complex:

```
Step 1: Identify overlap period where both proxy and real data exist

Step 2: Regress real data on proxy data over overlap period:
        Real(t) = α + β × Proxy(t) + ε

Step 3: Apply regression to historical proxy data:
        Adjusted_Proxy(t) = α + β × Proxy(t)    for all t < T
```

**Characteristics:**
- Captures systematic differences in level AND sensitivity
- Requires overlap period with both data sources
- RMA approval required for regression parameters

### 9.4 CDS Index Roll Handling

CDS indices (iTraxx, CDX) roll to new series semi-annually. The new series typically trades at a different spread level due to:
- Constituent changes (defaults, fallen angels, rising stars)
- Updated reference obligations
- Market conditions at roll

#### 9.4.1 Standard CDS Index Roll Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    CDS INDEX ROLL ADJUSTMENT                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Roll Date: 20 March / 20 September                                                     │
│                                                                                         │
│  Step 1: On roll date, both old series (e.g., Series 40) and new series (Series 41)     │
│          trade simultaneously                                                           │
│                                                                                         │
│  Step 2: Calculate roll differential:                                                   │
│                                                                                         │
│          Δ_Roll = New_Series_Spread(Roll_Date) - Old_Series_Spread(Roll_Date)           │
│                                                                                         │
│  Step 3: Adjust historical time series:                                                 │
│                                                                                         │
│          For all dates t < Roll_Date:                                                   │
│          Adjusted_Spread(t) = Old_Series_Spread(t) + Δ_Roll                             │
│                                                                                         │
│  Step 4: For dates t ≥ Roll_Date:                                                       │
│          Use New_Series_Spread(t) directly                                              │
│                                                                                         │
│  Result: Single continuous time series representing "on-the-run" index spread           │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 9.4.2 CDS Index Roll Example

| Date | Series 40 (Old) | Series 41 (New) | Adjusted History |
|------|-----------------|-----------------|------------------|
| 15-Mar | 85 bps | - | 85 + 12 = 97 bps |
| 18-Mar | 83 bps | - | 83 + 12 = 95 bps |
| 19-Mar | 84 bps | - | 84 + 12 = 96 bps |
| **20-Mar (Roll)** | **86 bps** | **98 bps** | **98 bps** (Δ = 12 bps) |
| 21-Mar | - | 100 bps | 100 bps |
| 22-Mar | - | 97 bps | 97 bps |

#### 9.4.3 Roll Calendar

| Index | Roll Frequency | Roll Dates | Lead Time |
|-------|----------------|------------|-----------|
| **iTraxx Main** | Semi-annual | 20 Mar, 20 Sep | Roll announced ~2 weeks prior |
| **iTraxx Crossover** | Semi-annual | 20 Mar, 20 Sep | Roll announced ~2 weeks prior |
| **CDX IG** | Semi-annual | 20 Mar, 20 Sep | Roll announced ~2 weeks prior |
| **CDX HY** | Semi-annual | 20 Mar, 20 Sep | Roll announced ~2 weeks prior |

### 9.5 Controls for Level Adjustment

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| LA-C01 | Level adjustment methodology documented and approved | Preventive | RMA |
| LA-C02 | Adjustment delta calculated and logged | Detective | RAV |
| LA-C03 | Adjusted vs. unadjusted history retained for audit | Detective | RAV |
| LA-C04 | CDS index rolls processed within 2 business days | Preventive | RAV |
| LA-C05 | Material adjustments (>10% level change) escalated | Detective | Market Risk |

### 9.6 Data Retention

For audit and model validation purposes:

| Data Element | Retention | Purpose |
|--------------|-----------|---------|
| **Original proxy/old series data** | 7 years | Audit trail |
| **Adjustment parameters** | 7 years | Reproduce adjustments |
| **Adjusted time series** | Active use | VaR calculation |
| **Roll differential calculations** | 7 years | Validation |

---

## 10. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| PX-C01 | Proxy requires joint approval before production | Preventive | RMA + MR |
| PX-C02 | All proxies tracked in Proxy Tracking Tool | Detective | RAV |
| PX-C03 | Exceptional proxies approved within 2 days | Detective | RMA |
| PX-C04 | Monthly proxy inventory review | Detective | Proxy & RniV Forum |
| PX-C05 | Proxy performance monitored | Detective | RMA |
| PX-C06 | Proxy lineage captured in time series | Detective | RAV |

---

## 11. Governance Forums

### 11.1 Proxy & RniV Forum

| Attribute | Description |
|-----------|-------------|
| **Frequency** | Monthly |
| **Chair** | Head of RMA |
| **Attendees** | Market Risk, RAV, Model Validation |
| **Purpose** | Review proxy inventory; approve/retire proxies; monitor NMRF |

### 11.2 Forum Responsibilities

- Review summary of all active proxies
- Approve proxies excluded from monitoring
- Identify proxies for retirement (when actual data available)
- Review FRTB modellability status

---

## 12. Related Documents

| Document | Relationship |
|----------|--------------|
| [Time Series Management](./time-series-overview.md) | Parent process |
| [Risk Factor Setup](./risk-factor-setup.md) | Defines risk factors requiring proxies |
| [Cleaning & Validation](./cleaning-validation.md) | Identifies gaps requiring proxies |
| [Curve Stripping](./curve-stripping.md) | May require proxied inputs |
| [VaR/SVaR Methodology (MR-L6-001)](../../L6-Models/market-risk/var-svar-methodology.md) | Section 7.4 RNIV Framework; Section 7.5 Proxy Governance |

---

## 13. Document Control

### 13.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |
| 1.1 | 2025-01-16 | Added Proxy Level Classification (Section 4) with waterfall logic and usage targets; added cross-reference to VaR/SVaR Methodology | RMA |

---

*End of Document*
