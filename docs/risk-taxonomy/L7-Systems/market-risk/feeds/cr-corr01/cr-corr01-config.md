---
# Document Metadata
document_id: CR-CORR-CFG-001
document_name: CR Corr01 Feed - IT Configuration Specification
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: CR-CORR-BRD-001  # CR Corr01 BRD
feed_id: CR-CORR-001
---

# CR Corr01 Feed - IT Configuration Specification

**Meridian Global Bank - Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-CORR-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Overview

This document provides the technical configuration details for the CR Corr01 (Credit Correlation 01) feed within the Murex Global Object Model (GOM). This feed extracts correlation sensitivity for Monte Carlo priced credit products.

### 1.1 Key Characteristics

| Property | Value |
|----------|-------|
| **Feed Name** | CR Corr01 |
| **File Pattern** | MxMGB_MR_Credit_Corr01_{Region}_{YYYYMMDD}.csv |
| **Source Table** | TBL_VESPA_SENS_REP only (Non-CRDI) |
| **Key Metric** | M_CORR01 |
| **Output Fields** | 13 |
| **Delimiter** | Semicolon (;) |
| **Encoding** | UTF-8 |

### 1.2 Key Differentiator

Unlike other CR feeds which have both Non-CRDI and CRDI components:
- **CR Corr01 extracts from Non-CRDI only**
- No UNION with TBL_VESPA_SENSCI_REP
- No CRDI-specific processing required

---

## 2. Murex GOM Architecture

### 2.1 Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     MUREX FRONT OFFICE                          │
│   Monte Carlo Valuation Batch → Corr01 Calculation              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SIMULATION VIEW                              │
│              VW_Vespa_Sensitivities                             │
│      (Corr01 captured during MC pricing)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATAMART TABLES                             │
│  ┌──────────────────────┐    ┌───────────────────────────────┐  │
│  │ TBL_VESPA_SENS_REP   │    │ TBL_AC_CRDCURVES_REP          │  │
│  │ (Sensitivities)      │    │ (Credit Curves - Issuer data) │  │
│  │ M_CORR01             │    │ M_ISSUER, M_LABEL             │  │
│  │ M_CURVE_NAM          │    │                               │  │
│  └──────────────────────┘    └───────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               TRANSACTION TABLES                          │   │
│  │  SB_TP_REP │ SB_TP_BD_REP │ SB_TP_EXT_REP                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA EXTRACTOR                               │
│                 DE_VESPA_CR_CORR01                               │
│   (SQL extraction with curve/issuer subqueries)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  EXTRACTION REQUEST                             │
│                ER_VESPA_CR_CORR01                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  REGIONAL PROCESSING                            │
│  LN_MR_VESPA_CORR01_RPT | HK_MR_VESPA_CORR01_RPT |             │
│  NY_MR_VESPA_CORR01_RPT | SP_MR_VESPA_CORR01_RPT               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OUTPUT FILES                                │
│         MxMGB_MR_Credit_Corr01_{Region}_{YYYYMMDD}.csv          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       PACKAGING                                 │
│    MxMGB_MR_Credit_Sens_{Region}_{YYYYMMDD}.zip           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Source Objects

### 3.1 Primary Source Table

| Property | Value |
|----------|-------|
| **Table Name** | TBL_VESPA_SENS_REP |
| **Description** | VESPA sensitivities for non-CRDI products |
| **Key Fields** | M_TRADE_NUM, M_REF_DATA, M_CORR01, M_CURVE_NAM |
| **Filter** | M_CORR01 <> 0 |
| **Population** | Via VW_Vespa_Sensitivities simulation view |

### 3.2 Supporting Tables

| Table | Purpose | Join Key |
|-------|---------|----------|
| **SB_TP_REP** | Trade static data | M_NB = M_TRADE_NUM |
| **SB_TP_BD_REP** | Bond/deal details | M_NB = M_TRADE_NUM |
| **TBL_AC_CRDCURVES_REP** | Credit curves (issuer lookup) | M_LABEL = M_CURVE_NAM |

