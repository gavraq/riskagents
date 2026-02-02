---
# Document Metadata
document_id: SENS-IDD-001
document_name: Sensitivities Feed - Interface Definition Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: MLRC

# Parent Reference
parent_document: MR-L7-003  # Feeds Overview
feed_id: SENS-001
---

# Sensitivities Feed - Interface Definition Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | SENS-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Approver** | MLRC |

---

## 1. Executive Summary

This Interface Definition Document (IDD) specifies the technical implementation details for extracting sensitivity data from Murex and delivering it to downstream risk systems. It covers:

- **Feeders**: Process for populating Datamart tables from Simulation Views
- **Extraction**: SQL queries for extracting data from Datamart tables
- **Delivery**: File transfer mechanisms to downstream consumers

---

## 2. Murex Data Flow Architecture

### 2.1 Component Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MUREX DATA FLOW                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐                                                       │
│  │ Processing Script│     **_SENS_FDR (Feeder)                              │
│  │    Feeder        │     **_SENS_RPT (Extraction)                          │
│  └────────┬─────────┘                                                       │
│           │                                                                  │
│           ▼                                                                  │
│  ┌──────────────────┐                                                       │
│  │     Feeder       │     TF_SENS_*, A_SENS_*                               │
│  └────────┬─────────┘                                                       │
│           │                                                                  │
│           ▼                                                                  │
│  ┌──────────────────┐     ┌──────────────────┐                              │
│  │ Simulation View  │────▶│  Datamart Table  │                              │
│  │ SV_FX_DELTA      │     │ A_FXDELTA.REP    │                              │
│  │ SV_FX_VEGA       │     │ A_FXVEGA.REP     │                              │
│  │ SV_IR_DV01       │     │ A_IRDV01.REP     │                              │
│  │ SV_CR_CS01       │     │ A_CRCS01.REP     │                              │
│  └──────────────────┘     └────────┬─────────┘                              │
│                                    │                                         │
│                                    ▼                                         │
│                           ┌──────────────────┐                              │
│                           │   Extraction     │     DE_SENS_*, ER_SENS_*     │
│                           └────────┬─────────┘                              │
│                                    │                                         │
│                                    ▼                                         │
│                           ┌──────────────────┐                              │
│                           │      Feed        │     MGB_Sens_*_YYYYMMDD.csv  │
│                           └────────┬─────────┘                              │
│                                    │                                         │
│                                    ▼                                         │
│                           ┌──────────────────┐                              │
│                           │   MFT Delivery   │     SFTP to RAP              │
│                           └──────────────────┘                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Processing Sequence

| Step | Component | Description | Timing |
|------|-----------|-------------|--------|
| 1 | Market Data | Load official EOD market data set | 18:00-18:30 |
| 2 | Valuation | Complete position revaluation | 18:30-21:00 |
| 3 | Feeder | Execute feeders to populate Datamart | 21:00-23:00 |
| 4 | Extraction | Run SQL extraction to generate feeds | 23:00-01:00 |
| 5 | Packaging | Compress and package feed files | 01:00-02:00 |
| 6 | Delivery | Transfer via MFT to downstream | 02:00-05:30 |

---

## 3. Feeder Configuration

### 3.1 FX Delta Feeders

#### 3.1.1 Non-Structured Products

| Region | Processing Script | Batch | Global Filter | Portfolio Nodes | Feeder | Datamart Table | Simulation View |
|--------|-------------------|-------|---------------|-----------------|--------|----------------|-----------------|
| LDN | LN_FXDELTA_FDR | BF_FXDLT_LN | BF_FXDELTA_LN | FXDLN, FXLNLN, IRLNLN, LMLNLN, PMLN | A_FXDELTA | A_FXDELTA.REP | SV_FX_DELTA |
| NYK | NY_FXDELTA_FDR | BF_FXDLT_NY | BF_FXDELTA_NY | FXNYNY, LMNYNY, PMNY | A_FXDELTA | A_FXDELTA.REP | SV_FX_DELTA |
| HKG | HK_FXDELTA_FDR | BF_FXDLT_HK | BF_FXDELTA_HK | FXHKHK, LMHKHK, PMSG | A_FXDELTA | A_FXDELTA.REP | SV_FX_DELTA |

