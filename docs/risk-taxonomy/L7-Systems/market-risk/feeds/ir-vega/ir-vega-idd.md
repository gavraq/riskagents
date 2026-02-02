---
# Document Metadata
document_id: IRV-IDD-001
document_name: IR Vega Sensitivities - Interface Design Document
version: 1.0
effective_date: 2025-01-13
next_review_date: 2026-01-13
owner: Market Risk Technology
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds/ir-vega
feed_family: IR Vega
document_type: IDD
---

# IR Vega Sensitivities - Interface Design Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | IRV-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Interface Overview

### 1.1 Interface Summary

| Attribute | Value |
|-----------|-------|
| **Interface Name** | IR Vega Sensitivities |
| **Interface ID** | MR-IF-IRV |
| **Direction** | Outbound |
| **Source System** | Murex |
| **Target Systems** | Plato, RDS |
| **Frequency** | Daily |
| **Transfer Method** | MFT (Managed File Transfer) |

### 1.2 Interface Scope

This interface provides trade-level interest rate volatility sensitivities (Vega) for option products, including:
- Swaptions
- Caps and Floors
- CRD Guarantees and Insurance
- Range Accruals with embedded optionality

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
MxMGB_MR_Rates_Vega_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Values |
|-----------|-------------|--------|
| MxMGB | Murex Meridian Global Bank prefix | Fixed |
| MR | Market Risk | Fixed |
| Rates | Asset class | Fixed |
| Vega | Sensitivity type | Fixed |
| {Region} | Trading region | LN, HK, NY, SP |
| {YYYYMMDD} | Business date | Date format |

### 2.3 Package Details

| Attribute | Value |
|-----------|-------|
| **Package Format** | ZIP |
| **Package Pattern** | MxGTS_Vespa_Sensitivities_{Region}_{YYYYMMDD}.zip |
| **Contents** | Multiple sensitivity feeds including IR Vega |
| **Compression** | Standard ZIP |

---

## 3. Field Specification

### 3.1 Field Layout (20 Fields)

| # | Field Name | Description | Type | Length | Mandatory | Source |
|---|------------|-------------|------|--------|-----------|--------|
| 1 | TRADE_NUM | Trade ID | Numeric | 16 | Yes | IRPV01_VEGAS |
| 2 | CURRENCY local | Currency of IR Vega | VarChar | 4 | Yes | Derived |
| 3 | FAMILY | Deal Family | VarChar | 16 | Yes | IRPV01_VEGAS |
| 4 | GROUP | Deal Group | VarChar | 5 | Yes | IRPV01_VEGAS |
| 5 | TYPE | Deal Type | VarChar | 16 | Yes | IRPV01_VEGAS |
| 6 | Category | Category | VarChar | 3 | No | Dynamic Table |
| 7 | Portfolio | Deal portfolio | VarChar | 16 | Yes | IRPV01_VEGAS |
| 8 | Profit Centre | Profit centre | VarChar | 20 | Yes | A_IR_VEGA.REP |
| 9 | Option Maturity | Option maturity pillar | VarChar | 15 | Yes | IRPV01_VEGAS |
| 10 | Option Maturity Date | Option maturity date | Date | 8 | Yes | IRPV01_VEGAS |
| 11 | Underl Maturity | Underlying maturity pillar | VarChar | 64 | Yes | IRPV01_VEGAS |
| 12 | Underl Maturity Date | Underlying maturity date | Date | 8 | Yes | IRPV01_VEGAS |
| 13 | Strike | Option Strike | Numeric | 16,2 | Yes | IRPV01_VEGAS |
| 14 | ATM Spread | ATM spread | Numeric | 10,2 | Yes | IRPV01_VEGAS |
| 15 | Vega Yield (local cur) | IR Vega in local currency | Numeric | 10,2 | Yes | Derived |
| 16 | ZAR_PROCESSING | JBSBSA Flag | VarChar | 1 | Yes | Extraction |
| 17 | Vega Yield (USD) | IR Vega in USD | Numeric | 10,2 | Yes | IRPV01_VEGAS |
| 18 | Vega Yield (ZAR) | IR Vega in ZAR | Numeric | 10,2 | Yes | IRPV01_VEGAS |
| 19 | Typology | Typology of deal | VarChar | 21 | Yes | IRPV01_VEGAS |
| 20 | Index | Interest rate index | VarChar | 64 | No | IRPV01_VEGAS |
| 21 | ATM Strike | ATM strike level | Numeric | 16,2 | No | IRPV01_VEGAS |

