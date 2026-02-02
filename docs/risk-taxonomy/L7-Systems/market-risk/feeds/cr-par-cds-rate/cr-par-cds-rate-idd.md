---
# Document Metadata
document_id: CR-PAR-IDD-001
document_name: CR Par CDS Rate Feed - Interface Design Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Steering Committee

# Parent Reference
parent_document: CR-PAR-BRD-001
feed_id: CR-PAR-001
---

# CR Par CDS Rate Feed - Interface Design Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-PAR-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Related BRD** | CR-PAR-BRD-001 |
| **Related Config** | CR-PAR-CFG-001 |

---

## 1. Interface Overview

### 1.1 Feed Summary

| Property | Value |
|----------|-------|
| **Feed Name** | CR Par CDS Rate Feed |
| **Feed ID** | CR-PAR-001 |
| **Source System** | Murex |
| **Target System** | VESPA / Plato Risk Engine |
| **Frequency** | Daily |
| **Format** | CSV (semicolon-delimited) |
| **Data Type** | Market Data (Par CDS Spread) |

### 1.2 File Naming Convention

| Component | Format | Example |
|-----------|--------|---------|
| Prefix | MxMGB | Murex Meridian Global Bank |
| Feed Type | Vespa_CR_Par_CDS_Rate | Par CDS Rate |
| Region | LN/HK/NY/SP | Trading region |
| Date | YYYYMMDD | As-of date |
| Extension | .csv | File format |

**Full Pattern**: `MxMGB_MR_Credit_ParCDS_{Region}_{YYYYMMDD}.csv`

**Examples**:
- `MxMGB_MR_Credit_ParCDS_LN_20250102.csv`
- `MxMGB_MR_Credit_ParCDS_HK_20250102.csv`
- `MxMGB_MR_Credit_ParCDS_NY_20250102.csv`

### 1.3 Package Delivery

Final delivery is packaged with other market risk feeds:
- **Zip File**: `MxMGB_MR_Credit_Sens_{Region}_{YYYYMMDD}.zip`
- **Contents**: CR Par CDS Rate + other sensitivity feeds

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
| 9 | CURVE_NAME | VarChar | 50 | Yes | Credit curve name |
| 10 | DATE | VarChar | 64 | Yes | Maturity pillar date |
| 11 | RECOVERY_RATE | Numeric | 12 | Yes | Recovery rate of issuer |
| 12 | PAR_CDS | American | 16,4 | Yes | Par CDS conventional spread / 100 |
| 13 | CURRENCY | VarChar | 4 | Yes | Trade currency (ISO) |
| 14 | CIF | Numeric | 9 | Conditional | Customer Information File ID |
| 15 | GLOBUS_ID | VarChar | 10 | Conditional | External issuer identifier |
| 16 | COUNTRY | VarChar | 30 | Conditional | Country of risk |
| 17 | ISIN | VarChar | 25 | Conditional | Reference obligation ISIN |
| 18 | MATURITY | Date | 8 | Yes | Trade maturity date |
| 19 | UNDERLYING | VarChar | 15 | Conditional | Reference obligation label |

**Note**: This feed has **19 fields** - fewer than CR Delta Zero/Par (23 fields). Fields **not included**:
- NOTIONAL
- MARKET
- RESTRUCTURING (RESTRUCT)
- CR01 sensitivity fields (USD conversion)

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
| **Example** | 27571964 |
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
| **Valid Values** | CDS, BOND, CRDI, etc. |
| **Example** | BOND |

#### 3.1.4 TYPE

| Property | Value |
|----------|-------|
| **Position** | 4 |
| **Data Type** | VarChar(16) |
| **Mandatory** | Yes |
| **Description** | Trade type |
| **Source** | M_TYPE from Simulation view |
| **Example** | (may be blank) |

#### 3.1.5 TYPOLOGY

| Property | Value |
|----------|-------|
| **Position** | 5 |
| **Data Type** | VarChar(21) |
| **Mandatory** | Yes |
| **Description** | Trade typology for risk classification |
| **Source** | M_TYPOLOGY from Simulation view |
| **Example** | IRD - CLN SINGLENAME, IRD - CP BOND |

#### 3.1.6 PORTFOLIO

| Property | Value |
|----------|-------|
| **Position** | 6 |
| **Data Type** | VarChar(20) |
| **Mandatory** | Yes |
| **Description** | Trading portfolio from Bookman hierarchy |
| **Source** | M_PORTFOLIO from Simulation view |
| **Example** | CTLNSBLGBB7FRT |
| **Validation** | Must exist in Bookman hierarchy |

#### 3.1.7 INSTRUMENT

