---
# Document Metadata
document_id: EN-IDD-001
document_name: Energy Sensitivities Feed - Interface Design Document
version: 1.0
effective_date: 2025-01-03
next_review_date: 2026-01-03
owner: Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: EN-BRD-001  # Energy Sensitivities BRD
feed_id: EN-001
---

# Energy Sensitivities Feed - Interface Design Document

**Meridian Global Bank - Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | EN-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 3 January 2025 |
| **Owner** | Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Interface Overview

### 1.1 Feed Summary

| Property | Value |
|----------|-------|
| **Feed Name** | Energy Sensitivities (MRGRNLI) |
| **Feed ID** | EN-001 |
| **Direction** | Outbound (Murex → Downstream) |
| **Source System** | Murex (VESPA) |
| **Target Systems** | Risk Data Warehouse, Plato, VESPA Reporting |
| **Frequency** | Daily (T+1) |
| **Format** | CSV (semicolon delimited) |
| **Encoding** | UTF-8 |

### 1.2 File Naming Convention

```
MxMGB_MR_Energy_Sens_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Values |
|-----------|-------------|--------|
| MxMGB | System prefix | Fixed |
| MR | Market Risk module | Fixed |
| Energy | Asset class | Fixed |
| Sens | Sensitivities | Fixed |
| Region | Trading region | LN, HK, NY, SP |
| YYYYMMDD | As-of date | Business date |

**Example**: `MxMGB_MR_Energy_Sens_LN_20250103.csv`

---

## 2. Field Specifications

### 2.1 Field Summary

| # | Field Name | Type | Length | Nullable | Description |
|---|------------|------|--------|----------|-------------|
| 1 | TP_PFOLIO | VarChar | 20 | No | Trading portfolio code |
| 2 | XV_INSTR | VarChar | 35 | No | Instrument/underlying name |
| 3 | CURVE_NAME | VarChar | 30 | Yes | Commodity price curve name |
| 4 | XV_CALMAT | VarChar | 10 | No | Tenor pillar/maturity |
| 5 | XV_UNIT | VarChar | 21 | Yes | Quotation unit |
| 6 | XV_PRICE | Numeric | 20,6 | No | Commodity price |
| 7 | TXV_DELTA | Numeric | 15,6 | No | Delta sensitivity |
| 8 | TXV_GAMMA | Numeric | 15,6 | No | Gamma sensitivity |
| 9 | TXV_THETA | Numeric | 15,6 | No | Theta sensitivity |
| 10 | TXV_VEGA | Numeric | 15,6 | No | Vega sensitivity |
| 11 | TXV_RHO | Numeric | 16,4 | No | Rho sensitivity (DV01×100) |
| 12 | XV_CURR | VarChar | 16 | Yes | Currency |
| 13 | SYS_DATE | VarChar | 8 | No | System extraction date |
| 14 | SYS_TIME | VarChar | 8 | No | System extraction time |

**Total Fields**: 14

---

## 3. Detailed Field Definitions

### 3.1 TP_PFOLIO

| Property | Value |
|----------|-------|
| **Position** | 1 |
| **Field Name** | TP_PFOLIO |
| **Data Type** | VarChar |
| **Length** | 20 |
| **Nullable** | No |
| **Description** | Trading portfolio code from Bookman hierarchy |
| **Source** | SV_MRGR_GREEKS.M_PORTFOLIO / SV_MRGR_RHO.M_PORTFOLIO |
| **Example** | ETLNSBLETROPT |

### 3.2 XV_INSTR

| Property | Value |
|----------|-------|
| **Position** | 2 |
| **Field Name** | XV_INSTR |
| **Data Type** | VarChar |
| **Length** | 35 |
| **Nullable** | No |
| **Description** | Instrument name (commodity underlying or currency for Rho) |
| **Source** | Complex logic (see Derivation Rules below) |
| **Example (Greeks)** | BR DATED_AVM |
| **Example (Rho)** | USD |

#### Derivation Rules for XV_INSTR

| Condition | Value |
|-----------|-------|
| RREPO FIXED (live trade) | M_TP_CMULAB0 \|\| '_FIN' |
| RREPO FV (live trade) | M_TP_CMULAB0 \|\| '_FV' |
| RREPO VV (live trade) | M_TP_CMULAB0 \|\| '_VV' |
| RREPO FIXED (purged) | M_UNDERLYIN \|\| '_FIN' |
| RREPO FV (purged) | M_UNDERLYIN \|\| '_FV' |
| RREPO VV (purged) | M_UNDERLYIN \|\| '_VV' |
| CER% and not LIVE | 'CER' |
| CER_PROJ% and Theta = 0 | 'CERPJ_' \|\| M_U_PROJ_NAM |
| Default (Greeks) | NVL(M_PL_INSTRU, M_TP_CMULAB0) |
| Rho records | M_CURRENCY |

### 3.3 CURVE_NAME

| Property | Value |
|----------|-------|
| **Position** | 3 |
| **Field Name** | CURVE_NAME |
| **Data Type** | VarChar |
| **Length** | 30 |
| **Nullable** | Yes |
| **Description** | Commodity price curve name |
| **Source (Greeks)** | SV_MRGR_GREEKS.M_CURVE_NAM |
| **Source (Rho)** | Empty string |
| **Example** | CR BR DATED PLT :Std |

### 3.4 XV_CALMAT

| Property | Value |
|----------|-------|
| **Position** | 4 |
| **Field Name** | XV_CALMAT |
| **Data Type** | VarChar |
| **Length** | 10 |
| **Nullable** | No |
| **Description** | Tenor pillar (commodity maturity for Greeks, IR pillar for Rho) |
| **Source (Greeks)** | SV_MRGR_GREEKS.M_PILLARS |
| **Source (Rho)** | SV_MRGR_RHO.M_DATE |
| **Example (Greeks)** | APR24, DEC23, FEB24 |
| **Example (Rho)** | 1M, 3M, 1Y, 5Y |

### 3.5 XV_UNIT

| Property | Value |
|----------|-------|
| **Position** | 5 |
| **Field Name** | XV_UNIT |
| **Data Type** | VarChar |
| **Length** | 21 |
| **Nullable** | Yes |
| **Description** | Quotation unit for commodity |
| **Source (Greeks)** | SV_MRGR_GREEKS.M_UNIT |
| **Source (Rho)** | Empty string |
| **Valid Values** | BBL (barrels), MT (metric tons), GAL (gallons), MMBTU, etc. |
| **Example** | BBL |

### 3.6 XV_PRICE

| Property | Value |
|----------|-------|
| **Position** | 6 |
| **Field Name** | XV_PRICE |
| **Data Type** | Numeric |
| **Length** | 20,6 |
| **Nullable** | No |
| **Description** | Commodity price |
| **Source** | Complex logic (see Derivation Rules below) |
| **Example** | 85.390000 |

#### Derivation Rules for XV_PRICE

| Condition | Value |
|-----------|-------|
| FREIGHT | M_MARKET_PR |
| GAL unit | M_PRICE × 100 |
| Financed (_FIN) and M_TP_RTFV0 = 'V' | M_TP_RTVLC02 |
| Financed (_FIN) and M_TP_RTFV1 = 'V' | M_TP_RTVLC12 |
| Default (Greeks) | M_PRICE |
| Rho records | 0 |

### 3.7 TXV_DELTA

| Property | Value |
|----------|-------|
| **Position** | 7 |
| **Field Name** | TXV_DELTA |
| **Data Type** | Numeric |
| **Length** | 15,6 |
| **Nullable** | No |
| **Description** | Commodity delta sensitivity in native units |
| **Source (Greeks)** | M_ADAPTED_D (for ASIAN/OFUT) or M_DELTA (others) |
| **Source (Rho)** | 0 |
| **Unit** | Native (BBL, MT, etc.) |
| **Example** | 29702.894874 |
| **Validation** | Can be positive (long) or negative (short) |

#### Delta Selection Logic

```sql
CASE WHEN M_GROUP IN ('ASIAN', 'OFUT')
     THEN M_ADAPTED_D
     ELSE M_DELTA
