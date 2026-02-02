---
# Document Metadata
document_id: CR-DZ-CFG-001
document_name: CR Delta Zero Feed - IT Configuration
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: CR-DZ-BRD-001
feed_id: CR-DZ-001
---

# CR Delta Zero Feed - IT Configuration

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-DZ-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Executive Summary

This document specifies the IT configuration for extracting CR Delta Zero (Credit Spread CS01 - Zero Curve) data from Murex and delivering it to downstream risk systems (Plato, RDS, VESPA). The CR Delta Zero feed is part of the broader Credit Sensitivities feed suite, sharing common infrastructure with 7 other CR sensitivity feeds.

### 1.1 Credit Sensitivities Architecture

The Credit Sensitivities extraction uses two parallel data flows:

| Data Flow | Products | Simulation View | Datamart Table |
|-----------|----------|-----------------|----------------|
| **Non-CRDI** | CDS, Bonds, CLNs | VW_Vespa_Sensitivities | TBL_VESPA_SENS.REP |
| **CRDI** | Credit Indices | VW_Vespa_Sensitivities_CRDI | TBL_VESPA_SENSCI.REP |

---

## 2. System Architecture

### 2.1 High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MUREX TRADING SYSTEM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    CREDIT TRADES                                      │   │
│  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐               │   │
│  │   │    CDS      │    │   Bonds     │    │    CRDI     │               │   │
│  │   │ (Single-    │    │ (Credit-    │    │  (Credit    │               │   │
│  │   │   name)     │    │   linked)   │    │   Indices)  │               │   │
│  │   └─────────────┘    └─────────────┘    └─────────────┘               │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                    ┌───────────────┴───────────────┐                        │
│                    ▼                               ▼                         │
│  ┌─────────────────────────────┐   ┌─────────────────────────────┐         │
│  │   VW_Vespa_Sensitivities    │   │ VW_Vespa_Sensitivities_CRDI │         │
│  │        (Non-CRDI)           │   │         (CRDI only)         │         │
│  │   15 outputs, 15 breakdowns │   │   7 outputs, 11 breakdowns  │         │
│  └─────────────────────────────┘   └─────────────────────────────┘         │
│                    │                               │                         │
│                    ▼                               ▼                         │
│  ┌─────────────────────────────┐   ┌─────────────────────────────┐         │
│  │     TF_VESPA_SENS           │   │    TF_VESPA_SENS_CRDI       │         │
│  │       (Feeder)              │   │        (Feeder)             │         │
│  └─────────────────────────────┘   └─────────────────────────────┘         │
│                    │                               │                         │
│                    ▼                               ▼                         │
│  ┌─────────────────────────────┐   ┌─────────────────────────────┐         │
│  │   TBL_VESPA_SENS.REP        │   │   TBL_VESPA_SENSCI.REP      │         │
│  │     (Datamart Table)        │   │     (Datamart Table)        │         │
│  └─────────────────────────────┘   └─────────────────────────────┘         │
│                    │                               │                         │
└────────────────────┼───────────────────────────────┼─────────────────────────┘
                     │                               │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           EXTRACTION LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │               DE_VESPA_CR_DELTA / ER_VESPA_CR_DELTA                  │   │
│  │                     (Data Extractor / Request)                        │   │
│  │                                                                       │   │
│  │   SQL Query joins:                                                    │   │
│  │   - TBL_VESPA_SENS_REP (Non-CRDI, M_GROUP <> 'CRDI')                 │   │
│  │   - TBL_VESPA_SENSCI_REP (CRDI, M_GROUP = 'CRDI')                    │   │
│  │   - SB_CP_REP (Counterparty/Issuer)                                  │   │
│  │   - SB_TP_REP / SB_TP_EXT_REP / SB_TP_BD_REP (Transaction)           │   │
│  │   - TBL_SE_ROOT_REP / SB_SE_HEAD_REP (Security)                      │   │
│  │   - TBL_CRD_RECOVERY_REP (Credit/Recovery)                           │   │
│  │   - SB_CRI_DEF_REP (Credit Index Definition)                         │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                     │                                        │
│                                     ▼                                        │
│               ┌─────────────────────────────────────────┐                   │
│               │     MxMGB_MR_Credit_CS01_**.csv         │                   │
│               │         (Output File)                   │                   │
│               └─────────────────────────────────────────┘                   │
│                                     │                                        │
└─────────────────────────────────────┼────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DELIVERY LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐         ┌──────────────────────┐                  │
│  │  process_reports.sh  │────────►│   ZIP Package        │                  │
│  │  (Compress/Package)  │         │   MxMGB_MR_Credit_   │                  │
│  └──────────────────────┘         │   Sens_Region_       │                  │
│                                   │   Date.zip           │                  │
│                                   └──────────────────────┘                  │
│                                            │                                 │
│                              ┌─────────────┼─────────────┐                  │
│                              ▼             ▼             ▼                  │
│                    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐         │
│                    │    Plato    │ │     RDS     │ │   VESPA     │         │
│                    │ (VaR Engine)│ │             │ │ (Reporting) │         │
│                    └─────────────┘ └─────────────┘ └─────────────┘         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Summary

