---
# Document Metadata
document_id: CR-DZ-IDD-001
document_name: CR Delta Zero Feed - Interface Design Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: CR-DZ-BRD-001
feed_id: CR-DZ-001
---

# CR Delta Zero Feed - Interface Design Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-DZ-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Executive Summary

This document specifies the interface design for the CR Delta Zero Feed (Credit Spread Sensitivity - Zero Curve). It defines the file format, field specifications, data types, validation rules, and delivery mechanism for credit delta zero data flowing from Murex to downstream risk systems.

---

## 2. Interface Overview

### 2.1 Interface Summary

| Property | Value |
|----------|-------|
| **Interface ID** | IF-CR-DZ-001 |
| **Interface Name** | CR Delta Zero Feed |
| **Source System** | Murex Trading System |
| **Target Systems** | Plato (VaR Engine), RDS, VESPA |
| **Direction** | Outbound (Murex → Downstream) |
| **Frequency** | Daily |
| **Trigger** | Batch completion |

### 2.2 Interface Participants

| Role | System | Contact |
|------|--------|---------|
| **Producer** | Murex | murex-support@meridianbank.com |
| **Consumer (Primary)** | Plato | plato-support@meridianbank.com |
| **Consumer (Secondary)** | RDS/VESPA | rds-support@meridianbank.com |
| **Operations** | Risk Technology | risk-tech-ops@meridianbank.com |

---

## 3. File Specification

### 3.1 File Properties

| Property | Value |
|----------|-------|
| **Format** | Delimited Text (CSV) |
| **Delimiter** | Semicolon (`;`) |
| **Text Qualifier** | None |
| **Encoding** | UTF-8 |
| **Line Ending** | Unix (LF) |
| **Header Row** | Yes (first row) |
| **Compression** | ZIP (packaged with other CR feeds) |
| **Encryption** | None (internal network) |

### 3.2 File Naming Convention

**Pattern**: `MxMGB_MR_Credit_CS01_{Region}_{Date}.csv`

| Component | Format | Example |
|-----------|--------|---------|
| Prefix | `MxMGB_MR_Credit` | Fixed |
| Region | 2-character code | `LN`, `HK`, `NY`, `SP` |
| Date | `YYYYMMDD` | `20250102` |
| Extension | `.csv` | Fixed |

**Example**: `MxMGB_MR_Credit_CS01_LN_20250102.csv`

**Package Name**: `MxMGB_MR_Credit_Sens_LN_20250102.zip`

### 3.3 File Size Expectations

| Metric | Expected | Alert Threshold |
|--------|----------|-----------------|
| Row Count | 5,000 - 8,000 | <4,000 or >12,000 |
| File Size (uncompressed) | 2-5 MB | <1 MB or >8 MB |
| File Size (compressed) | 200-500 KB | <100 KB or >1 MB |

---

## 4. Field Specification

### 4.1 Field Summary

The feed contains 23 fields:

| # | Field Name | Description |
|---|------------|-------------|
| 1 | TRADE_NUM | Trade number |
| 2 | FAMILY | Trade family |
| 3 | GROUP | Trade group |
| 4 | TYPE | Trade type |
| 5 | TYPOLOGY | Trade typology |
| 6 | PORTFOLIO | Portfolio |
| 7 | INSTRUMENT | PL Instrument |
| 8 | ISSUER | Issuer label |
| 9 | CURVE_NAME | Credit curve name |
| 10 | DATE | Maturity pillar |
| 11 | RECOVERY_RATE | Recovery rate |
| 12 | CR01__PA1 | CR Delta Zero (local currency) |
| 13 | CURRENCY | Currency |
| 14 | CIF | Customer Information File ID |
| 15 | GLOBUS_ID | External issuer ID |
| 16 | COUNTRY | Country of risk |
| 17 | ISIN | Reference obligation ISIN |
| 18 | MATURITY | Trade maturity date |
| 19 | UNDERLYING | Reference obligation label |
| 20 | RESTRUCT | Restructuring clause |
| 21 | NOTIONAL | Trade notional |
| 22 | MARKET | Security market |
| 23 | CR01__PA1 (USD) | CR Delta Zero (USD) |

### 4.2 Complete Field Definitions

