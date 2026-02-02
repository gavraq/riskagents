---
# Document Metadata
document_id: BM-IDD-001
document_name: Base Metals Sensitivities Feed - Interface Design Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: BM-BRD-001
feed_id: BM-001
---

# Base Metals Sensitivities Feed - Interface Design Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | BM-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Executive Summary

This document specifies the interface design for the Base Metals Sensitivities Feed. It defines the file format, field specifications, data types, validation rules, and delivery mechanism for sensitivity data flowing from Murex to downstream risk systems.

---

## 2. Interface Overview

### 2.1 Interface Summary

| Property | Value |
|----------|-------|
| **Interface ID** | IF-BM-SENS-001 |
| **Interface Name** | Base Metals Sensitivities Feed |
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
| **Delimiter** | Pipe (`|`) |
| **Text Qualifier** | Double Quote (`"`) |
| **Encoding** | UTF-8 |
| **Line Ending** | Unix (LF) |
| **Header Row** | Yes (first row) |
| **Compression** | GZIP (for transfer) |
| **Encryption** | PGP (for transfer) |

### 3.2 File Naming Convention

**Pattern**: `MxMGB_Sens_BM_Combined_{Region}_{Date}.csv`

| Component | Format | Example |
|-----------|--------|---------|
| Prefix | `MxMGB_Sens_BM_Combined` | Fixed |
| Region | 2-character code | `LN`, `HK`, `NY`, `SP` |
| Date | `YYYYMMDD` | `20250102` |
| Extension | `.csv` | Fixed |

**Example**: `MxMGB_Sens_BM_Combined_LN_20250102.csv`

**Compressed/Encrypted**: `MxMGB_Sens_BM_Combined_LN_20250102.csv.gz.pgp`

### 3.3 File Size Expectations

| Metric | Expected | Alert Threshold |
|--------|----------|-----------------|
| Row Count | 100,000 - 140,000 | <90,000 or >160,000 |
| File Size (uncompressed) | 40-60 MB | <30 MB or >80 MB |
| File Size (compressed) | 4-8 MB | <3 MB or >12 MB |

---

## 4. Field Specification

### 4.1 Field Summary

The feed contains 42 fields organized into logical categories:

| Category | Field Count | Fields |
|----------|-------------|--------|
| Identification | 4 | EXTRACTION_DATE, TRADE_ID, POSITION_ID, DEAL_NUMBER |
| Hierarchy | 8 | BOOK_CODE through ENTITY_NAME |
| Product | 6 | PRODUCT_TYPE through OPTION_STYLE |
| Underlying | 4 | METAL_CODE through LOT_SIZE |
| Dates | 4 | TRADE_DATE through PILLAR_LABEL |
| Sensitivity | 5 | SENSITIVITY_TYPE through DELTA_PILLAR |
| Processing | 6 | MARKET_DATA_SET through RECORD_TYPE |
| Reconciliation | 5 | BATCH_ID through CHECKSUM |

### 4.2 Complete Field Definitions

#### 4.2.1 Identification Fields

| # | Field Name | Data Type | Length | Nullable | Description |
|---|------------|-----------|--------|----------|-------------|
| 1 | EXTRACTION_DATE | DATE | 8 | No | Date of data extraction (YYYYMMDD) |
| 2 | TRADE_ID | VARCHAR | 50 | No | Murex trade identifier |
| 3 | POSITION_ID | VARCHAR | 50 | No | Position identifier |
| 4 | DEAL_NUMBER | INTEGER | 15 | No | Murex deal number |

#### 4.2.2 Hierarchy Fields

| # | Field Name | Data Type | Length | Nullable | Description |
|---|------------|-----------|--------|----------|-------------|
| 5 | BOOK_CODE | VARCHAR | 20 | No | Trading book code |
| 6 | BOOK_NAME | VARCHAR | 100 | No | Trading book name |
| 7 | DESK_CODE | VARCHAR | 20 | No | Trading desk code |
| 8 | DESK_NAME | VARCHAR | 100 | No | Trading desk name |
| 9 | DIVISION_CODE | VARCHAR | 20 | No | Division code |
| 10 | DIVISION_NAME | VARCHAR | 100 | No | Division name |
| 11 | ENTITY_CODE | VARCHAR | 20 | No | Legal entity code |
| 12 | ENTITY_NAME | VARCHAR | 100 | No | Legal entity name |

#### 4.2.3 Product Fields