#### 3.1.2 Structured Products (STB)

| Region | Processing Script | Batch | Global Filter | Portfolio Nodes | Feeder | Datamart Table | Simulation View |
|--------|-------------------|-------|---------------|-----------------|--------|----------------|-----------------|
| LDN | LN_FXDELTA_STB_FDR | BF_FXDLT_STB_LN | BF_STBDELTA_LN | FXDLN, IRLNLN, LMLNLN, PMLN | A_FXDELTA_STB | A_FXDELTA_STB.REP | SV_FX_DELTA_STB |
| NYK | NY_FXDELTA_STB_FDR | BF_FXDLT_STB_NY | BF_STBDELTA_NY | FXNYNY, LMNYNY, PMNY | A_FXDELTA_STB | A_FXDELTA_STB.REP | SV_FX_DELTA_STB |
| HKG | HK_FXDELTA_STB_FDR | BF_FXDLT_STB_HK | BF_STBDELTA_HK | FXHKHK, LMHKHK, PMSG | A_FXDELTA_STB | A_FXDELTA_STB.REP | SV_FX_DELTA_STB |

### 3.2 FX Vega Feeders

| Region | Processing Script | Batch | Global Filter | Portfolio Nodes | Feeder | Datamart Table | Simulation View |
|--------|-------------------|-------|---------------|-----------------|--------|----------------|-----------------|
| LDN | LN_FXVEGA_FDR | BF_FXVEG_LN | GF_LN_PORTFOLIOS | FXDLN, IRLN, LMLN, PMLN | TF_FXVEGA_STKMAT | A_FXVEGA_STK.REP | SV_FX_VEGA_MATURITY |
| NYK | NY_FXVEGA_FDR | BF_FXVEG_NY | GF_NY_PORTFOLIOS | LMNY, PMNY | TF_FXVEGA_STKMAT | A_FXVEGA_STK.REP | SV_FX_VEGA_MATURITY |
| HKG | HK_FXVEGA_FDR | BF_FXVEG_HK | GF_HK_PORTFOLIOS | LMHK, PMSG | TF_FXVEGA_STKMAT | A_FXVEGA_STK.REP | SV_FX_VEGA_MATURITY |

### 3.3 Interest Rate DV01 Feeders

| Region | Processing Script | Batch | Global Filter | Portfolio Nodes | Feeder | Datamart Table | Simulation View |
|--------|-------------------|-------|---------------|-----------------|--------|----------------|-----------------|
| LDN | LN_IRDV01_FDR | BF_IRDV01_LN | GF_LN_PORTFOLIOS | IRLN, LMLN, PMLN | TF_IR_DV01 | A_IRDV01.REP | SV_IR_DV01 |
| NYK | NY_IRDV01_FDR | BF_IRDV01_NY | GF_NY_PORTFOLIOS | IRNY, LMNY, PMNY | TF_IR_DV01 | A_IRDV01.REP | SV_IR_DV01 |
| HKG | HK_IRDV01_FDR | BF_IRDV01_HK | GF_HK_PORTFOLIOS | IRHK, LMHK, PMSG | TF_IR_DV01 | A_IRDV01.REP | SV_IR_DV01 |

### 3.4 Credit CS01 Feeders

| Region | Processing Script | Batch | Global Filter | Portfolio Nodes | Feeder | Datamart Table | Simulation View |
|--------|-------------------|-------|---------------|-----------------|--------|----------------|-----------------|
| LDN | LN_CRCS01_FDR | BF_CRCS01_LN | GF_LN_PORTFOLIOS | CRLN, LMLN | TF_CR_CS01 | A_CRCS01.REP | SV_CR_CS01 |
| NYK | NY_CRCS01_FDR | BF_CRCS01_NY | GF_NY_PORTFOLIOS | CRNY, LMNY | TF_CR_CS01 | A_CRCS01.REP | SV_CR_CS01 |
| HKG | HK_CRCS01_FDR | BF_CRCS01_HK | GF_HK_PORTFOLIOS | CRHK, LMHK | TF_CR_CS01 | A_CRCS01.REP | SV_CR_CS01 |

