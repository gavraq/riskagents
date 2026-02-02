---
# Document Metadata
document_id: CR-RR02-CFG-001
document_name: CR RR02 Feed - IT Configuration Specification
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: CR-RR02-BRD-001  # CR RR02 BRD
feed_id: CR-RR02-001
---

# CR RR02 Feed - IT Configuration Specification

**Meridian Global Bank - Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-RR02-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Overview

This document provides the technical configuration details for the CR RR02 (Credit Recovery Rate 02) feed within the Murex Global Object Model (GOM). This feed extracts recovery rate sensitivity WITHOUT propagation for credit products.

### 1.1 Key Characteristics

| Property | Value |
|----------|-------|
| **Feed Name** | CR RR02 |
| **File Pattern** | MxMGB_MR_Credit_RR02_{Region}_{YYYYMMDD}.csv |
| **Source Tables** | TBL_VESPA_SENS_REP (Non-CRDI) + TBL_VESPA_SENSCI_REP (CRDI) |
| **Structure** | UNION ALL |
| **Key Metric** | M_RECOVERY1 (RR02_SENSI) |
| **Output Fields** | 20 |
| **Delimiter** | Semicolon (;) |
| **Encoding** | UTF-8 |

### 1.2 Comparison with CR RR01 and CR Basis Rate

| Feed | Source Field | Propagation | Description |
|------|--------------|-------------|-------------|
| CR RR01 | M_RECOVERY_ | WITH | Full recovery risk |
| **CR RR02** | **M_RECOVERY1** | **WITHOUT** | **Pure recovery sensitivity** |
| CR Basis Rate | M_RECOVERY1 | WITHOUT | Same source as RR02 |

### 1.3 Historical Change Reference

| Change ID | Description |
|-----------|-------------|
| CM-6396 | Changed RR02_SENSI source from M_VALUE to M_RECOVERY1 |

---

## 2. Murex GOM Architecture

### 2.1 Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     MUREX FRONT OFFICE                          │
│        Valuation with Recovery Rate Bumping (No Spread Recal)   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SIMULATION VIEWS                             │
│   VW_Vespa_Sensitivities    │    VW_Vespa_Sensitivities_CRDI   │
│   (Non-CRDI RR02)           │    (CRDI RR02)                   │
│   M_RECOVERY1               │    M_RECOVERY1                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATAMART TABLES                             │
│  ┌──────────────────────┐    ┌───────────────────────────────┐  │
│  │ TBL_VESPA_SENS_REP   │    │ TBL_VESPA_SENSCI_REP          │  │
│  │ (Non-CRDI)           │    │ (CRDI)                        │  │
│  │ M_RECOVERY1          │    │ M_RECOVERY1                   │  │
│  └──────────────────────┘    └───────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               SUPPORTING TABLES                           │   │
│  │  SB_TP_REP │ SB_CP_REP │ TBL_CRD_RECOVERY_REP            │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA EXTRACTOR                               │
│                 DE_VESPA_CR_RR02                                 │
│           (UNION ALL: Non-CRDI + CRDI)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  EXTRACTION REQUEST                             │
│                ER_VESPA_CR_RR02                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  REGIONAL PROCESSING                            │
│  LN_MR_VESPA_R2_RPT | HK_MR_VESPA_R2_RPT |                      │
│  NY_MR_VESPA_R2_RPT | SP_MR_VESPA_R2_RPT                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OUTPUT FILES                                │
│         MxMGB_MR_Credit_RR02_{Region}_{YYYYMMDD}.csv            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Source Objects

### 3.1 Primary Source Tables

#### 3.1.1 Non-CRDI Source

| Property | Value |
|----------|-------|
| **Table Name** | TBL_VESPA_SENS_REP |
| **Description** | VESPA sensitivities for non-CRDI products |
| **Key Fields** | M_TRADE_NUM, M_RECOVERY1, M_RATE, M_DATE__ZER |
| **Filter** | M_GROUP <> 'CRDI' AND M_ISSUER IS NOT NULL AND M_DATE__ZER IS NOT NULL |
| **Population** | Via VW_Vespa_Sensitivities simulation view |

#### 3.1.2 CRDI Source

| Property | Value |
|----------|-------|
| **Table Name** | TBL_VESPA_SENSCI_REP |
| **Description** | VESPA sensitivities for credit index products |
| **Key Fields** | M_TRADE_NUM, M_RECOVERY1, M_PL_INSTRU |
| **Filter** | M_GROUP = 'CRDI' |
| **Population** | Via VW_Vespa_Sensitivities_CRDI simulation view |

### 3.2 Supporting Tables