| # | Field | Data Type | Length | Nullable | Description | Source |
|---|-------|-----------|--------|----------|-------------|--------|
| 1 | TRADE_NUM | Numeric | 10 | No | Murex trade number | VW_Vespa_Sensitivities.M_TRADE_NUM |
| 2 | FAMILY | VarChar | 16 | No | Trade family (CRD, IRD, EQD) | VW_Vespa_Sensitivities.M_FAMILY |
| 3 | GROUP | VarChar | 5 | No | Trade group (CDS, BOND, CRDI) | VW_Vespa_Sensitivities.M_GROUP |
| 4 | TYPE | VarChar | 16 | No | Trade type | VW_Vespa_Sensitivities.M_TYPE |
| 5 | TYPOLOGY | VarChar | 21 | No | Trade typology | VW_Vespa_Sensitivities.M_TYPOLOGY |
| 6 | PORTFOLIO | VarChar | 20 | No | Portfolio node | VW_Vespa_Sensitivities.M_PORTFOLIO |
| 7 | INSTRUMENT | VarChar | 30 | No | PL Instrument label | VW_Vespa_Sensitivities.M_PL_INSTRU |
| 8 | ISSUER | VarChar | 50 | No | Issuer label (or Index name for CRDI) | VW_Vespa_Sensitivities.M_ISSUER or M_PL_INSTRU |
| 9 | CURVE_NAME | VarChar | 50 | No | Credit curve name | VW_Vespa_Sensitivities.M_CURVE_NAM |
| 10 | DATE | VarChar | 64 | No | Maturity pillar (tenor bucket) | VW_Vespa_Sensitivities.M_DATE__ZER |
| 11 | RECOVERY_RATE | Numeric | 12 | No | Recovery rate (0-100), 0 for CRDI | VW_Vespa_Sensitivities.M_RATE |
| 12 | CR01__PA1 | Numeric | 12 | No | CR Delta Zero in local currency | VW_Vespa_Sensitivities.M_CR01__ZE1 |
| 13 | CURRENCY | VarChar | 4 | No | Sensitivity currency | VW_Vespa_Sensitivities.M_CURRENCY |
| 14 | CIF | Numeric | 9 | Yes | Customer Information File ID, 0 for CRDI | SB_CP_REP.M_U_CIF_ID |
| 15 | GLOBUS_ID | VarChar | 10 | Yes | External issuer identifier, blank for CRDI | SB_CP_REP.M_U_GLOBID |
| 16 | COUNTRY | VarChar | 30 | Yes | Country of risk, blank for CRDI | SB_CP_REP.M_U_RSK_CTRY |
| 17 | ISIN | VarChar | 25 | Yes | Reference obligation ISIN, blank for CRDI | SB_SE_HEAD_REP.M_SE_CODE or TBL_CRD_RECOVERY_REP.M_REF_OBLI1 |
| 18 | MATURITY | Date | 8 | No | Trade maturity date (DD/MM/YY) | SB_TP_REP.M_TP_DTEEXP |
| 19 | UNDERLYING | VarChar | 15 | Yes | Reference obligation label (CDS only) | TBL_CRD_RECOVERY_REP.M_REF_OBLIG |
| 20 | RESTRUCT | VarChar | 16 | No | Restructuring clause (CDS), 'NONE' if not applicable | TBL_CRD_RECOVERY_REP.M_RESTRUCTU |
| 21 | NOTIONAL | Numeric | 25 | No | Trade notional amount | SB_TP_BD_REP.M_TP_RTCCP02 or SB_TP_REP.M_TP_NOMINAL |
| 22 | MARKET | VarChar | 15 | Yes | Security market, blank for CRDI | SB_TP_EXT_REP.M_TP_SECMKT or TBL_SE_ROOT_REP.M_SE_MARKET |
| 23 | CR01__PA1 (USD) | Numeric | 16 | No | CR Delta Zero in USD | VW_Vespa_Sensitivities.M_CR01__ZER |

---

## 5. Field Value Specifications

### 5.1 FAMILY Values

| Code | Description | Products |
|------|-------------|----------|
| `CRD` | Credit Derivatives | CDS, CDX, iTraxx |
| `IRD` | Interest Rate Derivatives | Bonds with credit risk |
| `EQD` | Equity Derivatives | Equity-linked with credit risk |