### 3.5 Portfolio Filtering Rules

Portfolio filtering ensures completeness by selecting at Level 4 or Level 5 nodes in the Bookman hierarchy:

| Region | Level 4 Nodes | Level 5 Nodes (Selected) |
|--------|---------------|--------------------------|
| **London** | FXDLN, IRLN, LMLN, PMLN | All child portfolios except excluded |
| **New York** | PMNY, LMNY | All child portfolios |
| **Hong Kong** | PMSG, LMHK | All child portfolios |

**Filtering Criteria Applied:**
- Simulation Views include filters on:
  - Flow currency ≠ USD (for FX Delta)
  - Security Type = Structured (for STB products)
  - Deal Status = LIVE or MKT_OP
  - Entity Set = TRADING

---

## 4. Extraction Configuration

### 4.1 Extraction Process Overview

| Region | Processing Script | Batch | Single Extraction | Extraction Request |
|--------|-------------------|-------|-------------------|-------------------|
| LDN | LN_SENS_RPT | BE_SENS_LN | DE_SENS_LN | ER_SENS_ALL |
| NYK | NY_SENS_RPT | BE_SENS_NY | DE_SENS_NY | ER_SENS_ALL |
| HKG | HK_SENS_RPT | BE_SENS_HK | DE_SENS_HK | ER_SENS_ALL |

### 4.2 FX Delta Extraction SQL

The FX Delta extraction aggregates data from both STB and non-STB Datamart tables:

```sql
-- MGB FX Delta Extraction Request: ER_FXDELTA
-- Combines structured bonds and non-structured products

SELECT
    M_NB AS TRADE_NUMBER,
    M_PORTFOLIO AS PORTFOLIO,
    M_QUOTMODE0 AS CURRENCY_PAIR,
    CAST(CASE
        WHEN MAX(M_FXDELTA) != 0 THEN MAX(M_FXDELTA)
        ELSE MIN(M_FXDELTA)
    END AS NUMBER(22,2)) AS FX_DELTA,
    'USD' AS FX_DELTA_CCY,
    M_CLOSING_E AS CLOSING_ENTITY,
    M_LEGAL_ENT AS LEGAL_ENTITY,
    M_STATUS AS TRADE_STATUS
FROM (
    -- Part 1: Live deals from non-STB table
    SELECT
        pos.M_NB,
        pos.M_PORTFOLIO,
        pos.M_CLOSING_E,
        pos.M_LEGAL_ENT,
        pos.M_FXDELTA,
        pos.M_STATUS,
        pos.M_FXQUOT AS M_QUOTMODE0
    FROM DM.A_FXDELTA_REP pos
    JOIN DYN_AUDIT_REP aud ON pos.M_REF_DATA = aud.M_REF_DATA
    WHERE M_TAG_DATA = @LabelofData:C
      AND M_DELETED = 'N'
      AND M_OUTPUTTBL = 'A_FXDELTA.REP'
      AND M_STATUS IN ('LIVE', 'MKT_OP')
      AND @MxSQLExpression:C

    UNION ALL

    -- Part 2: Live deals from STB table
    SELECT
        stb.M_TRADE_NUM AS M_NB,
        stb.M_PORTFOLIO,
        stb.M_CLOSING_E,
        stb.M_LEGAL_ENT,
        stb.M_FX_DELTA1 AS M_FXDELTA,
        stb.M_STATUS,
        CASE
            WHEN stb.M_CURRENCY = stb.M_FLOW_CURR
            THEN stb.M_CURRENCY || '-' || stb.M_UNIT
            ELSE stb.M_CURRENCY || '-' || stb.M_FLOW_CURR
        END AS M_QUOTMODE0
    FROM DM.A_FXDELTA_STB_REP stb
    JOIN DYN_AUDIT_REP aud ON stb.M_REF_DATA = aud.M_REF_DATA
    WHERE M_TAG_DATA = @LabelofData:C
      AND M_DELETED = 'N'
      AND M_OUTPUTTBL = 'A_FXDELTA_STB.REP'
      AND M_STATUS IN ('LIVE', 'MKT_OP')

    UNION ALL

    -- Part 3: Dead/purged deals (aggregated)
    SELECT
        CAST(0 AS NUMBER(10,0)) AS M_NB,
        M_PORTFOLIO,
        M_CLOSING_E,
        M_LEGAL_ENT,
        SUM(M_FXDELTA) AS M_FXDELTA,
        '' AS M_STATUS,
        M_QUOTMODE0
    FROM DM.A_FXDELTA_REP pos
    WHERE M_STATUS NOT IN ('LIVE', 'MKT_OP') OR M_STATUS IS NULL
    GROUP BY M_PORTFOLIO, M_QUOTMODE0, M_CLOSING_E, M_LEGAL_ENT
) aa,
DM.TBL_FX_CNT_REP cnt
WHERE (
    (SUBSTR(aa.M_QUOTMODE0, 1, 3) = cnt.M_BASE AND SUBSTR(aa.M_QUOTMODE0, 5, 3) = cnt.M_UNDERLNG)
    OR
    (SUBSTR(aa.M_QUOTMODE0, 5, 3) = cnt.M_BASE AND SUBSTR(aa.M_QUOTMODE0, 1, 3) = cnt.M_UNDERLNG)
)
AND cnt.M_TYPE = 'OTC'
GROUP BY
    M_NB,
    M_PORTFOLIO,
    M_QUOTMODE0,
    M_CLOSING_E,
    M_LEGAL_ENT,
    M_STATUS
ORDER BY 2, 4, 1;
```

