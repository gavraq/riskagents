---
# Document Metadata
document_id: IR-IDD-001
document_name: IR Delta & Gamma - Interface Design Document
version: 1.0
effective_date: 2025-01-03
next_review_date: 2026-01-03
owner: Market Risk Technology
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds/ir-delta-gamma
feed_family: IR Delta & Gamma
document_type: IDD
---

# IR Delta & Gamma - Interface Design Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | IR-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 3 January 2025 |
| **Owner** | Market Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Introduction

### 1.1 Purpose

This Interface Design Document specifies the technical interface for the IR Delta & Gamma sensitivity feed from Murex to downstream risk systems. It provides the detailed file format, field specifications, and integration requirements.

### 1.2 Scope

This document covers:
- File naming conventions and delivery
- Record structure and field definitions
- Data types and validation rules
- Sample data and examples
- Consumer integration guidelines

### 1.3 Interface Summary

| Property | Value |
|----------|-------|
| **Interface Name** | IR Delta & Gamma Sensitivities |
| **Interface ID** | MR-IF-IR-001 |
| **Source System** | Murex (VESPA Module) |
| **Target Systems** | Risk Data Warehouse, Plato, VESPA Reporting |
| **Protocol** | MFT (Managed File Transfer) |
| **Format** | CSV (Comma-Separated Values) |
| **Frequency** | Daily (T+1) |

---

## 2. File Specification

### 2.1 File Naming Convention

#### Pattern
```
MxMGB_MR_Rates_DV01_{Region}_{YYYYMMDD}.csv
```

#### Components

| Component | Description | Example Values |
|-----------|-------------|----------------|
| MxMGB | Source system prefix (Murex, Meridian Global Bank) | MxMGB |
| MR | Domain (Market Risk) | MR |
| Rates | Asset class | Rates |
| DV01 | Sensitivity type | DV01 |
| {Region} | Trading region code | LN, HK, NY, SP |
| {YYYYMMDD} | Business date | 20250103 |

#### Examples

| Region | Example Filename |
|--------|------------------|
| London | MxMGB_MR_Rates_DV01_LN_20250103.csv |
| Hong Kong | MxMGB_MR_Rates_DV01_HK_20250103.csv |
| New York | MxMGB_MR_Rates_DV01_NY_20250103.csv |
| Singapore | MxMGB_MR_Rates_DV01_SP_20250103.csv |

### 2.2 File Properties

