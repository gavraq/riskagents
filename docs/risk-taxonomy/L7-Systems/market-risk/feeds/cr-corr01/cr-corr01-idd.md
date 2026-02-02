---
# Document Metadata
document_id: CR-CORR-IDD-001
document_name: CR Corr01 Feed - Interface Design Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: CR-CORR-BRD-001  # CR Corr01 BRD
feed_id: CR-CORR-001
---

# CR Corr01 Feed - Interface Design Document

**Meridian Global Bank - Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-CORR-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Interface Overview

### 1.1 Feed Summary

| Property | Value |
|----------|-------|
| **Feed Name** | CR Corr01 (Credit Correlation 01) |
| **Feed ID** | CR-CORR-001 |
| **Direction** | Outbound (Murex → Downstream) |
| **Source System** | Murex (VESPA) |
| **Target Systems** | Risk Data Warehouse, Plato, VESPA Reporting |
| **Frequency** | Daily (T+1) |
| **Format** | CSV (semicolon delimited) |
| **Encoding** | UTF-8 |

### 1.2 File Naming Convention

```
MxMGB_MR_Credit_Corr01_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Values |
|-----------|-------------|--------|
| MxMGB | System prefix | Fixed |
| Vespa | Module identifier | Fixed |
| CR_Corr01 | Feed type | Fixed |
| Region | Trading region | LN, HK, NY, SP |
| YYYYMMDD | As-of date | Business date |

**Example**: `MxMGB_MR_Credit_Corr01_LN_20250102.csv`

---

## 2. Field Specifications

### 2.1 Field Summary

| # | Field Name | Type | Length | Nullable | Description |
|---|------------|------|--------|----------|-------------|
| 1 | TRADE_NUM | Numeric | 10 | No | Murex trade identifier |
| 2 | PORTFOLIO | VarChar | 15 | No | Trading portfolio code |
| 3 | INSTRUMENT | VarChar | 35 | No | PL Instrument name |
| 4 | TRN_FAMILY | VarChar | 5 | No | Trade family code |
| 5 | TRN_GROUP | VarChar | 5 | No | Trade group code |
| 6 | TRN_TYPE | VarChar | 5 | Yes | Trade type code |
| 7 | SECURITY_CODE | VarChar | 15 | Yes | ISIN/Security code |
| 8 | CURRENCY | VarChar | 4 | No | Sensitivity currency |
| 9 | CREDIT_CURVE1 | VarChar | 50 | No | First credit curve name |
| 10 | CREDIT_CURVE2 | VarChar | 50 | Yes | Second credit curve name |
| 11 | CREDIT_ISSUER1 | VarChar | 35 | No | First issuer label |
| 12 | CREDIT_ISSUER2 | VarChar | 35 | Yes | Second issuer label |
| 13 | CREDIT_CORR01 | Numeric | 12,0 | No | Correlation sensitivity |

**Total Fields**: 13

---

## 3. Detailed Field Definitions

### 3.1 TRADE_NUM

| Property | Value |
|----------|-------|
| **Position** | 1 |
| **Field Name** | TRADE_NUM |
| **Data Type** | Numeric |
| **Length** | 10 |
| **Nullable** | No |
| **Description** | Unique Murex trade identifier |
| **Source** | SB_TP_REP.M_NB |
| **Example** | 27571964 |
| **Validation** | Must be positive integer |

### 3.2 PORTFOLIO

| Property | Value |
|----------|-------|
| **Position** | 2 |
| **Field Name** | PORTFOLIO |
| **Data Type** | VarChar |
| **Length** | 15 |
| **Nullable** | No |
| **Description** | Trading portfolio for Bookman hierarchy |
| **Source** | SB_TP_REP.M_TP_PFOLIO |
| **Example** | CTLNMGBLGBB7FRT |
| **Validation** | Must exist in portfolio hierarchy |

### 3.3 INSTRUMENT

| Property | Value |
|----------|-------|
| **Position** | 3 |
| **Field Name** | INSTRUMENT |
| **Data Type** | VarChar |
| **Length** | 35 |
| **Nullable** | No |
| **Description** | PL Instrument name |
| **Source** | SB_TP_REP.M_INSTRUMENT |
| **Example** | CLN 1942 - NAVMINE 4.76% 20/04/27 |
| **Validation** | Must be populated |

### 3.4 TRN_FAMILY

| Property | Value |
|----------|-------|
| **Position** | 4 |
| **Field Name** | TRN_FAMILY |
| **Data Type** | VarChar |
| **Length** | 5 |
| **Nullable** | No |
| **Description** | Trade family classification |
| **Source** | SB_TP_REP.M_TRN_FMLY |
| **Valid Values** | CRD, IRD, EQD |
| **Example** | IRD |
| **Validation** | Must be valid family code |

### 3.5 TRN_GROUP

| Property | Value |
|----------|-------|
| **Position** | 5 |
| **Field Name** | TRN_GROUP |
| **Data Type** | VarChar |
| **Length** | 5 |
| **Nullable** | No |
| **Description** | Trade group classification |
| **Source** | SB_TP_REP.M_TRN_GRP |
| **Valid Values** | BOND, CDS, CDO, CLO, CLN, BSKT |
| **Example** | BOND |
| **Validation** | Must be valid group code |

### 3.6 TRN_TYPE

| Property | Value |
|----------|-------|
| **Position** | 6 |
| **Field Name** | TRN_TYPE |
| **Data Type** | VarChar |
| **Length** | 5 |
| **Nullable** | Yes |
| **Description** | Trade type classification |
| **Source** | SB_TP_REP.M_TRN_TYPE |
| **Example** | CLN, FTD, CDO |
| **Validation** | Optional, must be valid if provided |

### 3.7 SECURITY_CODE

| Property | Value |
|----------|-------|
| **Position** | 7 |
| **Field Name** | SECURITY_CODE |
| **Data Type** | VarChar |
| **Length** | 15 |
| **Nullable** | Yes |
| **Description** | ISIN or security identifier |
| **Source** | SB_TP_BD_REP.M_TP_SECCODU |
| **Example** | XS2497911482 |
| **Validation** | Optional, valid ISIN format if provided |

### 3.8 CURRENCY

| Property | Value |
|----------|-------|
| **Position** | 8 |
| **Field Name** | CURRENCY |
| **Data Type** | VarChar |
| **Length** | 4 |
| **Nullable** | No |
| **Description** | Currency of the correlation sensitivity |
| **Source** | TBL_VESPA_SENS_REP.M_CURRENCY |
| **Valid Values** | ISO currency codes |
| **Example** | USD |
| **Validation** | Must be valid ISO currency code |

### 3.9 CREDIT_CURVE1

| Property | Value |
|----------|-------|
| **Position** | 9 |
| **Field Name** | CREDIT_CURVE1 |
| **Data Type** | VarChar |
| **Length** | 50 |
| **Nullable** | No |
| **Description** | First underlying credit curve (alphabetically) |
| **Source** | TBL_VESPA_SENS_REP.M_CURVE_NAM (via subquery) |
| **Example** | NMMC_USD_SNRFOR |
| **Validation** | Must be populated, must exist in credit curves |

**Derivation Logic**:
```sql
SELECT M_CURVE_NAM
FROM (
    SELECT T2.*, ROW_NUMBER() OVER (ORDER BY M_CURVE_NAM) row_num
    FROM (
        SELECT DISTINCT M_TRADE_NUM, M_CURVE_NAM
        FROM TBL_VESPA_SENS_REP
        WHERE M_CURVE_NAM NOT LIKE '(null)%'
    ) T2
)
WHERE row_num = 1
```

### 3.10 CREDIT_CURVE2

| Property | Value |
|----------|-------|
| **Position** | 10 |
| **Field Name** | CREDIT_CURVE2 |
| **Data Type** | VarChar |
| **Length** | 50 |
| **Nullable** | Yes |
| **Description** | Second underlying credit curve (alphabetically) |
| **Source** | TBL_VESPA_SENS_REP.M_CURVE_NAM (via subquery) |
| **Example** | MGB_USD_SNRFOR |
| **Validation** | Optional, must exist in credit curves if provided |

**Derivation Logic**:
```sql
SELECT M_CURVE_NAM
FROM (
    SELECT T2.*, ROW_NUMBER() OVER (ORDER BY M_CURVE_NAM) row_num
    FROM (
        SELECT DISTINCT M_TRADE_NUM, M_CURVE_NAM
        FROM TBL_VESPA_SENS_REP
        WHERE M_CURVE_NAM NOT LIKE '(null)%'
    ) T2
)
WHERE row_num = 2
```

**Note**: May be NULL for single-underlying correlation products.

### 3.11 CREDIT_ISSUER1

| Property | Value |
|----------|-------|
| **Position** | 11 |
| **Field Name** | CREDIT_ISSUER1 |
| **Data Type** | VarChar |
| **Length** | 35 |
| **Nullable** | No |
| **Description** | Issuer label for first credit curve |
| **Source** | TBL_AC_CRDCURVES_REP.M_ISSUER |
| **Example** | NMMC |
| **Validation** | Must be populated |

**Derivation Logic**:
```sql
SELECT DISTINCT M_ISSUER
FROM TBL_AC_CRDCURVES_REP
WHERE M_LABEL = CREDIT_CURVE1
  AND ROWNUM = 1
