---
# Document Metadata
document_id: CR-DP-IDD-001
document_name: CR Delta Par Feed - Interface Design Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Steering Committee

# Parent Reference
parent_document: CR-DP-BRD-001
feed_id: CR-DP-001
---

# CR Delta Par Feed - Interface Design Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-DP-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Related BRD** | CR-DP-BRD-001 |
| **Related Config** | CR-DP-CFG-001 |

---

## 1. Interface Overview

### 1.1 Feed Summary

| Property | Value |
|----------|-------|
| **Feed Name** | CR Delta Par Feed |
| **Feed ID** | CR-DP-001 |
| **Source System** | Murex |
| **Target System** | VESPA / Plato Risk Engine |
| **Frequency** | Daily |
| **Format** | CSV (semicolon-delimited) |
| **Sensitivity** | CR01 Par (Par Spread Curve) |

### 1.2 File Naming Convention

| Component | Format | Example |
|-----------|--------|---------|
| Prefix | MxMGB | Murex Meridian Global Bank |
| Feed Type | Vespa_CR_DeltaPAR | Credit Delta Par |
| Region | LN/HK/NY/SP | Trading region |
| Date | YYYYMMDD | As-of date |
| Extension | .csv | File format |

**Full Pattern**: `MxMGB_MR_Credit_CS01Par_{Region}_{YYYYMMDD}.csv`

**Examples**:
- `MxMGB_MR_Credit_CS01Par_LN_20250102.csv`
- `MxMGB_MR_Credit_CS01Par_HK_20250102.csv`
- `MxMGB_MR_Credit_CS01Par_NY_20250102.csv`

### 1.3 Package Delivery

Final delivery is packaged with other market risk feeds:
- **Zip File**: `MxMGB_MR_Credit_Sens_{Region}_{YYYYMMDD}.zip`
- **Contents**: CR Delta Par + other sensitivity feeds

---

## 2. Field Specifications

### 2.1 Field Summary

| # | Field Name | Data Type | Length | Mandatory | Description |
|---|------------|-----------|--------|-----------|-------------|
| 1 | TRADE_NUM | Numeric | 10 | Yes | Murex trade identifier |
| 2 | FAMILY | VarChar | 16 | Yes | Trade family (CRD, IRD, EQD) |
| 3 | GROUP | VarChar | 5 | Yes | Trade group |
| 4 | TYPE | VarChar | 16 | Yes | Trade type |
| 5 | TYPOLOGY | VarChar | 21 | Yes | Trade typology |
| 6 | PORTFOLIO | VarChar | 20 | Yes | Trading portfolio |
| 7 | INSTRUMENT | VarChar | 30 | Yes | PL Instrument |
| 8 | ISSUER | VarChar | 50 | Yes | Issuer name/label |
| 9 | CURVE_NAME | VarChar | 50 | Yes | Par credit curve name |
| 10 | DATE | VarChar | 8 | Yes | Maturity pillar date |
| 11 | RECOVERY_RATE | Numeric | 12 | Yes | Recovery rate of issuer |
| 12 | CR01 (PAR) QUOTATION | Numeric | 12 | Yes | CR01 Par in local currency |
| 13 | CURRENCY | VarChar | 4 | Yes | Trade currency (ISO) |
| 14 | CIF | Numeric | 9 | Conditional | Customer Information File ID |
| 15 | GLOBUS_ID | VarChar | 10 | Conditional | External issuer identifier |
| 16 | COUNTRY | VarChar | 30 | Conditional | Country of risk |
| 17 | ISIN | VarChar | 25 | Conditional | Reference obligation ISIN |
| 18 | MATURITY | Date | 8 | Yes | Trade maturity date |
| 19 | UNDERLYING | VarChar | 15 | Conditional | Reference obligation label |
| 20 | RESTRUCT | VarChar | 16 | Yes | Restructuring option |
| 21 | NOTIONAL | Numeric | 25 | Yes | Notional amount |
| 22 | MARKET | VarChar | 15 | Conditional | Security market |
| 23 | CR01 (PAR) QUOTATION (USD) | Numeric | 16 | Yes | CR01 Par in USD |

---

## 3. Field Definitions

### 3.1 Trade Identification Fields

#### 3.1.1 TRADE_NUM