### 3.3 No CRDI Source

Unlike other CR feeds, CR Corr01 does **NOT** include:
- TBL_VESPA_SENSCI_REP (CRDI sensitivities)
- Any UNION structure for credit indices

**Reason**: Plain credit indices don't have explicit correlation sensitivity - it's embedded in the index pricing model.

---

## 4. Data Extractor Configuration

### 4.1 Extractor Definition

| Property | Value |
|----------|-------|
| **Extractor Name** | DE_VESPA_CR_CORR01 |
| **Type** | SQL Extraction Request |
| **Target Table** | N/A (direct CSV output) |
| **Scheduling** | Via batch events |

### 4.2 SQL Extraction Query

```sql
SELECT
    TP.M_NB                    AS TRADE_NUM,
    TP.M_TP_PFOLIO             AS PORTFOLIO,
    TP.M_INSTRUMENT            AS INSTRUMENT,
    TP.M_TRN_FMLY              AS TRN_FAMILY,
    TP.M_TRN_GRP               AS TRN_GROUP,
    TP.M_TRN_TYPE              AS TRN_TYPE,
    TP_BD.M_TP_SECCODU         AS SECURITY_CODE,
    VSP.M_CURRENCY             AS CURRENCY,
    -- First Credit Curve (alphabetical)
    (SELECT M_CURVE_NAM AS CURVE1
     FROM (SELECT T2.*, ROW_NUMBER() OVER (ORDER BY M_CURVE_NAM) row_num
           FROM (SELECT DISTINCT M_TRADE_NUM, M_CURVE_NAM
                 FROM DM.TBL_VESPA_SENS_REP WSP
                 WHERE WSP.M_TRADE_NUM = VSP.M_TRADE_NUM
                   AND WSP.M_REF_DATA = VSP.M_REF_DATA
                   AND WSP.M_CURVE_NAM NOT LIKE '(null)%') T2)
     WHERE row_num = 1)        AS CREDIT_CURVE1,
    -- Second Credit Curve (alphabetical)
    (SELECT M_CURVE_NAM AS CURVE1
     FROM (SELECT T2.*, ROW_NUMBER() OVER (ORDER BY M_CURVE_NAM) row_num
           FROM (SELECT DISTINCT M_TRADE_NUM, M_CURVE_NAM
                 FROM DM.TBL_VESPA_SENS_REP WSP
                 WHERE WSP.M_TRADE_NUM = VSP.M_TRADE_NUM
                   AND WSP.M_REF_DATA = VSP.M_REF_DATA
                   AND WSP.M_CURVE_NAM NOT LIKE '(null)%') T2)
     WHERE row_num = 2)        AS CREDIT_CURVE2,
    -- First Issuer (via curve lookup)
    (SELECT DISTINCT M_ISSUER
     FROM DM.TBL_AC_CRDCURVES_REP CRDCR
     WHERE CRDCR.M_REF_DATA = @MxHistoricalData1:N
       AND CRDCR.M_LABEL IN (
           SELECT M_CURVE_NAM AS CURVE1
           FROM (SELECT T2.*, ROW_NUMBER() OVER (ORDER BY M_CURVE_NAM) row_num
                 FROM (SELECT DISTINCT M_TRADE_NUM, M_CURVE_NAM
                       FROM DM.TBL_VESPA_SENS_REP WSP
                       WHERE WSP.M_TRADE_NUM = VSP.M_TRADE_NUM
                         AND WSP.M_REF_DATA = VSP.M_REF_DATA
                         AND WSP.M_CURVE_NAM NOT LIKE '(null)%') T2)
           WHERE row_num = 1)
       AND ROWNUM = 1)         AS CREDIT_ISSUER1,
    -- Second Issuer (via curve lookup)
    (SELECT DISTINCT M_ISSUER
     FROM DM.TBL_AC_CRDCURVES_REP CRDCR
     WHERE CRDCR.M_REF_DATA = @MxHistoricalData1:N
       AND CRDCR.M_LABEL IN (
           SELECT M_CURVE_NAM AS CURVE1
           FROM (SELECT T2.*, ROW_NUMBER() OVER (ORDER BY M_CURVE_NAM) row_num
                 FROM (SELECT DISTINCT M_TRADE_NUM, M_CURVE_NAM
                       FROM DM.TBL_VESPA_SENS_REP WSP
                       WHERE WSP.M_TRADE_NUM = VSP.M_TRADE_NUM
                         AND WSP.M_REF_DATA = VSP.M_REF_DATA
                         AND WSP.M_CURVE_NAM NOT LIKE '(null)%') T2)
           WHERE row_num = 2)
       AND ROWNUM = 1)         AS CREDIT_ISSUER2,
    -- Correlation Sensitivity
    VSP.M_CORR01               AS CREDIT_CORR01

FROM DM.TBL_VESPA_SENS_REP VSP

INNER JOIN DM.SB_TP_REP TP
    ON VSP.M_TRADE_NUM = TP.M_NB
    AND TP.M_REF_DATA = @MxDataSetKey:N

INNER JOIN DM.SB_TP_BD_REP TP_BD
    ON TP_BD.M_NB = TP.M_NB
    AND TP_BD.M_REF_DATA = @MxDataSetKey:N

WHERE VSP.M_REF_DATA = @MxDataSetKey:N
  AND TP.M_TP_LENTDSP = @LegalEntity:C
  AND VSP.M_CORR01 <> 0
```