| Property | Value |
|----------|-------|
| **Format** | CSV |
| **Encoding** | UTF-8 |
| **Delimiter** | Comma (,) |
| **Text Qualifier** | Double Quote (") |
| **Escape Character** | Backslash (\) |
| **Line Ending** | Unix (LF) |
| **Header Row** | Yes (first row) |
| **Decimal Separator** | Period (.) |
| **Thousands Separator** | None |
| **Date Format** | YYYY-MM-DD |
| **Null Representation** | Empty string |

### 2.3 File Delivery

| Property | Value |
|----------|-------|
| **Delivery Method** | MFT (Managed File Transfer) |
| **Source Directory** | /data/outbound/vespa/ |
| **Target Directory** | /data/inbound/market_risk/ |
| **Delivery Time** | 05:00 GMT (T+1) |
| **SLA** | 99.5% on-time delivery |
| **Retry Policy** | 3 attempts, 15-minute intervals |

---

## 3. Record Structure

### 3.1 Field Overview

| # | Field Name | Type | Length | Nullable | Description |
|---|------------|------|--------|----------|-------------|
| 1 | TRADE_NUM | VARCHAR | 20 | N | Trade number |
| 2 | PORTFOLIO | VARCHAR | 30 | N | Trading portfolio |
| 3 | DATE | DATE | 10 | N | Pillar date |
| 4 | CURVENAME | VARCHAR | 50 | N | Interest rate curve |
| 5 | TYPOLOGY | VARCHAR | 30 | N | Product typology |
| 6 | FAMILY | VARCHAR | 10 | N | Trade family |
| 7 | GROUP | VARCHAR | 10 | N | Trade group |
| 8 | TYPE | VARCHAR | 10 | Y | Trade type |
| 9 | CATEGORY | VARCHAR | 20 | Y | Trade category |
| 10 | ISSUE | VARCHAR | 50 | Y | Issue identifier |
| 11 | PROFITCENTRE | VARCHAR | 20 | Y | Profit centre |
| 12 | DELTAUSD | NUMERIC | 18,4 | N | DV01 in USD |
| 13 | GAMMAUSD | NUMERIC | 18,4 | N | Gamma in USD |
| 14 | ZAR_PROCESSING | VARCHAR | 1 | Y | ZAR flag (deprecated) |
| 15 | DELTAZAR | NUMERIC | 18,4 | Y | DV01 ZAR (deprecated) |
| 16 | GAMMAZAR | NUMERIC | 18,4 | Y | Gamma ZAR (deprecated) |
| 17 | PARDELTAZAR | NUMERIC | 18,4 | Y | Par Delta ZAR (deprecated) |
| 18 | PARGAMMAZAR | NUMERIC | 18,4 | Y | Par Gamma ZAR (deprecated) |

### 3.2 Field Definitions

#### TRADE_NUM
| Property | Value |
|----------|-------|
| **Description** | Unique trade identifier from Murex |
| **Type** | VARCHAR(20) |
| **Nullable** | No |
| **Example** | "TRD123456789" |
| **Validation** | Alphanumeric, no special characters |

#### PORTFOLIO
| Property | Value |
|----------|-------|
| **Description** | Trading book/portfolio code |
| **Type** | VARCHAR(30) |
| **Nullable** | No |
| **Example** | "IRDLN_SWAPS_EUR" |
| **Validation** | Must exist in portfolio inventory |

#### DATE
| Property | Value |
|----------|-------|
| **Description** | Pillar date for the sensitivity |
| **Type** | DATE |
| **Format** | YYYY-MM-DD |
| **Nullable** | No |
| **Example** | "2025-03-15" |
| **Validation** | Must be valid date ≥ business date |

#### CURVENAME
| Property | Value |
|----------|-------|
| **Description** | Interest rate curve identifier |
| **Type** | VARCHAR(50) |
| **Nullable** | No |
| **Example** | "USD_SOFR", "EUR_EURIBOR_6M" |
| **Validation** | Must exist in curve inventory |

#### TYPOLOGY
| Property | Value |
|----------|-------|
| **Description** | Full product classification (Family\|Group\|Type) |
| **Type** | VARCHAR(30) |
| **Format** | {Family}\|{Group}\|{Type} |
| **Nullable** | No |
| **Example** | "IRD\|SWAP\|IRS", "IRD\|CF\|CAP" |

#### FAMILY
| Property | Value |
|----------|-------|
| **Description** | Product family code |
| **Type** | VARCHAR(10) |
| **Nullable** | No |
| **Valid Values** | IRD |
| **Example** | "IRD" |

#### GROUP
| Property | Value |
|----------|-------|
| **Description** | Product group within family |
| **Type** | VARCHAR(10) |
| **Nullable** | No |
| **Valid Values** | CF, OSWP, SWAP, FRA, FUT, BOND, REPO |
| **Example** | "SWAP", "CF" |

#### TYPE
| Property | Value |
|----------|-------|
| **Description** | Product type within group |
| **Type** | VARCHAR(10) |
| **Nullable** | Yes |
| **Example** | "IRS", "OIS", "CAP", "FLOOR" |

#### CATEGORY
| Property | Value |
|----------|-------|
| **Description** | Trade category classification |
| **Type** | VARCHAR(20) |
| **Nullable** | Yes |
| **Example** | "FLOW", "STRUCTURED" |

#### ISSUE
| Property | Value |
|----------|-------|
| **Description** | Issue or instrument identifier |
| **Type** | VARCHAR(50) |
| **Nullable** | Yes |
| **Example** | "US912810TM26" |

#### PROFITCENTRE
| Property | Value |
|----------|-------|
| **Description** | Profit centre code for P&L attribution |
| **Type** | VARCHAR(20) |
| **Nullable** | Yes |
| **Example** | "PC_RATES_LN" |

#### DELTAUSD
| Property | Value |
|----------|-------|
| **Description** | DV01 sensitivity in USD equivalent |
| **Type** | NUMERIC(18,4) |
| **Unit** | USD |
| **Nullable** | No |
| **Example** | -12345.6789 |
| **Interpretation** | P&L change for 1bp parallel shift |

#### GAMMAUSD
| Property | Value |
|----------|-------|
| **Description** | Gamma sensitivity in USD equivalent |
| **Type** | NUMERIC(18,4) |
| **Unit** | USD |
| **Nullable** | No |
| **Default** | 0 (for non-option products) |
| **Example** | 567.8901 |
| **Interpretation** | Rate of change of Delta for 1bp shift |

#### ZAR_PROCESSING (Deprecated)
| Property | Value |
|----------|-------|
| **Description** | Flag for ZAR currency processing |
| **Type** | VARCHAR(1) |
| **Valid Values** | Y, N |
| **Status** | Deprecated - SBSA exclusion |
| **Default** | N |

#### DELTAZAR (Deprecated)
| Property | Value |
|----------|-------|
| **Description** | DV01 in ZAR equivalent |
| **Type** | NUMERIC(18,4) |
| **Status** | Deprecated - SBSA exclusion |
| **Default** | 0 |

#### GAMMAZAR (Deprecated)
| Property | Value |
|----------|-------|
| **Description** | Gamma in ZAR equivalent |
| **Type** | NUMERIC(18,4) |
| **Status** | Deprecated - SBSA exclusion |
| **Default** | 0 |

#### PARDELTAZAR (Deprecated)
| Property | Value |
|----------|-------|
| **Description** | Par Delta in ZAR |
| **Type** | NUMERIC(18,4) |
| **Status** | Deprecated - SBSA exclusion |
| **Default** | 0 |

#### PARGAMMAZAR (Deprecated)
| Property | Value |
|----------|-------|
| **Description** | Par Gamma in ZAR |
| **Type** | NUMERIC(18,4) |
| **Status** | Deprecated - SBSA exclusion |
| **Default** | 0 |

---

## 4. Data Validation Rules

### 4.1 Field-Level Validations

| Rule ID | Field | Rule | Severity |
|---------|-------|------|----------|
| VAL-IR-001 | TRADE_NUM | NOT NULL AND LENGTH > 0 | Error |
| VAL-IR-002 | PORTFOLIO | NOT NULL AND LENGTH > 0 | Error |
| VAL-IR-003 | DATE | Valid date format YYYY-MM-DD | Error |
| VAL-IR-004 | DATE | DATE >= Business date | Warning |
| VAL-IR-005 | CURVENAME | NOT NULL AND LENGTH > 0 | Error |
| VAL-IR-006 | TYPOLOGY | Format: XXX\|XXX\|XXX | Warning |
| VAL-IR-007 | FAMILY | = 'IRD' | Error |
| VAL-IR-008 | GROUP | IN ('CF','OSWP','SWAP','FRA','FUT','BOND','REPO') | Warning |
| VAL-IR-009 | DELTAUSD | Numeric value | Error |
| VAL-IR-010 | GAMMAUSD | Numeric value | Error |
| VAL-IR-011 | GAMMAUSD | = 0 if GROUP NOT IN ('CF','OSWP') | Warning |

### 4.2 Record-Level Validations

| Rule ID | Rule | Description |
|---------|------|-------------|
| VAL-IR-R01 | Unique key | TRADE_NUM + DATE + CURVENAME must be unique |
| VAL-IR-R02 | Gamma consistency | If GROUP = 'CF' or 'OSWP', GAMMAUSD may be non-zero |
| VAL-IR-R03 | Typology match | TYPOLOGY = FAMILY + '\|' + GROUP + '\|' + TYPE |

### 4.3 File-Level Validations

| Rule ID | Rule | Description |
|---------|------|-------------|
| VAL-IR-F01 | Header present | First row must be header row |
| VAL-IR-F02 | Field count | Each row must have 18 fields |
| VAL-IR-F03 | Non-empty | File must contain at least 1 data row |
| VAL-IR-F04 | Record count | ±10% of previous day |

---

## 5. Sample Data

### 5.1 Header Row

```csv
TRADE_NUM,PORTFOLIO,DATE,CURVENAME,TYPOLOGY,FAMILY,GROUP,TYPE,CATEGORY,ISSUE,PROFITCENTRE,DELTAUSD,GAMMAUSD,ZAR_PROCESSING,DELTAZAR,GAMMAZAR,PARDELTAZAR,PARGAMMAZAR
```

### 5.2 Sample Records

#### Interest Rate Swap (Linear - No Gamma)
```csv
TRD000001234,IRDLN_SWAPS_EUR,2025-03-15,EUR_EURIBOR_6M,IRD|SWAP|IRS,IRD,SWAP,IRS,FLOW,,PC_RATES_LN,-15234.5678,0.0000,N,0.0000,0.0000,0.0000,0.0000
```

#### Cap (Option - Has Gamma)
```csv
TRD000005678,IRDLN_OPTIONS_USD,2025-06-15,USD_SOFR,IRD|CF|CAP,IRD,CF,CAP,FLOW,,PC_RATES_LN,8765.4321,234.5678,N,0.0000,0.0000,0.0000,0.0000
```

#### Swaption (Option - Has Gamma)
```csv
TRD000009012,IRDLN_SWAPTIONS_GBP,2026-01-15,GBP_SONIA,IRD|OSWP|SWAPTION,IRD,OSWP,SWAPTION,STRUCTURED,,PC_RATES_LN,-5432.1098,156.7890,N,0.0000,0.0000,0.0000,0.0000
```

#### FRA (Linear - No Gamma)
```csv
TRD000003456,IRDHK_FRA_USD,2025-04-15,USD_LIBOR_3M,IRD|FRA|,IRD,FRA,,FLOW,,PC_RATES_HK,2345.6789,0.0000,N,0.0000,0.0000,0.0000,0.0000
```

### 5.3 Complete Sample File

```csv
TRADE_NUM,PORTFOLIO,DATE,CURVENAME,TYPOLOGY,FAMILY,GROUP,TYPE,CATEGORY,ISSUE,PROFITCENTRE,DELTAUSD,GAMMAUSD,ZAR_PROCESSING,DELTAZAR,GAMMAZAR,PARDELTAZAR,PARGAMMAZAR
TRD000001234,IRDLN_SWAPS_EUR,2025-03-15,EUR_EURIBOR_6M,IRD|SWAP|IRS,IRD,SWAP,IRS,FLOW,,PC_RATES_LN,-15234.5678,0.0000,N,0.0000,0.0000,0.0000,0.0000
TRD000001234,IRDLN_SWAPS_EUR,2025-06-15,EUR_EURIBOR_6M,IRD|SWAP|IRS,IRD,SWAP,IRS,FLOW,,PC_RATES_LN,-14876.2345,0.0000,N,0.0000,0.0000,0.0000,0.0000
TRD000001234,IRDLN_SWAPS_EUR,2025-09-15,EUR_EURIBOR_6M,IRD|SWAP|IRS,IRD,SWAP,IRS,FLOW,,PC_RATES_LN,-14523.8901,0.0000,N,0.0000,0.0000,0.0000,0.0000
TRD000005678,IRDLN_OPTIONS_USD,2025-06-15,USD_SOFR,IRD|CF|CAP,IRD,CF,CAP,FLOW,,PC_RATES_LN,8765.4321,234.5678,N,0.0000,0.0000,0.0000,0.0000
TRD000005678,IRDLN_OPTIONS_USD,2025-09-15,USD_SOFR,IRD|CF|CAP,IRD,CF,CAP,FLOW,,PC_RATES_LN,8234.1234,198.7654,N,0.0000,0.0000,0.0000,0.0000
TRD000009012,IRDLN_SWAPTIONS_GBP,2026-01-15,GBP_SONIA,IRD|OSWP|SWAPTION,IRD,OSWP,SWAPTION,STRUCTURED,,PC_RATES_LN,-5432.1098,156.7890,N,0.0000,0.0000,0.0000,0.0000
```

---

## 6. Integration Guidelines

### 6.1 Consumer Onboarding

| Step | Description | Owner |
|------|-------------|-------|
| 1 | Request access via Service Desk | Consumer |
| 2 | Provide target system details | Consumer |
| 3 | Configure MFT delivery | Risk Technology |
| 4 | Provide sample files | Risk Technology |
| 5 | UAT validation | Consumer |
| 6 | Production go-live | Joint |

### 6.2 Recommended Processing

```
1. File Arrival
   └── Monitor MFT landing zone
   └── Validate file naming convention
   └── Check file size (non-zero)

2. File Validation
   └── Verify header row structure
   └── Count fields per row (18)
   └── Validate data types
   └── Check record count vs threshold

3. Data Loading
   └── Parse CSV with appropriate library
   └── Apply data type conversions
   └── Handle nullable fields
   └── Insert into staging table

4. Data Quality
   └── Run validation rules
   └── Generate exception report
   └── Alert on critical failures

5. Data Integration
   └── Transform as needed
   └── Load to target tables
   └── Update processing metadata
```

### 6.3 Error Handling Recommendations

| Error Type | Recommended Action |
|------------|-------------------|
| File not arrived | Wait until SLA, then alert |
| File empty | Reject, alert Risk Technology |
| Parse errors | Log and continue, report exceptions |
| Validation failures | Load valid records, quarantine failures |
| Duplicate records | Take latest by timestamp |

### 6.4 Aggregation Patterns

#### By Portfolio
```sql
SELECT
    PORTFOLIO,
    SUM(DELTAUSD) AS TOTAL_DELTA,
    SUM(GAMMAUSD) AS TOTAL_GAMMA
FROM IR_DELTA_GAMMA
GROUP BY PORTFOLIO;
```

#### By Curve
```sql
SELECT
    CURVENAME,
    SUM(DELTAUSD) AS TOTAL_DELTA,
    SUM(GAMMAUSD) AS TOTAL_GAMMA
FROM IR_DELTA_GAMMA
GROUP BY CURVENAME;
```

#### By Pillar Bucket
```sql
SELECT
    CASE
        WHEN DATE <= DATEADD(month, 3, GETDATE()) THEN '0-3M'
        WHEN DATE <= DATEADD(year, 1, GETDATE()) THEN '3M-1Y'
        WHEN DATE <= DATEADD(year, 5, GETDATE()) THEN '1Y-5Y'
        WHEN DATE <= DATEADD(year, 10, GETDATE()) THEN '5Y-10Y'
        ELSE '10Y+'
    END AS TENOR_BUCKET,
    SUM(DELTAUSD) AS TOTAL_DELTA,
    SUM(GAMMAUSD) AS TOTAL_GAMMA
FROM IR_DELTA_GAMMA
GROUP BY TENOR_BUCKET;
```

---

## 7. Change Management

### 7.1 Change Request Process

| Change Type | Lead Time | Approval |
|-------------|-----------|----------|
| New field addition | 4 weeks | Change Board |
| Field format change | 4 weeks | Change Board |
| File naming change | 2 weeks | Risk Technology Lead |
| Delivery time change | 2 weeks | Risk Technology Lead |
| New consumer | 1 week | Risk Technology Lead |

### 7.2 Version Compatibility

| Version | Status | Support Until |
|---------|--------|---------------|
| 1.0 | Current | - |

### 7.3 Deprecation Policy

- Deprecated fields retained for minimum 12 months
- Consumer notification 6 months before removal
- Migration support available during transition

---

## 8. Contact Information

### 8.1 Support Contacts

| Role | Team | Contact |
|------|------|---------|
| L1 Support | Risk Technology | risk.tech@meridianbank.com |
| L2 Support | Murex Support | murex.support@meridianbank.com |
| Data Quality | Risk Operations | risk.ops@meridianbank.com |
| Business Owner | Rates Trading | rates.trading@meridianbank.com |

### 8.2 Escalation Path

```
L1: Risk Technology Service Desk (response: 2 hours)
    ↓
L2: Murex Support Team (response: 4 hours)
    ↓
L3: Risk Technology Lead (response: same day)
    ↓
L4: Head of Risk Technology (response: next day)
```

---

## 9. Appendices

### Appendix A: Curve Name Reference

| Curve Name | Currency | Index | Description |
|------------|----------|-------|-------------|
| USD_SOFR | USD | SOFR | Secured Overnight Financing Rate |
| USD_LIBOR_3M | USD | LIBOR | 3-month USD LIBOR (legacy) |
| EUR_EURIBOR_6M | EUR | EURIBOR | 6-month EURIBOR |
| EUR_ESTER | EUR | ESTER | Euro Short-Term Rate |
| GBP_SONIA | GBP | SONIA | Sterling Overnight Index Average |
| GBP_LIBOR_6M | GBP | LIBOR | 6-month GBP LIBOR (legacy) |
| JPY_TONA | JPY | TONA | Tokyo Overnight Average Rate |
| CHF_SARON | CHF | SARON | Swiss Average Rate Overnight |

### Appendix B: Product Type Reference

| Family | Group | Type | Description | Has Gamma |
|--------|-------|------|-------------|-----------|
| IRD | CF | CAP | Interest Rate Cap | Yes |
| IRD | CF | FLOOR | Interest Rate Floor | Yes |
| IRD | CF | COLLAR | Cap + Floor combination | Yes |
| IRD | OSWP | SWAPTION | Option to enter swap | Yes |
| IRD | OSWP | STRADDLE | Payer + Receiver swaption | Yes |
| IRD | SWAP | IRS | Interest Rate Swap | No |
| IRD | SWAP | OIS | Overnight Index Swap | No |
| IRD | SWAP | BASIS | Basis Swap | No |
| IRD | SWAP | CCS | Cross Currency Swap | No |
| IRD | FRA | - | Forward Rate Agreement | No |
| IRD | FUT | ED | Eurodollar Future | No |
| IRD | FUT | SOFR | SOFR Future | No |
| IRD | BOND | FIXED | Fixed Rate Bond | No |
| IRD | BOND | FRN | Floating Rate Note | No |
| IRD | REPO | - | Repurchase Agreement | No |

### Appendix C: Maturity Set LNOFFICIAL

| Pillar | Days | Tenor Category |
|--------|------|----------------|
| O/N | 1 | Overnight |
| T/N | 2 | Tomorrow/Next |
| 1W | 7 | Short-term |
| 2W | 14 | Short-term |
| 1M | 30 | Money Market |
| 2M | 60 | Money Market |
| 3M | 90 | Money Market |
| 6M | 180 | Money Market |
| 9M | 270 | Money Market |
| 1Y | 365 | Swap |
| 2Y | 730 | Swap |
| 3Y | 1095 | Swap |
| 5Y | 1825 | Swap |
| 7Y | 2555 | Swap |
| 10Y | 3650 | Swap |
| 15Y | 5475 | Long-term |
| 20Y | 7300 | Long-term |
| 30Y | 10950 | Long-term |

---

## 10. Document Control

### 10.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-03 | Initial version | Risk Technology |

### 10.2 Approval

| Role | Name | Date |
|------|------|------|
| Technical Owner | Risk Technology Lead | |
| Data Owner | Head of Risk Data | |
| Approver | Risk Technology Change Board | |

---

*End of Document*