| Property | Value |
|----------|-------|
| **Position** | 1 |
| **Data Type** | Numeric(10) |
| **Mandatory** | Yes |
| **Description** | Unique Murex trade identifier |
| **Source** | M_TRADE_NUM from VW_Vespa_Sensitivities / VW_Vespa_Sensitivities_CRDI |
| **Example** | 28391262 |
| **Validation** | Numeric, not null |

#### 3.1.2 FAMILY

| Property | Value |
|----------|-------|
| **Position** | 2 |
| **Data Type** | VarChar(16) |
| **Mandatory** | Yes |
| **Description** | Trade family classification |
| **Source** | M_FAMILY from Simulation view |
| **Valid Values** | CRD, IRD, EQD |
| **Example** | IRD |

#### 3.1.3 GROUP

| Property | Value |
|----------|-------|
| **Position** | 3 |
| **Data Type** | VarChar(5) |
| **Mandatory** | Yes |
| **Description** | Trade group classification |
| **Source** | M_GROUP from Simulation view |
| **Valid Values** | CDS, BOND, CRDI, RTRN, etc. |
| **Example** | BOND |

#### 3.1.4 TYPE

| Property | Value |
|----------|-------|
| **Position** | 4 |
| **Data Type** | VarChar(16) |
| **Mandatory** | Yes |
| **Description** | Trade type |
| **Source** | M_TYPE from Simulation view |
| **Example** | SWAP |

#### 3.1.5 TYPOLOGY

| Property | Value |
|----------|-------|
| **Position** | 5 |
| **Data Type** | VarChar(21) |
| **Mandatory** | Yes |
| **Description** | Trade typology for risk classification |
| **Source** | M_TYPOLOGY from Simulation view |
| **Example** | IRD - CP BOND, CRD - GUARANTEE, CRD - INSURANCE |

#### 3.1.6 PORTFOLIO

| Property | Value |
|----------|-------|
| **Position** | 6 |
| **Data Type** | VarChar(20) |
| **Mandatory** | Yes |
| **Description** | Trading portfolio from Bookman hierarchy |
| **Source** | M_PORTFOLIO from Simulation view |
| **Example** | CTLNSBLCMAC2 |
| **Validation** | Must exist in Bookman hierarchy |

#### 3.1.7 INSTRUMENT

| Property | Value |
|----------|-------|
| **Position** | 7 |
| **Data Type** | VarChar(30) |
| **Mandatory** | Yes |
| **Description** | PL Instrument identifier |
| **Source** | M_PL_INSTRU from Simulation view |
| **Example** | GABON 6.95 06/16/25 REGS |
| **Note** | Used as ISSUER fallback when M_ISSUER is null |

### 3.2 Credit Reference Fields

#### 3.2.1 ISSUER

| Property | Value |
|----------|-------|
| **Position** | 8 |
| **Data Type** | VarChar(50) |
| **Mandatory** | Yes |
| **Description** | Issuer name (Non-CRDI) or Index label (CRDI) |
| **Source (Non-CRDI)** | CASE WHEN M_ISSUER IS NULL THEN M_PL_INSTRU ELSE M_ISSUER END |
| **Source (CRDI)** | M_PL_INSTRU (Index label) |
| **Example (Non-CRDI)** | GOVT OF GABON |
| **Example (CRDI)** | CDX.NA.IG.42 |

#### 3.2.2 CURVE_NAME

| Property | Value |
|----------|-------|
| **Position** | 9 |
| **Data Type** | VarChar(50) |
| **Mandatory** | Yes |
| **Description** | Par credit spread curve name |
| **Source (Non-CRDI)** | M_CURVE_NA1 from Simulation view |
| **Source (CRDI)** | M_PL_INSTRU |
| **Example** | GOVT OF GABON_USD_SNRFOR |

#### 3.2.3 DATE

| Property | Value |
|----------|-------|
| **Position** | 10 |
| **Data Type** | VarChar(8) |
| **Mandatory** | Yes |
| **Description** | Maturity pillar date for sensitivity |
| **Source (Non-CRDI)** | M_DATE__ZER from VW_Vespa_Sensitivities |
| **Source (CRDI)** | M_DATE from VW_Vespa_Sensitivities_CRDI |
| **Example** | 2Y, 5Y, 10Y |