### 4.3 FX Vega Extraction SQL

```sql
-- MGB FX Vega Extraction Request: ER_FXVEGA
-- Extracts vega by strike and maturity

SELECT
    SBL.M_PORTFOLIO AS PORTFOLIO,
    SBL.M_TRADE_NUM AS TRADE_NUMBER,
    SBL.M_LABEL AS INSTRUMENT,
    CASE
        WHEN SBL.M_INSTRUMEN = 'QFX Range Accrua' THEN 'IRD_IRS_RA'
        WHEN SBL.M_INSTRUMEN = 'Quanto Forward S' THEN 'IRD_IRS_FX'
        WHEN SBL.M_INSTRUMEN = 'QIR Range Accrua' THEN 'IRD_IRS_RA'
        ELSE ''
    END AS INSTRUMENT_TYPE,
    SUBSTR(FX.M_QUOTMODE0, 1, 3) AS LEV_QUOT,
    CASE
        WHEN SBL.M_VEGA_STK < 50.0 THEN 'Call'
        WHEN SBL.M_VEGA_STK > 50.0 THEN 'Put'
        ELSE 'ATM'
    END AS CALL_PUT,
    SBL.M_VEGA_MAT AS PILLAR,
    TO_CHAR(SBL.M_VEGA_MATD, 'YYYY-MM-DD') AS END_DATE,
    SBL.M_VEGA_STK AS VEGA_STRIKE,
    SBL.M_VEGA_USD AS FX_VEGA,
    'USD' AS FX_VEGA_CCY
FROM DM.A_FXVEGA_STK_REP SBL
LEFT OUTER JOIN DM.TBL_FX_CNT_REP FX
    ON SBL.M_LABEL = FX.M_LABEL AND SBL.M_REF_DATA = FX.M_REF_DATA
JOIN DM.SB_TP_REP TP
    ON TP.M_REF_DATA = SBL.M_REF_DATA AND TP.M_NB = SBL.M_TRADE_NUM
WHERE M_VEGA_MAT IS NOT NULL
  AND M_VEGA_STK > 0
  AND SBL.M_REF_DATA = @MxDataSetKey:N
  AND TP.M_TP_LENTDSP = @LegalEntity:C
ORDER BY
    SBL.M_PORTFOLIO,
    SBL.M_TRADE_NUM,
    SBL.M_LABEL,
    SBL.M_VEGA_MATD,
    SBL.M_VEGA_STK;
```

### 4.4 Interest Rate DV01 Extraction SQL

