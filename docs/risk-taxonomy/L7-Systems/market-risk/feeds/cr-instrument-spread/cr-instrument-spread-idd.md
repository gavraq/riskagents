---
# Document Metadata
document_id: CR-IS-IDD-001
document_name: CR Instrument Spread Feed - Interface Design Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: CR-IS-BRD-001  # CR Instrument Spread BRD
feed_id: CR-IS-001
---

# CR Instrument Spread Feed - Interface Design Document

**Meridian Global Bank - Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-IS-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Interface Overview

### 1.1 Feed Summary

| Property | Value |
|----------|-------|
| **Feed Name** | CR Instrument Spread (Credit Zero Spread CDS) |
| **Feed ID** | CR-IS-001 |
| **Direction** | Outbound (Murex → Downstream) |
| **Source System** | Murex (VESPA) |
| **Target Systems** | Risk Data Warehouse, Plato, VESPA Reporting |
| **Frequency** | Daily (T+1) |
| **Format** | CSV (semicolon delimited) |
| **Encoding** | UTF-8 |

### 1.2 File Naming Convention

```
MxMGB_MR_Credit_Spread_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Values |
|-----------|-------------|--------|
| MxMGB | System prefix | Fixed |
| Vespa | Module identifier | Fixed |
| CR_Instrument_Spread | Feed type | Fixed |
| Region | Trading region | LN, HK, NY, SP |
| YYYYMMDD | As-of date | Business date |

**Example**: `MxMGB_MR_Credit_Spread_LN_20250102.csv`

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
| 12 | **SPREAD** | Numeric | 16,6 | No | **Bond zero coupon spread** |
| 13 | CURRENCY | VarChar | 4 | No | Currency |
| 14 | CIF | Numeric | 9 | Yes | Customer Information File ID |
| 15 | GLOBUS_ID | VarChar | 10 | Yes | External issuer ID |
| 16 | COUNTRY | VarChar | 30 | Yes | Country of risk |
| 17 | ISIN | VarChar | 25 | Yes | Reference obligation ISIN |
| 18 | MATURITY | Date | 8 | No | Trade maturity date |
| 19 | UNDERLYING | VarChar | 15 | Yes | Reference obligation label |

**Total Fields**: 19 (Note: Unlike RR01/RR02, this feed does not include RESTRUCT)

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
| **Source** | TBL_VESPA_SENS_REP.M_TRADE_NUM / TBL_VESPA_SENSCIR_REP.M_TRADE_NUM |
| **Example** | 27522095 |

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
| **Example** | CDS |

### 3.5 TYPOLOGY

| Property | Value |
|----------|-------|
| **Position** | 5 |
| **Field Name** | TYPOLOGY |
| **Data Type** | VarChar |
| **Length** | 21 |
| **Nullable** | Yes |
| **Description** | Trade typology/strategy |
| **Source** | VSP.M_TYPOLOGY (Non-CRDI) / VSP.M_LABEL (CRDI) |
| **Example** | IRD - FX PASSTHROUGH, CDX.NA.IG |

### 3.6 PORTFOLIO

| Property | Value |
|----------|-------|
| **Position** | 6 |
| **Field Name** | PORTFOLIO |
| **Data Type** | VarChar |
| **Length** | 20 |
| **Nullable** | No |
| **Description** | Trading portfolio code in Bookman hierarchy |
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
| **Example** | FXPASS 1941-MZN 17% 11/05/25, CDX.NA.IG.S39 |

### 3.8 ISSUER

| Property | Value |
|----------|-------|
| **Position** | 8 |
| **Field Name** | ISSUER |
| **Data Type** | VarChar |
| **Length** | 50 |
| **Nullable** | No |
| **Description** | Issuer label for the credit entity |
| **Source (Non-CRDI)** | CASE WHEN M_ISSUER IS NULL THEN M_PL_INSTRU ELSE M_ISSUER END |
| **Source (CRDI)** | M_PL_INSTRU |
| **Example** | MGB, ABC Corporation, CDX.NA.IG.S39 |

### 3.9 CURVE_NAME

| Property | Value |
|----------|-------|
| **Position** | 9 |
| **Field Name** | CURVE_NAME |
| **Data Type** | VarChar |
| **Length** | 50 |
| **Nullable** | No |
| **Description** | Underlying credit curve name |
| **Source (Non-CRDI)** | VSP.M_CURVE_NA1 |
| **Source (CRDI)** | VSP.M_PL_INSTRU |
| **Example** | THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR |

### 3.10 DATE

| Property | Value |
|----------|-------|
| **Position** | 10 |
| **Field Name** | DATE |
| **Data Type** | VarChar |
| **Length** | 64 |
| **Nullable** | Yes |
| **Description** | Tenor pillar date for sensitivity |
| **Source (Non-CRDI)** | VSP.M_DATE__ZER |
| **Source (CRDI)** | Empty string ('') |
| **Valid Values** | 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, etc. |
| **Example** | 6M, 1Y, 2Y |

### 3.11 RECOVERY_RATE

| Property | Value |
|----------|-------|
| **Position** | 11 |
| **Field Name** | RECOVERY_RATE |
| **Data Type** | Numeric |
| **Length** | 12 |
| **Nullable** | No |
| **Description** | Recovery rate assumption for the issuer |
| **Source (Non-CRDI)** | VSP.M_RATE |
| **Source (CRDI)** | 0 (hardcoded) |
| **Unit** | Percentage (e.g., 40.000000 = 40%) |
| **Example** | 40.000000 |

### 3.12 SPREAD

| Property | Value |
|----------|-------|
| **Position** | 12 |
| **Field Name** | SPREAD |
| **Data Type** | Numeric |
| **Length** | 16,6 |
| **Nullable** | No |
| **Description** | **Bond zero coupon spread used in P&L computation** |
| **Source** | VSP.M_ZERO_SPRE / 100 (per CM-6402) |
| **Unit** | Decimal (e.g., 0.025000 = 250 basis points) |
| **Example** | 0.000000 |
| **Validation** | Can be positive, negative, or zero |

**Business Interpretation**:
- **Positive spread**: Credit risk premium over risk-free rate
- **Higher spread**: Higher perceived credit risk / wider market quote
- **Zero spread**: Typically for AAA credits or index-level aggregation
- **Negative spread**: Rare, indicates trading below risk-free (e.g., flight to quality)

**Change History**:
- **CM-6402**: Changed to divide M_ZERO_SPRE by 100 for decimal representation

### 3.13 CURRENCY

| Property | Value |
|----------|-------|
| **Position** | 13 |
| **Field Name** | CURRENCY |
| **Data Type** | VarChar |
| **Length** | 4 |
| **Nullable** | No |
| **Description** | Currency of the spread |
| **Source (Non-CRDI)** | VSP.M_CURRENCY2 |
| **Source (CRDI)** | VSP.M_CURRENCY |
| **Example** | MZN, USD, EUR |

### 3.14 CIF

| Property | Value |
|----------|-------|
| **Position** | 14 |
| **Field Name** | CIF |
| **Data Type** | Numeric |
| **Length** | 9 |
| **Nullable** | Yes |
| **Description** | Customer Information File ID for the issuer |
| **Source (Non-CRDI)** | CP.M_U_CIF_ID (from counterparty UDF) |
| **Source (CRDI)** | 0 (hardcoded) |
| **Example** | 100060635 |

### 3.15 GLOBUS_ID

| Property | Value |
|----------|-------|
| **Position** | 15 |
| **Field Name** | GLOBUS_ID |
| **Data Type** | VarChar |
| **Length** | 10 |
| **Nullable** | Yes |
| **Description** | External issuer ID from GLOBUS system |
| **Source (Non-CRDI)** | CP.M_U_GLOBID (from counterparty UDF) |
| **Source (CRDI)** | Empty string ('') |
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
| **Source (Non-CRDI)** | CP.M_U_RSK_CTRY (from counterparty UDF) |
| **Source (CRDI)** | Empty string ('') |
| **Example** | UNITED KINGDOM, UNITED STATES |

### 3.17 ISIN

| Property | Value |
|----------|-------|
| **Position** | 17 |
| **Field Name** | ISIN |
| **Data Type** | VarChar |
| **Length** | 25 |
| **Nullable** | Yes |
| **Description** | ISIN code of the underlying reference obligation |
| **Source (Non-CRDI)** | OBL.M_REF_OBLI1 (for CDS) / SE_CODE (for bonds) |
| **Source (CRDI)** | Empty string ('') |
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
| **Source** | TP.M_TP_DTEEXP (from SB_TP_REP) |
| **Format** | DD/MM/YY |
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
| **Source (Non-CRDI)** | OBL.M_REF_OBLIG (for CDS) |
| **Source (CRDI)** | Empty string ('') |
| **Example** | ABC 4.5% 2029 |

---

## 4. Record Layout

### 4.1 Header Record

```
TRADE_NUM;FAMILY;GROUP;TYPE;TYPOLOGY;PORTFOLIO;INSTRUMENT;ISSUER;CURVE_NAME;DATE;RECOVERY_RATE;SPREAD;CURRENCY;CIF;GLOBUS_ID;COUNTRY;ISIN;MATURITY;UNDERLYING
```

### 4.2 Data Record Example (Non-CRDI)

```
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;6M;40.000000;0.000000;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;
```

### 4.3 Data Record Example (CRDI)

```
28123456;CRD;CRDI;CRDI;CDX.NA.IG;CDXLNMGB01;CDX.NA.IG.S39;CDX.NA.IG.S39;CDX.NA.IG.S39;;0;0.006500;USD;0;;;20/06/28;
```

---

## 5. Sample Data

### 5.1 Complete File Example

```csv
TRADE_NUM;FAMILY;GROUP;TYPE;TYPOLOGY;PORTFOLIO;INSTRUMENT;ISSUER;CURVE_NAME;DATE;RECOVERY_RATE;SPREAD;CURRENCY;CIF;GLOBUS_ID;COUNTRY;ISIN;MATURITY;UNDERLYING
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;6M;40.000000;0.000000;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;1Y;40.000000;0.000000;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;2Y;40.000000;0.000000;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;
28234567;CRD;CDS;CDS;CDS_PROTECTION_BUYER;CDSLNMGB01;ABC Corp 5Y CDS;ABC Corporation;ABC_USD_SNRFOR;5Y;35.000000;0.025000;USD;100012345;123456;UNITED STATES;XS1234567890;15/06/29;ABC 4.5% 2029
28345678;CRD;CRDI;CRDI;iTraxx Europe;IDXLNMGB01;iTraxx Europe S40;iTraxx Europe S40;iTraxx Europe S40;;0;0.006200;EUR;0;;;20/12/28;
```

### 5.2 Spread Analysis Example

| Trade | Group | Issuer | Tenor | Spread (decimal) | Spread (bps) | Interpretation |
|-------|-------|--------|-------|------------------|--------------|----------------|
| 27522095 | BOND | MGB | 6M | 0.000000 | 0 | Zero spread (high quality) |
| 27522095 | BOND | MGB | 1Y | 0.000000 | 0 | Zero spread (high quality) |
| 28234567 | CDS | ABC Corp | 5Y | 0.025000 | 250 | Credit premium |
| 28345678 | CRDI | iTraxx Europe | - | 0.006200 | 62 | Index spread |

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
| VR-006 | SPREAD | Must be numeric | Reject |
| VR-007 | RECOVERY_RATE | 0 <= value <= 100 (non-CRDI) | Flag |
| VR-008 | CURRENCY | Must be valid ISO code | Reject |
| VR-009 | MATURITY | Must be valid date | Flag |

### 6.2 File-Level Validations

| Rule ID | Validation | Action |
|---------|------------|--------|
| VF-001 | File not empty (excluding header) | Warning |
| VF-002 | Header matches expected format | Reject file |
| VF-003 | Row count within expected range | Warning if variance >20% |
| VF-004 | All 19 fields present per row | Reject record |

### 6.3 Cross-Feed Validations

| Rule ID | Feeds | Validation | Action |
|---------|-------|------------|--------|
| VX-001 | IS, Delta Zero | Trade count match | Warning if different |
| VX-002 | IS, Delta Par | Issuer consistency | Flag mismatches |
| VX-003 | IS, RR01 | Recovery rate match | Flag if different |

---

## 7. Interface Schedule

### 7.1 Daily Schedule (GMT)

| Time | Event | Description |
|------|-------|-------------|
| 18:00 | Credit curve calibration | Curves available |
| 18:00 | Spread data | Market spreads loaded |
| 21:00 | Valuation batch complete | Spreads calculated |
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
|----------|--------------------|
| Valuation incomplete | Wait, re-run after completion |
| Partial extraction failure | Re-run from checkpoint |
| File delivery failure | Retry 3 times, then escalate |
| Data quality issue | Manual review, correction, re-run |

---

## 9. Comparison with Related Feeds

### 9.1 CR Instrument Spread vs Other CR Feeds

| Aspect | CR Instrument Spread | CR Delta Zero | CR RR01/RR02 |
|--------|---------------------|---------------|--------------|
| **Key Metric** | SPREAD (level) | CS01_ZERO (sensitivity) | RR01/RR02 (sensitivity) |
| **Unit** | Decimal (%) | Local currency | Local currency |
| **What it measures** | Actual spread value | P&L per 1bp move | P&L per recovery change |
| **Field Count** | 19 | 19 | 20 |
| **Has RESTRUCT** | No | No | Yes |
| **UNION Structure** | Yes | Yes | Yes |

### 9.2 Unique Characteristics

The CR Instrument Spread feed is unique in the CR suite because it provides:

1. **Actual spread levels** rather than sensitivities
2. **Valuation inputs** used in bond pricing
3. **Market observables** that can be compared to external quotes

This makes it essential for:
- P&L attribution (carry vs. spread movement)
- Mark verification (model price vs. market)
- Credit monitoring (spread level tracking)

---

## 10. Downstream Integration

### 10.1 Target Systems

| System | Usage | Key Fields |
|--------|-------|------------|
| Risk Data Warehouse | Storage, reporting | All fields |
| Plato (Risk Engine) | FRTB spread risk | SPREAD, CURVE_NAME |
| VESPA Reporting | Regulatory reporting | All fields |
| P&L Attribution | Spread carry analysis | SPREAD, DATE, CURRENCY |
| Credit Risk Systems | Spread monitoring | SPREAD, ISSUER, COUNTRY |

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
| [CR Instrument Spread BRD](./cr-instrument-spread-brd.md) | CR-IS-BRD-001 | Business requirements |
| [CR Instrument Spread IT Config](./cr-instrument-spread-config.md) | CR-IS-CFG-001 | Technical configuration |
| [CR Delta Zero IDD](../cr-delta-zero/cr-delta-zero-idd.md) | CR-DZ-IDD-001 | Related CS01 feed |
| [CR RR01 IDD](../cr-rr01/cr-rr01-idd.md) | CR-RR01-IDD-001 | UNION pattern reference |
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
