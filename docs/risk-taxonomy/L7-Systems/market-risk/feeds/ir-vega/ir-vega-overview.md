---
# Document Metadata
document_id: IRV-OVW-001
document_name: IR Vega Sensitivities - Feed Overview
version: 1.0
effective_date: 2025-01-13
next_review_date: 2026-01-13
owner: Market Risk Technology
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds/ir-vega
feed_family: IR Vega
document_type: Overview
---

# IR Vega Sensitivities - Feed Overview

## 1. Feed Summary

| Attribute | Value |
|-----------|-------|
| **Feed Name** | IR Vega Sensitivities |
| **Feed ID** | MR-FEED-IRV |
| **Asset Class** | Interest Rates |
| **Sensitivity Type** | IR Volatility (Vega) |
| **Source System** | Murex (VESPA Module) |
| **Business Owner** | Market Risk |
| **Technical Owner** | Market Risk Technology |

## 2. Purpose

The IR Vega Sensitivities feed provides trade-level interest rate volatility risk sensitivities (Vega) from Murex to downstream market risk systems. Vega measures the change in portfolio value for a 1% change in implied volatility, essential for managing option portfolios.

### 2.1 Key Use Cases

| Use Case | Description |
|----------|-------------|
| **VaR Calculation** | Input to Value-at-Risk models for options portfolios |
| **Limit Monitoring** | Daily monitoring against vega limits by desk, currency, maturity |
| **P&L Attribution** | Explaining daily P&L movements from volatility changes |
| **Hedging Decisions** | Identifying volatility exposures requiring hedge adjustment |
| **Regulatory Reporting** | FRTB vega risk charge calculations |
| **Stress Testing** | Volatility shock scenario analysis |

## 3. Feed Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    IR Vega Feed Architecture                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────────────┐                                          │
│   │  Processing Script  │                                          │
│   │   **_IRVEGA_FDR     │                                          │
│   └──────────┬──────────┘                                          │
│              │                                                      │
│              ▼                                                      │
│   ┌─────────────────────┐                                          │
│   │      Feeder         │                                          │
│   │   A_IRPV01_VEGA     │                                          │
│   └──────────┬──────────┘                                          │
│              │                                                      │
│              ▼                                                      │
│   ┌─────────────────────────────────────────────────────┐          │
│   │               Simulation View                        │          │
│   │              IRPV01_VEGAS                            │          │
│   │  ┌─────────────────────────────────────────────┐    │          │
│   │  │ Outputs (6 active + 9 hidden):              │    │          │
│   │  │ • Vega_Local, Vega_USD, Vega_ZAR           │    │          │
│   │  │ • ATM_Spread, Opt_Maturity, Opt_Mat_Date   │    │          │
│   │  │ • Underlying: Vega_Yield, Flat_Vega,       │    │          │
│   │  │   Normal_Vega (hidden)                      │    │          │
│   │  └─────────────────────────────────────────────┘    │          │
│   │  ┌─────────────────────────────────────────────┐    │          │
│   │  │ Breakdowns (13 active + 7 hidden):         │    │          │
│   │  │ • Currency, Trade Number, Portfolio        │    │          │
│   │  │ • Family, Group, Type, Typology           │    │          │
│   │  │ • Vol_nature, Strike, Und. Maturity       │    │          │
│   │  └─────────────────────────────────────────────┘    │          │
│   │  Filter: Opt_Maturity_Date NOT EMPTY                │          │
│   └──────────┬──────────────────────────────────────────┘          │
│              │                                                      │
│              ▼                                                      │
│   ┌─────────────────────┐                                          │
│   │   Datamart Table    │                                          │
│   │   A_IR_VEGA.REP     │ (also A_IRPV01_VEGA.REP)                │
│   └──────────┬──────────┘                                          │
│              │                                                      │
│              ▼                                                      │
│   ┌─────────────────────┐                                          │
│   │ Data Extractor      │     ┌──────────────────────┐            │
│   │ DE_IRD_PV01VEGA     │◄────┤ Reference Tables:    │            │
│   │                     │     │ • SB_RT_INDEX_REP    │            │
│   │ Extraction Request: │     │ • TBL_ADP_RT_RANGE   │            │
│   │ IRPV01_Vega_ZAR     │     │ • TBL_MD_FXSPOTS_REP │            │
│   └──────────┬──────────┘     └──────────────────────┘            │
│              │                                                      │
│              ▼                                                      │
│   ┌─────────────────────┐                                          │
│   │ Processing Script   │                                          │
│   │ **_VSPA_IRVEGA_RPT  │                                          │
│   └──────────┬──────────┘                                          │
│              │                                                      │
│              ▼                                                      │
│   ┌─────────────────────────────────────────────────────┐          │
│   │                  Output Feed                         │          │
│   │    MxMGB_MR_Rates_Vega_{Region}_{YYYYMMDD}.csv      │          │
│   │                                                      │          │
│   │    20 fields including:                              │          │
│   │    • Trade identifiers and attributes               │          │
│   │    • Option/Underlying maturity pillars             │          │
│   │    • Strike and ATM Spread                          │          │
│   │    • Vega in local currency, USD, ZAR               │          │
│   └─────────────────────────────────────────────────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 4. Volatility Type Selection Logic

A key feature of the IR Vega feed is the formula-based selection of the appropriate vega output based on product type and volatility nature:

```
┌─────────────────────────────────────────────────────────────────────┐
│                  Vega Output Selection Logic                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ IF Group = "CF" AND Vol_nature <> "Normal"                  │  │
│   │ THEN → Use Flat_Vega outputs                                │  │
│   │        (Cap/Floor with non-normal volatility)               │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                           │                                         │
│                           ▼ ELSE IF                                 │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ (Group IN ("OSWP", "CF") OR                                 │  │
│   │  Typology IN ("CRD - GUARANTEE", "CRD - INSURANCE",         │  │
│   │              "IRD - CAPS/FLOORS"))                          │  │
│   │ AND Vol_nature = "Normal"                                   │  │
│   │ THEN → Use Normal_Vega outputs                              │  │
│   │        (Swaptions, Cap/Floors with normal vol)              │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                           │                                         │
│                           ▼ ELSE                                    │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ All other products                                          │  │
│   │ THEN → Use Vega_Yield outputs                               │  │
│   │        (Default yield-based vega)                           │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.1 Volatility Types Explained

| Volatility Type | Applicable Products | Description |
|-----------------|---------------------|-------------|
| **Flat Vega** | Cap/Floor (non-normal vol) | Vega from cap volatility (par/flat volatilities) |
| **Normal Vega** | Swaptions, Cap/Floor (normal vol) | Vega assuming normal distribution |
| **Vega Yield** | Other IR options | Sensitivity to yield volatility |

## 5. Regional Processing

### 5.1 Regional Configuration

| Region | Processing Script | Market Data Set | Feeder Batches |
|--------|-------------------|-----------------|----------------|
| **LDN** | LN_IRVEGA_FDR | LNCLOSE | 3 (legacy split) |
| **HKG** | HK_IRVEGA_FDR | HKCLOSE | 1 |
| **NYK** | NY_IRVEGA_FDR | NYCLOSE | 1 |
| **SAO** | SP_IRVEGA_FDR | SPCLOSE | 1 |

### 5.2 London Three-Batch Configuration

London region requires 3 separate feeder batches due to historical Murex processing constraints:

| Batch | Global Filter | Portfolio Coverage |
|-------|---------------|-------------------|
| BF_PRVIRVEA_LN | BF_PRVIRVEA_LN | FXDLN, PMLN |
| BF_PRVIRVEB_LN | BF_PRVIRVEB_LN | IRLNSBL |
| BF_PRVIRVEC_LN | BF_PRVIRVEC_LN | LMLNSBL |

## 6. Special Handling: Range Accruals

Range accrual products require special currency handling through reference table joins:

```
┌─────────────────────────────────────────────────────────────────────┐
│                Range Accrual Currency Resolution                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   A_IR_VEGA.REP ──► TBL_ADP_RT_RANGE_REP ──► SB_RT_INDEX_REP       │
│   (Trade Number)    (Range Definition)        (Index Currency)      │
│                                                                     │
│   Currency = COALESCE(RT_INDEX.M_CURRENCY, IR_VEGA.M_CURRENCY)     │
│                                                                     │
│   If range accrual → use index currency                            │
│   Otherwise        → use trade currency                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 7. Comparison with Other IR Feeds

| Attribute | IR Delta & Gamma | IR Zero Basis | IR PDG | **IR Vega** |
|-----------|------------------|---------------|--------|-------------|
| **Sensitivity** | DV01, Gamma | Basis Zero | Par Delta, Gamma | Volatility |
| **Rate Type** | Zero rates | Basis spreads | Par rates | Vol surface |
| **Product Focus** | All IR | Basis swaps | Hedge attribution | Options |
| **Maturity Pillars** | RISK_VIEW | RISK_VIEW | RISK_VIEW | Option/Underlying |
| **Formula Outputs** | No | No | No | **Yes** |
| **Business Owner** | Market Risk | Market Risk | Product Control | Market Risk |

## 8. Output Specification

| Attribute | Value |
|-----------|-------|
| **File Format** | CSV (semicolon-delimited) |
| **File Pattern** | MxMGB_MR_Rates_Vega_{Region}_{YYYYMMDD}.csv |
| **Field Count** | 20 |
| **Delivery Method** | MFT (Managed File Transfer) |
| **Destinations** | Plato, RDS |
| **Package** | MxGTS_Vespa_Sensitivities_{Region}_{YYYYMMDD}.zip |

## 9. Key Features

### 9.1 Distinctive Characteristics

| Feature | Description |
|---------|-------------|
| **Formula-based outputs** | Vega type selected based on product and vol nature |
| **Two-dimensional pillars** | Both option maturity AND underlying maturity |
| **ATM spread tracking** | Distance from ATM for smile curve position |
| **Range accrual handling** | Special currency resolution via index lookup |
| **Multiple vega types** | Flat, Normal, and Yield vega calculations |

### 9.2 Filter Logic

The feed includes only trades with:
- Option Maturity Date NOT empty (ensures option-like products only)
- Family = 'IRD' OR Typology IN ('CRD - GUARANTEE', 'CRD - INSURANCE')
- Group <> 'OPT' (excludes bond options)
- Legal Entity <> 'SBSA' (SBSA exclusion)

## 10. Document Suite

| Document | Purpose | Status |
|----------|---------|--------|
| **Overview** (this document) | High-level feed description | Current |
| **BRD** | Business requirements | [ir-vega-brd.md](ir-vega-brd.md) |
| **IT Config** | Murex GOM configuration | [ir-vega-config.md](ir-vega-config.md) |
| **IDD** | Interface design document | [ir-vega-idd.md](ir-vega-idd.md) |

---

*Document generated as part of the Meridian Global Bank Risk Taxonomy Framework*
