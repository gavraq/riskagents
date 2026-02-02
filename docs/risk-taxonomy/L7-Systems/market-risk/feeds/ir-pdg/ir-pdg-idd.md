---
# Document Metadata
document_id: PDG-IDD-001
document_name: IR Par Delta Gamma (PDG) - Interface Design Document
version: 1.0
effective_date: 2025-01-03
next_review_date: 2026-01-03
owner: Product Control
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds/ir-pdg
feed_family: IR Par Delta Gamma
document_type: IDD
---

# IR Par Delta Gamma (PDG) - Interface Design Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | PDG-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 3 January 2025 |
| **Owner** | Product Control |
| **Approver** | Risk Technology Change Board |

---

## 1. Interface Overview

### 1.1 Purpose

This Interface Design Document specifies the technical interface for the IR Par Delta Gamma (PDG) feed from Murex to downstream risk systems. It defines file formats, field specifications, validation rules, and delivery mechanisms.

### 1.2 Interface Summary

| Property | Value |
|----------|-------|
| **Interface ID** | IF-MR-PDG-001 |
| **Interface Name** | IR Par Delta Gamma Feed |
| **Direction** | Outbound (Murex to Downstream) |
| **Frequency** | Daily (T+1) |
| **Business Owner** | Product Control |
| **Source System** | Murex |
| **Target Systems** | Plato, Risk Data Warehouse (RDS) |

### 1.3 Feed Files

| Feed | File Pattern | Description |
|------|--------------|-------------|
| IR PDG | `MxMGB_MR_Rates_PDG_{Region}_{YYYYMMDD}.csv` | IR Par Delta and Gamma sensitivities |

---

## 2. File Specification

### 2.1 File Format

| Property | Value |
|----------|-------|
| **Format** | CSV (Comma-Separated Values) |
| **Delimiter** | Semicolon (;) |
| **Text Qualifier** | None |
| **Header Row** | Yes (first row) |
| **Encoding** | UTF-8 |
| **Line Ending** | Unix (LF) |
| **Decimal Separator** | Period (.) |
| **Thousand Separator** | None |
| **Date Format** | DD MMM YYYY (e.g., "02 Jun 2023") |
| **Numeric Format** | American (e.g., 12345.67) |

### 2.2 File Naming Convention