| Property | Value |
|----------|-------|
| **Position** | 7 |
| **Data Type** | VarChar(30) |
| **Mandatory** | Yes |
| **Description** | PL Instrument identifier |
| **Source** | M_PL_INSTRU from Simulation view |
| **Example** | CLN 1942 - NAVMINE 4.76% 20/04 |
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
| **Example (Non-CRDI)** | SBL |
| **Example (CRDI)** | CDX.NA.IG.42 |

#### 3.2.2 CURVE_NAME

| Property | Value |
|----------|-------|
| **Position** | 9 |
| **Data Type** | VarChar(50) |
| **Mandatory** | Yes |
| **Description** | Credit spread curve name |
| **Source (Non-CRDI)** | M_CURVE_NA1 from Simulation view |
| **Source (CRDI)** | M_PL_INSTRU (Index label) |
| **Usage** | Join key to TBL_AC_CRDCURVES_REP |
| **Example** | SBL_USD_SNRFOR |

#### 3.2.3 DATE

| Property | Value |
|----------|-------|
| **Position** | 10 |
| **Data Type** | VarChar(64) |
| **Mandatory** | Yes |
| **Description** | Maturity pillar date for the par CDS rate |
| **Source (Non-CRDI)** | M_DATE__ZER from VW_Vespa_Sensitivities |
| **Source (CRDI)** | M_DATE from VW_Vespa_Sensitivities_CRDI |
| **Usage** | Join key to TBL_AC_CRDCURVES_REP (M_TENOR) |
| **Example** | 1Y, 3Y, 5Y |

#### 3.2.4 CIF

| Property | Value |
|----------|-------|
| **Position** | 14 |
| **Data Type** | Numeric(9) |
| **Mandatory** | Yes for Non-CRDI, Set to 0 for CRDI |
| **Description** | Customer Information File ID |
| **Source** | CP.M_U_CIF_ID from SB_CP_REP |
| **Example (Non-CRDI)** | 100060635 |
| **Example (CRDI)** | 0 |

#### 3.2.5 GLOBUS_ID

| Property | Value |
|----------|-------|
| **Position** | 15 |
| **Data Type** | VarChar(10) |
| **Mandatory** | Conditional (Non-CRDI only) |
| **Description** | External issuer identifier |
| **Source** | CP.M_U_GLOBID from SB_CP_REP |
| **Example (Non-CRDI)** | 101088 |
| **Example (CRDI)** | (blank) |

#### 3.2.6 COUNTRY

| Property | Value |
|----------|-------|
| **Position** | 16 |
| **Data Type** | VarChar(30) |
| **Mandatory** | Conditional (Non-CRDI only) |
| **Description** | Country of risk |
| **Source** | NVL(CP.M_U_RSK_CTRY, ' ') from SB_CP_REP |
| **Example (Non-CRDI)** | UNITED KINGDOM |
| **Example (CRDI)** | (space - multi-country indices) |

#### 3.2.7 ISIN

| Property | Value |
|----------|-------|
| **Position** | 17 |
| **Data Type** | VarChar(25) |
| **Mandatory** | Conditional |
| **Description** | Reference obligation ISIN code |
| **Source** | NVL(OBL.M_REF_OBLI1, ' ') from TBL_CRD_RECOVERY_REP |
| **Example (CDS)** | Reference obligation ISIN |
| **Example (BOND/CRDI)** | (space) |

### 3.3 Market Data Field

#### 3.3.1 PAR_CDS

| Property | Value |
|----------|-------|
| **Position** | 12 |
| **Data Type** | American(16,4) |
| **Mandatory** | Yes |
| **Description** | Par CDS conventional spread divided by 100 |
| **Source** | CUR.M_CONVENTIO / 100 from TBL_AC_CRDCURVES_REP |
| **Market Data Viewer** | MKTP_CRED_CURVES |
| **Unit** | Decimal (e.g., 0.0125 = 125 bps) |
| **Bond Handling** | Set to 0 (bonds use z-spread, not CDS spread) |
| **Example** | 0.000000 (typical for bonds) |

**PAR_CDS Calculation Logic**:
```sql
CASE WHEN M_GROUP = 'BOND'
     THEN 0
     ELSE CUR.M_CONVENTIO / 100
END AS PAR_CDS
```

**PAR_CDS Interpretation**:
| Value | Interpretation |
|-------|----------------|
| 0.0050 | 50 basis points |
| 0.0125 | 125 basis points |
| 0.0300 | 300 basis points (high-yield) |
| 0.0000 | Bond (no CDS spread) or no data |

#### 3.3.2 RECOVERY_RATE