| Component | Type | Purpose |
|-----------|------|---------|
| VW_Vespa_Sensitivities | Simulation View | Calculate credit sensitivities (Non-CRDI) |
| VW_Vespa_Sensitivities_CRDI | Simulation View | Calculate credit sensitivities (CRDI) |
| TF_VESPA_SENS | Feeder | Feed Non-CRDI data to datamart |
| TF_VESPA_SENS_CRDI | Feeder | Feed CRDI data to datamart |
| TBL_VESPA_SENS.REP | Datamart Table | Store Non-CRDI sensitivities |
| TBL_VESPA_SENSCI.REP | Datamart Table | Store CRDI sensitivities |
| DE_VESPA_CR_DELTA | Data Extractor | Extract CR Delta Zero data |
| ER_VESPA_CR_DELTA | Extraction Request | Configure extraction parameters |

---

## 3. Murex GOM Configuration

### 3.1 Simulation Views

#### 3.1.1 Non-CRDI Simulation View

**View Name**: `VW_Vespa_Sensitivities`

| Property | Value |
|----------|-------|
| **View Type** | Credit Sensitivity Simulation |
| **Product Filter** | All credit products except CRDI |
| **Output Count** | 15 outputs |
| **Breakdown Count** | 15 breakdowns |

**Outputs Configured**:

| Output | Dictionary Path | Description |
|--------|-----------------|-------------|
| Asset spread (par) | Formulas.PL security/future.Long future.Cheapest data.Market data.Spread.Asset swap (par).Value | Future asset swap spread |
| **CR01 (zero)** | RiskEngine.Results.Outputs.Credit.Delta.Zero.Value | **Credit delta based on zero/default spreads (USD)** |
| CR01 (par) | RiskEngine.Results.Outputs.Credit.Delta.Par.Value | Credit delta based on par spreads (USD) |
| CR01 (par) quotation | RiskEngine.Results.Outputs.Credit.Delta.Par quotation.Value | Credit delta based on market quotes (USD) |
| Recovery rate sens. | RiskEngine.Results.Outputs.Credit.Recovery rate sens.Value | Recovery rate sensitivity with propagation |
| Recovery rate 2 | RiskEngine.Results.Outputs.Credit.Recovery rate 2.Value | Recovery rate sensitivity without propagation |
| Credit par rate | RiskEngine.Results.Outputs.Credit.Delta.Par.Rate | Credit market rate |
| Equ Par Spread | RiskEngine.Results.Outputs.Credit.Delta.Par.Equ Par Spread | Equivalent par spread |
| Value (Interpolated spread) | RiskEngine.Results.Outputs.Credit.Interpolated spread.Value | Interpolated default spread |
| Eval spread | Formulas.PL security/future.Bond.Market data.Spread.Quoted.Value | Bond evaluation spread |
| Capital factor | RiskEngine.Results.Flows.Security flows.Security/future.Bond.Market data.Capital factor | Amortization × indexation factor |
| Zero spread | Formulas.PL security/future.Bond.Market data.Spread.Zero.Value | Bond zero coupon spread |
| CR01 (par) quotation local curr | RiskEngine.Results.Outputs.Credit.Delta.Par quotation.Value | CR01 in local currency |
| **CR01 (zero) local curr** | RiskEngine.Results.Outputs.Credit.Delta.Zero.Value | **Credit delta zero in local currency** |
| Corr01 | RiskEngine.Results.Outputs.Credit.Corr01.Corr01 | Correlation sensitivity (Monte Carlo) |

