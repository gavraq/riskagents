---
# Document Metadata
document_id: IRB-IDD-001
document_name: IR Zero Basis - Interface Design Document
version: 1.0
effective_date: 2025-01-03
next_review_date: 2026-01-03
owner: Market Risk Technology
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds/ir-zero-basis
feed_family: IR Zero Basis
document_type: IDD
---

# IR Zero Basis - Interface Design Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | IRB-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 3 January 2025 |
| **Owner** | Market Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Introduction

### 1.1 Purpose

This Interface Design Document specifies the technical interface for the IR Zero Basis sensitivity feed from Murex to downstream risk systems. It provides the detailed file format, field specifications, and integration requirements.

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
| **Interface Name** | IR Zero Basis Sensitivities |
| **Interface ID** | MR-IF-IRB-001 |
| **Source System** | Murex (VESPA Module) |
| **Target Systems** | Risk Data Warehouse, Plato, VESPA Reporting |
| **Protocol** | MFT (Managed File Transfer) |
| **Format** | CSV (Semicolon-Separated Values) |
| **Frequency** | Daily (T+1) |

---

## 2. File Specification

### 2.1 File Naming Convention

#### Pattern
```
MxMGB_MR_Rates_Basis_{Region}_{YYYYMMDD}.csv
```

#### Components

| Component | Description | Example Values |
|-----------|-------------|----------------|
| MxMGB | Source system prefix (Murex, Meridian Global Bank) | MxMGB |
| MR | Domain (Market Risk) | MR |
| Rates | Asset class | Rates |
| Basis | Sensitivity type | Basis |
| {Region} | Trading region code | LN, HK, NY, SP |
| {YYYYMMDD} | Business date | 20250103 |

#### Examples

| Region | Example Filename |
|--------|------------------|
| London | MxMGB_MR_Rates_Basis_LN_20250103.csv |
| Hong Kong | MxMGB_MR_Rates_Basis_HK_20250103.csv |
| New York | MxMGB_MR_Rates_Basis_NY_20250103.csv |
| Sao Paulo | MxMGB_MR_Rates_Basis_SP_20250103.csv |

### 2.2 File Properties

| Property | Value |
|----------|-------|
| **Format** | CSV |
| **Encoding** | UTF-8 |
| **Delimiter** | Semicolon (;) |
| **Text Qualifier** | None |
| **Line Ending** | Unix (LF) |
| **Header Row** | Yes (first row) |
| **Decimal Separator** | Period (.) |
| **Thousands Separator** | None |
| **Null Representation** | Empty string |

### 2.3 File Delivery

| Property | Value |
|----------|-------|
| **Delivery Method** | MFT (Managed File Transfer) |
| **Source Directory** | ./reports/today/eod |
| **Package Format** | ZIP (MxMGB_MR_Sensitivities_{Region}_{YYYYMMDD}.zip) |
| **Delivery Time** | 05:30 GMT (T+1) |
| **SLA** | 99.5% on-time delivery |
| **Retry Policy** | 3 attempts, 15-minute intervals |

---

## 3. Record Structure

### 3.1 Field Overview

| # | Field Name | Type | Length | Nullable | Description |
|---|------------|------|--------|----------|-------------|
| 1 | PORTFOLIO | VARCHAR | 16 | N | Trading portfolio |
| 2 | Trade Number | NUMERIC | 16 | N | Trade identifier |
| 3 | CURRENCY | VARCHAR | 4 | N | Basis curve currency |
| 4 | CURVE_NAM | VARCHAR | 50 | N | Interest rate curve name |
| 5 | Type | VARCHAR | 10 | Y | Generator type |
| 6 | Generat | VARCHAR | 15 | Y | Generator name |
| 7 | DATE | VARCHAR | 64 | N | Pillar date |
| 8 | Basis Zero | NUMERIC | 16,6 | N | IR Basis Zero (local CCY) |
| 9 | ZAR_PROCESSING | VARCHAR | 1 | Y | JBSBSA flag (deprecated) |
| 10 | Basis Zero (USD) | NUMERIC | 16,6 | N | IR Basis Zero in USD |
| 11 | Basis Zero (ZAR) | NUMERIC | 16,6 | Y | IR Basis Zero in ZAR (deprecated) |
| 12 | Typology | VARCHAR | 21 | Y | Product typology |