#### 3.2.4 CIF

| Property | Value |
|----------|-------|
| **Position** | 14 |
| **Data Type** | Numeric(9) |
| **Mandatory** | Yes for Non-CRDI, Set to 0 for CRDI |
| **Description** | Customer Information File ID |
| **Source** | cast(CP.M_U_CIF_ID as varchar(10)) from SB_CP_REP |
| **Example (Non-CRDI)** | 100089620 |
| **Example (CRDI)** | 0 |

#### 3.2.5 GLOBUS_ID

| Property | Value |
|----------|-------|
| **Position** | 15 |
| **Data Type** | VarChar(10) |
| **Mandatory** | Conditional (Non-CRDI only) |
| **Description** | External issuer identifier |
| **Source** | CP.M_U_GLOBID from SB_CP_REP |
| **Example (Non-CRDI)** | 127012 |
| **Example (CRDI)** | (blank) |

#### 3.2.6 COUNTRY

| Property | Value |
|----------|-------|
| **Position** | 16 |
| **Data Type** | VarChar(30) |
| **Mandatory** | Conditional (Non-CRDI only) |
| **Description** | Country of risk |
| **Source** | CP.M_U_RSK_CTRY from SB_CP_REP |
| **Example (Non-CRDI)** | GABON |
| **Example (CRDI)** | (blank - multi-country indices) |

#### 3.2.7 ISIN

| Property | Value |
|----------|-------|
| **Position** | 17 |
| **Data Type** | VarChar(25) |
| **Mandatory** | Conditional |
| **Description** | Reference obligation ISIN |
| **Source (Bonds)** | SE_HEAD.M_SE_CODE from SB_SE_HEAD_REP |
| **Source (CDS)** | rtrim(OBL.M_REF_OBLI1) from TBL_CRD_RECOVERY_REP |
| **Source (CRDI)** | Blank |
| **Example** | XS1245960684 |

### 3.3 Sensitivity Fields

#### 3.3.1 RECOVERY_RATE

| Property | Value |
|----------|-------|
| **Position** | 11 |
| **Data Type** | Numeric(12) |
| **Mandatory** | Yes |
| **Description** | Recovery rate of the issuer |
| **Source (Non-CRDI)** | M_RATE from VW_Vespa_Sensitivities |
| **Source (CRDI)** | Set to 0 |
| **Unit** | Percentage |
| **Example** | 27.523800 |

#### 3.3.2 CR01 (PAR) QUOTATION

| Property | Value |
|----------|-------|
| **Position** | 12 |
| **Data Type** | Numeric(12) |
| **Mandatory** | Yes |
| **Description** | Par credit spread sensitivity in trade currency |
| **Source** | M_CR01__PA2 from Simulation view |
| **Calculation** | P&L impact of 1bp parallel shift in par spread curve |
| **Unit** | Trade currency |
| **Sign Convention** | Negative = loss on spread widening (long credit risk) |
| **Example** | -26 |

#### 3.3.3 CR01 (PAR) QUOTATION (USD)

| Property | Value |
|----------|-------|
| **Position** | 23 |
| **Data Type** | Numeric(16) |
| **Mandatory** | Yes |
| **Description** | Par credit spread sensitivity converted to USD |
| **Source** | M_CR01__PA1 from Simulation view |
| **Calculation** | CR01 Par (Local) × FX Rate to USD |
| **Unit** | USD |
| **Example** | -26 |

#### 3.3.4 CURRENCY

| Property | Value |
|----------|-------|
| **Position** | 13 |
| **Data Type** | VarChar(4) |
| **Mandatory** | Yes |
| **Description** | Trade/sensitivity currency (ISO 4217) |
| **Source** | M_CURRENCY from Simulation view |
| **Example** | USD, EUR, GBP |

### 3.4 Trade Detail Fields

#### 3.4.1 MATURITY

| Property | Value |
|----------|-------|
| **Position** | 18 |
| **Data Type** | Date(8) |
| **Format** | DD/MM/YY |
| **Mandatory** | Yes |
| **Description** | Trade maturity date |
| **Source** | TP.M_TP_DTEEXP from SB_TP_REP |
| **Example** | 16/06/25 |

#### 3.4.2 UNDERLYING