### 5.2 GROUP Values

| Code | Description | Source Table |
|------|-------------|--------------|
| `CDS` | Single-name CDS | TBL_VESPA_SENS.REP |
| `BOND` | Corporate Bonds | TBL_VESPA_SENS.REP |
| `CRDI` | Credit Indices | TBL_VESPA_SENSCI.REP |

### 5.3 DATE (Tenor Pillar) Values

| Pillar | Description |
|--------|-------------|
| `6M` | Six months |
| `1Y` | One year |
| `2Y` | Two years |
| `3Y` | Three years |
| `5Y` | Five years |
| `7Y` | Seven years |
| `10Y` | Ten years |
| `15Y` | Fifteen years |
| `20Y` | Twenty years |
| `30Y` | Thirty years |

### 5.4 RESTRUCT Values

| Code | Description |
|------|-------------|
| `NONE` | No restructuring clause |
| `Yes` | Has restructuring clause |
| `MR` | Modified Restructuring |
| `MM` | Modified Modified Restructuring |
| `CR` | Complete Restructuring |

---

## 6. Non-CRDI vs CRDI Field Differences

| Field | Non-CRDI | CRDI |
|-------|----------|------|
| ISSUER | Issuer name from counterparty | Index label (e.g., CDX.NA.IG) |
| CURVE_NAME | Issuer credit curve | Index label |
| DATE | DATE__ZER (zero curve pillar) | DATE (par curve pillar) |
| RECOVERY_RATE | Issuer recovery rate (0-100%) | Always 0 |
| CIF | Issuer CIF | Always 0 |
| GLOBUS_ID | Issuer GLOBUS ID | Always blank |
| COUNTRY | Issuer country of risk | Always blank |
| ISIN | Reference obligation ISIN | Always blank |
| UNDERLYING | Reference obligation label | Always blank |
| MARKET | Security market | Always blank |

---

## 7. Sample Data

### 7.1 Sample Header Row

```
TRADE_NUM;FAMILY;GROUP;TYPE;TYPOLOGY;PORTFOLIO;INSTRUMENT;ISSUER;CURVE_NAME;DATE;RECOVERY_RATE;CR01__PA1;CURRENCY;CIF;GLOBUS_ID;COUNTRY;ISIN;MATURITY;UNDERLYING;RESTRUCT;NOTIONAL;MARKET;CR01__PA1 (USD)
```

### 7.2 Sample Data Records

**Non-CRDI Record (Bond)**:
```
26256820;IRD;BOND;CALL;IRD - CP BOND CALPUT;MMLNMGBLCTISD;MGB FRN 07/29 REGS;MGB;MGB_USD_SUBLT2;5Y;38.095200;0;USD;100060635.000000;101088;UNITED KINGDOM;BBG00PNR07D9;31/07/29;;NONE;-100000000.000000;USD CORP;0.00
```

**Non-CRDI Record (CDS)**:
```
26198745;CRD;CDS;SNCDS;CRD - SNAME CDS;CRDLNFLOW;ACME CORP 5Y CDS;ACME CORP;ACME_USD_SNR;5Y;40.000000;-2547.50;USD;100012345.000000;102567;UNITED STATES;US001234AB12;15/12/29;ACME_5Y_REF;MR;50000000.000000;USD CORP;-2547.50
```

**CRDI Record (Credit Index)**:
```
26301234;CRD;CRDI;CRDIDX;CRD - INDEX;CRDLNIDX;CDX.NA.IG.42;CDX.NA.IG.42;CDX.NA.IG.42;5Y;0;-15234.75;USD;0;;;;;;NONE;100000000.000000;;-15234.75
```

### 7.3 Full Sample File

