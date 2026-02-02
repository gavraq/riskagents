---
# Document Metadata
document_id: SENS-CFG-001
document_name: Sensitivities Feed - IT Configuration Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Technology Steering Committee

# Parent Reference
parent_document: MR-L7-003  # Feeds Overview
feed_id: SENS-001
brd_reference: SENS-BRD-001
---

# Sensitivities Feed - IT Configuration Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | SENS-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Approver** | Technology Steering Committee |

---

## 1. Purpose

This document describes the IT configuration in Murex for sensitivity calculations at Meridian Global Bank. It covers the system settings and configuration parameters that enable the business requirements specified in the Sensitivities BRD (SENS-BRD-001) to be calculated.

---

## 2. Murex Dataflow Overview

### 2.1 High-Level Architecture

The sensitivity calculation follows the Murex Global Operating Model pattern, with data flowing through the following components:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     SENSITIVITY CALCULATION DATAFLOW                                    │
│                     Meridian Global Bank                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  PROCESSING SCRIPTS                                                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Feeder Processing Scripts                  Extraction Processing Scripts       │    │
│  │  ─────────────────────────────              ─────────────────────────────────   │    │
│  │                                                                                 │    │
│  │  • LN_SENS_FDR (London)                     • LN_SENS_RPT (London)              │    │
│  │  • NY_SENS_FDR (New York)                   • NY_SENS_RPT (New York)            │    │
│  │  • HK_SENS_FDR (Hong Kong)                  • HK_SENS_RPT (Hong Kong)           │    │
│  │                                                                                 │    │
│  └──────────────────────────────────┬──────────────────────────────────────────────┘    │
│                                     │                                                   │
└─────────────────────────────────────┼───────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  FEEDERS AND SIMULATION VIEWS                                                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────┐                ┌─────────────────┐                                 │
│  │     FEEDER      │                │  SIMULATION     │                                 │
│  │                 │◄───────────────│     VIEW        │                                 │
│  │  TF_SENS_DELTA  │                │                 │                                 │
│  │  TF_SENS_VEGA   │                │  SV_FX_DELTA    │                                 │
│  │  TF_SENS_DV01   │                │  SV_FX_VEGA     │                                 │
│  │  TF_SENS_CS01   │                │  SV_IR_DV01     │                                 │
│  │                 │                │  SV_CR_CS01     │                                 │
│  └────────┬────────┘                └─────────────────┘                                 │
│           │                                                                             │
└───────────┼─────────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  DATAMART TABLES                                                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                                                                                 │    │
│  │  SB_SENS_DELTA.REP        │  FX Delta sensitivities                             │    │
│  │  SB_SENS_VEGA.REP         │  FX Vega sensitivities                              │    │
│  │  SB_SENS_DV01.REP         │  Interest rate DV01 sensitivities                   │    │
│  │  SB_SENS_CS01.REP         │  Credit spread CS01 sensitivities                   │    │
│  │  SB_SENS_GAMMA.REP        │  Gamma sensitivities                                │    │
│  │  SB_SENS_THETA.REP        │  Theta sensitivities                                │    │
│  │                                                                                 │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│           │                                                                             │
└───────────┼─────────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  EXTRACTION                                                                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Extraction Request: ER_SENS_ALL                                                │    │
│  │                                                                                 │    │
│  │  Output: MGB_Sens_{Region}_{YYYYMMDD}.csv                                       │    │
│  │                                                                                 │    │
│  │  Delivery Path: ./reports/today/eod                                             │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Summary

| Component Type | Component Name | Description |
|----------------|----------------|-------------|
| **Processing Script (Feeder)** | **_SENS_FDR | Regional feeder orchestration |
| **Batch of Feeders** | BF_SENS_** | Feeder batch per region |
| **Feeder/Dynamic Table** | TF_SENS_* | Individual sensitivity type feeders |
| **Simulation View** | SV_*_* | Murex calculation views |
| **Datamart Table** | SB_SENS_*.REP | Intermediate storage tables |
| **Processing Script (Extraction)** | **_SENS_RPT | Regional extraction orchestration |
| **Extraction Request** | ER_SENS_* | SQL extraction definition |

---

## 3. Market Data Sets

### 3.1 Market Data Configuration

Sensitivity calculations use the **official EOD market data sets** to ensure consistency with P&L and regulatory reporting:

| Region | Market Data Set | Description | Cut-off Time (GMT) |
|--------|-----------------|-------------|-------------------|
| **London** | LNCLOSE | London official close | 17:30 |
| **New York** | NYCLOSE | New York official close | 22:00 |
| **Hong Kong** | HKCLOSE | Hong Kong official close | 10:00 |