| Property | Value |
|----------|-------|
| **Position** | 19 |
| **Data Type** | VarChar(15) |
| **Mandatory** | Conditional (CDS only) |
| **Description** | Reference obligation label |
| **Source** | OBL.M_REF_OBLIG from TBL_CRD_RECOVERY_REP |
| **Example (CDS)** | Reference bond label |
| **Example (CRDI)** | (blank) |

#### 3.4.3 RESTRUCT

| Property | Value |
|----------|-------|
| **Position** | 20 |
| **Data Type** | VarChar(16) |
| **Mandatory** | Yes |
| **Description** | CDS restructuring clause |
| **Source** | CASE WHEN OBL.M_RESTRUCTU = 'Yes' THEN OBL.M_RESTRUCTU ELSE 'NONE' END |
| **Valid Values** | Yes, NONE |
| **Example** | NONE |

#### 3.4.4 NOTIONAL

| Property | Value |
|----------|-------|
| **Position** | 21 |
| **Data Type** | Numeric(25) |
| **Mandatory** | Yes |
| **Description** | Notional of the security or basket |
| **Complex Logic** | |

**Notional Calculation Logic**:
```sql
CASE
  -- IR Swaps: Capital Rate × Security Lot
  WHEN FAMILY = 'IRD' AND GROUP = 'RTRN' AND TYPE = 'SWAP'
  THEN M_TP_RTCAPI0 * M_TP_SECLOT

  -- Bonds: Direct notional
  WHEN GROUP = 'BOND'
  THEN M_TP_RTCCP02

  -- CDS: Absolute notional
  WHEN GROUP = 'CDS'
  THEN abs(M_TP_RTCCP02)

  -- CRDI: Absolute notional
  WHEN GROUP = 'CRDI'
  THEN abs(M_TP_RTCCP02)

  -- Other: Signed nominal based on buy/sell
  ELSE CASE WHEN M_TP_BUY = 'S'
            THEN (-1) * M_TP_NOMINAL
            ELSE M_TP_NOMINAL END
END
```

| Source | Table |
|--------|-------|
| M_TP_RTCAPI0, M_TP_SECLOT, M_TP_RTCCP02 | SB_TP_BD_REP |
| M_TP_NOMINAL, M_TP_BUY | SB_TP_REP |

**Example**: 155000.000000

#### 3.4.5 MARKET

| Property | Value |
|----------|-------|
| **Position** | 22 |
| **Data Type** | VarChar(15) |
| **Mandatory** | Conditional |
| **Description** | Security market |
| **Complex Logic** | |

**Market Calculation Logic**:
```sql
CASE
  -- IRD or EQD: Security market from extended transaction
  WHEN FAMILY IN ('IRD', 'EQD')
  THEN M_TP_SECMKT  -- from SB_TP_EXT_REP

  -- CDS: Market from security root
  WHEN FAMILY = 'CRD' AND GROUP = 'CDS'
  THEN (SELECT DISTINCT M_SE_MARKE FROM TBL_SE_ROOT_REP
        WHERE M_SE_LABEL = REF_OBLI2 AND M_SE_DED IS NULL)

  -- CRDI: Blank
  ELSE ''
END
```

**Example**: USD CORP

---

## 4. Data Flow

### 4.1 Three-Way UNION Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    CR Delta Par Extraction                      │
├─────────────────────────────────────────────────────────────────┤
│  PART 1: Non-CRDI (excl. Insurance/Guarantee)                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ VW_Vespa_Sensitivities                                  │    │
│  │ Filter: GROUP <> 'CRDI'                                 │    │
│  │         TYPOLOGY NOT IN (GUARANTEE, INSURANCE)          │    │
│  │ Joins: SB_CP_REP, TBL_CRD_RECOVERY_REP, SB_TP_*, etc.   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            ↓                                    │
│                      UNION ALL                                  │
│                            ↓                                    │
│  PART 2: Insurance & Guarantee Products                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ VW_Vespa_Sensitivities                                  │    │
│  │ Filter: TYPOLOGY IN (CRD - GUARANTEE, CRD - INSURANCE)  │    │
│  │ Additional: OBL.M_INSTRUMEN = OBL.M_ISSUER              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            ↓                                    │
│                      UNION ALL                                  │
│                            ↓                                    │
│  PART 3: Credit Index Products (CRDI)                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ VW_Vespa_Sensitivities_CRDI                             │    │
│  │ Filter: GROUP = 'CRDI'                                  │    │
│  │ Joins: SB_TP_REP, SB_TP_BD_REP, SB_CRI_DEF_REP          │    │
│  │ Defaults: RECOVERY_RATE=0, CIF=0, RESTRUCT='NONE'       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            ↓                                    │
│                   Combined Output File                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Sample Data