END AS TXV_DELTA
```

### 3.8 TXV_GAMMA

| Property | Value |
|----------|-------|
| **Position** | 8 |
| **Field Name** | TXV_GAMMA |
| **Data Type** | Numeric |
| **Length** | 15,6 |
| **Nullable** | No |
| **Description** | Gamma sensitivity (rate of delta change) |
| **Source (Greeks)** | M_GAMMA |
| **Source (Rho)** | 0 |
| **Unit** | USD |
| **Example** | -104.117815 |
| **Validation** | Typically positive for long options |

### 3.9 TXV_THETA

| Property | Value |
|----------|-------|
| **Position** | 9 |
| **Field Name** | TXV_THETA |
| **Data Type** | Numeric |
| **Length** | 15,6 |
| **Nullable** | No |
| **Description** | Theta sensitivity (time decay) |
| **Source (Greeks)** | M_THETA |
| **Source (Rho)** | 0 |
| **Unit** | USD |
| **Example** | 308.487016 |
| **Validation** | Typically negative (time decay), can be positive for certain structures |

### 3.10 TXV_VEGA

| Property | Value |
|----------|-------|
| **Position** | 10 |
| **Field Name** | TXV_VEGA |
| **Data Type** | Numeric |
| **Length** | 15,6 |
| **Nullable** | No |
| **Description** | Vega sensitivity (volatility) |
| **Source (Greeks)** | M_VEGA |
| **Source (Rho)** | 0 |
| **Unit** | USD |
| **Example** | -1927.163552 |
| **Validation** | Positive = long vol, Negative = short vol |

### 3.11 TXV_RHO

| Property | Value |
|----------|-------|
| **Position** | 11 |
| **Field Name** | TXV_RHO |
| **Data Type** | Numeric |
| **Length** | 16,4 |
| **Nullable** | No |
| **Description** | Rho sensitivity (interest rate risk) |
| **Source (Greeks)** | 0 |
| **Source (Rho)** | SUM(M_DV01__ZER × 100) |
| **Unit** | USD (scaled by 100) |
| **Example** | 1250.7500 |
| **Validation** | Can be positive or negative |

**Business Interpretation**:
- **Rho = DV01 × 100**: Scaled for reporting purposes
- **Positive**: Benefits from higher rates
- **Negative**: Suffers from higher rates

### 3.12 XV_CURR

| Property | Value |
|----------|-------|
| **Position** | 12 |
| **Field Name** | XV_CURR |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Nullable** | Yes |
| **Description** | Currency of the Greeks |
| **Source (Greeks)** | M_CURRENCY |
| **Source (Rho)** | Empty string |
| **Valid Values** | USD, EUR, GBP, etc. |
| **Example** | USD |

### 3.13 SYS_DATE

| Property | Value |
|----------|-------|
| **Position** | 13 |
| **Field Name** | SYS_DATE |
| **Data Type** | VarChar |
| **Length** | 8 |
| **Nullable** | No |
| **Description** | System extraction date |
| **Source** | SUBSTR(TO_CHAR(SYSTIMESTAMP, 'dd/mm/yy hh:miAM'), 1, 8) |
| **Format** | DD/MM/YY |
| **Example** | 03/01/25 |

### 3.14 SYS_TIME

| Property | Value |
|----------|-------|
| **Position** | 14 |
| **Field Name** | SYS_TIME |
| **Data Type** | VarChar |
| **Length** | 8 |
| **Nullable** | No |
| **Description** | System extraction time |
| **Source** | SUBSTR(TO_CHAR(SYSTIMESTAMP, 'dd/mm/yy hh:mm:ss'), 10, 8) |
| **Format** | HH:MM:SS |
| **Example** | 10:10:32 |

---

## 4. Record Layout

### 4.1 Header Record

```
TP_PFOLIO;XV_INSTR;CURVE_NAME;XV_CALMAT;XV_UNIT;XV_PRICE;TXV_DELTA;TXV_GAMMA;TXV_THETA;TXV_VEGA;TXV_RHO;XV_CURR;SYS_DATE;SYS_TIME
```

### 4.2 Data Record Example (Greeks - Oil Options)

```
ETLNSBLETROPT;BR DATED_AVM;CR BR DATED PLT :Std;APR24;BBL;85.390000;29702.894874;-104.117815;308.487016;-1927.163552;0.000000;USD;03/01/25;10:10:32
```

### 4.3 Data Record Example (Greeks - Linear)

```
CMLNMGBSWAPS;BRENT_FWD;CR BRENT ICE :Std;MAR25;BBL;78.500000;15000.000000;0.000000;0.000000;0.000000;0.000000;USD;03/01/25;10:10:32
```

### 4.4 Data Record Example (Rho)

```
ETLNSBLETROPT;USD;;1Y;;0;0.000000;0.000000;0.000000;0.000000;1250.750000;;03/01/25;10:10:32
```

---

## 5. Sample Data

### 5.1 Complete File Example

```csv
TP_PFOLIO;XV_INSTR;CURVE_NAME;XV_CALMAT;XV_UNIT;XV_PRICE;TXV_DELTA;TXV_GAMMA;TXV_THETA;TXV_VEGA;TXV_RHO;XV_CURR;SYS_DATE;SYS_TIME
ETLNSBLETROPT;BR DATED_AVM;CR BR DATED PLT :Std;APR24;BBL;85.390000;29702.894874;-104.117815;308.487016;-1927.163552;0.000000;USD;03/01/25;10:10:32
ETLNSBLETROPT;BR DATED_AVM;CR BR DATED PLT :Std;DEC23;BBL;89.490000;28284.273856;47.091066;72.332600;173.945737;0.000000;USD;03/01/25;10:10:32
ETLNSBLETROPT;BR DATED_AVM;CR BR DATED PLT :Std;FEB24;BBL;86.830000;28534.482869;-32.347981;225.265799;-658.277254;0.000000;USD;03/01/25;10:10:32
CMLNMGBSWAPS;BRENT_FWD;CR BRENT ICE :Std;MAR25;BBL;78.500000;15000.000000;0.000000;0.000000;0.000000;0.000000;USD;03/01/25;10:10:32
ETLNSBLETROPT;USD;;1Y;;0;0.000000;0.000000;0.000000;0.000000;1250.750000;;03/01/25;10:10:32
ETLNSBLETROPT;USD;;5Y;;0;0.000000;0.000000;0.000000;0.000000;325.250000;;03/01/25;10:10:32
```

### 5.2 Greeks vs Rho Record Comparison

| Field | Greeks Record | Rho Record |
|-------|---------------|------------|
| TP_PFOLIO | ETLNSBLETROPT | ETLNSBLETROPT |
| XV_INSTR | BR DATED_AVM | USD |
| CURVE_NAME | CR BR DATED PLT :Std | (empty) |
| XV_CALMAT | APR24 | 1Y |
| XV_UNIT | BBL | (empty) |
| XV_PRICE | 85.390000 | 0 |
| TXV_DELTA | 29702.894874 | 0.000000 |
| TXV_GAMMA | -104.117815 | 0.000000 |
| TXV_THETA | 308.487016 | 0.000000 |
| TXV_VEGA | -1927.163552 | 0.000000 |
| TXV_RHO | 0.000000 | 1250.750000 |
| XV_CURR | USD | (empty) |
| SYS_DATE | 03/01/25 | 03/01/25 |
| SYS_TIME | 10:10:32 | 10:10:32 |

---

## 6. Validation Rules

### 6.1 Record-Level Validations

| Rule ID | Field(s) | Validation | Action |
|---------|----------|------------|--------|
| VR-001 | TP_PFOLIO | Must be populated | Reject |
| VR-002 | TP_PFOLIO | Must exist in Bookman hierarchy | Flag |
| VR-003 | XV_INSTR | Must be populated | Reject |
| VR-004 | XV_CALMAT | Must be populated | Reject |
| VR-005 | XV_PRICE | Must be >= 0 for Greeks | Flag |
| VR-006 | TXV_DELTA through TXV_RHO | At least one must be non-zero | Reject |
| VR-007 | XV_CURR | Must be valid ISO code if populated | Flag |

### 6.2 File-Level Validations

| Rule ID | Validation | Action |
|---------|------------|--------|
| VF-001 | File not empty (excluding header) | Warning |
| VF-002 | Header matches expected format | Reject file |
| VF-003 | Row count within expected range | Warning if variance >20% |
| VF-004 | All 14 fields present per row | Reject record |

### 6.3 Business Validations

| Rule ID | Validation | Action |
|---------|------------|--------|
| VB-001 | Greeks: CURVE_NAME populated | Flag if empty |
| VB-002 | Greeks: XV_UNIT populated | Flag if empty |
| VB-003 | Linear products: Gamma, Theta, Vega = 0 | Flag if non-zero |
| VB-004 | Rho records: XV_INSTR is currency code | Flag if not |
| VB-005 | Greeks records: TXV_RHO = 0 | Flag if non-zero |
| VB-006 | Rho records: TXV_DELTA through TXV_VEGA = 0 | Flag if non-zero |

---

## 7. Interface Schedule

### 7.1 Daily Schedule (GMT)

| Time | Event | Description |
|------|-------|-------------|
| 18:00 | Commodity curve calibration | Prices available |
| 18:00 | Volatility surface calibration | Vol surfaces available |
| 21:00 | Valuation batch complete | Sensitivities calculated |
| 03:00 | Feeder batch start | Greeks and Rho feeding |
| 04:00 | Extraction batch start | UNION and output generation |
| 04:30 | Extraction complete | Files generated |
| 05:00 | Merge and packaging | ZIP files created |
| 05:30 | Delivery | Files available to downstream |

### 7.2 Regional Schedule

| Region | Extraction Start | Extraction End | Delivery |
|--------|------------------|----------------|----------|
| LN | 04:00 GMT | 04:30 GMT | 05:30 GMT |
| HK | 20:00 HKT | 20:30 HKT | 21:30 HKT |
| NY | 23:00 EST | 23:30 EST | 00:30 EST+1 |
| SP | 20:00 SGT | 20:30 SGT | 21:30 SGT |

---

## 8. Error Handling

### 8.1 Error Codes

| Code | Description | Severity | Action |
|------|-------------|----------|--------|
| E001 | Source table unavailable | Critical | Abort extraction |
| E002 | No data returned | Warning | Generate empty file with header |
| E003 | Field validation failure | Error | Reject record |
| E004 | Portfolio lookup failure | Warning | Use source portfolio |
| E005 | File write failure | Critical | Retry, escalate |
| E006 | Merge script failure | Error | Deliver unmerged files |

### 8.2 Error Recovery

| Scenario | Recovery Action |
|----------|-----------------|
| Valuation incomplete | Wait, re-run after completion |
| Partial extraction failure | Re-run from checkpoint |
| File delivery failure | Retry 3 times, then escalate |
| Data quality issue | Manual review, correction, re-run |

---

## 9. Risk Type Classification

### 9.1 LINEAR vs NON-LINEAR

The @RiskType parameter filters output by product classification:

```sql
CASE WHEN M_GROUP IN ('ASIAN', 'OFUT')
     THEN 'NON-LINEAR'
     ELSE 'LINEAR'