| # | Field Name | Data Type | Length | Nullable | Description |
|---|------------|-----------|--------|----------|-------------|
| 13 | PRODUCT_TYPE | VARCHAR | 30 | No | Product classification |
| 14 | PRODUCT_SUB_TYPE | VARCHAR | 30 | Yes | Sub-classification |
| 15 | INSTRUMENT_TYPE | VARCHAR | 30 | No | Instrument type |
| 16 | OPTION_TYPE | VARCHAR | 10 | Yes | Call/Put indicator |
| 17 | OPTION_STYLE | VARCHAR | 20 | Yes | American/European/Asian |
| 18 | BUY_SELL | VARCHAR | 4 | No | Trade direction (BUY/SELL) |

#### 4.2.4 Underlying Fields

| # | Field Name | Data Type | Length | Nullable | Description |
|---|------------|-----------|--------|----------|-------------|
| 19 | METAL_CODE | VARCHAR | 10 | No | Base metal code (CU, AL, etc.) |
| 20 | METAL_NAME | VARCHAR | 50 | No | Full metal name |
| 21 | LME_CODE | VARCHAR | 10 | No | LME commodity code |
| 22 | LOT_SIZE | DECIMAL | 10,2 | No | Lot size in MT |

#### 4.2.5 Date Fields

| # | Field Name | Data Type | Length | Nullable | Description |
|---|------------|-----------|--------|----------|-------------|
| 23 | TRADE_DATE | DATE | 8 | No | Trade execution date |
| 24 | MATURITY_DATE | DATE | 8 | No | Maturity/expiry date |
| 25 | PILLAR_DATE | DATE | 8 | No | Assigned pillar date |
| 26 | PILLAR_LABEL | VARCHAR | 10 | No | Pillar label (Cash, 1M, etc.) |

#### 4.2.6 Sensitivity Fields

| # | Field Name | Data Type | Length | Nullable | Description |
|---|------------|-----------|--------|----------|-------------|
| 27 | SENSITIVITY_TYPE | VARCHAR | 30 | No | Type of sensitivity |
| 28 | SENSITIVITY_VALUE | DECIMAL | 20,10 | No | Sensitivity value |
| 29 | SENSITIVITY_UNIT | VARCHAR | 10 | No | Unit (USD, MT, Lots) |
| 30 | SENSITIVITY_CCY | VARCHAR | 3 | No | Currency (always USD) |
| 31 | DELTA_PILLAR | INTEGER | 3 | Yes | Delta strike pillar (10-90) |

#### 4.2.7 Processing Fields

| # | Field Name | Data Type | Length | Nullable | Description |
|---|------------|-----------|--------|----------|-------------|
| 32 | MARKET_DATA_SET | VARCHAR | 20 | No | Market data set used |
| 33 | CALCULATION_DATE | DATE | 8 | No | Date of calculation |
| 34 | CALCULATION_TIME | TIME | 8 | No | Time of calculation (HH:MM:SS) |
| 35 | REGION_CODE | VARCHAR | 5 | No | Processing region |
| 36 | SOURCE_FILE | VARCHAR | 100 | No | Original source file name |
| 37 | RECORD_TYPE | VARCHAR | 10 | No | Record type (DATA/TOTAL) |

#### 4.2.8 Reconciliation Fields

| # | Field Name | Data Type | Length | Nullable | Description |
|---|------------|-----------|--------|----------|-------------|
| 38 | BATCH_ID | VARCHAR | 50 | No | Batch run identifier |
| 39 | BATCH_TIMESTAMP | TIMESTAMP | 26 | No | Batch execution timestamp |
| 40 | RECORD_SEQUENCE | INTEGER | 10 | No | Sequential record number |
| 41 | VERSION_NUMBER | INTEGER | 5 | No | Feed version (for resubmissions) |
| 42 | CHECKSUM | VARCHAR | 64 | No | Record-level SHA-256 checksum |

---

## 5. Sensitivity Type Codes

### 5.1 Sensitivity Type Reference