### 4.3 Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| @MxDataSetKey:N | Market data set reference | LNCLOSE |
| @MxHistoricalData1:N | Historical data reference | Same as @MxDataSetKey |
| @LegalEntity:C | Legal entity filter | MGB |

### 4.4 Key SQL Logic: Dual Curve/Issuer Extraction

The query uses **correlated subqueries with ROW_NUMBER()** to:
1. Find all distinct credit curves for each trade
2. Filter out null curves (NOT LIKE '(null)%')
3. Order alphabetically by curve name
4. Select first (row_num=1) and second (row_num=2) curves
5. Look up issuer from TBL_AC_CRDCURVES_REP for each curve

This approach handles correlation products with multiple underlying references.

---

## 5. Extraction Request Configuration

### 5.1 Extraction Request Definition

| Property | Value |
|----------|-------|
| **Request Name** | ER_VESPA_CR_CORR01 |
| **Extractor** | DE_VESPA_CR_CORR01 |
| **Output Format** | CSV |
| **Field Delimiter** | Semicolon (;) |
| **Include Header** | Yes |

### 5.2 Field Mappings

| # | Output Field | Source Expression |
|---|--------------|-------------------|
| 1 | TRADE_NUM | TP.M_NB |
| 2 | PORTFOLIO | TP.M_TP_PFOLIO |
| 3 | INSTRUMENT | TP.M_INSTRUMENT |
| 4 | TRN_FAMILY | TP.M_TRN_FMLY |
| 5 | TRN_GROUP | TP.M_TRN_GRP |
| 6 | TRN_TYPE | TP.M_TRN_TYPE |
| 7 | SECURITY_CODE | TP_BD.M_TP_SECCODU |
| 8 | CURRENCY | VSP.M_CURRENCY |
| 9 | CREDIT_CURVE1 | Subquery (first curve alphabetically) |
| 10 | CREDIT_CURVE2 | Subquery (second curve alphabetically) |
| 11 | CREDIT_ISSUER1 | Subquery (issuer for first curve) |
| 12 | CREDIT_ISSUER2 | Subquery (issuer for second curve) |
| 13 | CREDIT_CORR01 | VSP.M_CORR01 |

---

## 6. Regional Processing Configuration

### 6.1 Processing Scripts