```sql
-- MGB IR DV01 Extraction Request: ER_IRDV01
-- Extracts DV01 by currency and tenor

SELECT
    M_TRADE_NUM AS TRADE_NUMBER,
    M_PORTFOLIO AS PORTFOLIO,
    M_CURRENCY AS CURRENCY,
    M_TENOR AS TENOR_BUCKET,
    M_DV01_USD AS DV01,
    'USD' AS DV01_CCY,
    M_CONVEXITY AS CONVEXITY,
    M_CLOSING_E AS CLOSING_ENTITY,
    M_LEGAL_ENT AS LEGAL_ENTITY,
    M_STATUS AS TRADE_STATUS,
    M_PRODUCT_TYPE AS PRODUCT_TYPE
FROM DM.A_IRDV01_REP
WHERE M_REF_DATA = @MxDataSetKey:N
  AND M_TAG_DATA = @LabelofData:C
  AND M_DELETED = 'N'
  AND M_STATUS IN ('LIVE', 'MKT_OP')
ORDER BY M_PORTFOLIO, M_TRADE_NUM, M_CURRENCY, M_TENOR;
```

### 4.5 Credit CS01 Extraction SQL

```sql
-- MGB CR CS01 Extraction Request: ER_CRCS01
-- Extracts CS01 by issuer and tenor

SELECT
    M_TRADE_NUM AS TRADE_NUMBER,
    M_PORTFOLIO AS PORTFOLIO,
    M_ISSUER AS ISSUER,
    M_RATING AS RATING,
    M_SECTOR AS SECTOR,
    M_TENOR AS TENOR_BUCKET,
    M_CS01_USD AS CS01,
    'USD' AS CS01_CCY,
    M_JTD_USD AS JTD,
    M_CLOSING_E AS CLOSING_ENTITY,
    M_LEGAL_ENT AS LEGAL_ENTITY,
    M_STATUS AS TRADE_STATUS
FROM DM.A_CRCS01_REP
WHERE M_REF_DATA = @MxDataSetKey:N
  AND M_TAG_DATA = @LabelofData:C
  AND M_DELETED = 'N'
  AND M_STATUS IN ('LIVE', 'MKT_OP')
ORDER BY M_PORTFOLIO, M_TRADE_NUM, M_ISSUER, M_TENOR;
```

---

## 5. Feed Field Specifications

### 5.1 FX Delta Feed (MGB_FXDelta_{Region}_{YYYYMMDD}.csv)

| Field | Description | Type | Length | Source | Mandatory |
|-------|-------------|------|--------|--------|-----------|
| TRADE_NUMBER | Unique trade identifier | Numeric | 10 | M_NB from SV_FX_DELTA | Y |
| PORTFOLIO | Trading portfolio code | VarChar | 16 | PORTFOLIO from simulation view | Y |
| CURRENCY_PAIR | FX currency pair (e.g., EUR-USD) | VarChar | 16 | FXQUOT from simulation view | Y |
| FX_DELTA | FX Delta sensitivity in USD | Numeric | 22,2 | FX_DELTA_USD from simulation view | Y |
| FX_DELTA_CCY | Currency of FX Delta (always USD) | VarChar | 4 | Set at extraction level | Y |
| CLOSING_ENTITY | Booking entity code | VarChar | 16 | CLOSING_ENTITY from simulation view | Y |
| LEGAL_ENTITY | Legal entity code | VarChar | 16 | LEGAL_ENTITY from simulation view | Y |
| TRADE_STATUS | Trade status (LIVE/MKT_OP) | VarChar | 10 | STATUS from simulation view | N |

**Sample Output:**
```
TRADE_NUMBER;PORTFOLIO;CURRENCY_PAIR;FX_DELTA;FX_DELTA_CCY;CLOSING_ENTITY;LEGAL_ENTITY;TRADE_STATUS
12345678;FXLNSPOT;EUR-USD;1250000.00;USD;MGBLN;MGBLNL;LIVE
12345679;FXLNSPOT;GBP-USD;-875000.50;USD;MGBLN;MGBLNL;LIVE
0;FXLNFWD;JPY-USD;125.25;USD;MGBLN;MGBLNL;
```

### 5.2 FX Vega Feed (MGB_FXVega_{Region}_{YYYYMMDD}.csv)