### 3.2 Field Definitions

#### PORTFOLIO
| Property | Value |
|----------|-------|
| **Description** | Trading book/portfolio code |
| **Type** | VARCHAR(16) |
| **Nullable** | No |
| **Example** | "IRLNSBLG7P1" |
| **Validation** | Must exist in portfolio inventory |

#### Trade Number
| Property | Value |
|----------|-------|
| **Description** | Unique trade identifier from Murex |
| **Type** | NUMERIC(16) |
| **Nullable** | No |
| **Example** | 58249 |
| **Validation** | Positive integer |

#### CURRENCY
| Property | Value |
|----------|-------|
| **Description** | Currency of the basis curve |
| **Type** | VARCHAR(4) |
| **Nullable** | No |
| **Example** | "EUR", "GBP", "USD" |
| **Validation** | ISO 4217 currency code |

#### CURVE_NAM
| Property | Value |
|----------|-------|
| **Description** | Interest rate basis curve identifier |
| **Type** | VARCHAR(50) |
| **Nullable** | No |
| **Example** | "EUR_USD_3MESTR_3MSOFR" |
| **Validation** | Must exist in curve inventory |

#### Type
| Property | Value |
|----------|-------|
| **Description** | Generator type from curve configuration |
| **Type** | VARCHAR(10) |
| **Nullable** | Yes (may be blank for some pillars) |
| **Example** | "Basis swap" |
| **Source** | A_RTCT_REP.M_TYPE |

#### Generat
| Property | Value |
|----------|-------|
| **Description** | Generator name from curve configuration |
| **Type** | VARCHAR(15) |
| **Nullable** | Yes (may be blank for some pillars) |
| **Example** | "_EUR ESTR 3M /USD SOFR 3M [MT" |
| **Source** | A_RTCT_REP.M_GENERAT or M_D_GEN |

#### DATE
| Property | Value |
|----------|-------|
| **Description** | Maturity pillar from RISK_VIEW set |
| **Type** | VARCHAR(64) |
| **Nullable** | No |
| **Example** | "T/N", "1W", "3M", "5Y" |
| **Valid Values** | O/N, T/N, 1W, 1M, 2M, 3M, 6M, 9M, 1Y-40Y |

#### Basis Zero
| Property | Value |
|----------|-------|
| **Description** | IR Basis Zero sensitivity in local currency |
| **Type** | NUMERIC(16,6) |
| **Nullable** | No |
| **Example** | -0.030000 |
| **Interpretation** | P&L change for 1bp basis spread shift |

#### ZAR_PROCESSING (Deprecated)
| Property | Value |
|----------|-------|
| **Description** | Flag indicating JBSBSA closing entity |
| **Type** | VARCHAR(1) |
| **Valid Values** | Y, N |
| **Status** | Deprecated - SBSA exclusion |
| **Default** | N |

#### Basis Zero (USD)
| Property | Value |
|----------|-------|
| **Description** | IR Basis Zero sensitivity in USD equivalent |
| **Type** | NUMERIC(16,6) |
| **Nullable** | No |
| **Example** | -0.030000 |
| **Conversion** | Uses zero day FX spot rate |

#### Basis Zero (ZAR) (Deprecated)
| Property | Value |
|----------|-------|
| **Description** | IR Basis Zero sensitivity in ZAR equivalent |
| **Type** | NUMERIC(16,6) |
| **Status** | Deprecated - SBSA exclusion |
| **Default** | 0.000000 |

