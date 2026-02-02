# FX Vega Sensitivities - Interface Design Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | FXV-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Interface Overview

### 1.1 Interface Summary

| Attribute | Value |
|-----------|-------|
| **Interface Name** | FX Vega Sensitivities (Strike & Maturity) |
| **Interface ID** | MR-IF-FXV |
| **Direction** | Outbound |
| **Source System** | Murex |
| **Target Systems** | Plato, RDS |
| **Frequency** | Daily |
| **Transfer Method** | MFT (Managed File Transfer) |

---

## 2. File Specification

### 2.1 File Details

| Attribute | Value |
|-----------|-------|
| **File Format** | CSV |
| **Delimiter** | Semicolon (;) |
| **Character Encoding** | UTF-8 |
| **Header Row** | Yes |
| **Trailer Row** | No |
| **Record Terminator** | LF |
| **Decimal Separator** | Period (.) |

### 2.2 File Naming Convention

```
MxGTS_Vespa_FX_Vega_StkMat_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Values |
|-----------|-------------|--------|
| MxGTS | Murex GTS prefix | Fixed |
| Vespa | VESPA platform | Fixed |
| FX_Vega_StkMat | FX Vega Strike & Maturity | Fixed |
| {Region} | Trading region | LN, HK, NY, SP |
| {YYYYMMDD} | Business date | Date format |

### 2.3 Package Details

| Attribute | Value |
|-----------|-------|
| **Package Format** | ZIP |
| **Package Pattern** | MxGTS_Vespa_Sensitivities_{Region}_{YYYYMMDD}.zip |
| **Contents** | Multiple sensitivity feeds including FX Vega |
| **Packaging Script** | process_reports.sh |

---

## 3. Field Specification

### 3.1 Field Layout (11 Fields)

| # | Field Name | Description | Type | Length | Mandatory | Source |
|---|------------|-------------|------|--------|-----------|--------|
| 1 | PORTFOLIO | Portfolio code | VarChar | 16 | Yes | FX_VEGA_MATURITY |
| 2 | TRADE_NUMBER | Trade ID | Numeric | 10 | Yes | FX_VEGA_MATURITY |
| 3 | INSTRUMENT | Instrument label | VarChar | 16 | Yes | FX_VEGA_MATURITY |
| 4 | INSTRUMENT_TYPE | Standardized type | VarChar | 12 | Yes | Derived |
| 5 | LEV_QOT | Quotation currency | VarChar | 4 | Yes | TBL_FX_CNT_REP |
| 6 | CP | Call/Put/ATM flag | VarChar | 4 | Yes | Derived |
| 7 | PILLAR | Vega maturity pillar | VarChar | 64 | Yes | FX_VEGA_MATURITY |
| 8 | ENDDATE | Vega date | Date | 12 | Yes | FX_VEGA_MATURITY |
| 9 | VEGASTK | Vega strike | Numeric | 10 | Yes | FX_VEGA_MATURITY |
| 10 | VEGA | FX Vega in USD | Numeric | 12 | Yes | FX_VEGA_MATURITY |
| 11 | CCY | Currency of vega | VarChar | 4 | Yes | Fixed (USD) |

### 3.2 Field Details

#### Field 1: PORTFOLIO
| Attribute | Value |
|-----------|-------|
| **Description** | Trading book portfolio code |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | PORTFOLIO from simulation view FX_VEGA_MATURITY |
| **Example** | CTLNSBLEQLOA |

#### Field 2: TRADE_NUMBER
| Attribute | Value |
|-----------|-------|
| **Description** | Unique trade identifier |
| **Data Type** | Numeric |
| **Length** | 10 |
| **Mandatory** | Yes |
| **Source** | TRADE_NUM from simulation view FX_VEGA_MATURITY |
| **Example** | 27556022 |

#### Field 3: INSTRUMENT
| Attribute | Value |
|-----------|-------|
| **Description** | Label of the instrument being evaluated |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | INSTRUMENT from simulation view FX_VEGA_MATURITY |
| **Valid Values** | Quanto Forward Swap, QFX Range Accrual |
| **Example** | USD/JPY |

#### Field 4: INSTRUMENT_TYPE
| Attribute | Value |
|-----------|-------|
| **Description** | Standardized instrument type code (family/group/type) |
| **Data Type** | VarChar |
| **Length** | 12 |
| **Mandatory** | Yes |
| **Source** | Derived at extraction level via CASE statement |
| **Business Rule** | Maps Murex instrument labels to standard codes |
| **Example** | IRD_IRS_FX, IRD_IRS_RA |

**Mapping Rules**:
| Murex Instrument | Mapped Type |
|------------------|-------------|
| QFX Range Accrua | IRD_IRS_RA |
| Quanto Forward S | IRD_IRS_FX |
| QIR Range Accrua | IRD_IRS_RA |
| Insurance Instru | CRD_CDS_INS |
| Guarantee Instru | CRD_CDS_GUA |
| Other | (empty) |

#### Field 5: LEV_QOT
| Attribute | Value |
|-----------|-------|
| **Description** | First currency of the default spot quotation mode |
| **Data Type** | VarChar |
| **Length** | 4 |
| **Mandatory** | Yes |
| **Source** | First 3 characters of M_QUOTMODE0 from TBL_FX_CNT_REP based on LABEL from FX_VEGA_MATURITY |
| **Typical Values** | USD, JPY |
| **Example** | USD |

#### Field 6: CP
| Attribute | Value |
|-----------|-------|
| **Description** | Call/Put/ATM flag based on vega strike |
| **Data Type** | VarChar |
| **Length** | 4 |
| **Mandatory** | Yes |
| **Source** | Derived at extraction level from VEGA_STK |
| **Business Rule** | Strike < 50 = Call, Strike = 50 = ATM, Strike > 50 = Put |
| **Valid Values** | Call, Put, ATM |
| **Example** | Call, ATM, Put |

#### Field 7: PILLAR
| Attribute | Value |
|-----------|-------|
| **Description** | Vega maturity pillar from RISK_VIEW4 set |
| **Data Type** | VarChar |
| **Length** | 64 |
| **Mandatory** | Yes |
| **Source** | VEGA_MAT from simulation view FX_VEGA_MATURITY |
| **Valid Values** | O/N, T/N, 1W, 2W, 1M, 2M, 3M, 6M, 9M, 1Y, 18M, 2Y, 3Y, 4Y, 5Y, 6Y, 7Y, 8Y, 9Y, 10Y, 12Y, 15Y, 20Y, 25Y, 30Y, 35Y |
| **Example** | 3M |

#### Field 8: ENDDATE
| Attribute | Value |
|-----------|-------|
| **Description** | Vega date (date at which volatility is interpolated) |
| **Data Type** | Date |
| **Length** | 12 |
| **Format** | YYYY-MM-DD |
| **Mandatory** | Yes |
| **Source** | VEGA_MATD from simulation view FX_VEGA_MATURITY, formatted at extraction |
| **Example** | 03/04/2023 |

#### Field 9: VEGASTK
| Attribute | Value |
|-----------|-------|
| **Description** | Vega strike level (delta of the option) |
| **Data Type** | Numeric |
| **Length** | 10 |
| **Mandatory** | Yes |
| **Source** | VEGA_STK from simulation view FX_VEGA_MATURITY |
| **Valid Values** | 0, 5, 10, 25, 50, 75, 90, 95, 100 |
| **Business Rule** | Must be > 0 (filtered in WHERE clause) |
| **Example** | 5, 10, 25, 50, 75, 90 |

#### Field 10: VEGA
| Attribute | Value |
|-----------|-------|
| **Description** | FX Vega sensitivity in USD |
| **Data Type** | Numeric |
| **Length** | 12 |
| **Precision** | 2 decimal places |
| **Mandatory** | Yes |
| **Source** | VEGA_USD from simulation view FX_VEGA_MATURITY |
| **Definition** | Change in market value for 1% move in FX volatility. Discounted from settlement date to today. |
| **Example** | -36.14, 65.57, -104.76 |

#### Field 11: CCY
| Attribute | Value |
|-----------|-------|
| **Description** | Currency of the FX Vega |
| **Data Type** | VarChar |
| **Length** | 4 |
| **Mandatory** | Yes |
| **Source** | Fixed at extraction level |
| **Value** | USD |
| **Example** | USD |

---

## 4. Sample Data

### 4.1 Header Row
```
PORTFOLIO;TRADE_NUMBER;INSTRUMENT;INSTRUMENT_TYPE;LEV_QOT;CP;PILLAR;ENDDATE;VEGASTK;VEGA;CCY
```

### 4.2 Sample Records

```csv
CTLNSBLEQLOA;27556022;USD/JPY;IRD_IRS_FX;USD;Call;3M;03/04/2023;5;-36.14;USD
CTLNSBLEQLOA;27556022;USD/JPY;IRD_IRS_FX;USD;Call;3M;03/04/2023;10;-25.82;USD
CTLNSBLEQLOA;27556022;USD/JPY;IRD_IRS_FX;USD;Call;3M;03/04/2023;25;-89.02;USD
CTLNSBLEQLOA;27556022;USD/JPY;IRD_IRS_FX;USD;ATM;3M;03/04/2023;50;65.57;USD
CTLNSBLEQLOA;27556022;USD/JPY;IRD_IRS_FX;USD;Put;3M;03/04/2023;75;-104.76;USD
CTLNSBLEQLOA;27556022;USD/JPY;IRD_IRS_FX;USD;Put;3M;03/04/2023;90;-70.39;USD
```

**Note**: A single trade may have multiple records representing different strike levels on the volatility surface. Each strike level captures the vega exposure at that point.

---

## 5. Data Quality Rules

### 5.1 Validation Rules

| Rule ID | Field | Rule | Severity | Action |
|---------|-------|------|----------|--------|
| DQ-FXV-001 | TRADE_NUMBER | Must be numeric | Critical | Reject |
| DQ-FXV-002 | PORTFOLIO | Must not be null | Critical | Reject |
| DQ-FXV-003 | PILLAR | Must be valid pillar from RISK_VIEW4 | High | Warning |
| DQ-FXV-004 | VEGA | Must be numeric | Critical | Reject |
| DQ-FXV-005 | VEGASTK | Must be > 0 | High | Exclude |
| DQ-FXV-006 | CP | Must be Call, Put, or ATM | High | Warning |
| DQ-FXV-007 | CCY | Must be USD | High | Warning |
| DQ-FXV-008 | ENDDATE | Must be valid date | High | Warning |

### 5.2 Completeness Checks

| Check | Description | Threshold |
|-------|-------------|-----------|
| Record Count | Day-over-day variance | ±15% |
| Portfolio Coverage | All FX-sensitive portfolios | 100% |
| Strike Coverage | All standard strike levels | Monitor |
| Pillar Coverage | All relevant maturity pillars | Monitor |
| Zero Vega Count | Records with VEGA = 0 | Monitor trend |

---

## 6. Interface Dependencies

### 6.1 Upstream Dependencies

| System | Data | Timing | Impact if Delayed |
|--------|------|--------|-------------------|
| Market Data | FX volatility surfaces | 18:00 GMT | Vega calculation fails |
| Market Data | FX spot rates | 18:00 GMT | USD conversion fails |
| Valuation Batch | FX vega calculations | 21:00 GMT | Feed cannot run |
| Reference Data | TBL_FX_CNT_REP | Static | Quotation mode lookup fails |

### 6.2 Downstream Consumers

| System | Purpose | Frequency |
|--------|---------|-----------|
| Plato | Risk aggregation | Daily |
| RDS | Risk data store | Daily |
| VaR Engine | Risk calculation | Daily |
| Limit System | FX vega position limits | Daily |

---

## 7. Delivery Specification

### 7.1 Transfer Details

| Attribute | Value |
|-----------|-------|
| **Method** | Managed File Transfer (MFT) |
| **Protocol** | SFTP |
| **Directory** | ./reports/today/eod |
| **Retention** | 30 days |

### 7.2 MFT Configuration

| Region | Plato MFT ID | RDS MFT ID |
|--------|--------------|------------|
| LDN | MurexGTSSensitivitiesToPlato_LN | MurexGTSSensitivitiesToRDS_LN |
| HKG | MurexGTSSensitivitiesToPlato_HK | MurexGTSSensitivitiesToRDS_HK |
| NYK | MurexGTSSensitivitiesToPlato_NY | MurexGTSSensitivitiesToRDS_NY |
| SAO | MurexGTSSensitivitiesToPlato_SP | MurexGTSSensitivitiesToRDS_SP |

### 7.3 Delivery Schedule

| Region | Target Time (GMT) | SLA |
|--------|-------------------|-----|
| LDN | 05:30 | 95% |
| HKG | 05:30 | 95% |
| NYK | 05:30 | 95% |
| SAO | 05:30 | 95% |

---

## 8. Error Handling

### 8.1 Error Scenarios

| Scenario | Detection | Action | Escalation |
|----------|-----------|--------|------------|
| File not generated | Monitoring | Alert | Risk Tech L2 |
| Zero records | File check | Warning | Risk Ops |
| Late delivery | SLA tracking | Alert | Risk Tech L1 |
| MFT failure | Transfer log | Retry 3x | MFT Ops |
| Data quality breach | DQ rules | Alert | Risk Control |

### 8.2 Retry Policy

| Failure Type | Retry Count | Retry Interval | Final Action |
|--------------|-------------|----------------|--------------|
| MFT failure | 3 | 15 minutes | Manual escalation |
| Extraction failure | 1 | 30 minutes | Abort and alert |

---

## 9. Reconciliation

### 9.1 Daily Reconciliation

| Check | Source | Target | Tolerance |
|-------|--------|--------|-----------|
| Total FX Vega USD | Murex | Feed | ±$1,000 |
| Record Count | Murex | Feed | ±5% |
| Trade Count | Murex | Feed | 100% |
| Portfolio Count | Reference | Feed | 100% |

### 9.2 Reconciliation Contacts

| Role | Team | Responsibility |
|------|------|----------------|
| First Line | Risk Ops | Daily checks |
| Second Line | Risk Control | Break investigation |
| Technical | Risk Tech | System issues |

---

## 10. Change History

| Version | Date | Author | Change Description |
|---------|------|--------|-------------------|
| 1.0 | 2025-01-13 | Risk Technology | Initial document |

---

## Appendix A: Vega Strike Level Reference

### Strike Level Interpretation

| Strike Level | Delta | Option Type | Description |
|--------------|-------|-------------|-------------|
| 5 | 5-delta | Deep OTM Call | Far out-of-the-money call |
| 10 | 10-delta | OTM Call | Out-of-the-money call |
| 25 | 25-delta | OTM Call | Out-of-the-money call |
| 50 | 50-delta | ATM | At-the-money |
| 75 | 75-delta | OTM Put | Out-of-the-money put (25-delta put) |
| 90 | 90-delta | OTM Put | Out-of-the-money put (10-delta put) |
| 95 | 95-delta | Deep OTM Put | Far out-of-the-money put |

### Volatility Surface Coverage

The feed captures vega exposures across the FX volatility surface:
- **Maturity dimension**: 26 pillars from O/N to 35Y
- **Strike dimension**: Multiple delta levels from 5 to 95

---

## Appendix B: Maturity Pillar Reference

### RISK_VIEW4 Pillar Set

| Label | Example Date (Ref: 13 Jun 2023) |
|-------|--------------------------------|
| O/N | 14 Jun 2023 |
| T/N | 15 Jun 2023 |
| 1W | 20 Jun 2023 |
| 2W | 27 Jun 2023 |
| 1M | 13 Jul 2023 |
| 2M | 13 Aug 2023 |
| 3M | 13 Sep 2023 |
| 6M | 13 Dec 2023 |
| 9M | 13 Mar 2024 |
| 1Y | 13 Jun 2024 |
| 18M | 13 Dec 2024 |
| 2Y | 13 Jun 2025 |
| 3Y | 13 Jun 2026 |
| 4Y | 13 Jun 2027 |
| 5Y | 13 Jun 2028 |
| ... | ... |
| 35Y | 13 Jun 2058 |

Pillar dates are computed dynamically from the reference date of the environment.

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