| Field | Description | Type | Length | Source | Mandatory |
|-------|-------------|------|--------|--------|-----------|
| PORTFOLIO | Trading portfolio code | VarChar | 16 | PORTFOLIO from SV_FX_VEGA_MATURITY | Y |
| TRADE_NUMBER | Unique trade identifier | Numeric | 10 | TRADE_NUM from simulation view | Y |
| INSTRUMENT | Instrument label | VarChar | 16 | INSTRUMENT from simulation view | Y |
| INSTRUMENT_TYPE | Product classification | VarChar | 12 | Derived at extraction | N |
| LEV_QUOT | Base currency of pair | VarChar | 4 | From TBL_FX_CNT_REP | Y |
| CALL_PUT | Option type (Call/Put/ATM) | VarChar | 4 | Derived from VEGA_STK | Y |
| PILLAR | Vega maturity pillar (e.g., 3M, 1Y) | VarChar | 64 | VEGA_MAT from simulation view | Y |
| END_DATE | Vega maturity date | Date | 12 | VEGA_MATD from simulation view | Y |
| VEGA_STRIKE | Vega strike level (delta equivalent) | Numeric | 10 | VEGA_STK from simulation view | Y |
| FX_VEGA | FX Vega in USD | Numeric | 22,2 | VEGA_USD from simulation view | Y |
| FX_VEGA_CCY | Currency of FX Vega (always USD) | VarChar | 4 | Set at extraction level | Y |

**Maturity Pillars (RISK_VIEW4):**
O/N, T/N, 1W, 2W, 1M, 2M, 3M, 6M, 9M, 1Y, 18M, 2Y, 3Y, 4Y, 5Y, 6Y, 7Y, 8Y, 9Y, 10Y, 12Y, 15Y, 20Y, 25Y, 30Y, 35Y

**Sample Output:**
```
PORTFOLIO;TRADE_NUMBER;INSTRUMENT;INSTRUMENT_TYPE;LEV_QUOT;CALL_PUT;PILLAR;END_DATE;VEGA_STRIKE;FX_VEGA;FX_VEGA_CCY
FXLNOPTS;27556022;USD/JPY;IRD_IRS_FX;USD;Call;3M;2025-04-03;5;-36.14;USD
FXLNOPTS;27556022;USD/JPY;IRD_IRS_FX;USD;Call;3M;2025-04-03;10;-25.82;USD
FXLNOPTS;27556022;USD/JPY;IRD_IRS_FX;USD;ATM;3M;2025-04-03;50;65.57;USD
FXLNOPTS;27556022;USD/JPY;IRD_IRS_FX;USD;Put;3M;2025-04-03;75;-104.76;USD
```

### 5.3 Interest Rate DV01 Feed (MGB_IRDV01_{Region}_{YYYYMMDD}.csv)

| Field | Description | Type | Length | Source | Mandatory |
|-------|-------------|------|--------|--------|-----------|
| TRADE_NUMBER | Unique trade identifier | Numeric | 10 | M_TRADE_NUM | Y |
| PORTFOLIO | Trading portfolio code | VarChar | 16 | M_PORTFOLIO | Y |
| CURRENCY | Interest rate currency | VarChar | 4 | M_CURRENCY | Y |
| TENOR_BUCKET | Tenor bucket (e.g., 2Y, 5Y, 10Y) | VarChar | 10 | M_TENOR | Y |
| DV01 | DV01 sensitivity in USD | Numeric | 22,2 | M_DV01_USD | Y |
| DV01_CCY | Currency of DV01 (always USD) | VarChar | 4 | Set at extraction | Y |
| CONVEXITY | Convexity measure | Numeric | 22,4 | M_CONVEXITY | N |
| CLOSING_ENTITY | Booking entity code | VarChar | 16 | M_CLOSING_E | Y |
| LEGAL_ENTITY | Legal entity code | VarChar | 16 | M_LEGAL_ENT | Y |
| TRADE_STATUS | Trade status | VarChar | 10 | M_STATUS | N |
| PRODUCT_TYPE | Product classification | VarChar | 20 | M_PRODUCT_TYPE | N |

**Tenor Buckets:**
0-3M, 3-6M, 6M-1Y, 1-2Y, 2-3Y, 3-5Y, 5-7Y, 7-10Y, 10-15Y, 15-20Y, 20-30Y, 30Y+