**Breakdowns Configured**:

| Breakdown | Dictionary Path | Description |
|-----------|-----------------|-------------|
| Issuer | Formulas.Issuer.Issuer name | Issuer label |
| Curve name (zero) | Formulas.Issuer.Issuer name | Credit curve for delta zero |
| Curve name (par) | RiskEngine.Results.Outputs.Credit.Delta.Par.Credit key.Curve key.Curve name | Credit curve for delta par |
| Date (zero) | RiskEngine.Results.Outputs.Credit.Delta.Zero.Date | Maturity pillar date |
| Currency | RiskEngine.Results.Outputs.Credit.Recovery rate 2.Credit key.Currency | Sensitivity currency |
| Currency2 | (Duplicate of Currency) | Sensitivity currency |
| Country | Formulas.Credit key.Issuer.Country.Description | Issuer country |
| Rate | RiskEngine.Results.Outputs.Credit.Recovery rate sens.Recovery rate.Rate | Recovery rate |

**Date Breakdown Settings**:
- Mat. Source: Native Curve
- Bucket type: Pillars
- Split Mode: Surrounding pillars (fractional allocation)

#### 3.1.2 CRDI Simulation View

**View Name**: `VW_Vespa_Sensitivities_CRDI`

| Property | Value |
|----------|-------|
| **View Type** | Credit Index Sensitivity Simulation |
| **Product Filter** | CRDI products only (Sns origin = index) |
| **Output Count** | 7 outputs |
| **Breakdown Count** | 11 breakdowns |

**Outputs Configured**:

| Output | Dictionary Path | Description |
|--------|-----------------|-------------|
| **CR01 (zero)** | RiskEngine.Results.Outputs.Credit.Delta.Zero.Value | **Credit delta zero (USD)** |
| CR01 (par) | RiskEngine.Results.Outputs.Credit.Delta.Par.Value | Credit delta par (USD) |
| CR01 (par) quotation | RiskEngine.Results.Outputs.Credit.Delta.Par quotation.Value | Credit delta quotation (USD) |
| Recovery rate sens. | RiskEngine.Results.Outputs.Credit.Recovery rate sens.Value | Recovery rate sensitivity |
| Recovery rate 2 | RiskEngine.Results.Outputs.Credit.Recovery rate 2.Value | Recovery rate 2 |
| CR01 (par) quotation local curr | RiskEngine.Results.Outputs.Credit.Delta.Par quotation.Value | CR01 in local currency |
| **CR01 (zero) local curr** | RiskEngine.Results.Outputs.Credit.Delta.Zero.Value | **CR01 zero in local currency** |

**Key Difference**: CRDI view applies filter `Sns origin = index` to capture only index-level sensitivities.

### 3.2 CR01 (Zero) Calculation Details

**Definition**: CR01 (Zero) is the derivative of NPV with respect to credit spreads, measuring the variation of NPV due to credit curve default spread variations.

| Property | Value |
|----------|-------|
| **Bump Size** | 1 basis point (0.01%) |
| **Curve Type** | Zero/Default spread curve |
| **Direction** | Parallel shift up |
| **FX Conversion** | Zero day FX spot rate to USD |
| **Discounting** | From settlement date to today |

**Output Settings** (Murex):
- Expressed in: Specific unit
- Currency: USD
- Risk expression: Sensitivity
- Index split: All
- Adjusted: No

---

## 4. Regional Configuration

### 4.1 Non-CRDI Regional Setup

| Region | Processing Script | Batch | Global Filter | Portfolio Nodes |
|--------|-------------------|-------|---------------|-----------------|
| **LN** | LN_MR_VESPA_SENS_FDR | BF_VESPASENS_LN | GF_LN_PFOLIOS_RD | FXDLN, IRLN, LMLN, PMLN |
| **HK** | HK_MR_VESPA_SENS_FDR | BF_VESPASENS_HK | GF_HK_PFOLIOS_RD | LMHK, PMSG |
| **NY** | NY_MR_VESPA_SENS_FDR | BF_VESPASENS_NY | GF_NY_PFOLIOS_RD | LMNY, PMNY |
| **SP** | SP_MR_VESPA_SENS_FDR | BF_VESPASENS_SP | GF_SP_PFOLIOS_RD | LMSP |

