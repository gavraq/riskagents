---
# Document Metadata
document_id: CR-BAS-IDD-001
document_name: CR Basis Rate Feed - Interface Design Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Steering Committee

# Parent Reference
parent_document: CR-BAS-BRD-001
feed_id: CR-BAS-001
---

# CR Basis Rate Feed - Interface Design Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-BAS-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Related BRD** | CR-BAS-BRD-001 |
| **Related Config** | CR-BAS-CFG-001 |

---

## 1. Interface Overview

### 1.1 Feed Summary

| Property | Value |
|----------|-------|
| **Feed Name** | CR Basis Rate Feed |
| **Feed ID** | CR-BAS-001 |
| **Source System** | Murex |
| **Target System** | VESPA / Plato Risk Engine |
| **Frequency** | Daily |
| **Format** | CSV |
| **Sensitivity** | BASIS (Recovery Rate without Propagation) |

### 1.2 File Naming Convention

| Component | Format | Example |
|-----------|--------|---------|
| Prefix | MxMGB | Murex Meridian Global Bank |
| Feed Type | Vespa_CR_Basis_Rate | Credit Basis Rate |
| Region | LN/HK/NY/SP | Trading region |
| Date | YYYYMMDD | As-of date |
| Extension | .csv | File format |

**Full Pattern**: `MxMGB_MR_Credit_Basis_Rate_{Region}_{YYYYMMDD}.csv`

**Examples**:
- `MxMGB_MR_Credit_Basis_Rate_LN_20250102.csv`
- `MxMGB_MR_Credit_Basis_Rate_HK_20250102.csv`
- `MxMGB_MR_Credit_Basis_Rate_NY_20250102.csv`

---

## 2. Field Specifications

### 2.1 Field Summary

| # | Field Name | Data Type | Length | Mandatory | Description |
|---|------------|-----------|--------|-----------|-------------|
| 1 | TRADE_NUMBER | VARCHAR | 20 | Yes | Murex trade identifier |
| 2 | PORTFOLIO | VARCHAR | 50 | Yes | Trading portfolio |
| 3 | FAMILY | VARCHAR | 10 | Yes | Trade family (CRD, IRD, EQD) |
| 4 | GRP | VARCHAR | 10 | Yes | Trade group |
| 5 | TYPE | VARCHAR | 20 | Yes | Trade type |
| 6 | TYPOLOGY | VARCHAR | 30 | Yes | Trade typology |
| 7 | ISSUER | VARCHAR | 100 | Conditional | Issuer name/label |
| 8 | CURVE_NAME | VARCHAR | 100 | Yes | Credit curve name |
| 9 | CIF | VARCHAR | 20 | Conditional | Customer Information File ID |
| 10 | GLOBUS_ID | VARCHAR | 20 | Conditional | External issuer identifier |
| 11 | COUNTRY | VARCHAR | 3 | Conditional | Country of risk (ISO) |
| 12 | ISIN | VARCHAR | 12 | Conditional | Reference obligation ISIN |
| 13 | BASIS | DECIMAL | 18,6 | Yes | Recovery sensitivity (local ccy) |
| 14 | BASIS_USD | DECIMAL | 18,6 | Yes | Recovery sensitivity (USD) |
| 15 | CURRENCY | VARCHAR | 3 | Yes | Trade currency (ISO) |
| 16 | MATURITY | DATE | 10 | Yes | Trade maturity date |
| 17 | MDS | VARCHAR | 20 | Yes | Market data set |
| 18 | UNDERLYING | VARCHAR | 100 | No | Reference obligation |
| 19 | RESTRUCTURING | VARCHAR | 20 | Conditional | Restructuring clause (CDS) |
| 20 | ASOF_DATE | DATE | 10 | Yes | Feed as-of date |

**Note**: This feed contains **20 fields** compared to CR Delta Zero's 23 fields. The following fields are **not included**:
- CR01 (Local)
- CR01 (USD)
- NOTIONAL
- MARKET

---

## 3. Field Definitions

### 3.1 Trade Identification Fields

#### 3.1.1 TRADE_NUMBER

| Property | Value |
|----------|-------|
| **Position** | 1 |
| **Data Type** | VARCHAR(20) |
| **Mandatory** | Yes |
| **Description** | Unique Murex trade identifier |
| **Source** | M_NB (Trade Number) |
| **Example** | 12345678 |
| **Validation** | Numeric, not null |

#### 3.1.2 PORTFOLIO