### 3.2 Market Data Set Assignment

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  MARKET DATA SET CONFIGURATION                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Region        │  Processing Centre  │  Market Data Set  │  Fallback Set                │
│  ───────────────────────────────────────────────────────────────────────────────────    │
│  London        │  LONDON             │  LNCLOSE          │  NYCLOSE (T-1)               │
│  New York      │  NEWYORK            │  NYCLOSE          │  LNCLOSE                     │
│  Hong Kong     │  HONGKONG           │  HKCLOSE          │  LNCLOSE                     │
│                                                                                         │
│  NOTE: Fallback sets are used only in BCP scenarios with Market Risk Head approval      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sensitivity Calculations

### 4.1 FX Delta Sensitivities

#### 4.1.1 Simulation View: SV_FX_DELTA

| Attribute | Configuration |
|-----------|---------------|
| **Simulation View Name** | SV_FX_DELTA |
| **Description** | FX Delta sensitivity calculation for linear FX products |
| **Mode** | Detailed (trade-level output) |
| **Base Currency** | USD |

**Outputs**:

| Output | Dictionary Path | Definition |
|--------|-----------------|------------|
| **FX_DELTA** | Risk Engine.Results.Outputs.Fx.Delta.Value | Spot Delta Hedge in USD. dHedge@spot/dS is the P&L variation for spot price variations. Converted to USD using zero-day FX spot rate. |
| **FX_DELTA2** | Risk Engine.Results.Outputs.Fx.Delta.Value | Discounted delta in USD. dValue@horizon/dS0 is the P&L variation for discounted spot variations. |

**Breakdowns**:

| Breakdown | Dictionary Path | Definition |
|-----------|-----------------|------------|
| **FXQUOT** | Risk Engine.Results.Outputs.Fx.Delta.FX contract.FX quotation | FX quotation of the FX contract (currency pair) |
| **Portfolio** | Standard.Portfolio | Portfolio of the trade |
| **Trade Number** | Standard.Trade Number | Unique trade identifier |
| **Legal Entity** | Standard.Legal Entity | Legal entity of the trade |
| **Status** | Standard.Status | Trade status (LIVE, MKT_OP, etc.) |
| **Currency** | Standard.Currency | Currency of the sensitivity |
| **Label** | Standard.Label | Instrument label |

**Output Settings**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  FX DELTA OUTPUT SETTINGS                                                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Setting                    │  Value                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Expressed in               │  Specific unit                                            │
│  Currency                   │  USD                                                      │
│  Display unit with title    │  No                                                       │
│  Delta definition           │  dHedge@spot/dS                                           │
│  Delta at bucket/date       │  Follows delta definition                                 │
│  FX option delta            │  Yes                                                      │
│  Flow                       │  Yes                                                      │
│  Mkt value                  │  Yes                                                      │
│  Family projection          │  On                                                       │
│  Family                     │  FXDELTA (USD vs all other currencies)                    │
│  Accrual mode               │  No                                                       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.1.2 Structured Bonds (STB) FX Delta

For structured bonds, a separate simulation view (SV_STB_FX_DELTA) is used with additional filters:

| Filter | Value | Purpose |
|--------|-------|---------|
| **Flow Currency** | Not equal to USD | Exclude USD flows |
| **Sec Type** | Structured | Include only structured products |

**Additional Outputs for STB**:

| Output | Definition |
|--------|------------|
| **Past and Future Flows** | Cashflows converted to USD using zero-day spot rate (no financing/discounting) |
| **FX Delta USD** | Calculated: IF (Flow_Currency <> "USD") THEN IF (Past_and_Future_Flows == 0) THEN FX_delta_STB ELSE Past_and_Future_Flows |

### 4.2 FX Vega Sensitivities

#### 4.2.1 Simulation View: SV_FX_VEGA_MATURITY

| Attribute | Configuration |
|-----------|---------------|
| **Simulation View Name** | SV_FX_VEGA_MATURITY |
| **Description** | FX Vega sensitivity calculation for non-linear FX products |
| **Mode** | Detailed (trade-level output) |
| **Base Currency** | USD |

**Outputs**:

| Output | Dictionary Path | Definition |
|--------|-----------------|------------|
| **fx_vega_usd** | Risk Engine.Results.Outputs.Fx.Vega.Value | FX Vega in USD. P&L impact of 1% move in implied volatility. Discounted from settlement date to today. |

**Breakdowns**:

| Breakdown | Dictionary Path | Definition |
|-----------|-----------------|------------|
| **Contract** | Formulas.FX contract.Label | Label of the FX contract (currency pair) |
| **vega_date** | Risk Engine.Results.Outputs.Fx.Vega.Date | Date at which underlying volatility is interpolated |
| **vega_pillar** | Risk Engine.Results.Outputs.Fx.Vega.Date | Maturity pillar for bucketing (using RISK_VIEW4 maturity set) |
| **parallel_fx_vega** | Risk Engine.Results.Outputs.Fx.Vega.Strike | Vega Strike (0, 5, 10, 25, etc.) of the volatility curve |
| **Instrument** | Risk Engine.Source.Trade.Elements | Instrument label (e.g., Quanto Forward Swap, QFX Range Accrual) |
| **Model** | Risk Engine.Source.Trade.Elements.Body.Body desc.Evaluation.Model | Default pricing model |

**Maturity Set Configuration (RISK_VIEW4)**:

| Pillar | Description |
|--------|-------------|
| O/N | Overnight |
| T/N | Tomorrow/Next |
| 1W, 2W | Weekly |
| 1M, 2M, 3M, 6M, 9M | Monthly |
| 1Y, 18M, 2Y, 3Y, 4Y, 5Y | Annual |
| 6Y, 7Y, 8Y, 9Y, 10Y | Long-dated |
| 12Y, 15Y, 20Y, 25Y, 30Y, 35Y | Ultra long-dated |

**Note**: Sensitivities are bucketed to these pillars. If a cashflow falls between pillar dates, the contribution is split between adjacent pillars proportionally.

### 4.3 Interest Rate Sensitivities (DV01)

#### 4.3.1 Simulation View: SV_IR_DV01

| Attribute | Configuration |
|-----------|---------------|
| **Simulation View Name** | SV_IR_DV01 |
| **Description** | Interest rate DV01 calculation |
| **Mode** | Detailed (trade-level output) |
| **Base Currency** | USD |
| **Bump Size** | 1 basis point (0.01%) |
| **Bump Direction** | Up |

**Tenor Buckets**:

| Bucket ID | Range | Description |
|-----------|-------|-------------|
| IR01 | 0-3M | Short-term |
| IR02 | 3-6M | Short-term |
| IR03 | 6M-1Y | Short-term |
| IR04 | 1-2Y | Medium-term |
| IR05 | 2-3Y | Medium-term |
| IR06 | 3-5Y | Medium-term |
| IR07 | 5-7Y | Long-term |
| IR08 | 7-10Y | Long-term |
| IR09 | 10-15Y | Long-term |
| IR10 | 15-20Y | Ultra long-term |
| IR11 | 20-30Y | Ultra long-term |
| IR12 | 30Y+ | Ultra long-term |

### 4.4 Credit Spread Sensitivities (CS01)

#### 4.4.1 Simulation View: SV_CR_CS01

| Attribute | Configuration |
|-----------|---------------|
| **Simulation View Name** | SV_CR_CS01 |
| **Description** | Credit spread CS01 calculation |
| **Mode** | Detailed (trade-level output) |
| **Base Currency** | USD |
| **Bump Size** | 1 basis point (0.01%) |
| **Bump Direction** | Up |

**Tenor Buckets**:

| Bucket ID | Range | Description |
|-----------|-------|-------------|
| CR01 | 0-1Y | Short-term |
| CR02 | 1-3Y | Medium-term |
| CR03 | 3-5Y | Medium-term |
| CR04 | 5-10Y | Long-term |
| CR05 | 10Y+ | Ultra long-term |

---

## 5. Portfolio Scoping

### 5.1 Portfolio Hierarchy (Bookman)

The portfolio scope is defined by Level 4 portfolio nodes in the Bookman hierarchy:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  PORTFOLIO SCOPE BY REGION                                                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  LONDON REGION                                                                          │
│  ─────────────────                                                                      │
│  Level 4 Nodes: FXLN, IRLN, LMLN, PMLN                                                  │
│                                                                                         │
│  NEW YORK REGION                                                                        │
│  ───────────────────                                                                    │
│  Level 4 Nodes: FXNY, IRNY, LMNY, PMNY                                                  │
│                                                                                         │
│  HONG KONG REGION                                                                       │
│  ────────────────────                                                                   │
│  Level 4 Nodes: FXHK, LMHK, PMHK                                                        │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Global Filters