| Code | Description | Unit | Pillar Type |
|------|-------------|------|-------------|
| `AD_FWD_DELTA_MT` | Adapted Forward Delta | MT | Tenor |
| `AD_FWD_DELTA_USD` | Adapted Forward Delta | USD | Tenor |
| `DISC_AD_FWD_DELTA_MT` | Discounted Adapted Forward Delta | MT | Tenor |
| `DISC_AD_FWD_DELTA_USD` | Discounted Adapted Forward Delta | USD | Tenor |
| `DISC_AD_FWD_GAMMA_MT` | Discounted Adapted Forward Gamma | MT | Tenor |
| `DISC_AD_FWD_GAMMA_USD` | Discounted Adapted Forward Gamma | USD | Tenor |
| `QTY_LOTS` | Quantity in Lots | Lots | N/A |
| `QTY_MT` | Quantity in Metric Tonnes | MT | N/A |
| `QTY_USD` | Quantity in USD | USD | N/A |
| `VEGA` | Vega | USD | Tenor × Strike |
| `WEIGHTED_VEGA` | Weighted Vega | USD | Tenor × Strike |
| `VOLGA` | Volga | USD | Tenor |
| `VANNA` | Vanna | USD | Tenor |
| `THETA` | Theta | USD | N/A |

### 5.2 Pillar Label Reference

| Code | Description | Days to Maturity |
|------|-------------|------------------|
| `CASH` | Spot/Cash | 0-2 |
| `1M` | One Month | ~22 |
| `3M` | Three Months | ~66 |
| `6M` | Six Months | ~132 |
| `1Y` | One Year | ~264 |
| `18M` | Eighteen Months | ~396 |
| `2Y` | Two Years | ~528 |
| `3Y` | Three Years | ~792 |
| `5Y` | Five Years | ~1320 |
| `7Y` | Seven Years | ~1848 |
| `10Y` | Ten Years | ~2640 |

### 5.3 Delta Pillar Reference

| Code | Description |
|------|-------------|
| `10` | 10-delta (deep OTM) |
| `25` | 25-delta (OTM) |
| `50` | 50-delta (ATM) |
| `75` | 75-delta (ITM) |
| `90` | 90-delta (deep ITM) |

---

## 6. Metal Code Reference

### 6.1 Base Metals

| Metal Code | Metal Name | LME Code | Lot Size (MT) |
|------------|------------|----------|---------------|
| `CU` | Copper | `CA` | 25 |
| `AL` | Aluminium | `AH` | 25 |
| `ZN` | Zinc | `ZS` | 25 |
| `NI` | Nickel | `NI` | 6 |
| `PB` | Lead | `PB` | 25 |
| `SN` | Tin | `SN` | 5 |

---

## 7. Sample Data

### 7.1 Sample Records

```
EXTRACTION_DATE|TRADE_ID|POSITION_ID|DEAL_NUMBER|BOOK_CODE|BOOK_NAME|DESK_CODE|DESK_NAME|DIVISION_CODE|DIVISION_NAME|ENTITY_CODE|ENTITY_NAME|PRODUCT_TYPE|PRODUCT_SUB_TYPE|INSTRUMENT_TYPE|OPTION_TYPE|OPTION_STYLE|BUY_SELL|METAL_CODE|METAL_NAME|LME_CODE|LOT_SIZE|TRADE_DATE|MATURITY_DATE|PILLAR_DATE|PILLAR_LABEL|SENSITIVITY_TYPE|SENSITIVITY_VALUE|SENSITIVITY_UNIT|SENSITIVITY_CCY|DELTA_PILLAR|MARKET_DATA_SET|CALCULATION_DATE|CALCULATION_TIME|REGION_CODE|SOURCE_FILE|RECORD_TYPE|BATCH_ID|BATCH_TIMESTAMP|RECORD_SEQUENCE|VERSION_NUMBER|CHECKSUM
20250102|MX-BM-2025-001234|POS-BM-001234|1234567|BMLN001|London Base Metals 1|BMLN|Base Metals London|GM|Global Markets|MGBL|Meridian Global Bank London|LME_OPTION|VANILLA|OPTION|CALL|EUROPEAN|BUY|CU|Copper|CA|25|20241115|20250315|20250315|3M|DISC_AD_FWD_DELTA_USD|125847.2345678901|USD|USD||LNCLOSE|20250102|21:15:30|LN|MxMGB_Sens_BM_DAdFwdDeltaUS_LN_20250102.csv|DATA|BATCH-20250102-001|2025-01-02T21:30:00Z|1|a1b2c3d4e5f6...
20250102|MX-BM-2025-001234|POS-BM-001234|1234567|BMLN001|London Base Metals 1|BMLN|Base Metals London|GM|Global Markets|MGBL|Meridian Global Bank London|LME_OPTION|VANILLA|OPTION|CALL|EUROPEAN|BUY|CU|Copper|CA|25|20241115|20250315|20250315|3M|VEGA|8547.1234567890|USD|USD|50|LNCLOSE|20250102|21:15:30|LN|MxMGB_Sens_BM_Vega_LN_20250102.csv|DATA|BATCH-20250102-001|2025-01-02T21:30:00Z|2|b2c3d4e5f6g7...
20250102|MX-BM-2025-001234|POS-BM-001234|1234567|BMLN001|London Base Metals 1|BMLN|Base Metals London|GM|Global Markets|MGBL|Meridian Global Bank London|LME_OPTION|VANILLA|OPTION|CALL|EUROPEAN|BUY|CU|Copper|CA|25|20241115|20250315|20250315|3M|WEIGHTED_VEGA|4273.5617283945|USD|USD|50|LNCLOSE|20250102|21:15:30|LN|MxMGB_Sens_BM_WeightedVega_LN_20250102.csv|DATA|BATCH-20250102-001|2025-01-02T21:30:00Z|3|c3d4e5f6g7h8...
```