| Property | Value |
|----------|-------|
| **Position** | 2 |
| **Data Type** | VARCHAR(50) |
| **Mandatory** | Yes |
| **Description** | Trading portfolio from Bookman hierarchy |
| **Source** | M_TRN_FMLY (Trading Family) |
| **Example** | LN_CREDIT_TRADING |
| **Validation** | Must exist in Bookman hierarchy |

#### 3.1.3 FAMILY

| Property | Value |
|----------|-------|
| **Position** | 3 |
| **Data Type** | VARCHAR(10) |
| **Mandatory** | Yes |
| **Description** | Trade family classification |
| **Source** | M_TRN_FAM |
| **Valid Values** | CRD, IRD, EQD |
| **Example** | CRD |

#### 3.1.4 GRP

| Property | Value |
|----------|-------|
| **Position** | 4 |
| **Data Type** | VARCHAR(10) |
| **Mandatory** | Yes |
| **Description** | Trade group classification |
| **Source** | M_TRN_GRP |
| **Valid Values** | CDS, BOND, CRDI, CLN, etc. |
| **Example** | CDS |

#### 3.1.5 TYPE

| Property | Value |
|----------|-------|
| **Position** | 5 |
| **Data Type** | VARCHAR(20) |
| **Mandatory** | Yes |
| **Description** | Trade type |
| **Source** | M_TRN_TYPE |
| **Example** | CDS_SINGLE_NAME |

#### 3.1.6 TYPOLOGY

| Property | Value |
|----------|-------|
| **Position** | 6 |
| **Data Type** | VARCHAR(30) |
| **Mandatory** | Yes |
| **Description** | Trade typology for risk classification |
| **Source** | M_TYPOLOGY |
| **Example** | CDS_CORP_SENIOR |

### 3.2 Credit Reference Fields

#### 3.2.1 ISSUER

| Property | Value |
|----------|-------|
| **Position** | 7 |
| **Data Type** | VARCHAR(100) |
| **Mandatory** | Yes for Non-CRDI, No for CRDI |
| **Description** | Issuer name (Non-CRDI) or Index label (CRDI) |
| **Source (Non-CRDI)** | M_CREDIT_ISSUER |
| **Source (CRDI)** | CRDI_LABEL (Index identifier) |
| **Example (Non-CRDI)** | ACME_CORPORATION |
| **Example (CRDI)** | CDX.NA.IG.42 |

#### 3.2.2 CURVE_NAME

| Property | Value |
|----------|-------|
| **Position** | 8 |
| **Data Type** | VARCHAR(100) |
| **Mandatory** | Yes |
| **Description** | Credit spread curve name |
| **Source (Non-CRDI)** | M_CREDIT_CURVE |
| **Source (CRDI)** | CRDI_LABEL |
| **Example** | ACME_CORP_EUR_SENIOR |

#### 3.2.3 CIF

| Property | Value |
|----------|-------|
| **Position** | 9 |
| **Data Type** | VARCHAR(20) |
| **Mandatory** | Yes for Non-CRDI, No for CRDI |
| **Description** | Customer Information File ID |
| **Source** | M_CIF |
| **Example (Non-CRDI)** | CIF12345678 |
| **Example (CRDI)** | 0 |

#### 3.2.4 GLOBUS_ID

| Property | Value |
|----------|-------|
| **Position** | 10 |
| **Data Type** | VARCHAR(20) |
| **Mandatory** | Conditional (Non-CRDI only) |
| **Description** | External issuer identifier |
| **Source** | M_GLOBUS_ID |
| **Example (Non-CRDI)** | GLB987654321 |
| **Example (CRDI)** | (blank) |

#### 3.2.5 COUNTRY

| Property | Value |
|----------|-------|
| **Position** | 11 |
| **Data Type** | VARCHAR(3) |
| **Mandatory** | Conditional (Non-CRDI only) |
| **Description** | Country of risk (ISO 3166-1 alpha-2 or alpha-3) |
| **Source** | M_COUNTRY_RISK |
| **Example (Non-CRDI)** | US, GB, DE |
| **Example (CRDI)** | (blank - multi-country indices) |

#### 3.2.6 ISIN

| Property | Value |
|----------|-------|
| **Position** | 12 |
| **Data Type** | VARCHAR(12) |
| **Mandatory** | Conditional (Non-CRDI bonds) |
| **Description** | Reference obligation ISIN |
| **Source** | M_ISIN |
| **Example (Bond)** | US912828X000 |
| **Example (CDS/CRDI)** | (blank) |

### 3.3 Sensitivity Fields

#### 3.3.1 BASIS