END AS RISK_TYPE
```

| Risk Type | Product Groups | Greeks Profile |
|-----------|----------------|----------------|
| **LINEAR** | FUT, FWD, SPOT, SWAP, OPT | Delta only |
| **NON-LINEAR** | ASIAN, OFUT | Full Greeks |

### 9.2 Feed Configuration

The primary Energy Sensitivities feed (`MxMGB_MR_Energy_Sens_**`) uses:
- @RiskType = 'NON-LINEAR'

For linear-only reporting, a separate extraction may be configured with:
- @RiskType = 'LINEAR'

---

## 10. Downstream Integration

### 10.1 Target Systems

| System | Usage | Key Fields |
|--------|-------|------------|
| Risk Data Warehouse | Storage, reporting | All fields |
| Plato (Risk Engine) | FRTB commodity risk | Delta, Gamma, Vega |
| VESPA Reporting | Regulatory reporting | All fields |
| Trading Dashboard | Position monitoring | Delta, XV_INSTR |
| P&L Attribution | Greeks decomposition | All Greeks |

### 10.2 Integration Points

| Integration | Protocol | Format |
|-------------|----------|--------|
| Risk DW Load | File-based | CSV |
| Plato Feed | SFTP | CSV (in ZIP) |
| Reporting Extract | Database | Table load |

---

## 11. Special Cases

### 11.1 RREPO Deal Handling

Commodity Repurchase (RREPO) deals have special instrument naming:

| Deal Type | Instrument Suffix | Source |
|-----------|-------------------|--------|
| COM - RREPO FIXED | _FIN | Financing leg |
| COM - RREPO FV | _FV | Fixed-Variable leg |
| COM - RREPO VV | _VV | Variable-Variable leg |

For live trades: Uses M_TP_CMULAB0 from SB_TP_REP
For purged trades: Uses M_UNDERLYIN from simulation view

### 11.2 Carbon Emission Rights

| Scenario | Instrument Value |
|----------|------------------|
| CER position not LIVE | 'CER' |
| CER_PROJ with no Theta | 'CERPJ_' + Project Name |
| CER_PROJ with Theta | Standard PL Instrument |

### 11.3 Price Adjustments

| Commodity | Adjustment |
|-----------|------------|
| FREIGHT | Use M_MARKET_PR |
| GAL unit | M_PRICE × 100 |
| Financed deals | Financing rate from SB_TP_BD_REP |

---

## 12. Related Documents

| Document | ID | Relationship |
|----------|-----|-------------|
| [Energy Sensitivities Overview](./energy-sensitivities-overview.md) | EN-OVW-001 | Parent overview |
| [Energy Sensitivities BRD](./energy-sensitivities-brd.md) | EN-BRD-001 | Business requirements |
| [Energy Sensitivities IT Config](./energy-sensitivities-config.md) | EN-CFG-001 | Technical configuration |
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Feed family parent |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |

---

## 13. Document Control

### 13.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-03 | Initial version | Risk Technology |

### 13.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Technical review | Annual | January 2026 |
| Schema review | On change | As needed |
| Integration review | Quarterly | April 2025 |

---

*End of Document*