### 3.2 Field Details

#### Field 1: TRADE_NUM
| Attribute | Value |
|-----------|-------|
| **Description** | Unique trade identifier in Murex |
| **Data Type** | Numeric |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | Trade Number in simulation view IRPV01_VEGAS |
| **Business Rule** | Must not be null |
| **Example** | 27942079 |

#### Field 2: CURRENCY local
| Attribute | Value |
|-----------|-------|
| **Description** | Currency of the interest rate vega sensitivity |
| **Data Type** | VarChar |
| **Length** | 4 |
| **Mandatory** | Yes |
| **Source** | Derived: COALESCE(RT_INDEX.M_CURRENCY, IR_VEGA.M_CURRENCY) |
| **Business Rule** | For range accruals, use index currency; otherwise use trade currency |
| **Example** | EUR, USD, GBP |

#### Field 3: FAMILY
| Attribute | Value |
|-----------|-------|
| **Description** | Deal family classification |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | Family breakdown in simulation view IRPV01_VEGAS |
| **Valid Values** | IRD, CRD |
| **Example** | IRD |

#### Field 4: GROUP
| Attribute | Value |
|-----------|-------|
| **Description** | Deal group classification |
| **Data Type** | VarChar |
| **Length** | 5 |
| **Mandatory** | Yes |
| **Source** | Group breakdown in simulation view IRPV01_VEGAS |
| **Valid Values** | OSWP, CF, CDS, etc. |
| **Business Rule** | Determines vega type selection |
| **Example** | OSWP |

#### Field 5: TYPE
| Attribute | Value |
|-----------|-------|
| **Description** | Deal type classification |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | Type breakdown in simulation view IRPV01_VEGAS |
| **Example** | SWAPTION |

#### Field 6: Category
| Attribute | Value |
|-----------|-------|
| **Description** | Category classification |
| **Data Type** | VarChar |
| **Length** | 3 |
| **Mandatory** | No |
| **Source** | Set to blank in dynamic table |
| **Default** | Empty string |

#### Field 7: Portfolio
| Attribute | Value |
|-----------|-------|
| **Description** | Trading book portfolio code |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | Portfolio breakdown in simulation view IRPV01_VEGAS |
| **Example** | CTLNSBLFRNNY |

#### Field 8: Profit Centre
| Attribute | Value |
|-----------|-------|
| **Description** | Cost centre / profit centre of the deal |
| **Data Type** | VarChar |
| **Length** | 20 |
| **Mandatory** | Yes |
| **Source** | COSTCENT in A_IR_VEGA.REP (UDF from portfolio) |
| **Example** | 21895 |

#### Field 9: Option Maturity
| Attribute | Value |
|-----------|-------|
| **Description** | Option maturity pillar (expiry tenor) |
| **Data Type** | VarChar |
| **Length** | 15 |
| **Mandatory** | Yes |
| **Source** | Opt_Maturity formula output in IRPV01_VEGAS |
| **Valid Values** | Standard tenor pillars (1M, 3M, 6M, 1Y, 2Y, etc.) |
| **Example** | 6M |

#### Field 10: Option Maturity Date
| Attribute | Value |
|-----------|-------|
| **Description** | Option maturity date |
| **Data Type** | Date |
| **Length** | 8 |
| **Format** | DD/MM/YYYY |
| **Mandatory** | Yes |
| **Source** | Opt_Maturity_Date formula output in IRPV01_VEGAS |
| **Business Rule** | Must not be empty (used as filter) |
| **Example** | 12/01/2024 |

#### Field 11: Underl Maturity
| Attribute | Value |
|-----------|-------|
| **Description** | Underlying instrument maturity pillar |
| **Data Type** | VarChar |
| **Length** | 64 |
| **Mandatory** | Yes |
| **Source** | Und. Maturity breakdown in IRPV01_VEGAS |
| **Valid Values** | Standard tenor pillars |
| **Example** | 2Y |