| Property | Value |
|----------|-------|
| **Position** | 13 |
| **Data Type** | DECIMAL(18,6) |
| **Mandatory** | Yes |
| **Description** | Recovery rate sensitivity in trade currency (NO propagation) |
| **Source** | M_RECOVERY1 (Recovery Rate 2 in Simulation) |
| **Calculation** | P&L impact of recovery rate bump WITHOUT propagation to credit spread curve |
| **Unit** | Trade currency |
| **Sign Convention** | Positive = gain on recovery rate increase |
| **Example** | -12500.000000 |

**Key Distinction**:
- **BASIS** uses `M_RECOVERY1` (Recovery Rate 2) - does NOT propagate to spreads
- **RR01** uses `M_RECOVERY` (Recovery Rate 1) - DOES propagate to spreads

#### 3.3.2 BASIS_USD

| Property | Value |
|----------|-------|
| **Position** | 14 |
| **Data Type** | DECIMAL(18,6) |
| **Mandatory** | Yes |
| **Description** | Recovery rate sensitivity converted to USD |
| **Calculation** | BASIS × FX Rate (trade ccy to USD) |
| **Unit** | USD |
| **FX Rate Source** | COB FX rates from regional market data set |
| **Example** | -15625.000000 |

### 3.4 Trade Detail Fields

#### 3.4.1 CURRENCY

| Property | Value |
|----------|-------|
| **Position** | 15 |
| **Data Type** | VARCHAR(3) |
| **Mandatory** | Yes |
| **Description** | Trade/sensitivity currency (ISO 4217) |
| **Source** | M_CURRENCY |
| **Example** | EUR, USD, GBP |

#### 3.4.2 MATURITY

| Property | Value |
|----------|-------|
| **Position** | 16 |
| **Data Type** | DATE |
| **Format** | YYYY-MM-DD |
| **Mandatory** | Yes |
| **Description** | Trade maturity date |
| **Source** | M_MATURITY_DATE |
| **Example** | 2030-06-20 |

#### 3.4.3 MDS

| Property | Value |
|----------|-------|
| **Position** | 17 |
| **Data Type** | VARCHAR(20) |
| **Mandatory** | Yes |
| **Description** | Market data set used for valuation |
| **Source** | Batch parameter |
| **Valid Values** | LNCLOSE, HKCLOSE, NYCLOSE, SPCLOSE |
| **Example** | LNCLOSE |

#### 3.4.4 UNDERLYING

| Property | Value |
|----------|-------|
| **Position** | 18 |
| **Data Type** | VARCHAR(100) |
| **Mandatory** | No |
| **Description** | Reference obligation identifier |
| **Source** | M_UNDERLYING |
| **Example** | ACME 5.5% 2030 |

#### 3.4.5 RESTRUCTURING

| Property | Value |
|----------|-------|
| **Position** | 19 |
| **Data Type** | VARCHAR(20) |
| **Mandatory** | Conditional (CDS only) |
| **Description** | CDS restructuring clause type |
| **Source** | M_RESTRUCTURING |
| **Valid Values** | CR, MR, MM, XR, NR |
| **Example** | MM (Modified Modified) |

**Restructuring Clause Values**:
| Code | Description |
|------|-------------|
| CR | Full Restructuring |
| MR | Modified Restructuring |
| MM | Modified Modified Restructuring |
| XR | No Restructuring |
| NR | No Restructuring (legacy) |

#### 3.4.6 ASOF_DATE

| Property | Value |
|----------|-------|
| **Position** | 20 |
| **Data Type** | DATE |
| **Format** | YYYY-MM-DD |
| **Mandatory** | Yes |
| **Description** | Feed as-of date (business date) |
| **Source** | Batch parameter |
| **Example** | 2025-01-02 |

---

## 4. Data Flow

### 4.1 Non-CRDI Data Flow

```
VW_Vespa_Sensitivities (Simulation View)
    ↓ FD_VESPA_SENS (Feeder)
TBL_VESPA_SENS_REP (Datamart Table)
    ↓ DE_VESPA_CR_BASIS (Data Extractor)
CSV Output (Non-CRDI Records)
    ↓ UNION ALL
Combined Output File
```

### 4.2 CRDI Data Flow

```
VW_Vespa_Sensitivities_CRDI (Simulation View)
    ↓ FD_VESPA_SENSCI (Feeder)
TBL_VESPA_SENSCI_REP (Datamart Table)
    ↓ DE_VESPA_CR_BASIS (Data Extractor)
CSV Output (CRDI Records)
    ↓ UNION ALL
Combined Output File
```

### 4.3 Combined Output

The final output file contains both Non-CRDI and CRDI records via UNION ALL:
- **Non-CRDI records**: Source from TBL_VESPA_SENS_REP with full issuer details
- **CRDI records**: Source from TBL_VESPA_SENSCI_REP with index labels