#### Typology
| Property | Value |
|----------|-------|
| **Description** | Product classification (Family\|Group\|Type) |
| **Type** | VARCHAR(21) |
| **Nullable** | Yes |
| **Example** | "IRD\|BS\|", "FXD\|CS\|" |

---

## 4. Data Validation Rules

### 4.1 Field-Level Validations

| Rule ID | Field | Rule | Severity |
|---------|-------|------|----------|
| VAL-IRB-001 | PORTFOLIO | NOT NULL AND LENGTH > 0 | Error |
| VAL-IRB-002 | Trade Number | Positive integer | Error |
| VAL-IRB-003 | CURRENCY | Valid ISO 4217 code | Error |
| VAL-IRB-004 | CURVE_NAM | NOT NULL AND LENGTH > 0 | Error |
| VAL-IRB-005 | DATE | Valid pillar from RISK_VIEW | Error |
| VAL-IRB-006 | Basis Zero | Numeric value | Error |
| VAL-IRB-007 | Basis Zero (USD) | Numeric value | Error |
| VAL-IRB-008 | ZAR_PROCESSING | IN ('Y', 'N', '') | Warning |

### 4.2 Record-Level Validations

| Rule ID | Rule | Description |
|---------|------|-------------|
| VAL-IRB-R01 | Non-zero filter | At least one of Basis Zero or Basis Zero (ZAR) must be non-zero |
| VAL-IRB-R02 | Unique key | Trade Number + CURVE_NAM + DATE must be unique |
| VAL-IRB-R03 | Currency consistency | CURRENCY must match first 3 chars of CURVE_NAM |

### 4.3 File-Level Validations

| Rule ID | Rule | Description |
|---------|------|-------------|
| VAL-IRB-F01 | Header present | First row must be header row |
| VAL-IRB-F02 | Field count | Each row must have 12 fields |
| VAL-IRB-F03 | Non-empty | File must contain at least 1 data row |
| VAL-IRB-F04 | Record count | ±10% of previous day |

---

## 5. Sample Data

### 5.1 Header Row

```csv
PORTFOLIO;Trade Number;CURRENCY;CURVE_NAM;Type;Generat;DATE;Basis Zero;ZAR_PROCESSING;Basis Zero (USD);Basis Zero (ZAR);Typology
```

### 5.2 Sample Records

#### EUR/USD Basis Swap - Short Pillar
```csv
IRLNSBLG7P1;58249;EUR;EUR_USD_3MESTR_3MSOFR;;;T/N;-0.03;N;-0.03;-0.63;
```

#### EUR/USD Basis Swap - With Generator
```csv
IRLNSBLG7P1;58249;EUR;EUR_USD_3MESTR_3MSOFR;Basis swap;_EUR ESTR 3M /USD SOFR 3M [MT;1W;-0.05;N;-0.05;-0.94;
```

#### GBP/USD Basis Swap - Short Pillar
```csv
FXDLNPROPALL;58277;GBP;GBP_USD_3MSONIA_3MSOFR;;;T/N;0.00;N;0.00;0.06;
```

#### GBP/USD Basis Swap - With Generator
```csv
FXDLNPROPALL;58277;GBP;GBP_USD_3MSONIA_3MSOFR;Basis swap;_GBP SONIA 3M / USD SOFR 3M [M;1W;0.00;N;0.00;0.09;
```

### 5.3 Complete Sample File

