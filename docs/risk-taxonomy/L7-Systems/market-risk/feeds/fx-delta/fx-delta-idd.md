# FX Delta Sensitivities - Interface Design Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | FXD-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Interface Overview

### 1.1 Interface Summary

| Attribute | Value |
|-----------|-------|
| **Interface Name** | FX Delta Sensitivities |
| **Interface ID** | MR-IF-FXD |
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
MxMGB_MR_FX_Pos_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Values |
|-----------|-------------|--------|
| MxMGB | Murex Meridian Global Bank prefix | Fixed |
| MR | Market Risk | Fixed |
| FX | Asset class | Fixed |
| Pos | Position/Delta | Fixed |
| {Region} | Trading region | LN, HK, NY, SP |
| {YYYYMMDD} | Business date | Date format |

### 2.3 Package Details

| Attribute | Value |
|-----------|-------|
| **Package Format** | ZIP |
| **Package Pattern** | MxGTS_Vespa_Sensitivities_{Region}_{YYYYMMDD}.zip |
| **Contents** | Multiple sensitivity feeds including FX Delta |

---

## 3. Field Specification

### 3.1 Field Layout (8 Fields)

| # | Field Name | Description | Type | Length | Mandatory | Source |
|---|------------|-------------|------|--------|-----------|--------|
| 1 | TRADENUMBER | Trade ID | Numeric | 10 | Yes | Derived |
| 2 | PORTFOLIO | Portfolio code | VarChar | 16 | Yes | Simulation View |
| 3 | CURRENCY_PAIR | FX quotation | VarChar | 16 | Yes | Derived |
| 4 | FXDELTA | FX delta in USD | Numeric | 22,2 | Yes | Derived |
| 5 | FXDELTA_CURR | Currency of FXDELTA | VarChar | 4 | Yes | Fixed (USD) |
| 6 | FXDELTA_ZAR | FX delta in ZAR | Numeric | 22,2 | Yes | Simulation View |
| 7 | FXDELTA_CURR2 | Currency of FXDELTA_ZAR | VarChar | 4 | Yes | Fixed (ZAR) |
| 8 | ZAR_PROCESSING | JBSBSA flag | VarChar | 1 | Yes | Derived |

### 3.2 Field Details

#### Field 1: TRADENUMBER
| Attribute | Value |
|-----------|-------|
| **Description** | Unique trade identifier |
| **Data Type** | Numeric |
| **Length** | 10 |
| **Mandatory** | Yes |
| **Source** | M_NB from FXDELTAPOSRPT or M_TRADE_NUM from STB_Fx_Delta_ONLY |
| **Business Rule** | Set to 0 for dead/purged deals (aggregated) |
| **Example** | 12345678, 0 |

#### Field 2: PORTFOLIO
| Attribute | Value |
|-----------|-------|
| **Description** | Trading book portfolio code |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | Portfolio breakdown from simulation views |
| **Example** | ALCOLNSBLCBHED |

#### Field 3: CURRENCY_PAIR
| Attribute | Value |
|-----------|-------|
| **Description** | FX currency pair in quotation mode |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Format** | CCY1-CCY2 |
| **Mandatory** | Yes |
| **Source** | FXQUOT from FXDELTAPOSRPT, or derived from FLOW_CURR/CURRENCY/UNIT for STB |
| **Reference** | Standardized via TBL_FX_CNT_REP |
| **Example** | EUR-USD, GBP-USD, AED-ZAR |

#### Field 4: FXDELTA
| Attribute | Value |
|-----------|-------|
| **Description** | FX spot delta in USD |
| **Data Type** | Numeric |
| **Length** | 22,2 |
| **Mandatory** | Yes |
| **Source** | FX_Delta_USD from STB for live STB deals, FXDELTA from FXDELTAPOSRPT otherwise |
| **Business Rule** | Use MAX if non-zero, else use MIN (handles sign convention) |
| **Example** | -16405968.99, 0.00 |

#### Field 5: FXDELTA_CURR
| Attribute | Value |
|-----------|-------|
| **Description** | Currency of FXDELTA field |
| **Data Type** | VarChar |
| **Length** | 4 |
| **Mandatory** | Yes |
| **Source** | Fixed at extraction level |
| **Value** | USD |
| **Example** | USD |

#### Field 6: FXDELTA_ZAR
| Attribute | Value |
|-----------|-------|
| **Description** | FX delta in ZAR |
| **Data Type** | Numeric |
| **Length** | 22,2 |
| **Mandatory** | Yes |
| **Source** | FXDELTA_ZAR from simulation view FXDELTAPOSRPT |
| **Note** | **DEPRECATED** - JBSBSA legacy field |
| **Example** | 0.38, 0.00 |