| Property | Value |
|----------|-------|
| **Position** | 11 |
| **Data Type** | Numeric(12) |
| **Mandatory** | Yes |
| **Description** | Recovery rate of the issuer |
| **Source (Non-CRDI)** | M_RATE from VW_Vespa_Sensitivities |
| **Source (CRDI)** | Set to 0 |
| **Unit** | Percentage |
| **Example** | 40.000000 |

#### 3.3.3 CURRENCY

| Property | Value |
|----------|-------|
| **Position** | 13 |
| **Data Type** | VarChar(4) |
| **Mandatory** | Yes |
| **Description** | Trade/curve currency (ISO 4217) |
| **Source (Non-CRDI)** | M_CURRENCY2 from Simulation view |
| **Source (CRDI)** | M_CURRENCY from Simulation view |
| **Example** | USD, EUR, MZN |

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
| **Example** | 20/04/27 |

#### 3.4.2 UNDERLYING

| Property | Value |
|----------|-------|
| **Position** | 19 |
| **Data Type** | VarChar(15) |
| **Mandatory** | Conditional (CDS only) |
| **Description** | Reference obligation label |
| **Source** | NVL(OBL.M_REF_OBLIG, ' ') from TBL_CRD_RECOVERY_REP |
| **Example (CDS)** | Reference obligation |
| **Example (BOND/CRDI)** | (space) |

---

## 4. Data Flow

### 4.1 Two-Way UNION Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    CR Par CDS Rate Extraction                   │
├─────────────────────────────────────────────────────────────────┤
│  PART 1: Non-CRDI Positions                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ TBL_VESPA_SENS_REP (position data)                      │    │
│  │ Filter: GROUP <> 'CRDI'                                 │    │
│  │         ISSUER IS NOT NULL                              │    │
│  │ Join: TBL_AC_CRDCURVES_REP (par CDS spread)             │    │
│  │       On CURVE_NAME = M_LABEL, DATE = M_TENOR           │    │
│  │ PAR_CDS: 0 for BOND, M_CONVENTIO/100 otherwise          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            ↓                                    │
│                      UNION ALL                                  │
│                            ↓                                    │
│  PART 2: CRDI (Credit Index) Positions                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ TBL_VESPA_SENSCI_REP (position data)                    │    │
│  │ Filter: GROUP = 'CRDI'                                  │    │
│  │ Join: TBL_AC_CRDCURVES_REP (par CDS spread)             │    │
│  │       On PL_INSTRU = M_LABEL                            │    │
│  │ PAR_CDS: M_CONVENTIO/100 from index curve               │    │
│  │ Defaults: RECOVERY_RATE=0, CIF=0                        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            ↓                                    │
│                   Combined Output File                          │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Credit Curve Join

```
Position Data                    Credit Curve Data
(TBL_VESPA_SENS_REP)            (TBL_AC_CRDCURVES_REP)
┌─────────────────┐              ┌─────────────────┐
│ M_CURVE_NA1     │──────────────│ M_LABEL         │
│ M_DATE__ZER     │──────────────│ M_TENOR         │
│                 │              │ M_CONVENTIO     │──→ PAR_CDS
└─────────────────┘              └─────────────────┘
```

---

## 5. Sample Data

### 5.1 CLN Example

```csv
TRADE_NUM;FAMILY;GROUP;TYPE;TYPOLOGY;PORTFOLIO;INSTRUMENT;ISSUER;CURVE_NAME;DATE;RECOVERY_RATE;PAR_CDS;CURRENCY;CIF;GLOBUS_ID;COUNTRY;ISIN;MATURITY;UNDERLYING
27571964;IRD;BOND;;IRD - CLN SINGLENAME;CTLNSBLGBB7FRT;CLN 1942 - NAVMINE 4.76% 20/04;SBL;SBL_USD_SNRFOR;1Y;40.000000;0.000000;USD;100060635.000000;101088;UNITED KINGDOM;;20/04/27;
```

### 5.2 Corporate Bond Example

```csv
26450310;IRD;BOND;;IRD - CP BOND;TSLNSBLADDT1;ICBC VAR PERP;SBL;SBL_USD_SNRFOR;1Y;40.000000;0.000000;USD;100060635.000000;101088;UNITED KINGDOM;;20/12/69;
```

### 5.3 FX Passthrough Example

```csv
27382553;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNSBLLEMP7FRT;FXPASS 1929-MZN 14.5% 11/02/20;SBL;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;3Y;40.000000;0.000000;MZN;100060635.000000;101088;UNITED KINGDOM;;09/02/27;
```

### 5.4 CRDI Example