### 7.2 Sample Header Row

```
EXTRACTION_DATE|TRADE_ID|POSITION_ID|DEAL_NUMBER|BOOK_CODE|BOOK_NAME|DESK_CODE|DESK_NAME|DIVISION_CODE|DIVISION_NAME|ENTITY_CODE|ENTITY_NAME|PRODUCT_TYPE|PRODUCT_SUB_TYPE|INSTRUMENT_TYPE|OPTION_TYPE|OPTION_STYLE|BUY_SELL|METAL_CODE|METAL_NAME|LME_CODE|LOT_SIZE|TRADE_DATE|MATURITY_DATE|PILLAR_DATE|PILLAR_LABEL|SENSITIVITY_TYPE|SENSITIVITY_VALUE|SENSITIVITY_UNIT|SENSITIVITY_CCY|DELTA_PILLAR|MARKET_DATA_SET|CALCULATION_DATE|CALCULATION_TIME|REGION_CODE|SOURCE_FILE|RECORD_TYPE|BATCH_ID|BATCH_TIMESTAMP|RECORD_SEQUENCE|VERSION_NUMBER|CHECKSUM
```

---

## 8. Validation Rules

### 8.1 Field-Level Validation

| Field | Rule | Error Action |
|-------|------|--------------|
| EXTRACTION_DATE | Valid date, <= today | Reject record |
| TRADE_ID | Not null, valid format | Reject record |
| BOOK_CODE | Exists in Bookman | Map to UNMAPPED |
| METAL_CODE | Valid base metal code | Reject record |
| SENSITIVITY_TYPE | Valid type code | Reject record |
| SENSITIVITY_VALUE | Numeric, within range | Flag for review |
| PILLAR_LABEL | Valid pillar code | Reject record |
| DELTA_PILLAR | 10, 25, 50, 75, or 90 | Reject record |

### 8.2 Record-Level Validation

| Rule | Description | Error Action |
|------|-------------|--------------|
| Unique Key | TRADE_ID + SENSITIVITY_TYPE + PILLAR_DATE + DELTA_PILLAR | Reject duplicate |
| Sign Consistency | Delta sign matches BUY_SELL direction | Flag for review |
| Gamma Consistency | Gamma and Delta have consistent signs | Flag for review |
| Weighted Vega | If Vega exists, Weighted Vega must exist | Flag for review |

### 8.3 File-Level Validation

| Rule | Description | Threshold |
|------|-------------|-----------|
| Row Count | Within expected range | 90,000 - 160,000 |
| Header Match | Header matches specification | Exact match |
| No Empty File | File contains data rows | >0 data rows |
| Checksum Valid | Control file checksum matches | Exact match |

### 8.4 Cross-File Validation

| Rule | Description | Tolerance |
|------|-------------|-----------|
| Position Coverage | All positions in Trade feed have sensitivities | 100% |
| Metal Coverage | All metals have at least one sensitivity | 100% |
| Total Delta | Sum of delta matches risk system | 0.1% |

---

## 9. Error Handling

### 9.1 Error Codes

| Code | Severity | Description | Action |
|------|----------|-------------|--------|
| `BM-ERR-001` | Critical | File not received by SLA | Escalate to L2 |
| `BM-ERR-002` | High | Row count outside threshold | Investigate, may proceed |
| `BM-ERR-003` | High | Checksum mismatch | Request retransmission |
| `BM-ERR-004` | Medium | Records failed validation | Exclude, process rest |
| `BM-ERR-005` | Medium | Hierarchy unmapped | Map to UNMAPPED |
| `BM-ERR-006` | Low | Missing optional field | Accept, log warning |

