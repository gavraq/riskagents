---
# Document Metadata
document_id: CR-RR01-IDD-001
document_name: CR RR01 Feed - Interface Design Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: CR-RR01-BRD-001  # CR RR01 BRD
feed_id: CR-RR01-001
---

# CR RR01 Feed - Interface Design Document

**Meridian Global Bank - Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-RR01-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Interface Overview

### 1.1 Feed Summary

| Property | Value |
|----------|-------|
| **Feed Name** | CR RR01 (Credit Recovery Rate 01) |
| **Feed ID** | CR-RR01-001 |
| **Direction** | Outbound (Murex → Downstream) |
| **Source System** | Murex (VESPA) |
| **Target Systems** | Risk Data Warehouse, Plato, VESPA Reporting |
| **Frequency** | Daily (T+1) |
| **Format** | CSV (semicolon delimited) |
| **Encoding** | UTF-8 |

### 1.2 File Naming Convention

```
MxMGB_MR_Credit_RR01_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Values |
|-----------|-------------|--------|
| MxMGB | System prefix | Fixed |
| Vespa | Module identifier | Fixed |
| CR_RR01 | Feed type | Fixed |
| Region | Trading region | LN, HK, NY, SP |
| YYYYMMDD | As-of date | Business date |

**Example**: `MxMGB_MR_Credit_RR01_LN_20250102.csv`

---

## 2. Field Specifications

### 2.1 Field Summary

| # | Field Name | Type | Length | Nullable | Description |
|---|------------|------|--------|----------|-------------|
| 1 | TRADE_NUM | Numeric | 10 | No | Murex trade identifier |
| 2 | FAMILY | VarChar | 16 | No | Trade family code |
| 3 | GROUP | VarChar | 5 | No | Trade group code |
| 4 | TYPE | VarChar | 16 | Yes | Trade type code |
| 5 | TYPOLOGY | VarChar | 21 | Yes | Trade typology |
| 6 | PORTFOLIO | VarChar | 20 | No | Trading portfolio code |
| 7 | INSTRUMENT | VarChar | 30 | No | PL Instrument name |
| 8 | ISSUER | VarChar | 50 | No | Issuer label |
| 9 | CURVE_NAME | VarChar | 50 | No | Credit curve name |
| 10 | DATE | VarChar | 64 | Yes | Tenor pillar date |
| 11 | RECOVERY_RATE | Numeric | 12 | No | Recovery rate (%) |
| 12 | RR01_SENSI | Numeric | 16,2 | No | Recovery rate sensitivity |
| 13 | CURRENCY | VarChar | 4 | No | Sensitivity currency |
| 14 | CIF | Numeric | 9 | Yes | Customer Information File ID |
| 15 | GLOBUS_ID | VarChar | 10 | Yes | External issuer ID |
| 16 | COUNTRY | VarChar | 30 | Yes | Country of risk |
| 17 | ISIN | VarChar | 25 | Yes | Reference obligation ISIN |
| 18 | MATURITY | Date | 8 | No | Trade maturity date |
| 19 | UNDERLYING | VarChar | 15 | Yes | Reference obligation label |
| 20 | RESTRUCT | VarChar | 16 | No | Restructuring terms |

**Total Fields**: 20

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
| **Source** | TBL_VESPA_SENS_REP.M_TRADE_NUM / TBL_VESPA_SENSCI_REP.M_TRADE_NUM |
| **Example** | 27522095 |
| **Validation** | Must be positive integer |

### 3.2 FAMILY

| Property | Value |
|----------|-------|
| **Position** | 2 |
| **Field Name** | FAMILY |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Nullable** | No |
| **Description** | Trade family classification |
| **Source** | VSP.M_FAMILY |
| **Valid Values** | CRD, IRD, EQD, FXD |
| **Example** | IRD |

### 3.3 GROUP

| Property | Value |
|----------|-------|
| **Position** | 3 |
| **Field Name** | GROUP |
| **Data Type** | VarChar |
| **Length** | 5 |
| **Nullable** | No |
| **Description** | Trade group classification |
| **Source** | VSP.M_GROUP |
| **Valid Values** | CDS, BOND, CRDI, CLN, CDO |
| **Example** | BOND |

### 3.4 TYPE

| Property | Value |
|----------|-------|
| **Position** | 4 |
| **Field Name** | TYPE |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Nullable** | Yes |
| **Description** | Trade type classification |
| **Source** | VSP.M_TYPE |
| **Example** | CDS, FRN, CLN |

### 3.5 TYPOLOGY

| Property | Value |
|----------|-------|
| **Position** | 5 |
| **Field Name** | TYPOLOGY |
| **Data Type** | VarChar |
| **Length** | 21 |
| **Nullable** | Yes |
| **Description** | Trade typology for risk classification |
| **Source** | VSP.M_TYPOLOGY (Non-CRDI) / VSP.M_LABEL (CRDI) |
| **Example** | IRD - FX PASSTHROUGH |

### 3.6 PORTFOLIO

| Property | Value |
|----------|-------|
| **Position** | 6 |
| **Field Name** | PORTFOLIO |
| **Data Type** | VarChar |
| **Length** | 20 |
| **Nullable** | No |
| **Description** | Trading portfolio for Bookman hierarchy |
| **Source** | VSP.M_PORTFOLIO |
| **Example** | LMLNMGBLEMP7FRT |

### 3.7 INSTRUMENT

| Property | Value |
|----------|-------|
| **Position** | 7 |
| **Field Name** | INSTRUMENT |
| **Data Type** | VarChar |
| **Length** | 30 |
| **Nullable** | No |
| **Description** | PL Instrument name |
| **Source** | VSP.M_PL_INSTRU |
| **Example** | FXPASS 1941-MZN 17% 11/05/25 |

### 3.8 ISSUER

| Property | Value |
|----------|-------|
| **Position** | 8 |
| **Field Name** | ISSUER |
| **Data Type** | VarChar |
| **Length** | 50 |
| **Nullable** | No |
| **Description** | Issuer label (or PL Instrument for CRDI) |
| **Source Non-CRDI** | CASE WHEN M_ISSUER IS NULL THEN M_PL_INSTRU ELSE M_ISSUER END |
| **Source CRDI** | VSP.M_PL_INSTRU |
| **Example** | THE MIN ECO FIN REP MOZAMBIQUE |

### 3.9 CURVE_NAME

| Property | Value |
|----------|-------|
| **Position** | 9 |
| **Field Name** | CURVE_NAME |
| **Data Type** | VarChar |
| **Length** | 50 |
| **Nullable** | No |
| **Description** | Credit spread curve name |
| **Source Non-CRDI** | VSP.M_CURVE_NA1 |
| **Source CRDI** | VSP.M_PL_INSTRU |
| **Example** | MOZAMBIQUE_MZN_SNRFOR |

### 3.10 DATE

| Property | Value |
|----------|-------|
| **Position** | 10 |
| **Field Name** | DATE |
| **Data Type** | VarChar |
| **Length** | 64 |
| **Nullable** | Yes |
| **Description** | Tenor pillar date |
| **Source Non-CRDI** | VSP.M_DATE__ZER |
| **Source CRDI** | '' (blank) |
| **Valid Values** | 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 15Y, 20Y, 30Y |
| **Example** | 1Y |

### 3.11 RECOVERY_RATE

| Property | Value |
|----------|-------|
| **Position** | 11 |
| **Field Name** | RECOVERY_RATE |
| **Data Type** | Numeric |
| **Length** | 12 |
| **Nullable** | No |
| **Description** | Recovery rate assumption (percentage) |
| **Source Non-CRDI** | VSP.M_RATE |
| **Source CRDI** | 0 |
| **Unit** | Percentage (e.g., 40.0 = 40%) |
| **Example** | 40.000000 |
| **Validation** | 0 <= value <= 100 |

### 3.12 RR01_SENSI

| Property | Value |
|----------|-------|
| **Position** | 12 |
| **Field Name** | RR01_SENSI |
| **Data Type** | Numeric |
| **Length** | 16,2 |
| **Nullable** | No |
| **Description** | Recovery rate sensitivity WITH propagation |
| **Source** | VSP.M_RECOVERY_ |
| **Unit** | Local currency |
| **Example** | 132.13 |
| **Validation** | Can be positive, negative, or zero |

**Business Interpretation**:
- **Positive**: Higher recovery = higher P&L
- **Negative**: Higher recovery = lower P&L
- **Magnitude**: P&L impact per 1% recovery change (with spread recalibration)

### 3.13 CURRENCY

| Property | Value |
|----------|-------|
| **Position** | 13 |
| **Field Name** | CURRENCY |
| **Data Type** | VarChar |
| **Length** | 4 |
| **Nullable** | No |
| **Description** | Currency of the sensitivity |
| **Source Non-CRDI** | VSP.M_CURRENCY2 |
| **Source CRDI** | VSP.M_CURRENCY |
| **Valid Values** | ISO currency codes |
| **Example** | MZN |

### 3.14 CIF

| Property | Value |
|----------|-------|
| **Position** | 14 |
| **Field Name** | CIF |
| **Data Type** | Numeric |
| **Length** | 9 |
| **Nullable** | Yes |
| **Description** | Customer Information File identifier |
| **Source Non-CRDI** | CP.M_U_CIF_ID |
| **Source CRDI** | 0 |
| **Example** | 100060635 |

### 3.15 GLOBUS_ID

| Property | Value |
|----------|-------|
| **Position** | 15 |
| **Field Name** | GLOBUS_ID |
| **Data Type** | VarChar |
| **Length** | 10 |
| **Nullable** | Yes |
| **Description** | External issuer identifier (GLOBUS system) |
| **Source Non-CRDI** | CP.M_U_GLOBID |
| **Source CRDI** | '' (blank) |
| **Example** | 101088 |

### 3.16 COUNTRY

| Property | Value |
|----------|-------|
| **Position** | 16 |
| **Field Name** | COUNTRY |
| **Data Type** | VarChar |
| **Length** | 30 |
| **Nullable** | Yes |
| **Description** | Country of risk for the issuer |
| **Source Non-CRDI** | CP.M_U_RSK_CTRY |
| **Source CRDI** | '' (blank) |
| **Example** | UNITED KINGDOM |

### 3.17 ISIN

| Property | Value |
|----------|-------|
| **Position** | 17 |
| **Field Name** | ISIN |
| **Data Type** | VarChar |
| **Length** | 25 |
| **Nullable** | Yes |
| **Description** | ISIN of reference obligation |
| **Source Non-CRDI** | OBL.M_REF_OBLI1 |
| **Source CRDI** | '' (blank) |
| **Example** | XS1234567890 |

### 3.18 MATURITY

| Property | Value |
|----------|-------|
| **Position** | 18 |
| **Field Name** | MATURITY |
| **Data Type** | Date |
| **Length** | 8 |
| **Nullable** | No |
| **Description** | Trade maturity date |
| **Source** | TP.M_TP_DTEEXP |
| **Format** | DD/MM/YY or YYYY-MM-DD |
| **Example** | 11/05/25 |

### 3.19 UNDERLYING

| Property | Value |
|----------|-------|
| **Position** | 19 |
| **Field Name** | UNDERLYING |
| **Data Type** | VarChar |
| **Length** | 15 |
| **Nullable** | Yes |
| **Description** | Reference obligation label (CDS only) |
| **Source Non-CRDI** | OBL.M_REF_OBLIG |
| **Source CRDI** | '' (blank) |
| **Example** | MOZAM 7.5% 2023 |

### 3.20 RESTRUCT

| Property | Value |
|----------|-------|
| **Position** | 20 |
| **Field Name** | RESTRUCT |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Nullable** | No |
| **Description** | CDS restructuring terms |
| **Source Non-CRDI** | CASE WHEN OBL.M_RESTRUCTU = 'Yes' THEN OBL.M_RESTRUCTU ELSE 'NONE' END |
| **Source CRDI** | 'NONE' |
| **Valid Values** | Yes, NONE |
| **Example** | NONE |

---

## 4. Record Layout

### 4.1 Header Record

```
TRADE_NUM;FAMILY;GROUP;TYPE;TYPOLOGY;PORTFOLIO;INSTRUMENT;ISSUER;CURVE_NAME;DATE;RECOVERY_RATE;RR01_SENSI;CURRENCY;CIF;GLOBUS_ID;COUNTRY;ISIN;MATURITY;UNDERLYING;RESTRUCT
```

### 4.2 Data Record Example (Non-CRDI)

```
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB; THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;1Y;40.000000;132.13;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;;NONE
```

### 4.3 Data Record Example (CRDI)

```
28123456;CRD;CRDI;CRDI;CDX.NA.IG;CDXLNMGB01;CDX.NA.IG.S39;CDX.NA.IG.S39;CDX.NA.IG.S39;;0;5420.50;USD;0;;;20/06/28;;NONE
```

---

## 5. Sample Data

### 5.1 Complete File Example

```csv
TRADE_NUM;FAMILY;GROUP;TYPE;TYPOLOGY;PORTFOLIO;INSTRUMENT;ISSUER;CURVE_NAME;DATE;RECOVERY_RATE;RR01_SENSI;CURRENCY;CIF;GLOBUS_ID;COUNTRY;ISIN;MATURITY;UNDERLYING;RESTRUCT
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB; THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;6M;40.000000;0.00;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;;NONE
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB; THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;1Y;40.000000;132.13;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;;NONE
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB; THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;2Y;40.000000;229.75;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;;NONE
28234567;CRD;CDS;CDS;CDS_PROTECTION_BUYER;CDSLNMGB01;ABC Corp 5Y CDS;ABC Corporation;ABC_USD_SNRFOR;5Y;35.000000;-1250.00;USD;100012345;123456;UNITED STATES;XS1234567890;15/06/29;ABC 4.5% 2029;Yes
28345678;CRD;CRDI;CRDI;iTraxx Europe;IDXLNMGB01;iTraxx Europe S40;iTraxx Europe S40;iTraxx Europe S40;;0;8750.25;EUR;0;;;20/12/28;;NONE
```

### 5.2 Sample Data Interpretation

| Trade | Type | Recovery | RR01 | Interpretation |
|-------|------|----------|------|----------------|
| 27522095 (6M) | Bond | 40% | 0.00 | Near-term: no recovery sensitivity |
| 27522095 (1Y) | Bond | 40% | 132.13 | 1% recovery up = +132 MZN P&L |
| 27522095 (2Y) | Bond | 40% | 229.75 | Longer tenor = higher sensitivity |
| 28234567 | CDS Buy | 35% | -1250.00 | Protection buyer loses if recovery up |
| 28345678 | iTraxx | N/A | 8750.25 | Index-level aggregated sensitivity |

---

## 6. Validation Rules

### 6.1 Record-Level Validations

| Rule ID | Field(s) | Validation | Action |
|---------|----------|------------|--------|
| VR-001 | TRADE_NUM | Must be positive integer | Reject |
| VR-002 | FAMILY | Must be valid family code | Reject |
| VR-003 | GROUP | Must be valid group code | Reject |
| VR-004 | PORTFOLIO | Must exist in Bookman hierarchy | Flag |
| VR-005 | ISSUER | Must be populated | Reject |
| VR-006 | RECOVERY_RATE | 0 <= value <= 100 (non-CRDI) | Flag |
| VR-007 | CURRENCY | Must be valid ISO code | Reject |
| VR-008 | MATURITY | Must be valid date | Flag |
| VR-009 | RESTRUCT | Must be 'Yes' or 'NONE' | Flag |

### 6.2 File-Level Validations

| Rule ID | Validation | Action |
|---------|------------|--------|
| VF-001 | File not empty (excluding header) | Warning |
| VF-002 | Header matches expected format | Reject file |
| VF-003 | Row count within expected range | Warning if variance >20% |
| VF-004 | All 20 fields present per row | Reject record |

### 6.3 Cross-Field Validations

| Rule ID | Fields | Validation | Action |
|---------|--------|------------|--------|
| VX-001 | GROUP, DATE | CRDI should have blank DATE | Warning |
| VX-002 | GROUP, RECOVERY_RATE | CRDI should have RECOVERY_RATE = 0 | Warning |
| VX-003 | GROUP, CIF | CRDI should have CIF = 0 | Warning |
| VX-004 | GROUP, RESTRUCT | Non-CDS should have RESTRUCT = 'NONE' | Info |

---

## 7. Interface Schedule

### 7.1 Daily Schedule (GMT)

| Time | Event | Description |
|------|-------|-------------|
| 18:00 | Credit curve calibration | Curves available |
| 18:00 | Recovery rate data | Recovery assumptions |
| 21:00 | Valuation batch complete | Sensitivities calculated |
| 03:00 | Extraction batch start | Regional processing |
| 04:00 | Extraction complete | Files generated |
| 05:00 | Packaging | ZIP file created |
| 05:30 | Delivery | Files available to downstream |

### 7.2 Regional Schedule

| Region | Extraction Start | Extraction End | Delivery |
|--------|------------------|----------------|----------|
| LN | 03:00 GMT | 04:00 GMT | 05:30 GMT |
| HK | 21:00 HKT | 22:00 HKT | 23:30 HKT |
| NY | 22:00 EST | 23:00 EST | 00:30 EST+1 |
| SP | 21:00 SGT | 22:00 SGT | 23:30 SGT |

---

## 8. Error Handling

### 8.1 Error Codes

| Code | Description | Severity | Action |
|------|-------------|----------|--------|
| E001 | Source table unavailable | Critical | Abort extraction |
| E002 | No data returned | Warning | Generate empty file with header |
| E003 | Field validation failure | Error | Reject record |
| E004 | Counterparty lookup failure | Warning | Null CIF/GLOBUS_ID/COUNTRY |
| E005 | File write failure | Critical | Retry, escalate |

### 8.2 Error Recovery

| Scenario | Recovery Action |
|----------|-----------------|
| Valuation incomplete | Wait, re-run after completion |
| Partial extraction failure | Re-run from checkpoint |
| File delivery failure | Retry 3 times, then escalate |
| Data quality issue | Manual review, correction, re-run |

---

## 9. Comparison with Related Feeds

### 9.1 CR RR01 vs CR RR02 vs CR Basis Rate

| Aspect | CR RR01 | CR RR02 | CR Basis Rate |
|--------|---------|---------|---------------|
| **Source Field** | M_RECOVERY_ | M_RECOVERY1 | M_RECOVERY1 |
| **Propagation** | WITH | WITHOUT | WITHOUT |
| **Sensitivity Name** | RR01_SENSI | RR02_SENSI | RECOVERY_RATE_SENSI |
| **Field Count** | 20 | 20 | 20 |
| **Magnitude** | Higher | Lower | Same as RR02 |

### 9.2 Field Count Comparison

| Feed | Fields | Structure |
|------|--------|-----------|
| CR Delta Zero | 23 | UNION |
| CR Delta Par | 23 | 3-way UNION |
| CR Basis Rate | 20 | UNION |
| CR Par CDS Rate | 19 | UNION |
| CR Corr01 | 13 | Non-CRDI only |
| **CR RR01** | **20** | **UNION** |
| CR RR02 | 20 | UNION |

---

## 10. Downstream Integration

### 10.1 Target Systems

| System | Usage | Key Fields |
|--------|-------|------------|
| Risk Data Warehouse | Storage, reporting | All fields |
| Plato (Risk Engine) | Recovery risk calculation | RR01_SENSI, CURRENCY |
| VESPA Reporting | Regulatory reporting | All fields |
| P&L Attribution | P&L explain | RR01_SENSI, TRADE_NUM |
| Jump-to-Default | JTD calculation | RR01_SENSI, RECOVERY_RATE |

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
| [CR RR01 BRD](./cr-rr01-brd.md) | CR-RR01-BRD-001 | Business requirements |
| [CR RR01 IT Config](./cr-rr01-config.md) | CR-RR01-CFG-001 | Technical configuration |
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