```csv
PORTFOLIO;Trade Number;CURRENCY;CURVE_NAM;Type;Generat;DATE;Basis Zero;ZAR_PROCESSING;Basis Zero (USD);Basis Zero (ZAR);Typology
IRLNSBLG7P1;58249;EUR;EUR_USD_3MESTR_3MSOFR;;;T/N;-0.03;N;-0.03;-0.63;
IRLNSBLG7P1;58249;EUR;EUR_USD_3MESTR_3MSOFR;Basis swap;_EUR ESTR 3M /USD SOFR 3M [MT;1W;-0.05;N;-0.05;-0.94;
IRLNSBLG7P1;58249;EUR;EUR_USD_3MESTR_3MSOFR;Basis swap;_EUR ESTR 3M /USD SOFR 3M [MT;1M;-0.12;N;-0.12;-2.31;
IRLNSBLG7P1;58249;EUR;EUR_USD_3MESTR_3MSOFR;Basis swap;_EUR ESTR 3M /USD SOFR 3M [MT;3M;-0.25;N;-0.25;-4.82;
FXDLNPROPALL;58277;GBP;GBP_USD_3MSONIA_3MSOFR;;;T/N;0.00;N;0.00;0.06;
FXDLNPROPALL;58277;GBP;GBP_USD_3MSONIA_3MSOFR;Basis swap;_GBP SONIA 3M / USD SOFR 3M [M;1W;0.00;N;0.00;0.09;
FXDLNPROPALL;58277;GBP;GBP_USD_3MSONIA_3MSOFR;Basis swap;_GBP SONIA 3M / USD SOFR 3M [M;1M;0.01;N;0.01;0.18;
```

---

## 6. Basis Curve Reference

### 6.1 Common Basis Curves

| Curve Name | Currency | Description |
|------------|----------|-------------|
| EUR_USD_3MESTR_3MSOFR | EUR | EUR ESTR 3M vs USD SOFR 3M basis |
| GBP_USD_3MSONIA_3MSOFR | GBP | GBP SONIA 3M vs USD SOFR 3M basis |
| USD_3MLIBOR_SOFR | USD | USD 3M LIBOR vs SOFR basis (legacy) |
| EUR_3M6M_BASIS | EUR | EUR 3M vs 6M tenor basis |
| USD_1M3M_BASIS | USD | USD 1M vs 3M tenor basis |
| JPY_USD_3MTONA_3MSOFR | JPY | JPY TONA 3M vs USD SOFR 3M basis |

### 6.2 Generator Types

| Type | Description |
|------|-------------|
| Basis swap | Cross-currency or cross-index basis swap |
| Tenor swap | Same currency, different tenor basis |
| XCS | Cross-currency swap generator |

---

## 7. Integration Guidelines

### 7.1 Consumer Onboarding

| Step | Description | Owner |
|------|-------------|-------|
| 1 | Request access via Service Desk | Consumer |
| 2 | Provide target system details | Consumer |
| 3 | Configure MFT delivery | Risk Technology |
| 4 | Provide sample files | Risk Technology |
| 5 | UAT validation | Consumer |
| 6 | Production go-live | Joint |

### 7.2 Recommended Processing

```
1. File Arrival
   └── Monitor MFT landing zone
   └── Extract from ZIP package
   └── Validate file naming convention

2. File Validation
   └── Verify header row structure
   └── Count fields per row (12)
   └── Validate delimiter (semicolon)

3. Data Loading
   └── Parse CSV with semicolon delimiter
   └── Apply data type conversions
   └── Handle empty Type/Generat fields
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

### 7.3 Aggregation Patterns

#### By Portfolio
```sql
SELECT
    PORTFOLIO,
    SUM("Basis Zero (USD)") AS TOTAL_BASIS_USD
FROM IR_ZERO_BASIS
GROUP BY PORTFOLIO;
```

#### By Currency
```sql
SELECT
    CURRENCY,
    SUM("Basis Zero (USD)") AS TOTAL_BASIS_USD
FROM IR_ZERO_BASIS
GROUP BY CURRENCY;
```

#### By Pillar Bucket
```sql
SELECT
    CASE
        WHEN DATE IN ('O/N', 'T/N', '1W') THEN 'Short'
        WHEN DATE IN ('1M', '2M', '3M', '6M', '9M') THEN 'Money Market'
        WHEN DATE IN ('1Y', '2Y', '3Y', '4Y', '5Y') THEN 'Short Swap'
        WHEN DATE IN ('6Y', '7Y', '8Y', '9Y', '10Y', '12Y') THEN 'Medium Swap'
        ELSE 'Long Swap'
    END AS TENOR_BUCKET,
    SUM("Basis Zero (USD)") AS TOTAL_BASIS_USD