**Common Components** (Non-CRDI):
- Feeder: `TF_VESPA_SENS`
- Datamart Table: `TBL_VESPA_SENS.REP`
- Dynamic Table: `VW_GTS_Vespa_Sens`
- Simulation View: `VW_Vespa_Sensitivities`

### 4.2 CRDI Regional Setup

| Region | Processing Script | Batch | Global Filter | Portfolio Nodes |
|--------|-------------------|-------|---------------|-----------------|
| **LN** | LN_MR_VES_SENSCI_FDR | BF_VESPCRDI_LN | GF_LN_PFOLIOS_RD | FXDLN, IRLN, LMLN, PMLN |
| **HK** | HK_MR_VES_SENSCI_FDR | BF_VESPCRDI_HK | GF_HK_PFOLIOS_RD | LMHK, PMSG |
| **NY** | NY_MR_VES_SENSCI_FDR | BF_VESPCRDI_NY | GF_NY_PFOLIOS_RD | LMNY, PMNY |
| **SP** | SP_MR_VES_SENSCI_FDR | BF_VESPCRDI_SP | GF_SP_PFOLIOS_RD | LMSP |

**Common Components** (CRDI):
- Feeder: `TF_VESPA_SENS_CRDI`
- Datamart Table: `TBL_VESPA_SENSCI.REP`
- Dynamic Table: `VW_GTS_Vespa_Sens_CI`
- Simulation View: `VW_Vespa_Sensitivities_CRDI`

### 4.3 Market Data Sets

| Region | Market Data Set | Snapshot Time |
|--------|-----------------|---------------|
| **LN** | LNCLOSE | 18:30 GMT |
| **HK** | HKCLOSE | 10:30 GMT |
| **NY** | NYCLOSE | 22:00 GMT |
| **SP** | SPCLOSE | 10:30 GMT |

---

## 5. Extraction Configuration

### 5.1 Extraction Request

**Request Name**: `ER_VESPA_CR_DELTA`

| Property | Value |
|----------|-------|
| **Data Extractor** | DE_VESPA_CR_DELTA |
| **Output Format** | CSV (semicolon-delimited) |
| **Output Directory** | ./reports/today/eod |
| **File Pattern** | MxMGB_MR_Credit_CS01_{Region}_{Date}.csv |

### 5.2 SQL Extraction Query Structure

The extraction uses a UNION ALL of two queries:

**Part 1: Non-CRDI Query**
```sql
SELECT
  VSP.M_TRADE_NUM as TRADE_NUM,
  VSP.M_FAMILY as FAMILY,
  VSP.M_GROUP as GRP,
  VSP.M_TYPE as TYPE,
  VSP.M_TYPOLOGY as TYPOLOGY,
  VSP.M_PORTFOLIO as PORTFOLIO,
  VSP.M_PL_INSTRU as INSTRUMENT,
  CASE WHEN VSP.M_ISSUER IS NULL
       THEN VSP.M_PL_INSTRU
       ELSE VSP.M_ISSUER END as ISSUER,
  VSP.M_CURVE_NAM as CURVE_NAME,
  VSP.M_DATE__ZER as DTE,
  VSP.M_RATE as RECOVERY_RATE,
  VSP.M_CR01__ZE1 as CR01__PA1,
  VSP.M_CURRENCY as CURRENCY,
  CP.M_U_CIF_ID as CIF,
  CP.M_U_GLOBID as GLOBUS_ID,
  CP.M_U_RSK_CTRY as COUNTRY,
  CASE WHEN VSP.M_GROUP = 'BOND'
       THEN SE_HEAD.M_SE_CODE
       ELSE OBL.M_REF_OBLI1 END as ISIN,
  TP.M_TP_DTEEXP as MATURITY,
  OBL.M_REF_OBLIG as UNDERLYING,
  CASE WHEN OBL.M_RESTRUCTU = 'Yes'
       THEN OBL.M_RESTRUCTU
       ELSE 'NONE' END as RESTRUCT,
  -- Notional calculation (complex logic)
  CASE WHEN VSP.M_GROUP IN ('BOND','CDS')
       THEN CASE WHEN VSP.M_GROUP='BOND'
                 THEN TP_BD_2.M_TP_RTCCP02
                 ELSE ABS(TP_BD_2.M_TP_RTCCP02) END
       ELSE CASE WHEN TP.M_TP_BUY='S'
                 THEN (-1)*TP.M_TP_NOMINAL
                 ELSE TP.M_TP_NOMINAL END
  END as NOTIONAL,
  -- Market field
  CASE WHEN VSP.M_FAMILY IN('IRD','EQD')
       THEN TP_EXT.M_TP_SECMKT
       WHEN (VSP.M_FAMILY = 'CRD' AND VSP.M_GROUP = 'CDS')
       THEN (SELECT DISTINCT ROOT.M_SE_MARKET
             FROM DM.TBL_SE_ROOT_REP ROOT
             WHERE ROOT.M_SE_LABEL = OBL.M_REF_OBLI2)
       ELSE '' END as MARKET,
  VSP.M_CR01__ZER as CR01_PA1
FROM DM.TBL_VESPA_SENS_REP VSP
  LEFT JOIN DM.SB_CP_REP CP ON (VSP.M_ISSUER = CP.M_DSP_LABEL)
  LEFT JOIN DM.TBL_CRD_RECOVERY_REP OBL ON (VSP.M_TRADE_NUM = OBL.M_NB)
  JOIN DM.SB_TP_REP TP ON (VSP.M_TRADE_NUM = TP.M_NB)
  JOIN DM.SB_TP_EXT_REP TP_EXT ON (VSP.M_TRADE_NUM = TP_EXT.M_NB)
  LEFT JOIN DM.SB_SE_HEAD_REP SE_HEAD ON (SE_HEAD.M_SE_D_LABEL = TP.M_INSTRUMENT)
  LEFT JOIN DM.SB_TP_BD_REP TP_BD_2 ON (VSP.M_TRADE_NUM = TP_BD_2.M_NB)
WHERE VSP.M_REF_DATA = @MxDataSetKey:N
  AND TP.M_TP_LENTDSP = @LegalEntity:C
  AND TP.M_STP_STATUS IN ('RELE','VERI','STTL')
  AND VSP.M_DATE__ZER IS NOT NULL
  AND VSP.M_ISSUER IS NOT NULL
  AND VSP.M_GROUP <> 'CRDI'
```

**Part 2: CRDI Query**
```sql
UNION ALL

SELECT
  VSP.M_TRADE_NUM as TRADE_NUM,
  VSP.M_FAMILY as FAMILY,
  VSP.M_GROUP as GRP,
  VSP.M_TYPE as TYPE,
  VSP.M_TYPOLOGY as TYPOLOGY,
  VSP.M_PORTFOLIO as PORTFOLIO,
  VSP.M_PL_INSTRU as INSTRUMENT,
  VSP.M_PL_INSTRU as ISSUER,  -- For CRDI, issuer = instrument label
  VSP.M_PL_INSTRU as CURVE_NAME,
  VSP.M_DATE as DTE,
  0 as RECOVERY_RATE,  -- Set to 0 for CRDI
  VSP.M_CR01__ZE1 as CR01__PA1,
  VSP.M_CURRENCY as CURRENCY,
  0 as CIF,
  '' as GLOBUS_ID,
  '' as COUNTRY,
  '' as ISIN,
  TP.M_TP_DTEEXP as MATURITY,
  '' as UNDERLYING,
  'NONE' as RESTRUCT,
  ABS(TP_BD.M_TP_RTCCP02) as NOTIONAL,
  '' as MARKET,
  VSP.M_CR01__ZER as CR01_PA1
FROM DM.TBL_VESPA_SENSCI_REP VSP
  JOIN DM.SB_TP_REP TP ON (VSP.M_TRADE_NUM = TP.M_NB)
  JOIN DM.SB_TP_BD_REP TP_BD ON (VSP.M_TRADE_NUM = TP_BD.M_NB)
  LEFT JOIN DM.SB_CRI_DEF_REP CRI ON (VSP.M_PL_INSTRU = CRI.M_INDEX_LBL)
WHERE VSP.M_REF_DATA = @MxDataSetKey:N
  AND TP.M_TP_LENTDSP = @LegalEntity:C
  AND TP.M_STP_STATUS IN ('RELE','VERI','STTL')
  AND VSP.M_GROUP = 'CRDI'
```