### 5.4 Credit CS01 Feed (MGB_CRCS01_{Region}_{YYYYMMDD}.csv)

| Field | Description | Type | Length | Source | Mandatory |
|-------|-------------|------|--------|--------|-----------|
| TRADE_NUMBER | Unique trade identifier | Numeric | 10 | M_TRADE_NUM | Y |
| PORTFOLIO | Trading portfolio code | VarChar | 16 | M_PORTFOLIO | Y |
| ISSUER | Credit issuer name/ID | VarChar | 50 | M_ISSUER | Y |
| RATING | Credit rating | VarChar | 10 | M_RATING | N |
| SECTOR | Industry sector | VarChar | 30 | M_SECTOR | N |
| TENOR_BUCKET | Tenor bucket (e.g., 1Y, 5Y) | VarChar | 10 | M_TENOR | Y |
| CS01 | CS01 sensitivity in USD | Numeric | 22,2 | M_CS01_USD | Y |
| CS01_CCY | Currency of CS01 (always USD) | VarChar | 4 | Set at extraction | Y |
| JTD | Jump-to-default exposure | Numeric | 22,2 | M_JTD_USD | N |
| CLOSING_ENTITY | Booking entity code | VarChar | 16 | M_CLOSING_E | Y |
| LEGAL_ENTITY | Legal entity code | VarChar | 16 | M_LEGAL_ENT | Y |
| TRADE_STATUS | Trade status | VarChar | 10 | M_STATUS | N |

**Tenor Buckets:**
0-1Y, 1-3Y, 3-5Y, 5-10Y, 10Y+

---

## 6. Delivery Configuration

### 6.1 Feed Packaging

All sensitivity feeds are packaged into a single ZIP file per region:

| Component | Format | Example |
|-----------|--------|---------|
| **Package Name** | MGB_Sensitivities_{Region}_{YYYYMMDD}.zip | MGB_Sensitivities_LDN_20250102.zip |
| **FX Delta Feed** | MGB_FXDelta_{Region}_{YYYYMMDD}.csv | MGB_FXDelta_LDN_20250102.csv |
| **FX Vega Feed** | MGB_FXVega_{Region}_{YYYYMMDD}.csv | MGB_FXVega_LDN_20250102.csv |
| **IR DV01 Feed** | MGB_IRDV01_{Region}_{YYYYMMDD}.csv | MGB_IRDV01_LDN_20250102.csv |
| **CR CS01 Feed** | MGB_CRCS01_{Region}_{YYYYMMDD}.csv | MGB_CRCS01_LDN_20250102.csv |

### 6.2 Packaging Script

```bash
#!/bin/bash
# process_sens_feeds.sh - Package sensitivity feeds for delivery

REGION=$1
DATE=$(date +%Y%m%d)
FEED_DIR=/app/murex/reports/today/eod
OUTPUT_DIR=/app/murex/mft/outbound

# Create package
cd $FEED_DIR
zip -j ${OUTPUT_DIR}/MGB_Sensitivities_${REGION}_${DATE}.zip \
    MGB_FXDelta_${REGION}_${DATE}.csv \
    MGB_FXVega_${REGION}_${DATE}.csv \
    MGB_IRDV01_${REGION}_${DATE}.csv \
    MGB_CRCS01_${REGION}_${DATE}.csv

# Generate checksum
md5sum ${OUTPUT_DIR}/MGB_Sensitivities_${REGION}_${DATE}.zip > \
    ${OUTPUT_DIR}/MGB_Sensitivities_${REGION}_${DATE}.md5

echo "Package created: MGB_Sensitivities_${REGION}_${DATE}.zip"
```

### 6.3 MFT Delivery Configuration

| Region | MFT Flow ID | Destination | Schedule |
|--------|-------------|-------------|----------|
| LDN | MGB_SensToRAP_LN | RAP (Risk Aggregation Platform) | 05:00 GMT |
| NYK | MGB_SensToRAP_NY | RAP (Risk Aggregation Platform) | 05:30 GMT |
| HKG | MGB_SensToRAP_HK | RAP (Risk Aggregation Platform) | 05:30 GMT |