#### Field 12: Underl Maturity Date
| Attribute | Value |
|-----------|-------|
| **Description** | Underlying instrument maturity date |
| **Data Type** | Date |
| **Length** | 8 |
| **Mandatory** | Yes |
| **Source** | Und. Maturity breakdown in IRPV01_VEGAS |
| **Example** | 14/07/25 |

#### Field 13: Strike
| Attribute | Value |
|-----------|-------|
| **Description** | Option strike rate |
| **Data Type** | Numeric |
| **Length** | 16,2 |
| **Mandatory** | Yes |
| **Source** | Strike breakdown in IRPV01_VEGAS |
| **Example** | 0.00 |

#### Field 14: ATM Spread
| Attribute | Value |
|-----------|-------|
| **Description** | Distance from at-the-money (strike - forward) |
| **Data Type** | Numeric |
| **Length** | 10,2 |
| **Mandatory** | Yes |
| **Source** | ATM_Spread formula output in IRPV01_VEGAS |
| **Business Rule** | Positive = OTM call / ITM put; Negative = ITM call / OTM put |
| **Example** | 0.00 |

#### Field 15: Vega Yield (local cur)
| Attribute | Value |
|-----------|-------|
| **Description** | IR Vega in local currency |
| **Data Type** | Numeric |
| **Length** | 10,2 |
| **Mandatory** | Yes |
| **Source** | Derived from Vega_USD * FX rate for range accruals, else Vega_Local |
| **Business Rule** | See vega type selection formula |
| **Example** | 0.890000 |

#### Field 16: ZAR_PROCESSING
| Attribute | Value |
|-----------|-------|
| **Description** | Flag indicating if closing entity is JBSBSA |
| **Data Type** | VarChar |
| **Length** | 1 |
| **Mandatory** | Yes |
| **Source** | Extraction logic: IF M_CLOSING_E = 'JBSBSA' THEN 'Y' ELSE 'N' |
| **Valid Values** | Y, N |
| **Example** | N |

#### Field 17: Vega Yield (USD)
| Attribute | Value |
|-----------|-------|
| **Description** | IR Vega in USD |
| **Data Type** | Numeric |
| **Length** | 10,2 |
| **Mandatory** | Yes |
| **Source** | Vega_USD formula output in IRPV01_VEGAS |
| **Business Rule** | Converted using zero-day FX spot |
| **Example** | 0.99 |

#### Field 18: Vega Yield (ZAR)
| Attribute | Value |
|-----------|-------|
| **Description** | IR Vega in ZAR |
| **Data Type** | Numeric |
| **Length** | 10,2 |
| **Mandatory** | Yes |
| **Source** | Vega_ZAR formula output in IRPV01_VEGAS |
| **Note** | **DEPRECATED** - To be decommissioned |
| **Example** | 17.97 |

#### Field 19: Typology
| Attribute | Value |
|-----------|-------|
| **Description** | Product typology classification |
| **Data Type** | VarChar |
| **Length** | 21 |
| **Mandatory** | Yes |
| **Source** | Typology breakdown in IRPV01_VEGAS |
| **Business Rule** | Used in vega type selection formula |
| **Example** | CRD - INSURANCE |

#### Field 20: Index
| Attribute | Value |
|-----------|-------|
| **Description** | Interest rate index / PL instrument |
| **Data Type** | VarChar |
| **Length** | 64 |
| **Mandatory** | No |
| **Source** | PL Instrument breakdown in IRPV01_VEGAS |
| **Example** | SOCIETE IVOIRIENNE DE RAFFINAG |

#### Field 21: ATM Strike
| Attribute | Value |
|-----------|-------|
| **Description** | At-the-money strike level from volatility surface |
| **Data Type** | Numeric |
| **Length** | 16,2 |
| **Mandatory** | No |
| **Source** | Strike1 (M_STRIKE1) from A_IR_VEGA.REP |
| **Example** | 3.7145 |

---

## 4. Sample Data

### 4.1 Header Row
```
TRADE_NUM;CURRENCY local;FAMILY;GROUP;TYPE;Category;Portfolio;Profit Centre;Option Maturity;Option Maturity Date;Underl Maturity;Underl Maturity Date;Strike;ATM Spread;Vega Yield (local cur);ZAR_PROCESSING;Vega Yield (USD);Vega Yield (ZAR);Typology;Index;ATM Strike
```

### 4.2 Sample Records