#### Field 7: FXDELTA_CURR2
| Attribute | Value |
|-----------|-------|
| **Description** | Currency of FXDELTA_ZAR field |
| **Data Type** | VarChar |
| **Length** | 4 |
| **Mandatory** | Yes |
| **Source** | Fixed at extraction level |
| **Value** | ZAR |
| **Note** | **DEPRECATED** - JBSBSA legacy field |
| **Example** | ZAR |

#### Field 8: ZAR_PROCESSING
| Attribute | Value |
|-----------|-------|
| **Description** | Flag indicating if closing entity is JBSBSA |
| **Data Type** | VarChar |
| **Length** | 1 |
| **Mandatory** | Yes |
| **Source** | Derived at extraction: IF M_CLOSING_E = 'JBSBSA' THEN 'Y' ELSE 'N' |
| **Valid Values** | Y, N |
| **Note** | **DEPRECATED** - Always 'N' since SBSA excluded from extraction |
| **Example** | N |

---

## 4. Sample Data

### 4.1 Header Row
```
TRADENUMBER;PORTFOLIO;CURRENCY_PAIR;FXDELTA;FXDELTA_CURR;FXDELTA_ZAR;FXDELTA_CURR2;ZAR_PROCESSING
```

### 4.2 Sample Records

```csv
0;ALCOLNSBLCBHED;AED-ZAR;0.00;USD;0.38;ZAR;N
0;ALCOLNSBLCBHED;EUR-USD;0.00;USD;0.00;ZAR;N
0;ALCOLNSBLCBHED;EUR-ZAR;0.00;USD;0.00;ZAR;N
0;ALCOLNSBLCBHED;GBP-USD;-16405968.99;USD;0.00;ZAR;N
12345678;FXLNSBL;EUR-USD;5000000.00;USD;0.00;ZAR;N
```

**Note**: Records with TRADENUMBER = 0 are aggregated dead/purged deals.

---

## 5. Data Quality Rules

### 5.1 Validation Rules

| Rule ID | Field | Rule | Severity | Action |
|---------|-------|------|----------|--------|
| DQ-FXD-001 | TRADENUMBER | Must be numeric (including 0) | Critical | Reject |
| DQ-FXD-002 | PORTFOLIO | Must not be null | Critical | Reject |
| DQ-FXD-003 | CURRENCY_PAIR | Must be CCY1-CCY2 format (7 chars) | High | Warning |
| DQ-FXD-004 | CURRENCY_PAIR | CCY codes must be 3 characters | High | Warning |
| DQ-FXD-005 | FXDELTA | Must be numeric | Critical | Reject |
| DQ-FXD-006 | FXDELTA_CURR | Must be USD | High | Warning |
| DQ-FXD-007 | Legal Entity | Must not be SBSA | High | Exclude |

### 5.2 Completeness Checks

| Check | Description | Threshold |
|-------|-------------|-----------|
| Record Count | Day-over-day variance | ±10% |
| Portfolio Coverage | All FX-sensitive portfolios | 100% |
| Currency Coverage | All traded currency pairs | 100% |
| Zero Delta Count | Records with FXDELTA = 0 | Monitor trend |

---

## 6. Interface Dependencies

### 6.1 Upstream Dependencies

| System | Data | Timing | Impact if Delayed |
|--------|------|--------|-------------------|
| Market Data | FX spot rates | 18:00 GMT | USD conversion fails |
| Valuation Batch | FX delta calculations | 21:00 GMT | Feed cannot run |
| Reference Data | TBL_FX_CNT_REP | Static | Currency pair standardization fails |

### 6.2 Downstream Consumers

| System | Purpose | Frequency |
|--------|---------|-----------|
| Plato | Risk aggregation | Daily |
| RDS | Risk data store | Daily |
| VaR Engine | Risk calculation | Daily |
| Limit System | FX position limits | Daily |

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
| Total FX Delta USD | Murex | Feed | ±$5,000 |
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

## Appendix A: Currency Pair Construction Reference

### For Structured Bonds (STB)

| Product Type | Currency Pair Logic |
|--------------|---------------------|
| IRD - FX LINKED NOTE | FLOW_CURR || '-' || UNIT |
| Other STB (CURRENCY = FLOW_CURR) | CURRENCY || '-' || UNIT |
| Other STB (CURRENCY ≠ FLOW_CURR) | CURRENCY || '-' || FLOW_CURR |

### For Non-Structured Products

| Source | Logic |
|--------|-------|
| FXDELTAPOSRPT | Use FXQUOT directly |

### Standardization via TBL_FX_CNT_REP

The extraction joins to TBL_FX_CNT_REP to ensure currency pairs follow market convention (e.g., EUR-USD not USD-EUR).

---

## Appendix B: Trade Status Reference

| Status | Treatment in Feed |
|--------|-------------------|
| LIVE | Full trade-level detail |
| MKT_OP | Full trade-level detail |
| Other | Aggregated with TRADENUMBER = 0 |
| NULL | Aggregated with TRADENUMBER = 0 |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