```
TRADE_NUM;FAMILY;GROUP;TYPE;TYPOLOGY;PORTFOLIO;INSTRUMENT;ISSUER;CURVE_NAME;DATE;RECOVERY_RATE;CR01__PA1;CURRENCY;CIF;GLOBUS_ID;COUNTRY;ISIN;MATURITY;UNDERLYING;RESTRUCT;NOTIONAL;MARKET;CR01__PA1 (USD)
26256820;IRD;BOND;CALL;IRD - CP BOND CALPUT;MMLNMGBLCTISD;MGB FRN 07/29 REGS;MGB;MGB_USD_SUBLT2;5Y;38.095200;0;USD;100060635.000000;101088;UNITED KINGDOM;BBG00PNR07D9;31/07/29;;NONE;-100000000.000000;USD CORP;0.00
26256820;IRD;BOND;CALL;IRD - CP BOND CALPUT;MMLNMGBLCTISD;MGB FRN 07/29 REGS;MGB;MGB_USD_SUBLT2;7Y;38.095200;0;USD;100060635.000000;101088;UNITED KINGDOM;BBG00PNR07D9;31/07/29;;NONE;-100000000.000000;USD CORP;0.00
26256820;IRD;BOND;CALL;IRD - CP BOND CALPUT;MMLNMGBLCTISD;MGB FRN 07/29 REGS;MGB;MGB_USD_SUBLT2;6M;38.095200;103;USD;100060635.000000;101088;UNITED KINGDOM;BBG00PNR07D9;31/07/29;;NONE;-100000000.000000;USD CORP;102.84
26198745;CRD;CDS;SNCDS;CRD - SNAME CDS;CRDLNFLOW;ACME CORP 5Y CDS;ACME CORP;ACME_USD_SNR;5Y;40.000000;-2547.50;USD;100012345.000000;102567;UNITED STATES;US001234AB12;15/12/29;ACME_5Y_REF;MR;50000000.000000;USD CORP;-2547.50
26301234;CRD;CRDI;CRDIDX;CRD - INDEX;CRDLNIDX;CDX.NA.IG.42;CDX.NA.IG.42;CDX.NA.IG.42;5Y;0;-15234.75;USD;0;;;;;;NONE;100000000.000000;;-15234.75
```

---

## 8. Validation Rules

### 8.1 Field-Level Validation

| Field | Rule | Error Action |
|-------|------|--------------|
| TRADE_NUM | Not null, numeric | Reject record |
| FAMILY | Valid family code (CRD, IRD, EQD) | Reject record |
| GROUP | Valid group code (CDS, BOND, CRDI) | Reject record |
| PORTFOLIO | Not null | Reject record |
| ISSUER | Not null | Reject record |
| CURVE_NAME | Not null | Reject record |
| DATE | Valid tenor pillar | Reject record |
| RECOVERY_RATE | 0-100 for non-CRDI, 0 for CRDI | Flag for review |
| CR01__PA1 | Numeric | Reject record |
| CR01__PA1 (USD) | Numeric | Reject record |

### 8.2 Record-Level Validation

| Rule | Description | Error Action |
|------|-------------|--------------|
| Unique Key | TRADE_NUM + DATE must be unique per trade | Aggregate |
| Sign Consistency | CR01 sign should align with position direction | Flag for review |
| Currency Consistency | CR01 local vs USD should differ only by FX rate | Flag for review |
| CRDI Fields | CRDI records must have blank CIF, GLOBUS_ID, etc. | Flag for review |

### 8.3 File-Level Validation

| Rule | Description | Threshold |
|------|-------------|-----------|
| Row Count | Within expected range | 4,000 - 12,000 |
| Header Match | Header matches specification | Exact match |
| No Empty File | File contains data rows | >0 data rows |

### 8.4 Cross-File Validation

| Rule | Description | Tolerance |
|------|-------------|-----------|
| Position Coverage | All credit positions should have CR01 | 100% |
| Issuer Coverage | All issuers mapped | 100% |
| Total CR01 vs Risk System | Sum matches risk matrices | 0.1% |

---

## 9. Error Handling

### 9.1 Error Codes

| Code | Severity | Description | Action |
|------|----------|-------------|--------|
| `CR-ERR-001` | Critical | File not received by SLA | Escalate to L2 |
| `CR-ERR-002` | High | Row count outside threshold | Investigate |
| `CR-ERR-003` | High | Missing issuer | Map to UNMAPPED |
| `CR-ERR-004` | Medium | Recovery rate missing | Use sector default |
| `CR-ERR-005` | Medium | ISIN not found | Flag, proceed |
| `CR-ERR-006` | Low | Outlier CR01 value | Flag for review |

### 9.2 Error Log Format