```
MxMGB_MR_Rates_PDG_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Example |
|-----------|-------------|---------|
| MxMGB | System identifier | MxMGB |
| MR | Asset class (Market Risk) | MR |
| Rates | Sub-asset class | Rates |
| PDG | Feed type (Par Delta Gamma) | PDG |
| Region | Trading region code | LN, HK, NY, SP |
| YYYYMMDD | Business date | 20250103 |

### 2.3 File Examples

| Region | Filename |
|--------|----------|
| London | `MxMGB_MR_Rates_PDG_LN_20250103.csv` |
| Hong Kong | `MxMGB_MR_Rates_PDG_HK_20250103.csv` |
| New York | `MxMGB_MR_Rates_PDG_NY_20250103.csv` |
| Sao Paulo | `MxMGB_MR_Rates_PDG_SP_20250103.csv` |

---

## 3. Field Specifications

### 3.1 Complete Field List (26 Fields)

| # | Field Name | Data Type | Length | Nullable | Description |
|---|------------|-----------|--------|----------|-------------|
| 1 | PORTFOLIO | VarChar | 16 | No | Trading portfolio code |
| 2 | Family | VarChar | 16 | No | Product family classification |
| 3 | Group | VarChar | 5 | No | Product group classification |
| 4 | Type | VarChar | 16 | Yes | Product type classification |
| 5 | Instrument | VarChar | 50 | Yes | P&L instrument name |
| 6 | Sec_code | VarChar | 16 | Yes | Security code |
| 7 | Trade Number | Numeric | 16 | No | Unique trade identifier (0 for DEAD) |
| 8 | CURRENCY | VarChar | 4 | No | Curve currency code |
| 9 | CURVE_NAM | VarChar | 35 | No | Interest rate curve name |
| 10 | CurveType | VarChar | 10 | No | Curve type (Swap, Bond, etc.) |
| 11 | Generat | VarChar | 10 | Yes | Generator name for pillar |
| 12 | DATE | VarChar | 64 | No | Pillar date |
| 13 | Delta Par | American | 16,2 | No | IR Delta Par (local currency) |
| 14 | Delta Par(USD) | American | 16,2 | No | IR Delta Par (USD) |
| 15 | Gamma Par | American | 16,2 | No | IR Gamma Par (local currency) |
| 16 | Gamma Par(USD) | American | 16,2 | No | IR Gamma Par (USD) |
| 17 | act. Notional | American | 25,8 | No | Bond notional amount |
| 18 | Evaluation(Bond) | VarChar | 50 | No | Bond evaluation mode |
| 19 | ZAR_PROCESSING | VarChar | 1 | No | ZAR processing flag (Y/N) |
| 20 | Delta Par(ZAR) | American | 12,2 | No | IR Delta Par (ZAR) - Deprecated |
| 21 | Gamma Par(ZAR) | American | 16,2 | No | IR Gamma Par (ZAR) - Deprecated |
| 22 | Typology | VarChar | 21 | Yes | Product typology |
| 23 | Curve_Spread | VarChar | 1 | No | Curve spread flag (Y/N) |
| 24 | Convexity_Spread | VarChar | 1 | No | Convexity spread flag (Y/N) |
| 25 | RBC_FMLY | VarChar | 20 | Yes | Risk Basket Family (blank) |
| 26 | RBC_GRP | VarChar | 20 | Yes | Risk Basket Group (blank) |
| 27 | RBC_TYPE | VarChar | 20 | Yes | Risk Basket Type (blank) |
| 28 | RBC_INSTRUMENT | VarChar | 50 | Yes | Risk Basket Instrument (blank) |

### 3.2 Field Details

#### 3.2.1 PORTFOLIO

| Property | Value |
|----------|-------|
| **Field** | PORTFOLIO |
| **Type** | VarChar |
| **Length** | 16 |
| **Description** | Trading portfolio or book code |
| **Source** | MDS_IRPV01TTL.Portfolio |
| **Example** | PMLNSBPDSF, LMLNSBL |

#### 3.2.2 Family

| Property | Value |
|----------|-------|
| **Field** | Family |
| **Type** | VarChar |
| **Length** | 16 |
| **Description** | Product family in Murex hierarchy |
| **Source** | MDS_IRPV01TTL.Family |
| **Example** | IRD, FXD, COM |

#### 3.2.3 Group

| Property | Value |
|----------|-------|
| **Field** | Group |
| **Type** | VarChar |
| **Length** | 5 |
| **Description** | Product group in Murex hierarchy |
| **Source** | MDS_IRPV01TTL.Group |
| **Example** | SWAP, CF, OSWP, SPOT |

#### 3.2.4 Type

| Property | Value |
|----------|-------|
| **Field** | Type |
| **Type** | VarChar |
| **Length** | 16 |
| **Description** | Product type in Murex hierarchy |
| **Source** | MDS_IRPV01TTL.Type |
| **Example** | IRS, CAP, FLOOR, SWAPTION |

#### 3.2.5 Instrument

| Property | Value |
|----------|-------|
| **Field** | Instrument |
| **Type** | VarChar |
| **Length** | 50 |
| **Description** | P&L instrument name |
| **Source** | MDS_IRPV01TTL.PL Instrument |
| **Example** | XPD, EUR/USD |

#### 3.2.6 Sec_code

| Property | Value |
|----------|-------|
| **Field** | Sec_code |
| **Type** | VarChar |
| **Length** | 16 |
| **Description** | Security code for bonds and structured products |
| **Source** | MDS_IRPV01TTL.Sec Code |
| **Example** | GB0001234567 |

#### 3.2.7 Trade Number

| Property | Value |
|----------|-------|
| **Field** | Trade Number |
| **Type** | Numeric |
| **Length** | 16 |
| **Description** | Unique Murex trade identifier. Set to 0 for DEAD status trades |
| **Source** | MDS_IRPV01TTL.Trade Number |
| **Example** | 28249787 |

#### 3.2.8 CURRENCY

| Property | Value |
|----------|-------|
| **Field** | CURRENCY |
| **Type** | VarChar |
| **Length** | 4 |
| **Description** | Interest rate curve currency. For Bonds, uses Sec Currency |
| **Source** | MDS_IRPV01TTL.Currency / Sec Currency |
| **Example** | USD, EUR, GBP |

#### 3.2.9 CURVE_NAM

| Property | Value |
|----------|-------|
| **Field** | CURVE_NAM |
| **Type** | VarChar |
| **Length** | 35 |
| **Description** | Interest rate curve name for sensitivity calculation |
| **Source** | MDS_IRPV01TTL.Curve Name |
| **Example** | USD_SOFR_ANFUTS, EUR_ESTR |

#### 3.2.10 CurveType

| Property | Value |
|----------|-------|
| **Field** | CurveType |
| **Type** | VarChar |
| **Length** | 10 |
| **Description** | Type of rate curve generator. Defaults to 'Bond' if null |
| **Source** | A_RTCT_REP.M_TYPE |
| **Example** | Swap, Bond, Basis swap |

#### 3.2.11 Generat

| Property | Value |
|----------|-------|
| **Field** | Generat |
| **Type** | VarChar |
| **Length** | 10 |
| **Description** | Generator instrument name for the pillar |
| **Source** | MDS_IRPV01TTL.Generator |
| **Example** | USD SOFR, EUR ESTR |

#### 3.2.12 DATE

| Property | Value |
|----------|-------|
| **Field** | DATE |
| **Type** | VarChar |
| **Length** | 64 |
| **Description** | Maturity pillar date from LNOFFICIAL maturity set |
| **Source** | MDS_IRPV01TTL.Date |
| **Format** | Label (e.g., 1M, 6M, 1Y) or date |
| **Example** | 1M, 6M, 1Y, 10Y |

#### 3.2.13 Delta Par

| Property | Value |
|----------|-------|
| **Field** | Delta Par |
| **Type** | American (Numeric) |
| **Length** | 16,2 |
| **Description** | IR Par Delta sensitivity in native currency. Change in NPV per 1bp parallel shift in par yield curve |
| **Source** | MDS_IRPV01TTL.DV01(par) |
| **Example** | -142.24 |

#### 3.2.14 Delta Par(USD)

| Property | Value |
|----------|-------|
| **Field** | Delta Par(USD) |
| **Type** | American (Numeric) |
| **Length** | 16,2 |
| **Description** | IR Par Delta sensitivity converted to USD using zero day FX spot rate |
| **Source** | MDS_IRPV01TTL.DV01(par) USD |
| **Example** | -142.24 |

#### 3.2.15 Gamma Par

| Property | Value |
|----------|-------|
| **Field** | Gamma Par |
| **Type** | American (Numeric) |
| **Length** | 16,2 |
| **Description** | IR Par Gamma (convexity) in native currency. Set to 0 if no Gamma match (non-options) |
| **Source** | IRPV02_GAMMAS.GAMMA_PAR_CCY |
| **Example** | 0.00 |

#### 3.2.16 Gamma Par(USD)

| Property | Value |
|----------|-------|
| **Field** | Gamma Par(USD) |
| **Type** | American (Numeric) |
| **Length** | 16,2 |
| **Description** | IR Par Gamma converted to USD. Set to 0 if no Gamma match |
| **Source** | IRPV02_GAMMAS.GAMMA_PAR_USD |
| **Example** | 0.00 |

#### 3.2.17 act. Notional

| Property | Value |
|----------|-------|
| **Field** | act. Notional |
| **Type** | American (Numeric) |
| **Length** | 25,8 |
| **Description** | Bond notional amount. 0 for non-bond trades |
| **Source** | A_BOND_NOTIONAL.REP.M_TP_RTCCP02 or calculated |
| **Logic** | BOND: M_TP_RTCCP02, RTRN: M_TP_RTCAPI0 * M_TP_SECLOT, else: 0 |
| **Example** | 0.00000000, 1000000.00000000 |

#### 3.2.18 Evaluation(Bond)

| Property | Value |
|----------|-------|
| **Field** | Evaluation(Bond) |
| **Type** | VarChar |
| **Description** | Bond evaluation mode. 'XXX' for non-bond/RTRN trades |
| **Source** | TBL_BOND_MKTDATA_REP.M_EVAL_MODE |
| **Values** | XXX, Zero coupon spread, Mark to Market, Yield spread, etc. |
| **Example** | XXX |

#### 3.2.19 ZAR_PROCESSING

| Property | Value |
|----------|-------|
| **Field** | ZAR_PROCESSING |
| **Type** | VarChar |
| **Length** | 1 |
| **Description** | Flag indicating ZAR processing based on Closing Entity. **DEPRECATED** |
| **Source** | MDS_IRPV01TTL.Closing Entity |
| **Logic** | 'Y' if Closing Entity = 'JBSBSA', else 'N' |
| **Example** | N |

#### 3.2.20 Delta Par(ZAR)

| Property | Value |
|----------|-------|
| **Field** | Delta Par(ZAR) |
| **Type** | American (Numeric) |
| **Length** | 12,2 |
| **Description** | IR Par Delta in ZAR. **DEPRECATED - for backward compatibility only** |
| **Source** | MDS_IRPV01TTL.DV01(par) ZAR |
| **Example** | -2507.95 |

#### 3.2.21 Gamma Par(ZAR)

| Property | Value |
|----------|-------|
| **Field** | Gamma Par(ZAR) |
| **Type** | American (Numeric) |
| **Length** | 16,2 |
| **Description** | IR Par Gamma in ZAR. **DEPRECATED - for backward compatibility only** |
| **Source** | IRPV02_GAMMAS.GAMMA_PAR_ZAR |
| **Example** | 0.00 |

#### 3.2.22 Typology

| Property | Value |
|----------|-------|
| **Field** | Typology |
| **Type** | VarChar |
| **Length** | 21 |
| **Description** | Product typology classification |
| **Source** | MDS_IRPV01TTL.Typology |
| **Example** | PM - FWD UA, IRS - FIXED FLOAT |

#### 3.2.23 Curve_Spread

| Property | Value |
|----------|-------|
| **Field** | Curve_Spread |
| **Type** | VarChar |
| **Length** | 1 |
| **Description** | Flag indicating if the curve pillar has a spread |
| **Source** | A_RTCT_REP.M_BID_S |
| **Logic** | 'N' if M_BID_S is null or Group is FUTURE, else 'Y' |
| **Example** | N |

#### 3.2.24 Convexity_Spread

| Property | Value |
|----------|-------|
| **Field** | Convexity_Spread |
| **Type** | VarChar |
| **Length** | 1 |
| **Description** | Flag indicating if the curve has a convexity spread |
| **Source** | A_RATES_REP.M_S_BID1 |
| **Logic** | 'N' if M_S_BID1 is null or Group is FUTURE, else 'Y' |
| **Example** | N |

#### 3.2.25-28 RBC Fields

| Property | Value |
|----------|-------|
| **Fields** | RBC_FMLY, RBC_GRP, RBC_TYPE, RBC_INSTRUMENT |
| **Type** | VarChar |
| **Description** | Risk Basket Composition fields - placeholders set to blank |
| **Source** | Set at extraction level |
| **Value** | '' (empty string) |

---

## 4. Data Validation Rules

### 4.1 Mandatory Field Validation

| Field | Rule | Severity |
|-------|------|----------|
| PORTFOLIO | Not null, not empty | Error |
| Trade Number | Not null (0 for DEAD) | Error |
| CURRENCY | Not null, valid ISO code | Error |
| CURVE_NAM | Not null | Error |
| DATE | Not null, valid pillar | Error |
| Delta Par | Not null, numeric | Error |
| Delta Par(USD) | Not null, numeric | Error |

### 4.2 Business Rule Validation

| Rule ID | Rule | Action |
|---------|------|--------|
| VAL-PDG-001 | At least one of Delta Par or Gamma Par must be non-zero | Exclude record |
| VAL-PDG-002 | Legal Entity must not be 'SBSA' | Exclude record |
| VAL-PDG-003 | DATE must be a valid LNOFFICIAL pillar | Warning |
| VAL-PDG-004 | CURVE_NAM must exist in curve inventory | Warning |
| VAL-PDG-005 | Trade Number must be positive or 0 (for DEAD) | Error |

### 4.3 Referential Integrity

| Source Field | Reference Table | Reference Field |
|--------------|-----------------|-----------------|
| CURVE_NAM | A_CURVENAME_REP | M_LABEL |
| Trade Number | TRN_HDR | M_NB |
| PORTFOLIO | PTF_REP | M_LABEL |

---

## 5. Sample Data

### 5.1 Header Row

```
PORTFOLIO;Family;Group;Type;Instrument;Sec_code;Trade Number;CURRENCY;CURVE_NAM;CurveType;Generat;DATE;Delta Par;Delta Par(USD);Gamma Par;Gamma Par(USD);act. Notional;Evaluation(Bond);ZAR_PROCESSING;Delta Par(ZAR);Gamma Par(ZAR);Typology;Curve_Spread;Convexity_Spread;RBC_FMLY;RBC_GRP;RBC_TYPE;RBC_INSTRUMENT
```

### 5.2 Sample Data Rows

```
PMLNSBPDSF;COM;SPOT;;XPD;;28249787;USD;USD_SOFR_ANFUTS;Swap;USD SOFR;1M;0.00;0.00;0.00;0.00;0.00000000;XXX;N;-0.01;0.00;PM - FWD UA;N;N;;;;
PMLNSBPDSF;COM;SPOT;;XPD;;28249787;USD;USD_SOFR_ANFUTS;Swap;USD SOFR;6M;1.17;1.17;0.00;0.00;0.00000000;XXX;N;20.69;0.00;PM - FWD UA;N;N;;;;
PMLNSBPDSF;COM;SPOT;;XPD;;27993236;USD;USD_SOFR_ANFUTS;Swap;USD SOFR;15M;-142.24;-142.24;0.00;0.00;0.00000000;XXX;N;-2507.95;0.00;PM - FWD UA;N;N;;;;
LMLNSBL;IRD;OSWP;SWAPTION;EUR IRS;;28112456;EUR;EUR_ESTR;Swap;EUR ESTR;5Y;523.45;567.89;12.34;13.38;0.00000000;XXX;N;9231.02;217.50;IRS - SWAPTION;Y;Y;;;;
```

### 5.3 Record Count by Region (Typical Day)

| Region | Approximate Records |
|--------|---------------------|
| LDN | 150,000 - 250,000 |
| HKG | 30,000 - 50,000 |
| NYK | 50,000 - 80,000 |
| SAO | 10,000 - 20,000 |

---

## 6. Delivery Specification

### 6.1 File Packaging

| Property | Value |
|----------|-------|
| **Package Format** | ZIP |
| **Package Pattern** | `MxMGB_MR_Sensitivities_{Region}_{YYYYMMDD}.zip` |
| **Compression** | Standard ZIP |
| **Contents** | PDG file + other market risk sensitivity reports |

### 6.2 Delivery Mechanism

| Property | Value |
|----------|-------|
| **Method** | Managed File Transfer (MFT) |
| **Protocol** | SFTP |
| **Encryption** | In transit via TLS |

### 6.3 MFT Transfer IDs

| Target | MFT ID Pattern |
|--------|---------------|
| Plato | MurexMGBSensitivitiesToPlato_{Region} |
| RDS | MurexMGBSensitivitiesToRDS_{Region} |

### 6.4 Delivery Paths

| Target | Path |
|--------|------|
| Plato | /incoming/murex/sensitivities/ |
| RDS | /feeds/market_risk/pdg/ |

---

## 7. Processing Schedule

### 7.1 Daily Timeline

| Time (GMT) | Event | System |
|------------|-------|--------|
| 18:00 | Market data close | Market Data |
| 21:00 | Valuation batch complete | Murex |
| 02:00 | IR Delta feeder start | Murex |
| 02:30 | IR Gamma feeder start | Murex |
| 03:30 | All feeders complete | Murex |
| 04:00 | Extraction start | Murex |
| 04:30 | File generation | Murex |
| 05:00 | File packaging | Murex |
| 05:30 | MFT delivery to targets | MFT |
| 06:00 | Target system pickup | Plato/RDS |

### 7.2 Regional Timing

| Region | Feeder Start | Extraction | Delivery |
|--------|--------------|------------|----------|
| LDN | 02:00 GMT | 04:00 GMT | 05:30 GMT |
| HKG | 14:00 HKT | 16:00 HKT | 17:30 HKT |
| NYK | 21:00 EST | 23:00 EST | 00:30 EST |
| SAO | 23:00 BRT | 01:00 BRT | 02:30 BRT |

---

## 8. Error Handling

### 8.1 File-Level Errors

| Error | Detection | Action |
|-------|-----------|--------|
| Empty file | Record count = 0 | Alert, do not deliver |
| File generation failure | No file created | Retry, escalate |
| Invalid file format | Header mismatch | Reject, escalate |
| Truncated file | Unexpected EOF | Reject, retry |

### 8.2 Record-Level Errors

| Error | Detection | Action |
|-------|-----------|--------|
| Missing mandatory field | Null check | Reject record, log |
| Invalid data type | Type validation | Reject record, log |
| Business rule violation | Rule validation | Exclude record, log |
| Referential integrity failure | Lookup failure | Warning, continue |

### 8.3 Delivery Errors

| Error | Detection | Action |
|-------|-----------|--------|
| MFT connection failure | Connection timeout | Retry (3 attempts) |
| Authentication failure | Auth error code | Alert, escalate |
| Transfer timeout | Transfer incomplete | Retry, escalate |
| Target system unavailable | No acknowledgment | Queue, retry |

---

## 9. Reconciliation

### 9.1 Daily Reconciliation Checks

| Check | Source | Target | Tolerance |
|-------|--------|--------|-----------|
| Record count | Murex extraction log | File record count | ±5% |
| Sum of Delta Par(USD) | Murex valuation | File total | ±$10,000 |
| Trade coverage | Murex position inventory | Unique trade count | 100% |
| Portfolio coverage | Portfolio list | Unique portfolios | 100% |

### 9.2 Reconciliation Report

| Report | Frequency | Recipients |
|--------|-----------|------------|
| Daily Reconciliation Summary | Daily | Risk Technology, Product Control |
| Break Report | Daily (if breaks) | Risk Operations |
| Monthly Trend Report | Monthly | Risk Technology Management |

---

## 10. Data Quality Metrics

### 10.1 Completeness Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Feed delivery rate | 99.5% | Deliveries / Business days |
| Record completeness | 99.9% | Non-null mandatory fields |
| Trade coverage | 100% | Trades with sensitivity / Live trades |

### 10.2 Accuracy Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Delta Par accuracy | ±0.01% | Sample validation vs front office |
| Gamma Par accuracy | ±0.1% | Sample validation vs front office |
| Currency accuracy | 100% | Valid ISO codes |

### 10.3 Timeliness Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| On-time delivery | 95% | Delivery by 05:30 GMT |
| Average delivery time | <5:30 GMT | Median delivery timestamp |
| Maximum delay | <30 minutes | 95th percentile delay |

---

## 11. Change Management

### 11.1 Interface Change Process

| Change Type | Approval Required | Lead Time |
|-------------|-------------------|-----------|
| New field addition | Risk Technology Change Board | 4 weeks |
| Field format change | Risk Technology + Product Control | 2 weeks |
| Delivery time change | Operations Committee | 2 weeks |
| File format change | All stakeholders | 6 weeks |

### 11.2 Version History

| Version | Date | Change | Impact |
|---------|------|--------|--------|
| 1.0 | 2025-01-03 | Initial version | New interface |

---

## 12. Contacts

### 12.1 Technical Contacts

| Role | Team | Responsibility |
|------|------|----------------|
| Source System Support | Murex Support | Feed generation issues |
| MFT Operations | IT Operations | Transfer issues |
| Target System Support | Plato/RDS Team | Loading issues |

### 12.2 Business Contacts

| Role | Team | Responsibility |
|------|------|----------------|
| Data Owner | Product Control | Data requirements |
| Data Quality | Risk Operations | Reconciliation |
| Change Management | Risk Technology | Interface changes |

---

## 13. Appendix

### 13.1 Glossary

| Term | Definition |
|------|------------|
| DV01 | Dollar Value of 1 basis point - sensitivity to 1bp rate change |
| Par Rate | Quoted market rate (e.g., swap rate) vs derived zero rate |
| Gamma | Second derivative - convexity or rate of change of delta |
| STB | Structured Bond - complex bond structure with embedded components |
| RBC | Risk Basket Composition - breakdown of structured product risk |

### 13.2 Related Documents

| Document | ID | Description |
|----------|-----|-------------|
| IR PDG Overview | PDG-OVW-001 | Feed overview |
| IR PDG BRD | PDG-BRD-001 | Business requirements |
| IR PDG IT Config | PDG-CFG-001 | Murex configuration |
| Data Dictionary | MR-L7-002 | Field definitions |

---

## 14. Document Control

### 14.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-03 | Initial version | Risk Technology |

### 14.2 Approval

| Role | Name | Date |
|------|------|------|
| Business Owner | Head of Product Control | |
| Technical Owner | Head of Risk Technology | |
| Approver | Risk Technology Change Board | |

---

*End of Document*