| Region | Script Name | Description |
|--------|-------------|-------------|
| **LN** | LN_MR_VESPA_CORR01_RPT | London Corr01 processing |
| **HK** | HK_MR_VESPA_CORR01_RPT | Hong Kong Corr01 processing |
| **NY** | NY_MR_VESPA_CORR01_RPT | New York Corr01 processing |
| **SP** | SP_MR_VESPA_CORR01_RPT | Singapore Corr01 processing |

### 6.2 Batch Event Configuration

| Region | Batch Event | Dependency | Schedule |
|--------|-------------|------------|----------|
| **LN** | BE_VESPA_CORR01_LN | MC valuation complete | 03:30 GMT |
| **HK** | BE_VESPA_CORR01_HK | MC valuation complete | 21:30 HKT |
| **NY** | BE_VESPA_CORR01_NY | MC valuation complete | 22:30 EST |
| **SP** | BE_VESPA_CORR01_SP | MC valuation complete | 21:30 SGT |

### 6.3 Market Data Set Mapping

| Region | Market Data Set | @MxDataSetKey |
|--------|-----------------|---------------|
| LN | LNCLOSE | LNCLOSE reference |
| HK | HKCLOSE | HKCLOSE reference |
| NY | NYCLOSE | NYCLOSE reference |
| SP | SPCLOSE | SPCLOSE reference |

---

## 7. Output File Configuration

### 7.1 File Naming Convention