```csv
87654321;CRD;CRDI;INDEX_CDS;CDX_IG;LN_INDEX_TRADING;CDX.NA.IG.42;CDX.NA.IG.42;CDX.NA.IG.42;5Y;0;0.005500;USD;0;;;;;;;
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
| VAL-005 | PAR_CDS | Not null | Reject record |
| VAL-006 | CURRENCY | Valid ISO 4217 code | Reject record |
| VAL-007 | MATURITY | Valid date | Reject record |

### 6.2 Conditional Field Validation

| Rule ID | Condition | Field | Rule | Error Action |
|---------|-----------|-------|------|--------------|
| VAL-008 | GROUP ≠ CRDI | ISSUER | Not null (or use INSTRUMENT) | Use INSTRUMENT |
| VAL-009 | GROUP = BOND | PAR_CDS | Must be 0 | Flag violation |
| VAL-010 | GROUP ≠ CRDI | RECOVERY_RATE | Between 0 and 100 | Flag for review |

### 6.3 Cross-Feed Validation

| Rule ID | Rule | Tolerance | Action |
|---------|------|-----------|--------|
| VAL-011 | Position count matches CR Delta Zero | 0% | Investigate |
| VAL-012 | PAR_CDS matches MKTP_CRED_CURVES | 0.01% | Investigate |

---

## 7. Comparison with Other CR Feeds

### 7.1 Field Comparison

| Field | CR Par CDS | CR Delta Zero | CR Delta Par |
|-------|------------|---------------|--------------|
| TRADE_NUM | Yes | Yes | Yes |
| FAMILY | Yes | Yes | Yes |
| GROUP | Yes | Yes | Yes |
| TYPE | Yes | Yes | Yes |
| TYPOLOGY | Yes | Yes | Yes |
| PORTFOLIO | Yes | Yes | Yes |
| INSTRUMENT | Yes | No | Yes |
| ISSUER | Yes | Yes | Yes |
| CURVE_NAME | Yes | Yes | Yes |
| DATE | Yes | No | Yes |
| RECOVERY_RATE | Yes | Yes | Yes |
| PAR_CDS | **Yes** | No | No |
| CR01 (Zero) | No | **Yes** | No |
| CR01 (Par) | No | No | **Yes** |
| CURRENCY | Yes | Yes | Yes |
| CIF | Yes | Yes | Yes |
| GLOBUS_ID | Yes | Yes | Yes |
| COUNTRY | Yes | Yes | Yes |
| ISIN | Yes | Yes | Yes |
| MATURITY | Yes | Yes | Yes |
| UNDERLYING | Yes | Yes | Yes |
| RESTRUCT | No | Yes | Yes |
| NOTIONAL | No | Yes | Yes |
| MARKET | No | Yes | Yes |
| CR01 USD | No | Yes | Yes |
| **Total Fields** | **19** | **23** | **23** |

### 7.2 Key Differences

| Aspect | CR Par CDS Rate | CR Delta Zero/Par |
|--------|-----------------|-------------------|
| **Data Type** | Market data (spread level) | Sensitivity (P&L impact) |
| **Key Metric** | PAR_CDS (spread / 100) | CR01 (1bp sensitivity) |
| **Source** | TBL_AC_CRDCURVES_REP | Simulation calculation |
| **Bonds** | PAR_CDS = 0 | CR01 calculated |
| **USD Conversion** | No | Yes |
| **Field Count** | 19 | 23 |

---

## 8. Error Handling

### 8.1 Error Codes

| Error Code | Description | Severity | Action |
|------------|-------------|----------|--------|
| ERR-PAR-001 | Missing mandatory field | Critical | Reject record |
| ERR-PAR-002 | Invalid field format | Critical | Reject record |
| ERR-PAR-003 | Issuer not mapped | Warning | Use INSTRUMENT |
| ERR-PAR-004 | Curve not found | Warning | Set PAR_CDS to null |
| ERR-PAR-005 | Portfolio not in Bookman | Critical | Map to UNMAPPED |
| ERR-PAR-006 | Bond with non-zero PAR_CDS | Warning | Flag, correct to 0 |

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
| Accuracy | PAR_CDS matches curves | Curve data validation |
| Consistency | Bonds have PAR_CDS = 0 | Daily check |

---

## 10. Related Documentation

| Document | ID | Relationship |
|----------|-----|--------------|
| [CR Par CDS Rate BRD](./cr-par-cds-rate-brd.md) | CR-PAR-BRD-001 | Business requirements |
| [CR Par CDS Rate IT Config](./cr-par-cds-rate-config.md) | CR-PAR-CFG-001 | Technical configuration |
| [CR Delta Zero IDD](../cr-delta-zero/cr-delta-zero-idd.md) | CR-DZ-IDD-001 | Related interface |
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