---

## 5. Sample Data

### 5.1 Non-CRDI Example (Single-Name CDS)

```csv
TRADE_NUMBER,PORTFOLIO,FAMILY,GRP,TYPE,TYPOLOGY,ISSUER,CURVE_NAME,CIF,GLOBUS_ID,COUNTRY,ISIN,BASIS,BASIS_USD,CURRENCY,MATURITY,MDS,UNDERLYING,RESTRUCTURING,ASOF_DATE
12345678,LN_CREDIT_TRADING,CRD,CDS,CDS_SINGLE_NAME,CDS_CORP_SENIOR,ACME_CORPORATION,ACME_CORP_EUR_SENIOR,CIF12345678,GLB987654321,US,,-25000.000000,-28125.000000,EUR,2030-06-20,LNCLOSE,,MM,2025-01-02
```

### 5.2 CRDI Example (Credit Index)

```csv
TRADE_NUMBER,PORTFOLIO,FAMILY,GRP,TYPE,TYPOLOGY,ISSUER,CURVE_NAME,CIF,GLOBUS_ID,COUNTRY,ISIN,BASIS,BASIS_USD,CURRENCY,MATURITY,MDS,UNDERLYING,RESTRUCTURING,ASOF_DATE
87654321,LN_INDEX_TRADING,CRD,CRDI,INDEX_CDS,CDX_IG,CDX.NA.IG.42,CDX.NA.IG.42,0,,,,-150000.000000,-150000.000000,USD,2030-06-20,LNCLOSE,,,2025-01-02
```

### 5.3 Corporate Bond Example

```csv
TRADE_NUMBER,PORTFOLIO,FAMILY,GRP,TYPE,TYPOLOGY,ISSUER,CURVE_NAME,CIF,GLOBUS_ID,COUNTRY,ISIN,BASIS,BASIS_USD,CURRENCY,MATURITY,MDS,UNDERLYING,RESTRUCTURING,ASOF_DATE
23456789,LN_BOND_TRADING,IRD,BOND,CORP_BOND,BOND_CORP_SENIOR,BETA_INDUSTRIES,BETA_IND_USD_SENIOR,CIF23456789,GLB123456789,GB,US912828X000,-8500.000000,-8500.000000,USD,2028-03-15,LNCLOSE,BETA 5.5% 2028,,2025-01-02
```

---

## 6. Validation Rules

### 6.1 Mandatory Field Validation

| Rule ID | Field | Rule | Error Action |
|---------|-------|------|--------------|
| VAL-001 | TRADE_NUMBER | Not null, numeric | Reject record |
| VAL-002 | PORTFOLIO | Must exist in Bookman | Reject record |
| VAL-003 | FAMILY | Must be CRD, IRD, or EQD | Reject record |
| VAL-004 | GRP | Valid group code | Reject record |
| VAL-005 | BASIS | Not null | Reject record |
| VAL-006 | BASIS_USD | Not null | Reject record |
| VAL-007 | CURRENCY | Valid ISO 4217 code | Reject record |
| VAL-008 | ASOF_DATE | Valid date, matches batch date | Reject record |

### 6.2 Conditional Field Validation

| Rule ID | Condition | Field | Rule | Error Action |
|---------|-----------|-------|------|--------------|
| VAL-009 | GRP ≠ CRDI | ISSUER | Not null | Reject record |
| VAL-010 | GRP ≠ CRDI | CIF | Not null | Reject record |
| VAL-011 | GRP = CDS | RESTRUCTURING | Valid restructuring code | Flag for review |
| VAL-012 | GRP = BOND | ISIN | Valid ISIN format | Flag for review |

### 6.3 Cross-Field Validation

| Rule ID | Rule | Error Action |
|---------|------|--------------|
| VAL-013 | If BASIS ≠ 0, then BASIS_USD ≠ 0 | Flag for review |
| VAL-014 | BASIS sign consistent with trade direction | Flag for review |
| VAL-015 | No duplicate TRADE_NUMBER + CURVE_NAME combinations | Take latest |

---

## 7. Error Handling

### 7.1 Error Codes

| Error Code | Description | Severity | Action |
|------------|-------------|----------|--------|
| ERR-BAS-001 | Missing mandatory field | Critical | Reject record |
| ERR-BAS-002 | Invalid field format | Critical | Reject record |
| ERR-BAS-003 | Issuer not mapped | Warning | Flag, include record |
| ERR-BAS-004 | BASIS outlier detected | Warning | Flag, include record |
| ERR-BAS-005 | Portfolio not in Bookman | Critical | Map to UNMAPPED |
| ERR-BAS-006 | FX rate missing | Critical | Use T-1 rate |