### 5.1 Bond Example (Non-CRDI)

```csv
TRADE_NUM;FAMILY;GROUP;TYPE;TYPOLOGY;PORTFOLIO;INSTRUMENT;ISSUER;CURVE_NAME;DATE;RECOVERY_RATE;CR01(PAR) QUOTATION;CURRENCY;CIF;GLOBUS_ID;COUNTRY;ISIN;MATURITY;UNDERLYING;RESTRUCT;NOTIONAL;MARKET;CR01 (PAR) QUOTATION (USD)
28391262;IRD;BOND;;IRD - CP BOND;CTLNSBLCMAC2;GABON 6.95 06/16/25 REGS;GOVT OF GABON;GOVT OF GABON_USD_SNRFOR;2Y;27.523800;-26;USD;100089620;127012;GABON;XS1245960684;16/06/25;;NONE;155000.000000;USD CORP;-26
```

### 5.2 Multiple Tenors Example

```csv
28391262;IRD;BOND;;IRD - CP BOND;CTLNSBLCMAC2;GABON 6.95 06/16/25 REGS;GOVT OF GABON;GOVT OF GABON_USD_SNRFOR;1Y;27.523800;0;USD;100089620;127012;GABON;XS1245960684;16/06/25;;NONE;155000.000000;USD CORP;0
28391262;IRD;BOND;;IRD - CP BOND;CTLNSBLCMAC2;GABON 6.95 06/16/25 REGS;GOVT OF GABON;GOVT OF GABON_USD_SNRFOR;6M;27.523800;0;USD;100089620;127012;GABON;XS1245960684;16/06/25;;NONE;155000.000000;USD CORP;0
```

### 5.3 CRDI Example

```csv
87654321;CRD;CRDI;INDEX_CDS;CDX_IG;LN_INDEX_TRADING;CDX.NA.IG.42;CDX.NA.IG.42;CDX.NA.IG.42;5Y;0;-1500;USD;0;;;;;;;NONE;10000000.000000;;-1500
```

---

## 6. Validation Rules

### 6.1 Mandatory Field Validation

| Rule ID | Field | Rule | Error Action |
|---------|-------|------|--------------|
| VAL-001 | TRADE_NUM | Not null, numeric | Reject record |
| VAL-002 | FAMILY | Must be CRD, IRD, or EQD | Reject record |
| VAL-003 | GROUP | Valid group code | Reject record |
| VAL-004 | PORTFOLIO | Must exist in Bookman | Reject record |
| VAL-005 | CR01 (PAR) QUOTATION | Not null | Reject record |
| VAL-006 | CR01 (PAR) QUOTATION (USD) | Not null | Reject record |
| VAL-007 | CURRENCY | Valid ISO 4217 code | Reject record |
| VAL-008 | NOTIONAL | Not null, numeric | Reject record |

### 6.2 Conditional Field Validation

| Rule ID | Condition | Field | Rule | Error Action |
|---------|-----------|-------|------|--------------|
| VAL-009 | GROUP ≠ CRDI | ISSUER | Not null (or use INSTRUMENT) | Use INSTRUMENT |
| VAL-010 | GROUP ≠ CRDI | RECOVERY_RATE | Between 0 and 100 | Flag for review |
| VAL-011 | GROUP = CDS | RESTRUCT | Valid restructuring value | Flag for review |
| VAL-012 | GROUP = BOND | ISIN | Valid ISIN format | Flag for review |

### 6.3 Cross-Feed Validation

| Rule ID | Rule | Tolerance | Action |
|---------|------|-----------|--------|
| VAL-013 | Position count matches CR Delta Zero | 0% | Investigate |
| VAL-014 | CR01 Par vs CR01 Zero ratio reasonable | ±50% | Flag outliers |