```
MxMGB_MR_Credit_Corr01_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Example |
|-----------|-------------|---------|
| MxMGB | Meridian Global Bank prefix | MxMGB |
| Vespa | VESPA system identifier | Vespa |
| CR_Corr01 | Feed type identifier | CR_Corr01 |
| Region | Trading region code | LN, HK, NY, SP |
| YYYYMMDD | As-of date | 20250102 |

### 7.2 File Format Specification

| Property | Value |
|----------|-------|
| **Format** | CSV |
| **Delimiter** | Semicolon (;) |
| **Encoding** | UTF-8 |
| **Line Ending** | LF (Unix) |
| **Header Row** | Yes |
| **Quoting** | Double quotes for text with delimiters |

### 7.3 Sample Output

```csv
TRADE_NUM;PORTFOLIO;INSTRUMENT;TRN_FAMILY;TRN_GROUP;TRN_TYPE;SECURITY_CODE;CURRENCY;CREDIT_CURVE1;CREDIT_CURVE2;CREDIT_ISSUER1;CREDIT_ISSUER2;CREDIT_CORR01
27571964;CTLNMGBLGBB7FRT;CLN 1942 - NAVMINE 4.76% 20/04/27;IRD;BOND;;XS2497911482;USD;NMMC_USD_SNRFOR;MGB_USD_SNRFOR;NMMC;MGB;-2014
28123456;CDOLNMGB01;CDO TRANCHE 2024-1 EQUITY;CRD;CDO;;XS1234567890;USD;AAA_USD_SNRFOR;BBB_USD_SNRFOR;AAA Corp;BBB Corp;125000
```

---

## 8. Packaging and Delivery

### 8.1 Packaging Script

| Property | Value |
|----------|-------|
| **Script** | process_reports.sh |
| **Function** | Compress and package CR Corr01 with other VESPA feeds |
| **Output** | MxMGB_MR_Credit_Sens_{Region}_{YYYYMMDD}.zip |

### 8.2 Files Included in Package

The CR Corr01 file is packaged with other CR feeds:
- MxMGB_MR_Credit_CS01_*.csv
- MxMGB_MR_Credit_CS01Par_*.csv
- MxMGB_MR_Credit_Basis_*.csv
- MxMGB_MR_Credit_ParCDS_*.csv
- **MxMGB_MR_Credit_Corr01_*.csv**
- MxMGB_MR_Credit_Spread_*.csv
- MxMGB_MR_Credit_RR01_*.csv
- MxMGB_MR_Credit_RR02_*.csv

### 8.3 Delivery Configuration

| Property | Value |
|----------|-------|
| **Protocol** | SFTP |
| **Target** | Risk data warehouse / Plato |
| **Frequency** | Daily (T+1) |
| **Retention** | 7 years |

---

## 9. Data Quality Controls

### 9.1 Extraction Validation

| Check | Description | Action on Failure |
|-------|-------------|-------------------|
| Row count | >0 rows extracted | Warning (may be valid if no MC positions) |
| Null TRADE_NUM | Trade identifier populated | Reject record |
| Null CREDIT_CURVE1 | Primary curve populated | Flag for review |
| Zero CREDIT_CORR01 | Filtered in WHERE clause | Should not occur |

### 9.2 Reconciliation Points

| Reconciliation | Source | Target | Tolerance |
|----------------|--------|--------|-----------|
| Position count | Murex MC valuation report | Feed output | Review variance |
| Corr01 values | VW_Vespa_Sensitivities | Feed output | 0.01% |
| Curve/Issuer | TBL_AC_CRDCURVES_REP | Feed output | 0% |

---

## 10. Performance Considerations

### 10.1 Query Optimization

The Corr01 query uses **correlated subqueries** which can be expensive. Optimization strategies:

| Strategy | Description |
|----------|-------------|
| **Indexing** | Ensure indexes on M_TRADE_NUM, M_REF_DATA, M_CURVE_NAM |
| **Parallel execution** | Enable parallel query hints |
| **Statistics** | Maintain up-to-date table statistics |

### 10.2 Expected Volumes

| Metric | Expected Value |
|--------|----------------|
| **Positions per region** | 500-2,000 (MC-priced only) |
| **Total rows** | 2,000-8,000 across regions |
| **File size** | 100KB - 500KB per region |
| **Extraction time** | 5-15 minutes |

### 10.3 Monte Carlo Dependency

The Corr01 feed depends on Monte Carlo valuation completion:
- MC valuation is typically longer-running than analytical pricing
- Schedule Corr01 extraction after MC batch confirmation
- Allow buffer time for MC variability

---

## 11. Error Handling

### 11.1 Common Error Scenarios

| Error | Cause | Resolution |
|-------|-------|------------|
| No rows returned | No MC-priced positions or all Corr01=0 | Valid scenario - confirm with Risk |
| Curve lookup failure | Credit curve missing from TBL_AC_CRDCURVES_REP | Check curve calibration |
| Issuer not found | Curve exists but no issuer mapping | Check market data enrichment |
| Timeout | Complex subqueries on large data | Optimize indexes, increase timeout |

### 11.2 Error Logging

| Field | Description |
|-------|-------------|
| Timestamp | Error occurrence time |
| Batch ID | Batch event identifier |
| Error code | System error code |
| Message | Detailed error message |
| Trade affected | Trade number if applicable |

---

## 12. Monitoring and Alerts

### 12.1 Key Metrics

| Metric | Threshold | Alert |
|--------|-----------|-------|
| Extraction completion | By 04:00 GMT | Email to L2 Support |
| Row count variance | >20% vs. T-1 | Review flag |
| Error count | >0 | L2 Support notification |
| File delivery | By 05:30 GMT | Escalation to L2 |

### 12.2 Dashboard Metrics

| Metric | Visualization |
|--------|---------------|
| Daily position count | Time series |
| Corr01 sum by region | Bar chart |
| Extraction duration | Trend line |
| Error rate | Traffic light |

---

## 13. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [CR Corr01 BRD](./cr-corr01-brd.md) | CR-CORR-BRD-001 | Business requirements |
| [CR Corr01 IDD](./cr-corr01-idd.md) | CR-CORR-IDD-001 | Interface specification |
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |

---

## 14. Document Control

### 14.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-02 | Initial version | Risk Technology |

### 14.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Technical review | Annual | January 2026 |
| Performance review | Quarterly | April 2025 |
| Security review | Annual | January 2026 |

---

*End of Document*