### 5.3 Extraction Filters

| Filter | Non-CRDI | CRDI | Purpose |
|--------|----------|------|---------|
| STP Status | RELE, VERI, STTL | RELE, VERI, STTL | Live deals only |
| Legal Entity | @LegalEntity:C (MGB) | @LegalEntity:C (MGB) | Single entity |
| Group | <> 'CRDI' | = 'CRDI' | Product separation |
| Issuer | IS NOT NULL | (uses instrument) | Must have issuer |
| Date Zero | IS NOT NULL | (uses Date) | Must have sensitivity |

---

## 6. Batch Processing

### 6.1 Processing Sequence

| Step | Job Name | Description | Dependency | Duration |
|------|----------|-------------|------------|----------|
| 1 | BJ_CREDIT_CURVE_CAL | Calibrate credit curves | Market data loaded | 30 min |
| 2 | BJ_VALUATION_CR | Run credit valuation | BJ_CREDIT_CURVE_CAL | 45 min |
| 3 | BF_VESPASENS_{Region} | Run Non-CRDI feeder | BJ_VALUATION_CR | 30 min |
| 4 | BF_VESPCRDI_{Region} | Run CRDI feeder | BJ_VALUATION_CR | 15 min |
| 5 | **_MR_VESPA_D_RPT | Extract CR Delta Zero | Feeders complete | 20 min |
| 6 | process_reports.sh | Package all CR feeds | Extraction complete | 5 min |
| 7 | MFT Transfer | Deliver to downstream | Package complete | 10 min |

### 6.2 Batch Schedule

| Job | Schedule | Start Time | SLA |
|-----|----------|------------|-----|
| BJ_CREDIT_CURVE_CAL | Daily | 18:00 GMT | 18:30 |
| BJ_VALUATION_CR | Daily | 18:30 GMT | 19:30 |
| BF_VESPASENS_LN | Daily | 19:30 GMT | 20:30 |
| BF_VESPCRDI_LN | Daily | 19:30 GMT | 20:00 |
| LN_MR_VESPA_D_RPT | Daily | 20:30 GMT | 21:30 |
| process_reports.sh | Daily | 21:30 GMT | 22:00 |
| MFT Transfer | Daily | 22:00 GMT | 05:30 |

---

## 7. Datamart Tables

### 7.1 TBL_VESPA_SENS.REP (Non-CRDI)

| Column | Data Type | Description |
|--------|-----------|-------------|
| M_REF_DATA | NUMBER | Market data set reference |
| M_TRADE_NUM | NUMBER | Trade number |
| M_FAMILY | VARCHAR2(16) | Trade family (CRD, IRD) |
| M_GROUP | VARCHAR2(5) | Trade group (CDS, BOND) |
| M_TYPE | VARCHAR2(16) | Trade type |
| M_TYPOLOGY | VARCHAR2(21) | Trade typology |
| M_PORTFOLIO | VARCHAR2(20) | Portfolio |
| M_PL_INSTRU | VARCHAR2(30) | PL Instrument |
| M_ISSUER | VARCHAR2(50) | Issuer label |
| M_CURVE_NAM | VARCHAR2(50) | Credit curve name |
| M_DATE__ZER | DATE | Date pillar (zero) |
| M_RATE | NUMBER | Recovery rate |
| M_CR01__ZER | NUMBER | CR01 (zero) in USD |
| M_CR01__ZE1 | NUMBER | CR01 (zero) in local currency |
| M_CURRENCY | VARCHAR2(4) | Currency |

### 7.2 TBL_VESPA_SENSCI.REP (CRDI)