| Table | Purpose | Join Key |
|-------|---------|----------|
| **SB_TP_REP** | Trade static data | M_NB = M_TRADE_NUM |
| **SB_CP_REP** | Counterparty/Issuer data | M_DSP_LABEL = M_ISSUER |
| **TBL_CRD_RECOVERY_REP** | Credit recovery details | M_NB = M_TRADE_NUM (CDS only) |
| **SB_CRI_DEF_REP** | Credit index definitions | M_INDEX_LBL = M_PL_INSTRU (CRDI) |

---

## 4. Data Extractor Configuration

### 4.1 Extractor Definition

| Property | Value |
|----------|-------|
| **Extractor Name** | DE_VESPA_CR_RR02 |
| **Type** | SQL Extraction Request |
| **Target Table** | N/A (direct CSV output) |
| **Scheduling** | Via batch events |

### 4.2 SQL Extraction Query - Non-CRDI Component

```sql
SELECT
    VSP.M_TRADE_NUM                    AS TRADE_NUM,
    VSP.M_FAMILY                       AS FAMILY,
    VSP.M_GROUP                        AS M_GROUP,
    VSP.M_TYPE                         AS M_TYPE,
    VSP.M_TYPOLOGY                     AS TYPOLOGY,
    VSP.M_PORTFOLIO                    AS PORTFOLIO,
    VSP.M_PL_INSTRU                    AS INSTRUMENT,
    CASE WHEN VSP.M_ISSUER IS NULL
         THEN VSP.M_PL_INSTRU
         ELSE VSP.M_ISSUER
    END                                AS ISSUER,
    VSP.M_CURVE_NA1                    AS CURVE_NAME,
    VSP.M_DATE__ZER                    AS M_DATE,
    VSP.M_RATE                         AS RECOVERY_RATE,
    -- VSP.M_VALUE                     AS RR02_SENSI,  -- Original (deprecated)
    VSP.M_RECOVERY1                    AS RR02_SENSI,  -- CM-6396: Changed to M_RECOVERY1
    VSP.M_CURRENCY2                    AS CURRENCY,
    CP.M_U_CIF_ID                      AS CIF,
    CP.M_U_GLOBID                      AS GLOBUS_ID,
    CP.M_U_RSK_CTRY                    AS COUNTRY,
    OBL.M_REF_OBLI1                    AS ISIN,
    TP.M_TP_DTEEXP                     AS MATURITY,
    OBL.M_REF_OBLIG                    AS UNDERLYING,
    CASE WHEN OBL.M_RESTRUCTU = 'Yes'
         THEN OBL.M_RESTRUCTU
         ELSE 'NONE'
    END                                AS RESTRUCT

FROM DM.TBL_VESPA_SENS_REP VSP

LEFT JOIN DM.SB_CP_REP CP
    ON VSP.M_ISSUER = CP.M_DSP_LABEL
    AND CP.M_REF_DATA = @MxDataSetKey:N

LEFT JOIN DM.TBL_CRD_RECOVERY_REP OBL
    ON VSP.M_TRADE_NUM = OBL.M_NB
    AND VSP.M_REF_DATA = OBL.M_REF_DATA
    AND VSP.M_GROUP = 'CDS'

INNER JOIN DM.SB_TP_REP TP
    ON TP.M_REF_DATA = VSP.M_REF_DATA
    AND VSP.M_TRADE_NUM = TP.M_NB
    AND TP.M_TP_LENTDSP = @LegalEntity:C
    AND TP.M_STP_STATUS IN ('RELE', 'VERI', 'STTL')

WHERE VSP.M_REF_DATA = @MxDataSetKey:N
  AND VSP.M_DATE__ZER IS NOT NULL
  AND VSP.M_ISSUER IS NOT NULL
  AND VSP.M_GROUP <> 'CRDI'
```

### 4.3 SQL Extraction Query - CRDI Component