---

## 7. Comparison with CR Delta Zero

### 7.1 Field Comparison

| Field | CR Delta Par | CR Delta Zero | Notes |
|-------|--------------|---------------|-------|
| TRADE_NUM | Yes | Yes (TRADE_NUMBER) | Same |
| FAMILY | Yes | Yes | Same |
| GROUP | Yes | Yes (GRP) | Same |
| TYPE | Yes | Yes | Same |
| TYPOLOGY | Yes | Yes | Same |
| PORTFOLIO | Yes | Yes | Same |
| **INSTRUMENT** | **Yes** | No | CR Delta Par only |
| ISSUER | Yes | Yes | Same |
| CURVE_NAME | Yes | Yes | Same |
| DATE | Yes | No | CR Delta Par uses DATE |
| RECOVERY_RATE | Yes | Yes | Same |
| CR01 (PAR) | Yes | No | CR Delta Par sensitivity |
| CR01 (Zero) | No | Yes | CR Delta Zero sensitivity |
| CURRENCY | Yes | Yes | Same |
| CIF | Yes | Yes | Same |
| GLOBUS_ID | Yes | Yes | Same |
| COUNTRY | Yes | Yes | Same |
| ISIN | Yes | Yes | Same |
| MATURITY | Yes | Yes | Same |
| UNDERLYING | Yes | Yes | Same |
| RESTRUCT | Yes | Yes (RESTRUCTURING) | Same |
| NOTIONAL | Yes | Yes | Same |
| MARKET | Yes | Yes | Same |
| CR01 (PAR) USD | Yes | No | CR Delta Par USD |
| CR01 (Zero) USD | No | Yes | CR Delta Zero USD |
| **Total Fields** | **23** | **23** | Same count |

### 7.2 Key Differences

| Aspect | CR Delta Par | CR Delta Zero |
|--------|--------------|---------------|
| **Curve Type** | Par spread curve | Zero/default spread curve |
| **Source Fields** | M_CR01__PA2, M_CR01__PA1 | M_CR01, M_CR01_USD |
| **INSTRUMENT Field** | Included | Not included |
| **Extraction Structure** | 3-way UNION | 2-way UNION |
| **Insurance/Guarantee** | Separate UNION part | Same as standard |
| **Delimiter** | Semicolon (;) | Comma (,) |

---

## 8. Error Handling

### 8.1 Error Codes

| Error Code | Description | Severity | Action |
|------------|-------------|----------|--------|
| ERR-DP-001 | Missing mandatory field | Critical | Reject record |
| ERR-DP-002 | Invalid field format | Critical | Reject record |
| ERR-DP-003 | Issuer not mapped | Warning | Use INSTRUMENT |
| ERR-DP-004 | CR01 Par outlier detected | Warning | Flag, include record |
| ERR-DP-005 | Portfolio not in Bookman | Critical | Map to UNMAPPED |
| ERR-DP-006 | FX rate missing | Critical | Use T-1 rate |

---

## 9. Interface SLAs

### 9.1 Timing SLAs

| Metric | Target | Escalation |
|--------|--------|------------|
| File delivery | 05:30 GMT | >06:00 → L2 |
| File size | >0 bytes | Empty file → L2 |
| Record count | Within 10% of T-1 | Variance → RAV |
| Match CR Delta Zero count | 100% | Mismatch → Investigate |

### 9.2 Quality SLAs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Completeness | 100% positions | Position count reconciliation |
| Accuracy | 100% valid values | Validation rule pass rate |
| Consistency | CR01 Par/Zero ratio stable | Daily comparison |

---

## 10. Related Documentation

| Document | ID | Relationship |
|----------|-----|--------------|
| [CR Delta Par BRD](./cr-delta-par-brd.md) | CR-DP-BRD-001 | Business requirements |
| [CR Delta Par IT Config](./cr-delta-par-config.md) | CR-DP-CFG-001 | Technical configuration |
| [CR Delta Zero IDD](../cr-delta-zero/cr-delta-zero-idd.md) | CR-DZ-IDD-001 | Related Zero interface |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |

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
| Field specification review | Semi-annual | July 2025 |
| Consumer alignment | Quarterly | April 2025 |

---

*End of Document*