### 7.2 Error Handling Matrix

| Error Type | Handling | Escalation |
|------------|----------|------------|
| Missing trade | Log and report | Daily reconciliation |
| Invalid sensitivity | Reject with reason | L2 Support |
| Unmapped hierarchy | Map to UNMAPPED | Bookman Team |
| Calculation failure | Use T-1 value | L2 Support |

---

## 8. Interface SLAs

### 8.1 Timing SLAs

| Metric | Target | Escalation |
|--------|--------|------------|
| File delivery | 05:30 GMT | >06:00 → L2 |
| File size | >0 bytes | Empty file → L2 |
| Record count | Within 10% of T-1 | Variance → RAV |
| Processing time | <60 minutes | >90 mins → L2 |

### 8.2 Quality SLAs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Completeness | 100% positions | Position count reconciliation |
| Accuracy | 100% valid values | Validation rule pass rate |
| Consistency | Match T-1 ± 10% | Daily comparison |

---

## 9. Downstream Integration

### 9.1 Consumer Systems

| System | Purpose | Fields Required |
|--------|---------|-----------------|
| VESPA | Risk reporting | All fields |
| Plato Risk Engine | VaR calculation | Sensitivity fields |
| Credit Limits System | Concentration monitoring | ISSUER, BASIS_USD |
| P&L Attribution | P&L explain | BASIS, TRADE_NUMBER |

### 9.2 Data Transformations

| Consumer | Transformation |
|----------|----------------|
| VESPA | Direct load, no transformation |
| Plato | Aggregate by CURVE_NAME |
| Credit Limits | Sum BASIS_USD by ISSUER |
| P&L Attribution | Match to T-1 for delta |

---

## 10. Comparison with Related Feeds

### 10.1 Field Comparison: CR Basis vs CR Delta Zero

| Field | CR Basis | CR Delta Zero | Notes |
|-------|----------|---------------|-------|
| TRADE_NUMBER | Yes | Yes | Same |
| PORTFOLIO | Yes | Yes | Same |
| FAMILY | Yes | Yes | Same |
| GRP | Yes | Yes | Same |
| TYPE | Yes | Yes | Same |
| TYPOLOGY | Yes | Yes | Same |
| ISSUER | Yes | Yes | Same |
| CURVE_NAME | Yes | Yes | Same |
| CIF | Yes | Yes | Same |
| GLOBUS_ID | Yes | Yes | Same |
| COUNTRY | Yes | Yes | Same |
| ISIN | Yes | Yes | Same |
| CR01 | **No** | Yes | CR Delta Zero only |
| CR01_USD | **No** | Yes | CR Delta Zero only |
| BASIS | Yes | **No** | CR Basis only |
| BASIS_USD | Yes | **No** | CR Basis only |
| RECOVERY_RATE | **No** | Yes | CR Delta Zero only |
| NOTIONAL | **No** | Yes | CR Delta Zero only |
| MARKET | **No** | Yes | CR Delta Zero only |
| CURRENCY | Yes | Yes | Same |
| MATURITY | Yes | Yes | Same |
| MDS | Yes | Yes | Same |
| UNDERLYING | Yes | Yes | Same |
| RESTRUCTURING | Yes | Yes | Same |
| ASOF_DATE | Yes | Yes | Same |
| **Total Fields** | **20** | **23** | |

### 10.2 Sensitivity Comparison

| Sensitivity | Source Field | Propagation | Feed |
|-------------|--------------|-------------|------|
| CR01 (Zero) | M_CREDIT_DELTA | N/A | CR Delta Zero |
| BASIS | M_RECOVERY1 | No | CR Basis Rate |
| RR01 | M_RECOVERY | Yes | CR RR01 |
| RR02 | M_RECOVERY1 | No | CR RR02 |

---

## 11. Related Documentation

| Document | ID | Relationship |
|----------|-----|--------------|
| [CR Basis BRD](./cr-basis-brd.md) | CR-BAS-BRD-001 | Business requirements |
| [CR Basis IT Config](./cr-basis-config.md) | CR-BAS-CFG-001 | Technical configuration |
| [CR Delta Zero IDD](../cr-delta-zero/cr-delta-zero-idd.md) | CR-DZ-IDD-001 | Related CR01 interface |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |
| [Murex GOM Guide](../../murex-gom-guide.md) | MR-L7-GOM | GOM reference |

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
| Field specification review | Semi-annual | July 2025 |
| Consumer alignment | Quarterly | April 2025 |

---

*End of Document*