FROM IR_ZERO_BASIS
GROUP BY TENOR_BUCKET;
```

#### By Basis Curve
```sql
SELECT
    CURVE_NAM,
    COUNT(DISTINCT "Trade Number") AS TRADE_COUNT,
    SUM("Basis Zero (USD)") AS TOTAL_BASIS_USD
FROM IR_ZERO_BASIS
GROUP BY CURVE_NAM
ORDER BY ABS(SUM("Basis Zero (USD)")) DESC;
```

---

## 8. Comparison with Related Feeds

### 8.1 IR Sensitivity Feeds

| Feed | File Pattern | Sensitivity | Maturity Set |
|------|--------------|-------------|--------------|
| IR Zero Basis | MxMGB_MR_Rates_Basis_* | Basis spread | RISK_VIEW (40Y) |
| IR Delta & Gamma | MxMGB_MR_Rates_DV01_* | Outright IR | LNOFFICIAL (30Y) |

### 8.2 Field Comparison

| Field | IR Zero Basis | IR Delta & Gamma |
|-------|---------------|------------------|
| Trade ID | Trade Number | TRADE_NUM |
| Portfolio | PORTFOLIO | PORTFOLIO |
| Curve | CURVE_NAM | CURVENAME |
| Pillar | DATE | DATE |
| Sensitivity | Basis Zero | DELTAUSD |
| Convexity | N/A | GAMMAUSD |
| Generator | Type, Generat | N/A |

---

## 9. Change Management

### 9.1 Change Request Process

| Change Type | Lead Time | Approval |
|-------------|-----------|----------|
| New field addition | 4 weeks | Change Board |
| Field format change | 4 weeks | Change Board |
| File naming change | 2 weeks | Risk Technology Lead |
| Delivery time change | 2 weeks | Risk Technology Lead |
| New consumer | 1 week | Risk Technology Lead |

### 9.2 Version Compatibility

| Version | Status | Support Until |
|---------|--------|---------------|
| 1.0 | Current | - |

---

## 10. Contact Information

### 10.1 Support Contacts

| Role | Team | Contact |
|------|------|---------|
| L1 Support | Risk Technology | risk.tech@meridianbank.com |
| L2 Support | Murex Support | murex.support@meridianbank.com |
| Data Quality | Risk Operations | risk.ops@meridianbank.com |
| Business Owner | Rates Trading | rates.trading@meridianbank.com |

### 10.2 Escalation Path

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

## 11. Appendices

### Appendix A: Maturity Set RISK_VIEW

| Pillar | Tenor Category | Pillar | Tenor Category |
|--------|---------------|--------|---------------|
| O/N | Short-term | 6Y | Medium Swap |
| T/N | Short-term | 7Y | Medium Swap |
| 1W | Short-term | 8Y | Medium Swap |
| 1M | Money Market | 9Y | Medium Swap |
| 2M | Money Market | 10Y | Medium Swap |
| 3M | Money Market | 12Y | Medium Swap |
| 6M | Money Market | 15Y | Long Swap |
| 9M | Money Market | 20Y | Long Swap |
| 1Y | Short Swap | 25Y | Long Swap |
| 2Y | Short Swap | 30Y | Long Swap |
| 3Y | Short Swap | 35Y | Long Swap |
| 4Y | Short Swap | 40Y | Long Swap |
| 5Y | Short Swap | | |

### Appendix B: Portfolio Node Reference

See IT Configuration document (IRB-CFG-001) for complete portfolio node listings by region.

---

## 12. Document Control

### 12.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-03 | Initial version | Risk Technology |

### 12.2 Approval

| Role | Name | Date |
|------|------|------|
| Technical Owner | Risk Technology Lead | |
| Data Owner | Head of Risk Data | |
| Approver | Risk Technology Change Board | |

---

*End of Document*