| Field | Description |
|-------|-------------|
| TIMESTAMP | Error occurrence time |
| ERROR_CODE | Error code from table above |
| FILE_NAME | Source file name |
| RECORD_NUMBER | Line number in file |
| TRADE_NUM | Trade number affected |
| FIELD_NAME | Field causing error |
| FIELD_VALUE | Actual value |
| EXPECTED | Expected value/format |
| ACTION_TAKEN | Reject/Flag/Accept |

---

## 10. Delivery Mechanism

### 10.1 Transfer Protocol

| Property | Value |
|----------|-------|
| **Protocol** | SFTP |
| **Host** | mft.meridianbank.com |
| **Port** | 22 |
| **Authentication** | SSH Key |
| **Directory** | /outbound/credit/ |

### 10.2 Package Contents

The CR Delta Zero feed is delivered as part of a ZIP package containing all 8 CR Sensitivity feeds:

| # | File | Description |
|---|------|-------------|
| 1 | MxMGB_MR_Credit_CS01_*.csv | **CR Delta Zero (this feed)** |
| 2 | MxMGB_MR_Credit_CS01Par_*.csv | CR Delta Par |
| 3 | MxMGB_MR_Credit_Basis_*.csv | CR Basis Rate |
| 4 | MxMGB_MR_Credit_ParCDS_*.csv | CR Par CDS Rate |
| 5 | MxMGB_MR_Credit_Spread_*.csv | CR Instrument Spread |
| 6 | MxMGB_MR_Credit_Corr01_*.csv | CR Corr01 |
| 7 | MxMGB_MR_Credit_RR01_*.csv | CR RR01 |
| 8 | MxMGB_MR_Credit_RR02_*.csv | CR RR02 |

### 10.3 Transfer Schedule

| Step | Time (GMT) | Description |
|------|------------|-------------|
| Extraction Complete | 21:30 | Individual CSV files ready |
| Package Complete | 22:00 | ZIP file created |
| Transfer Start | 22:05 | MFT pickup |
| Transfer Complete | 22:15 | Files delivered |
| Acknowledgment | 23:00 | Target system confirms |

---

## 11. Consumer Integration Guide

### 11.1 Plato (VaR Engine)

| Property | Value |
|----------|-------|
| **Load Process** | Automated batch load |
| **Load Table** | `PLATO.STG_CR_DELTA_ZERO` |
| **Processing** | Immediate after load |
| **Key Fields** | TRADE_NUM, DATE, ISSUER |
| **Risk Factor Mapping** | By CURVE_NAME |

### 11.2 RDS (Risk Data Store)

| Property | Value |
|----------|-------|
| **Load Process** | ETL job |
| **Load Table** | `RDS.FACT_CR_SENSITIVITIES` |
| **Processing** | T+1 morning |
| **Forward To** | VESPA |
| **Retention** | 7 years |

### 11.3 VESPA (Risk Reporting)

| Property | Value |
|----------|-------|
| **Source** | Via RDS |
| **Usage** | Credit risk reporting, concentration analysis |
| **Aggregations** | By issuer, sector, rating, country |

---

## 12. Resubmission Process

### 12.1 Resubmission Triggers

| Trigger | Process |
|---------|---------|
| File corruption | Regenerate and resend |
| Missing data | Rerun extraction |
| Incorrect valuations | Rerun after curve fix |
| Consumer request | Resend existing file |

### 12.2 Resubmission Naming

**Pattern**: `MxMGB_MR_Credit_CS01_{Region}_{Date}_V{Version}.csv`

**Example**: `MxMGB_MR_Credit_CS01_LN_20250102_V1.csv`

---

## 13. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [CR Delta Zero BRD](./cr-delta-zero-brd.md) | CR-DZ-BRD-001 | Business requirements |
| [CR Delta Zero IT Config](./cr-delta-zero-config.md) | CR-DZ-CFG-001 | IT configuration |
| [Credit Sensitivities Overview](../credit-sensitivities-overview.md) | CR-OV-001 | Suite overview |
| [Sensitivities IDD](../sensitivities/sensitivities-idd.md) | SENS-IDD-001 | General sensitivities IDD |

---

## 14. Document Control

### 14.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-02 | Initial version | Risk Technology Change Board |

### 14.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Schema review | Semi-annual | July 2025 |
| Consumer feedback | Quarterly | April 2025 |

---

*End of Document*