```sql
UNION ALL

SELECT
    VSP.M_TRADE_NUM                    AS TRADE_NUM,
    VSP.M_FAMILY                       AS FAMILY,
    VSP.M_GROUP                        AS M_GROUP,
    VSP.M_TYPE                         AS M_TYPE,
    VSP.M_LABEL                        AS TYPOLOGY,
    VSP.M_PORTFOLIO                    AS PORTFOLIO,
    VSP.M_PL_INSTRU                    AS INSTRUMENT,
    VSP.M_PL_INSTRU                    AS ISSUER,
    VSP.M_PL_INSTRU                    AS CURVE_NAME,
    ''                                 AS M_DATE,
    0                                  AS RECOVERY_RATE,
    -- VSP.M_VALUE                     AS RR02_SENSI,  -- Original (deprecated)
    VSP.M_RECOVERY1                    AS RR02_SENSI,  -- CM-6396: Changed to M_RECOVERY1
    VSP.M_CURRENCY                     AS CURRENCY,
    0                                  AS CIF,
    ''                                 AS GLOBUS_ID,
    ''                                 AS COUNTRY,
    ''                                 AS ISIN,
    TP.M_TP_DTEEXP                     AS MATURITY,
    ''                                 AS UNDERLYING,
    'NONE'                             AS RESTRUCT

FROM DM.TBL_VESPA_SENSCI_REP VSP

INNER JOIN DM.SB_TP_REP TP
    ON TP.M_REF_DATA = VSP.M_REF_DATA
    AND VSP.M_TRADE_NUM = TP.M_NB
    AND TP.M_TP_LENTDSP = @LegalEntity:C
    AND TP.M_STP_STATUS IN ('RELE', 'VERI', 'STTL')

LEFT JOIN DM.SB_CRI_DEF_REP CRI
    ON VSP.M_PL_INSTRU = CRI.M_INDEX_LBL
    AND CRI.M_REF_DATA = @MxDataSetKey:N

WHERE VSP.M_REF_DATA = @MxDataSetKey:N
  AND VSP.M_GROUP = 'CRDI'
```

### 4.4 Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| @MxDataSetKey:N | Market data set reference | LNCLOSE |
| @LegalEntity:C | Legal entity filter | MGB |

### 4.5 Key Differences from CR RR01

| Aspect | CR RR02 | CR RR01 |
|--------|---------|---------|
| **Source Field** | M_RECOVERY1 | M_RECOVERY_ |
| **Propagation** | WITHOUT | WITH |
| **Processing Scripts** | **_MR_VESPA_R2_RPT | **_MR_VESPA_R1_RPT |
| **Batch Events** | BE_VESPA_R2_** | BE_VESPA_R1_** |

---

## 5. Extraction Request Configuration

### 5.1 Extraction Request Definition

| Property | Value |
|----------|-------|
| **Request Name** | ER_VESPA_CR_RR02 |
| **Extractor** | DE_VESPA_CR_RR02 |
| **Output Format** | CSV |
| **Field Delimiter** | Semicolon (;) |
| **Include Header** | Yes |

### 5.2 Field Mappings

| # | Output Field | Non-CRDI Source | CRDI Source |
|---|--------------|-----------------|-------------|
| 1 | TRADE_NUM | VSP.M_TRADE_NUM | VSP.M_TRADE_NUM |
| 2 | FAMILY | VSP.M_FAMILY | VSP.M_FAMILY |
| 3 | GROUP | VSP.M_GROUP | VSP.M_GROUP |
| 4 | TYPE | VSP.M_TYPE | VSP.M_TYPE |
| 5 | TYPOLOGY | VSP.M_TYPOLOGY | VSP.M_LABEL |
| 6 | PORTFOLIO | VSP.M_PORTFOLIO | VSP.M_PORTFOLIO |
| 7 | INSTRUMENT | VSP.M_PL_INSTRU | VSP.M_PL_INSTRU |
| 8 | ISSUER | VSP.M_ISSUER (or M_PL_INSTRU) | VSP.M_PL_INSTRU |
| 9 | CURVE_NAME | VSP.M_CURVE_NA1 | VSP.M_PL_INSTRU |
| 10 | DATE | VSP.M_DATE__ZER | '' (blank) |
| 11 | RECOVERY_RATE | VSP.M_RATE | 0 |
| 12 | RR02_SENSI | **VSP.M_RECOVERY1** | **VSP.M_RECOVERY1** |
| 13 | CURRENCY | VSP.M_CURRENCY2 | VSP.M_CURRENCY |
| 14 | CIF | CP.M_U_CIF_ID | 0 |
| 15 | GLOBUS_ID | CP.M_U_GLOBID | '' (blank) |
| 16 | COUNTRY | CP.M_U_RSK_CTRY | '' (blank) |
| 17 | ISIN | OBL.M_REF_OBLI1 | '' (blank) |
| 18 | MATURITY | TP.M_TP_DTEEXP | TP.M_TP_DTEEXP |
| 19 | UNDERLYING | OBL.M_REF_OBLIG | '' (blank) |
| 20 | RESTRUCT | OBL.M_RESTRUCTU logic | 'NONE' |

---

## 6. Regional Processing Configuration

### 6.1 Processing Scripts

| Region | Script Name | Description |
|--------|-------------|-------------|
| **LN** | LN_MR_VESPA_R2_RPT | London RR02 processing |
| **HK** | HK_MR_VESPA_R2_RPT | Hong Kong RR02 processing |
| **NY** | NY_MR_VESPA_R2_RPT | New York RR02 processing |
| **SP** | SP_MR_VESPA_R2_RPT | Singapore RR02 processing |