```csv
27942079;EUR;CRD;CDS;;;CTLNSBLFRNNY;21895;6M;12/01/2024;2Y;14/07/25;0.00;0.00;0.890000;N;0.99;17.97;CRD - INSURANCE;SOCIETE IVOIRIENNE DE RAFFINAG;3.7145
27942079;EUR;CRD;CDS;;;CTLNSBLFRNNY;21895;1Y;12/07/2024;1Y;12/07/24;0.00;0.00;0.130000;N;0.15;2.72;CRD - INSURANCE;SOCIETE IVOIRIENNE DE RAFFINAG;3.6776
27942079;EUR;CRD;CDS;;;CTLNSBLFRNNY;21895;1M;14/08/2023;3Y;13/07/26;0.00;0.00;0.110000;N;0.12;2.20;CRD - INSURANCE;SOCIETE IVOIRIENNE DE RAFFINAG;3.6385
```

---

## 5. Data Quality Rules

### 5.1 Validation Rules

| Rule ID | Field | Rule | Severity | Action |
|---------|-------|------|----------|--------|
| DQ-IRV-001 | TRADE_NUM | Must not be null | Critical | Reject |
| DQ-IRV-002 | TRADE_NUM | Must be numeric | Critical | Reject |
| DQ-IRV-003 | Option Maturity Date | Must not be empty | Critical | Reject (filter) |
| DQ-IRV-004 | CURRENCY | Must be valid ISO code | High | Warning |
| DQ-IRV-005 | FAMILY | Must be IRD or CRD | High | Reject |
| DQ-IRV-006 | GROUP | Must not be OPT | High | Reject (filter) |
| DQ-IRV-007 | Vega values | Must be numeric | Critical | Reject |
| DQ-IRV-008 | Legal Entity | Must not be SBSA | High | Exclude |
| DQ-IRV-009 | FX Rate | Must exist for non-USD | Medium | Default to 1 |

### 5.2 Completeness Checks

| Check | Description | Threshold |
|-------|-------------|-----------|
| Record Count | Day-over-day variance | ±10% |
| Portfolio Coverage | All vega-sensitive portfolios | 100% |
| Currency Coverage | All traded currencies | 100% |
| Missing Vega | Records with null vega | <0.1% |

---

## 6. Interface Dependencies

### 6.1 Upstream Dependencies

| System | Data | Timing | Impact if Delayed |
|--------|------|--------|-------------------|
| Market Data | Volatility surfaces | 18:00 GMT | Feed cannot run |
| Market Data | FX spots | 18:00 GMT | Currency conversion fails |
| Valuation Batch | Vega calculations | 21:00 GMT | Feed cannot run |
| Reference Data | RT_INDEX | Static | Range accrual currency missing |
| Reference Data | RT_RANGE | Daily | Range accrual lookup fails |

### 6.2 Downstream Consumers

| System | Purpose | Frequency |
|--------|---------|-----------|
| Plato | Risk aggregation | Daily |
| RDS | Risk data store | Daily |
| VaR Engine | Risk calculation | Daily |
| Limit System | Vega limit monitoring | Daily |

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
| Total Vega USD | Murex | Feed | ±$5,000 |
| Record Count | Murex | Feed | ±5% |
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

## Appendix A: Vega Type Selection Reference

| Condition | Vega Type | Applied To |
|-----------|-----------|------------|
| Group = "CF" AND Vol_nature <> "Normal" | Flat_Vega | Cap/Floor with non-normal vol |
| (Group IN ("OSWP", "CF") OR Typology IN ("CRD - GUARANTEE", "CRD - INSURANCE", "IRD - CAPS/FLOORS")) AND Vol_nature = "Normal" | Normal_Vega | Swaptions, Cap/Floor with normal vol, CRD products |
| All other cases | Vega_Yield | Default yield-based vega |

---

## Appendix B: Currency Resolution Reference

| Product Type | Currency Source | Logic |
|--------------|-----------------|-------|
| Range Accrual | RT_INDEX.M_CURRENCY | From interest rate index definition |
| Standard IR Option | IR_VEGA.M_CURRENCY | From trade currency |
| Any product with USD | Trade currency | No FX conversion |
| Non-USD products | FX-converted | Using TBL_MD_FXSPOTS_REP |

---

*End of Document*