### 9.2 Error Log Format

| Field | Description |
|-------|-------------|
| TIMESTAMP | Error occurrence time |
| ERROR_CODE | Error code from table above |
| FILE_NAME | Source file name |
| RECORD_NUMBER | Line number in file |
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
| **Directory** | /outbound/basemetals/ |

### 10.2 Transfer Schedule

| Step | Time (GMT) | Description |
|------|------------|-------------|
| File Ready | 22:30 | Files available in source |
| Transfer Start | 22:35 | MFT pickup |
| Transfer Complete | 22:45 | Files delivered |
| Acknowledgment | 23:00 | Target system confirms |

### 10.3 Control File

**File Name**: `MxMGB_Sens_BM_Combined_{Region}_{Date}.ctl`

| Field | Description | Example |
|-------|-------------|---------|
| FILE_NAME | Data file name | `MxMGB_Sens_BM_Combined_LN_20250102.csv.gz.pgp` |
| ROW_COUNT | Number of data rows | `125847` |
| CHECKSUM | SHA-256 hash | `a1b2c3d4...` |
| EXTRACTION_DATE | COB date | `20250102` |
| REGION | Region code | `LN` |
| GENERATION_TIME | File creation time | `2025-01-02T22:30:00Z` |
| FILE_SIZE | Size in bytes | `5242880` |

### 10.4 Acknowledgment File

**File Name**: `MxMGB_Sens_BM_Combined_{Region}_{Date}.ack`

| Field | Description | Example |
|-------|-------------|---------|
| FILE_NAME | Received file name | `MxMGB_Sens_BM_Combined_LN_20250102.csv.gz.pgp` |
| STATUS | Receipt status | `SUCCESS` or `FAILED` |
| ROWS_LOADED | Rows successfully loaded | `125847` |
| ROWS_REJECTED | Rows rejected | `0` |
| RECEIPT_TIME | Time of receipt | `2025-01-02T22:45:00Z` |
| ERROR_DETAILS | Error message if failed | (empty if success) |

---

## 11. Resubmission Process

### 11.1 Resubmission Triggers

| Trigger | Process |
|---------|---------|
| File corruption | Regenerate and resend |
| Missing data | Rerun extraction with corrections |
| Incorrect valuations | Rerun after market data fix |
| Consumer request | Resend existing file |

### 11.2 Resubmission Naming

**Pattern**: `MxMGB_Sens_BM_Combined_{Region}_{Date}_V{Version}.csv`

| Version | Description |
|---------|-------------|
| V1 | First resubmission |
| V2 | Second resubmission |
| Vn | nth resubmission |

**Example**: `MxMGB_Sens_BM_Combined_LN_20250102_V1.csv`

### 11.3 Resubmission Notification

Email notification sent to:
- risk-tech-ops@meridianbank.com
- plato-support@meridianbank.com
- rds-support@meridianbank.com

Subject: `[RESUBMISSION] Base Metals Sensitivities Feed - {Region} - {Date} - V{Version}`

---

## 12. Consumer Integration Guide

### 12.1 Plato (VaR Engine)

| Property | Value |
|----------|-------|
| **Load Process** | Automated batch load |
| **Load Table** | `PLATO.STG_BM_SENSITIVITIES` |
| **Processing** | Immediate after load |
| **Dependencies** | Trade feed must be loaded first |

### 12.2 RDS (Risk Data Store)

| Property | Value |
|----------|-------|
| **Load Process** | ETL job |
| **Load Table** | `RDS.FACT_BM_SENSITIVITIES` |
| **Processing** | T+1 morning |
| **Forward To** | VESPA |

### 12.3 VESPA (Risk Reporting)

| Property | Value |
|----------|-------|
| **Source** | Via RDS |
| **Usage** | Reporting and analytics |
| **Retention** | 7 years |

---

## 13. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Base Metals BRD](./base-metals-brd.md) | BM-BRD-001 | Business requirements |
| [Base Metals IT Config](./base-metals-config.md) | BM-CFG-001 | IT configuration |
| [Sensitivities IDD](../sensitivities/sensitivities-idd.md) | SENS-IDD-001 | General sensitivities IDD |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |

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