```

### 3.12 CREDIT_ISSUER2

| Property | Value |
|----------|-------|
| **Position** | 12 |
| **Field Name** | CREDIT_ISSUER2 |
| **Data Type** | VarChar |
| **Length** | 35 |
| **Nullable** | Yes |
| **Description** | Issuer label for second credit curve |
| **Source** | TBL_AC_CRDCURVES_REP.M_ISSUER |
| **Example** | MGB |
| **Validation** | Optional, corresponds to CREDIT_CURVE2 |

**Derivation Logic**:
```sql
SELECT DISTINCT M_ISSUER
FROM TBL_AC_CRDCURVES_REP
WHERE M_LABEL = CREDIT_CURVE2
  AND ROWNUM = 1
```

**Note**: May be NULL if CREDIT_CURVE2 is NULL.

### 3.13 CREDIT_CORR01

| Property | Value |
|----------|-------|
| **Position** | 13 |
| **Field Name** | CREDIT_CORR01 |
| **Data Type** | Numeric |
| **Length** | 12,0 |
| **Nullable** | No |
| **Description** | Correlation sensitivity (Corr01) in local currency |
| **Source** | TBL_VESPA_SENS_REP.M_CORR01 |
| **Unit** | Local currency (whole units) |
| **Example** | -2014 |
| **Validation** | Non-zero (filtered in extraction) |

**Business Interpretation**:
- **Positive value**: Long correlation - P&L increases if correlation rises
- **Negative value**: Short correlation - P&L decreases if correlation rises
- **Magnitude**: P&L impact per 1bp correlation change

---

## 4. Record Layout

### 4.1 Header Record

```
TRADE_NUM;PORTFOLIO;INSTRUMENT;TRN_FAMILY;TRN_GROUP;TRN_TYPE;SECURITY_CODE;CURRENCY;CREDIT_CURVE1;CREDIT_CURVE2;CREDIT_ISSUER1;CREDIT_ISSUER2;CREDIT_CORR01
```

### 4.2 Data Record Example

```
27571964;CTLNMGBLGBB7FRT;CLN 1942 - NAVMINE 4.76% 20/04/27;IRD;BOND;;XS2497911482;USD;NMMC_USD_SNRFOR;MGB_USD_SNRFOR;NMMC;MGB;-2014
```

### 4.3 Field Positions

| Position | Field | Start | End | Length |
|----------|-------|-------|-----|--------|
| 1 | TRADE_NUM | 1 | Variable | 10 |
| 2 | PORTFOLIO | Variable | Variable | 15 |
| 3 | INSTRUMENT | Variable | Variable | 35 |
| 4 | TRN_FAMILY | Variable | Variable | 5 |
| 5 | TRN_GROUP | Variable | Variable | 5 |
| 6 | TRN_TYPE | Variable | Variable | 5 |
| 7 | SECURITY_CODE | Variable | Variable | 15 |
| 8 | CURRENCY | Variable | Variable | 4 |
| 9 | CREDIT_CURVE1 | Variable | Variable | 50 |
| 10 | CREDIT_CURVE2 | Variable | Variable | 50 |
| 11 | CREDIT_ISSUER1 | Variable | Variable | 35 |
| 12 | CREDIT_ISSUER2 | Variable | Variable | 35 |
| 13 | CREDIT_CORR01 | Variable | Variable | 12 |

---

## 5. Sample Data

### 5.1 Complete File Example

```csv
TRADE_NUM;PORTFOLIO;INSTRUMENT;TRN_FAMILY;TRN_GROUP;TRN_TYPE;SECURITY_CODE;CURRENCY;CREDIT_CURVE1;CREDIT_CURVE2;CREDIT_ISSUER1;CREDIT_ISSUER2;CREDIT_CORR01
27571964;CTLNMGBLGBB7FRT;CLN 1942 - NAVMINE 4.76% 20/04/27;IRD;BOND;;XS2497911482;USD;NMMC_USD_SNRFOR;MGB_USD_SNRFOR;NMMC;MGB;-2014
28123456;CDOLNMGB01;CDO TRANCHE 2024-1 EQUITY;CRD;CDO;CDO;XS1234567890;USD;AAA_USD_SNRFOR;BBB_USD_SNRFOR;AAA Corp;BBB Corp;125000
28234567;CDOLNMGB01;CDO TRANCHE 2024-1 MEZZ;CRD;CDO;CDO;XS1234567891;USD;AAA_USD_SNRFOR;BBB_USD_SNRFOR;AAA Corp;BBB Corp;-45000
28345678;FTDLNMGB01;FTD BASKET 2024-Q1;CRD;BSKT;FTD;XS2345678901;EUR;CCC_EUR_SNRFOR;DDD_EUR_SNRFOR;CCC Corp;DDD Corp;-8500
28456789;CLNHKMGB01;CLN ASIA CREDIT 2024-2;CRD;CLN;CLN;XS3456789012;USD;EEE_USD_SNRFOR;;EEE Corp;;32000
```

### 5.2 Sample Data Interpretation

| Trade | Type | Correlation Position | Meaning |
|-------|------|---------------------|---------|
| 27571964 | CLN | Short (-2014) | Loses if correlation rises |
| 28123456 | CDO Equity | Long (+125000) | Benefits from higher correlation |
| 28234567 | CDO Mezz | Short (-45000) | Loses if correlation rises |
| 28345678 | FTD | Short (-8500) | FTDs are typically short correlation |
| 28456789 | CLN | Long (+32000) | Single-reference (CURVE2 null) |

---

## 6. Validation Rules

### 6.1 Record-Level Validations

| Rule ID | Field(s) | Validation | Action |
|---------|----------|------------|--------|
| VR-001 | TRADE_NUM | Must be positive integer | Reject |
| VR-002 | PORTFOLIO | Must exist in Bookman hierarchy | Flag |
| VR-003 | TRN_FAMILY | Must be valid family code | Reject |
| VR-004 | TRN_GROUP | Must be valid group code | Reject |
| VR-005 | CURRENCY | Must be valid ISO code | Reject |
| VR-006 | CREDIT_CURVE1 | Must be populated | Reject |
| VR-007 | CREDIT_ISSUER1 | Must be populated | Flag |
| VR-008 | CREDIT_CORR01 | Must be non-zero | Filter (WHERE clause) |

### 6.2 File-Level Validations

| Rule ID | Validation | Action |
|---------|------------|--------|
| VF-001 | File not empty (excluding header) | Warning |
| VF-002 | No duplicate TRADE_NUM | Reject duplicates |
| VF-003 | All fields present in header | Reject file |
| VF-004 | Row count within expected range | Warning if variance >20% |

### 6.3 Cross-Field Validations

| Rule ID | Fields | Validation | Action |
|---------|--------|------------|--------|
| VX-001 | CREDIT_CURVE2, CREDIT_ISSUER2 | If CURVE2 populated, ISSUER2 should be populated | Warning |
| VX-002 | TRN_GROUP, CREDIT_CORR01 | Correlation products should have Corr01 | Info |

---

## 7. Interface Schedule

### 7.1 Daily Schedule (GMT)

| Time | Event | Description |
|------|-------|-------------|
| 18:00 | Credit curve calibration | Curves available |
| 20:00 | Monte Carlo valuation | Corr01 calculated |
| 21:00 | TBL_VESPA_SENS_REP populated | Data available |
| 03:30 | Extraction batch start | Regional processing |
| 04:30 | Extraction complete | Files generated |
| 05:00 | Packaging | ZIP file created |
| 05:30 | Delivery | Files available to downstream |

### 7.2 Regional Schedule

| Region | Extraction Start | Extraction End | Delivery |
|--------|------------------|----------------|----------|
| LN | 03:30 GMT | 04:00 GMT | 05:30 GMT |
| HK | 21:30 HKT | 22:00 HKT | 23:30 HKT |
| NY | 22:30 EST | 23:00 EST | 00:30 EST+1 |
| SP | 21:30 SGT | 22:00 SGT | 23:30 SGT |

---

## 8. Error Handling

### 8.1 Error Codes

| Code | Description | Severity | Action |
|------|-------------|----------|--------|
| E001 | Source table unavailable | Critical | Abort extraction |
| E002 | No data returned | Warning | Generate empty file with header |
| E003 | Field validation failure | Error | Reject record |
| E004 | Curve lookup failure | Warning | Null curve/issuer |
| E005 | File write failure | Critical | Retry, escalate |

### 8.2 Error Recovery

| Scenario | Recovery Action |
|----------|-----------------|
| MC valuation incomplete | Wait, re-run after completion |
| Partial extraction failure | Re-run from checkpoint |
| File delivery failure | Retry 3 times, then escalate |
| Data quality issue | Manual review, correction, re-run |

---

## 9. Comparison with Other CR Feeds

### 9.1 Field Count Comparison

| Feed | Fields | Structure |
|------|--------|-----------|
| CR Delta Zero | 23 | Non-CRDI + CRDI UNION |
| CR Delta Par | 23 | Non-CRDI + CRDI UNION (3-way) |
| CR Basis Rate | 20 | Non-CRDI + CRDI UNION |
| CR Par CDS Rate | 19 | Non-CRDI + CRDI UNION |
| **CR Corr01** | **13** | **Non-CRDI only** |
| CR Instrument Spread | TBD | TBD |
| CR RR01 | TBD | TBD |
| CR RR02 | TBD | TBD |

### 9.2 Key Structural Differences

| Aspect | CR Corr01 | Other CR Feeds |
|--------|-----------|----------------|
| **CRDI Component** | No | Yes |
| **Tenor Pillars** | No | Yes (most) |
| **USD Conversion** | No | Yes (most) |
| **Multiple Curves/Issuers** | Yes (2 each) | No (single) |
| **NOTIONAL** | No | Yes (sensitivity feeds) |
| **MARKET** | No | Yes (sensitivity feeds) |

---

## 10. Downstream Integration

### 10.1 Target Systems

| System | Usage | Key Fields |
|--------|-------|------------|
| Risk Data Warehouse | Storage, reporting | All fields |
| Plato (Risk Engine) | Correlation risk calculation | CREDIT_CORR01, CURRENCY |
| VESPA Reporting | Regulatory reporting | All fields |
| P&L Attribution | P&L explain | CREDIT_CORR01, TRADE_NUM |

### 10.2 Integration Points

| Integration | Protocol | Format |
|-------------|----------|--------|
| Risk DW Load | File-based | CSV |
| Plato Feed | SFTP | CSV (in ZIP) |
| Reporting Extract | Database | Table load |

---

## 11. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [CR Corr01 BRD](./cr-corr01-brd.md) | CR-CORR-BRD-001 | Business requirements |
| [CR Corr01 IT Config](./cr-corr01-config.md) | CR-CORR-CFG-001 | Technical configuration |
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |

---

## 12. Document Control

### 12.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-02 | Initial version | Risk Technology |

### 12.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Technical review | Annual | January 2026 |
| Schema review | On change | As needed |
| Integration review | Quarterly | April 2025 |

---

*End of Document*