| Filter Name | Description | Applied To |
|-------------|-------------|------------|
| **GF_LN_PORTFOLIOS** | London portfolio filter | London feeders |
| **GF_NY_PORTFOLIOS** | New York portfolio filter | New York feeders |
| **GF_HK_PORTFOLIOS** | Hong Kong portfolio filter | Hong Kong feeders |

### 5.3 Transaction Filters

| Filter | Value | Purpose |
|--------|-------|---------|
| **Deal Status** | Not DEAD | Exclude terminated trades |
| **Entity Set** | TRADING | Trading book only |
| **Book Type** | Trading Book | Regulatory scope |

---

## 6. Batch Configuration

### 6.1 Feeder Batches by Region

#### 6.1.1 London Region

| Batch | Processing Script | Global Filter | Portfolio Nodes | Feeders |
|-------|------------------|---------------|-----------------|---------|
| BF_SENS_LN | LN_SENS_FDR | GF_LN_PORTFOLIOS | FXLN, IRLN, LMLN, PMLN | TF_SENS_DELTA, TF_SENS_VEGA, TF_SENS_DV01, TF_SENS_CS01 |

#### 6.1.2 New York Region

| Batch | Processing Script | Global Filter | Portfolio Nodes | Feeders |
|-------|------------------|---------------|-----------------|---------|
| BF_SENS_NY | NY_SENS_FDR | GF_NY_PORTFOLIOS | FXNY, IRNY, LMNY, PMNY | TF_SENS_DELTA, TF_SENS_VEGA, TF_SENS_DV01, TF_SENS_CS01 |

#### 6.1.3 Hong Kong Region

| Batch | Processing Script | Global Filter | Portfolio Nodes | Feeders |
|-------|------------------|---------------|-----------------|---------|
| BF_SENS_HK | HK_SENS_FDR | GF_HK_PORTFOLIOS | FXHK, LMHK, PMHK | TF_SENS_DELTA, TF_SENS_VEGA, TF_SENS_DV01, TF_SENS_CS01 |

### 6.2 Feeder Dependencies

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  FEEDER DEPENDENCY CHAIN                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  [Market Data Snapshot] ──▶ [Valuation Batch] ──▶ [Sensitivity Feeders]                 │
│                                                                                         │
│  LNCLOSE (17:30)            VAL_LN (19:00)         BF_SENS_LN (22:00)                   │
│  NYCLOSE (22:00)            VAL_NY (00:00+1)       BF_SENS_NY (02:00+1)                 │
│  HKCLOSE (10:00)            VAL_HK (12:00)         BF_SENS_HK (14:00)                   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Processing Timeline

### 7.1 Daily Schedule (GMT)

| Time | Process | Region | Description |
|------|---------|--------|-------------|
| 17:30 | Market Data | LN | London EOD snapshot |
| 19:00 | Valuation | LN | London valuation batch |
| 22:00 | Sensitivity Feeder | LN | London sensitivity calculation |
| 22:00 | Market Data | NY | New York EOD snapshot |
| 00:00+1 | Valuation | NY | New York valuation batch |
| 02:00+1 | Sensitivity Feeder | NY | New York sensitivity calculation |
| 03:00+1 | Extraction | All | Regional extractions |
| 04:00+1 | Consolidation | All | Global feed consolidation |
| 05:30+1 | Feed Delivery | All | **Sensitivity Feed SLA** |

---

## 8. Error Handling

### 8.1 Calculation Failures

| Error Type | Detection | Action |
|------------|-----------|--------|
| **Position not valued** | Zero MTM with non-zero notional | Flag as ERROR, exclude from feed |
| **Sensitivity calculation failure** | NULL sensitivity output | Use T-1 sensitivity, flag with FALLBACK |
| **Market data missing** | Missing curve/vol surface | Use proxy data, flag with PROXY |
| **Model failure** | Pricing model exception | Escalate to L2 support |

### 8.2 Recovery Procedures

| Scenario | Procedure | RTO |
|----------|-----------|-----|
| Single position failure | Exclude and report | Continue |
| Multiple position failures (>10) | Pause batch, investigate | 30 minutes |
| Batch failure | Restart from checkpoint | 1 hour |
| Market data failure | Switch to fallback data | 30 minutes |

---

## 9. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Sensitivities BRD](./sensitivities-brd.md) | SENS-BRD-001 | Business requirements |
| [Sensitivities IDD](./sensitivities-idd.md) | SENS-IDD-001 | Interface specification |
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |

---

## 10. Document Control

### 10.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-02 | Initial version | Technology Steering Committee |

### 10.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Configuration audit | Quarterly | April 2025 |
| Batch schedule review | Monthly | February 2025 |

---

*End of Document*