| Column | Data Type | Description |
|--------|-----------|-------------|
| M_REF_DATA | NUMBER | Market data set reference |
| M_TRADE_NUM | NUMBER | Trade number |
| M_FAMILY | VARCHAR2(16) | Trade family |
| M_GROUP | VARCHAR2(5) | Trade group (CRDI) |
| M_TYPE | VARCHAR2(16) | Trade type |
| M_TYPOLOGY | VARCHAR2(21) | Trade typology |
| M_PORTFOLIO | VARCHAR2(20) | Portfolio |
| M_PL_INSTRU | VARCHAR2(30) | PL Instrument (=Index label) |
| M_DATE | DATE | Date pillar |
| M_CR01__ZER | NUMBER | CR01 (zero) in USD |
| M_CR01__ZE1 | NUMBER | CR01 (zero) in local currency |
| M_CURRENCY | VARCHAR2(4) | Currency |

---

## 8. Delivery Configuration

### 8.1 Packaging Script

**Script**: `process_reports.sh`

The script compresses and packages all 8 CR Sensitivity reports into a single ZIP file:

```bash
#!/bin/bash
REGION=$1
DATE=$2
OUTPUT_DIR="./reports/today/eod"
PACKAGE_NAME="MxMGB_MR_Credit_Sens_${REGION}_${DATE}.zip"

# Package all CR feeds
zip ${PACKAGE_NAME} \
  MxMGB_MR_Credit_CS01_${REGION}_${DATE}.csv \
  MxMGB_MR_Credit_CS01Par_${REGION}_${DATE}.csv \
  MxMGB_MR_Credit_Basis_${REGION}_${DATE}.csv \
  MxMGB_MR_Credit_ParCDS_${REGION}_${DATE}.csv \
  MxMGB_MR_Credit_Spread_${REGION}_${DATE}.csv \
  MxMGB_MR_Credit_Corr01_${REGION}_${DATE}.csv \
  MxMGB_MR_Credit_RR01_${REGION}_${DATE}.csv \
  MxMGB_MR_Credit_RR02_${REGION}_${DATE}.csv
```

### 8.2 MFT Configuration

| Property | Plato Delivery | RDS Delivery |
|----------|----------------|--------------|
| **MFT ID** | MurexGTSSensitivitiesToPlato_{Region} | MurexGTSSensitivitiesToRDS_{Region} |
| **Protocol** | SFTP | SFTP |
| **Source Path** | ./reports/today/eod | ./reports/today/eod |
| **File Pattern** | MxMGB_MR_Credit_Sens_*.zip | MxMGB_MR_Credit_Sens_*.zip |

### 8.3 Target Systems

| Target | Path | Format | Frequency |
|--------|------|--------|-----------|
| **Plato** | /plato/inbound/credit/ | ZIP containing CSVs | Daily |
| **RDS** | /rds/inbound/sensitivities/ | ZIP containing CSVs | Daily |
| **VESPA** | Via RDS forward | ZIP containing CSVs | Daily |

---

## 9. Monitoring and Alerting

### 9.1 Monitoring Checkpoints

| Checkpoint | Expected | Alert Threshold |
|------------|----------|-----------------|
| Credit curve calibration | 18:30 GMT | +30 min |
| Credit valuation complete | 19:30 GMT | +30 min |
| Non-CRDI feeder complete | 20:30 GMT | +30 min |
| CRDI feeder complete | 20:00 GMT | +30 min |
| Extraction complete | 21:30 GMT | +30 min |
| Package complete | 22:00 GMT | +15 min |
| Delivery to Plato | 05:30 GMT | +30 min |
| Row count | >5,000 | <4,000 or >10,000 |

### 9.2 Alert Distribution

| Severity | Recipients | Method |
|----------|------------|--------|
| Critical | L2 Support, Credit Risk Ops | Pager, SMS |
| High | Risk Technology | Email, Slack |
| Medium | Operations | Email |
| Low | Monitoring Dashboard | Dashboard only |

---

## 10. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [CR Delta Zero BRD](./cr-delta-zero-brd.md) | CR-DZ-BRD-001 | Business requirements |
| [CR Delta Zero IDD](./cr-delta-zero-idd.md) | CR-DZ-IDD-001 | Interface specification |
| [Credit Sensitivities Overview](../credit-sensitivities-overview.md) | CR-OV-001 | Suite overview |
| [Sensitivities IT Config](../sensitivities/sensitivities-config.md) | SENS-CFG-001 | General sensitivities |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-02 | Initial version | Risk Technology Change Board |

### 11.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Configuration audit | Quarterly | April 2025 |
| Performance review | Monthly | February 2025 |

---

*End of Document*