### 6.2 Batch Event Configuration

| Region | Batch Event | Dependency | Schedule |
|--------|-------------|------------|----------|
| **LN** | BE_VESPA_R2_LN | Valuation complete | 03:00 GMT |
| **HK** | BE_VESPA_R2_HK | Valuation complete | 21:00 HKT |
| **NY** | BE_VESPA_R2_NY | Valuation complete | 22:00 EST |
| **SP** | BE_VESPA_R2_SP | Valuation complete | 21:00 SGT |

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
MxMGB_MR_Credit_RR02_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Example |
|-----------|-------------|---------|
| MxMGB | Meridian Global Bank prefix | MxMGB |
| Vespa | VESPA system identifier | Vespa |
| CR_RR02 | Feed type identifier | CR_RR02 |
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
TRADE_NUM;FAMILY;GROUP;TYPE;TYPOLOGY;PORTFOLIO;INSTRUMENT;ISSUER;CURVE_NAME;DATE;RECOVERY_RATE;RR02_SENSI;CURRENCY;CIF;GLOBUS_ID;COUNTRY;ISIN;MATURITY;UNDERLYING;RESTRUCT
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;6M;40.000000;11.04;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;;NONE
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;1Y;40.000000;220.87;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;;NONE
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;2Y;40.000000;625.53;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;;NONE
```

---

## 8. Packaging and Delivery

### 8.1 Packaging Script

| Property | Value |
|----------|-------|
| **Script** | process_reports.sh |
| **Function** | Compress and package CR RR02 with other VESPA feeds |
| **Output** | MxMGB_MR_Credit_Sens_{Region}_{YYYYMMDD}.zip |

### 8.2 Files Included in Package

The CR RR02 file is packaged with other CR feeds:
- MxMGB_MR_Credit_CS01_*.csv
- MxMGB_MR_Credit_CS01Par_*.csv
- MxMGB_MR_Credit_Basis_*.csv
- MxMGB_MR_Credit_ParCDS_*.csv
- MxMGB_MR_Credit_Corr01_*.csv
- MxMGB_MR_Credit_Spread_*.csv
- MxMGB_MR_Credit_RR01_*.csv
- **MxMGB_MR_Credit_RR02_*.csv**

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
| Row count | >0 rows extracted | Warning |
| Null TRADE_NUM | Trade identifier populated | Reject record |
| Null RR02_SENSI | Sensitivity must exist | Flag for review |
| Invalid RECOVERY_RATE | Between 0% and 100% | Flag for review |

### 9.2 Reconciliation Points

| Reconciliation | Source | Target | Tolerance |
|----------------|--------|--------|-----------|
| Position count | CR RR01 | CR RR02 | 0% |
| RR02 values | VW_Vespa_Sensitivities | Feed output | 0.01% |
| RR02 vs CR Basis Rate | CR RR02 | CR Basis Rate | 0.01% (same source) |

---

## 10. Performance Considerations

### 10.1 Query Optimization

| Strategy | Description |
|----------|-------------|
| **Indexing** | Ensure indexes on M_TRADE_NUM, M_REF_DATA, M_GROUP |
| **Parallel execution** | Enable parallel hints for UNION components |
| **Statistics** | Maintain up-to-date table statistics |

### 10.2 Expected Volumes

| Metric | Expected Value |
|--------|----------------|
| **Non-CRDI positions per region** | 5,000-15,000 |
| **CRDI positions per region** | 500-2,000 |
| **Total rows (with tenor expansion)** | 50,000-150,000 |
| **File size** | 5MB - 20MB per region |
| **Extraction time** | 10-30 minutes |

---

## 11. Error Handling

### 11.1 Common Error Scenarios

| Error | Cause | Resolution |
|-------|-------|------------|
| No rows returned | Empty source tables | Check upstream batches |
| Missing counterparty | Issuer not in SB_CP_REP | Check counterparty setup |
| RR02 calculation missing | Valuation failed | Check pricing batch |
| Timeout | Large data volume | Increase timeout, optimize query |

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
| RR02 sum by issuer | Bar chart |
| RR01 vs RR02 comparison | Scatter plot |
| Extraction duration | Trend line |

---

## 13. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [CR RR02 BRD](./cr-rr02-brd.md) | CR-RR02-BRD-001 | Business requirements |
| [CR RR02 IDD](./cr-rr02-idd.md) | CR-RR02-IDD-001 | Interface specification |
| [CR RR01 Config](../cr-rr01/cr-rr01-config.md) | CR-RR01-CFG-001 | With propagation config |
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