**MFT Connection Details:**

| Parameter | Value |
|-----------|-------|
| Protocol | SFTP |
| Host | rap-ingest.meridianbank.com |
| Port | 22 |
| Directory | /inbound/sensitivities/{region}/ |
| User | svc_murex_mft |
| Authentication | SSH Key |
| Encryption | AES-256 |

### 6.4 Downstream Consumers

| Consumer | Purpose | SLA |
|----------|---------|-----|
| **RAP** | Risk Aggregation Platform - VaR calculation | 06:00 GMT |
| **RDS** | Risk Data Store - Reporting warehouse | 07:00 GMT |
| **LMT** | Limit Monitoring Tool - Real-time limits | 06:30 GMT |

---

## 7. Data Quality Controls

### 7.1 Pre-Extraction Validation

| Check | Description | Action |
|-------|-------------|--------|
| Position count | Compare Datamart count vs expected | Alert if variance > 1% |
| NULL values | Check mandatory fields for NULLs | Reject record, log exception |
| Numeric ranges | Validate sensitivities within bounds | Flag outliers for review |
| Reference data | Verify all portfolios mapped | Map unmapped to UNKNOWN |

### 7.2 Post-Extraction Validation

| Check | Description | Threshold |
|-------|-------------|-----------|
| Row count | Compare to T-1 feed | Alert if variance > 10% |
| Total sensitivity | Sum of all sensitivities vs T-1 | Alert if variance > 20% |
| File size | Compare file size to T-1 | Alert if variance > 25% |
| Checksum | Verify MD5 checksum | Must match |

### 7.3 Reconciliation Points

| Reconciliation | Frequency | Tolerance | Owner |
|----------------|-----------|-----------|-------|
| Feed position count vs Murex positions | Daily | 0% | RAV Team |
| Total DV01: Feed vs Risk matrices | Daily | 0.1% | Market Risk |
| Total FX Delta: Feed vs P&L | Daily | 1% | P&L Control |

---

## 8. Error Handling

### 8.1 Exception Types

| Exception Code | Description | Handling |
|----------------|-------------|----------|
| E001 | Feeder failure | Retry 3x, then escalate to L2 |
| E002 | Extraction SQL error | Alert DBA, use T-1 data |
| E003 | Missing market data | Use proxy rates, flag records |
| E004 | MFT delivery failure | Retry 5x, escalate to L2 |
| E005 | File corruption | Regenerate feed, resend |

### 8.2 Fallback Procedures

| Scenario | Procedure |
|----------|-----------|
| Complete feed failure | Use T-1 feed with STALE flag |
| Partial data | Deliver available data with INCOMPLETE flag |
| Late delivery | Notify downstream, deliver when available |

### 8.3 Escalation Matrix

| Level | Time | Contact |
|-------|------|---------|
| L1 | 0-30 min | Risk Technology On-Call |
| L2 | 30-60 min | Risk Technology Manager |
| L3 | 60+ min | Head of Risk Technology + Head of Market Risk |

---

## 9. Environment Configuration

### 9.1 Server Configuration

| Environment | Server | Database | Purpose |
|-------------|--------|----------|---------|
| Production | murex-prd-app01 | MXPRD | Live processing |
| UAT | murex-uat-app01 | MXUAT | Testing |
| DR | murex-dr-app01 | MXDR | Disaster recovery |

### 9.2 Directory Paths

| Path | Purpose |
|------|---------|
| /app/murex/reports/today/eod | Daily EOD feed output |
| /app/murex/mft/outbound | MFT staging directory |
| /app/murex/logs/feeds | Feed processing logs |
| /app/murex/archive/feeds | Historical feed archive |

---

## 10. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Sensitivities BRD](./sensitivities-brd.md) | SENS-BRD-001 | Business requirements |
| [Sensitivities IT Config](./sensitivities-config.md) | SENS-CFG-001 | IT configuration |
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |
| [System Architecture](../../system-architecture.md) | MR-L7-001 | System context |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-02 | Initial version | Risk Technology |

### 11.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Technical review | Annual | January 2026 |
| Reconciliation review | Semi-annual | July 2025 |
| Security review | Annual | January 2026 |

---

*End of Document*
