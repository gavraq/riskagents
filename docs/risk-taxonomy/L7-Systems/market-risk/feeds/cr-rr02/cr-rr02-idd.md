---
# Document Metadata
document_id: CR-RR02-IDD-001
document_name: CR RR02 Feed - Interface Design Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: CR-RR02-BRD-001  # CR RR02 BRD
feed_id: CR-RR02-001
---

# CR RR02 Feed - Interface Design Document

**Meridian Global Bank - Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-RR02-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Interface Overview

### 1.1 Feed Summary

| Property | Value |
|----------|-------|
| **Feed Name** | CR RR02 (Credit Recovery Rate 02) |
| **Feed ID** | CR-RR02-001 |
| **Direction** | Outbound (Murex → Downstream) |
| **Source System** | Murex (VESPA) |
| **Target Systems** | Risk Data Warehouse, Plato, VESPA Reporting |
| **Frequency** | Daily (T+1) |
| **Format** | CSV (semicolon delimited) |
| **Encoding** | UTF-8 |

### 1.2 File Naming Convention

```
MxMGB_MR_Credit_RR02_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Values |
|-----------|-------------|--------|
| MxMGB | System prefix | Fixed |
| Vespa | Module identifier | Fixed |
| CR_RR02 | Feed type | Fixed |
| Region | Trading region | LN, HK, NY, SP |
| YYYYMMDD | As-of date | Business date |

**Example**: `MxMGB_MR_Credit_RR02_LN_20250102.csv`

---

## 2. Field Specifications

### 2.1 Field Summary

| # | Field Name | Type | Length | Nullable | Description |
|---|------------|------|--------|----------|-------------|
| 1 | TRADE_NUM | Numeric | 10 | No | Murex trade identifier |
| 2 | FAMILY | VarChar | 16 | No | Trade family code |
| 3 | GROUP | VarChar | 5 | No | Trade group code |
| 4 | TYPE | VarChar | 16 | Yes | Trade type code |
| 5 | TYPOLOGY | VarChar | 21 | Yes | Trade typology |
| 6 | PORTFOLIO | VarChar | 20 | No | Trading portfolio code |
| 7 | INSTRUMENT | VarChar | 30 | No | PL Instrument name |
| 8 | ISSUER | VarChar | 50 | No | Issuer label |
| 9 | CURVE_NAME | VarChar | 50 | No | Credit curve name |
| 10 | DATE | VarChar | 64 | Yes | Tenor pillar date |
| 11 | RECOVERY_RATE | Numeric | 12 | No | Recovery rate (%) |
| 12 | RR02_SENSI | Numeric | 16,2 | No | Recovery rate sensitivity (without propagation) |
| 13 | CURRENCY | VarChar | 4 | No | Sensitivity currency |
| 14 | CIF | Numeric | 9 | Yes | Customer Information File ID |
| 15 | GLOBUS_ID | VarChar | 10 | Yes | External issuer ID |
| 16 | COUNTRY | VarChar | 30 | Yes | Country of risk |
| 17 | ISIN | VarChar | 25 | Yes | Reference obligation ISIN |
| 18 | MATURITY | Date | 8 | No | Trade maturity date |
| 19 | UNDERLYING | VarChar | 15 | Yes | Reference obligation label |
| 20 | RESTRUCT | VarChar | 16 | No | Restructuring terms |

**Total Fields**: 20 (identical to CR RR01)

---

## 3. Detailed Field Definitions

### 3.1 TRADE_NUM

| Property | Value |
|----------|-------|
| **Position** | 1 |
| **Field Name** | TRADE_NUM |
| **Data Type** | Numeric |
| **Length** | 10 |
| **Nullable** | No |
| **Description** | Unique Murex trade identifier |
| **Source** | TBL_VESPA_SENS_REP.M_TRADE_NUM / TBL_VESPA_SENSCI_REP.M_TRADE_NUM |
| **Example** | 27522095 |

### 3.2 FAMILY

| Property | Value |
|----------|-------|
| **Position** | 2 |
| **Field Name** | FAMILY |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Nullable** | No |
| **Description** | Trade family classification |
| **Source** | VSP.M_FAMILY |
| **Valid Values** | CRD, IRD, EQD, FXD |
| **Example** | IRD |

### 3.3 GROUP

| Property | Value |
|----------|-------|
| **Position** | 3 |
| **Field Name** | GROUP |
| **Data Type** | VarChar |
| **Length** | 5 |
| **Nullable** | No |
| **Description** | Trade group classification |
| **Source** | VSP.M_GROUP |
| **Valid Values** | CDS, BOND, CRDI, CLN, CDO |
| **Example** | BOND |

### 3.4-3.11 (Same as CR RR01)

*Fields 4-11 are identical to CR RR01. See CR RR01 IDD for detailed specifications.*

### 3.12 RR02_SENSI

| Property | Value |
|----------|-------|
| **Position** | 12 |
| **Field Name** | RR02_SENSI |
| **Data Type** | Numeric |
| **Length** | 16,2 |
| **Nullable** | No |
| **Description** | Recovery rate sensitivity WITHOUT propagation |
| **Source** | VSP.M_RECOVERY1 (changed from M_VALUE per CM-6396) |
| **Unit** | Local currency |
| **Example** | 220.87 |
| **Validation** | Can be positive, negative, or zero |

**Business Interpretation**:
- **Positive**: Higher recovery = higher P&L (direct effect)
- **Negative**: Higher recovery = lower P&L (direct effect)
- **Magnitude**: P&L impact per 1% recovery change (spread held constant)
- **Relationship**: Typically RR02 <= RR01 (but not always)

### 3.13-3.20 (Same as CR RR01)

*Fields 13-20 are identical to CR RR01. See CR RR01 IDD for detailed specifications.*

---

## 4. Record Layout

### 4.1 Header Record

```
TRADE_NUM;FAMILY;GROUP;TYPE;TYPOLOGY;PORTFOLIO;INSTRUMENT;ISSUER;CURVE_NAME;DATE;RECOVERY_RATE;RR02_SENSI;CURRENCY;CIF;GLOBUS_ID;COUNTRY;ISIN;MATURITY;UNDERLYING;RESTRUCT
```

### 4.2 Data Record Example (Non-CRDI)

```
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;1Y;40.000000;220.87;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;;NONE
```

### 4.3 Data Record Example (CRDI)

```
28123456;CRD;CRDI;CRDI;CDX.NA.IG;CDXLNMGB01;CDX.NA.IG.S39;CDX.NA.IG.S39;CDX.NA.IG.S39;;0;3250.25;USD;0;;;20/06/28;;NONE
```

---

## 5. Sample Data

### 5.1 Complete File Example

```csv
TRADE_NUM;FAMILY;GROUP;TYPE;TYPOLOGY;PORTFOLIO;INSTRUMENT;ISSUER;CURVE_NAME;DATE;RECOVERY_RATE;RR02_SENSI;CURRENCY;CIF;GLOBUS_ID;COUNTRY;ISIN;MATURITY;UNDERLYING;RESTRUCT
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;6M;40.000000;11.04;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;;NONE
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;1Y;40.000000;220.87;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;;NONE
27522095;IRD;BOND;;IRD - FX PASSTHROUGH;LMLNMGBLEMP7FRT;FXPASS 1941-MZN 17% 11/05/25;MGB;THE MIN ECO FIN REP MOZAMBIQUE_MZN_SNRFOR;2Y;40.000000;625.53;MZN;100060635.000000;101088;UNITED KINGDOM;;11/05/25;;NONE
28234567;CRD;CDS;CDS;CDS_PROTECTION_BUYER;CDSLNMGB01;ABC Corp 5Y CDS;ABC Corporation;ABC_USD_SNRFOR;5Y;35.000000;-850.00;USD;100012345;123456;UNITED STATES;XS1234567890;15/06/29;ABC 4.5% 2029;Yes
28345678;CRD;CRDI;CRDI;iTraxx Europe;IDXLNMGB01;iTraxx Europe S40;iTraxx Europe S40;iTraxx Europe S40;;0;5200.75;EUR;0;;;20/12/28;;NONE
```

### 5.2 RR01 vs RR02 Comparison (Same Trade)

| Trade | Tenor | RR01 | RR02 | Difference | Interpretation |
|-------|-------|------|------|------------|----------------|
| 27522095 | 6M | 0.00 | 11.04 | -11.04 | RR02 > RR01 (unusual) |
| 27522095 | 1Y | 132.13 | 220.87 | -88.74 | RR02 > RR01 (unusual) |
| 27522095 | 2Y | 229.75 | 625.53 | -395.78 | RR02 > RR01 (unusual) |

**Note**: In this sample, RR02 > RR01, which is atypical. This occurs when the spread propagation effect is negative (opposite direction to direct recovery effect).

---

## 6. Validation Rules

### 6.1 Record-Level Validations

| Rule ID | Field(s) | Validation | Action |
|---------|----------|------------|--------|
| VR-001 | TRADE_NUM | Must be positive integer | Reject |
| VR-002 | FAMILY | Must be valid family code | Reject |
| VR-003 | GROUP | Must be valid group code | Reject |
| VR-004 | PORTFOLIO | Must exist in Bookman hierarchy | Flag |
| VR-005 | ISSUER | Must be populated | Reject |
| VR-006 | RECOVERY_RATE | 0 <= value <= 100 (non-CRDI) | Flag |
| VR-007 | CURRENCY | Must be valid ISO code | Reject |
| VR-008 | MATURITY | Must be valid date | Flag |
| VR-009 | RESTRUCT | Must be 'Yes' or 'NONE' | Flag |

### 6.2 File-Level Validations

| Rule ID | Validation | Action |
|---------|------------|--------|
| VF-001 | File not empty (excluding header) | Warning |
| VF-002 | Header matches expected format | Reject file |
| VF-003 | Row count within expected range | Warning if variance >20% |
| VF-004 | All 20 fields present per row | Reject record |

### 6.3 Cross-Feed Validations

| Rule ID | Feeds | Validation | Action |
|---------|-------|------------|--------|
| VX-001 | RR02, RR01 | Position count match | Warning if different |
| VX-002 | RR02, CR Basis Rate | RR02 ≈ CR Basis Rate | Flag if >1% variance |
| VX-003 | RR02, RR01 | RR02 < RR01 (typical) | Info if RR02 > RR01 |

---

## 7. Interface Schedule

### 7.1 Daily Schedule (GMT)

| Time | Event | Description |
|------|-------|-------------|
| 18:00 | Credit curve calibration | Curves available |
| 18:00 | Recovery rate data | Recovery assumptions |
| 21:00 | Valuation batch complete | Sensitivities calculated |
| 03:00 | Extraction batch start | Regional processing |
| 04:00 | Extraction complete | Files generated |
| 05:00 | Packaging | ZIP file created |
| 05:30 | Delivery | Files available to downstream |

### 7.2 Regional Schedule

| Region | Extraction Start | Extraction End | Delivery |
|--------|------------------|----------------|----------|
| LN | 03:00 GMT | 04:00 GMT | 05:30 GMT |
| HK | 21:00 HKT | 22:00 HKT | 23:30 HKT |
| NY | 22:00 EST | 23:00 EST | 00:30 EST+1 |
| SP | 21:00 SGT | 22:00 SGT | 23:30 SGT |

---

## 8. Error Handling

### 8.1 Error Codes

| Code | Description | Severity | Action |
|------|-------------|----------|--------|
| E001 | Source table unavailable | Critical | Abort extraction |
| E002 | No data returned | Warning | Generate empty file with header |
| E003 | Field validation failure | Error | Reject record |
| E004 | Counterparty lookup failure | Warning | Null CIF/GLOBUS_ID/COUNTRY |
| E005 | File write failure | Critical | Retry, escalate |

### 8.2 Error Recovery

| Scenario | Recovery Action |
|----------|-----------------|
| Valuation incomplete | Wait, re-run after completion |
| Partial extraction failure | Re-run from checkpoint |
| File delivery failure | Retry 3 times, then escalate |
| Data quality issue | Manual review, correction, re-run |

---

## 9. Comparison with Related Feeds

### 9.1 CR RR02 vs CR RR01 vs CR Basis Rate

| Aspect | CR RR02 | CR RR01 | CR Basis Rate |
|--------|---------|---------|---------------|
| **Source Field** | M_RECOVERY1 | M_RECOVERY_ | M_RECOVERY1 |
| **Propagation** | WITHOUT | WITH | WITHOUT |
| **Sensitivity Name** | RR02_SENSI | RR01_SENSI | RECOVERY_RATE_SENSI |
| **Field Count** | 20 | 20 | 20 |
| **Same Source As** | CR Basis Rate | - | CR RR02 |

### 9.2 Source Field Summary

| Source Field | Feeds Using It | Description |
|--------------|----------------|-------------|
| M_RECOVERY_ | CR RR01 | With propagation |
| M_RECOVERY1 | CR RR02, CR Basis Rate | Without propagation |

---

## 10. Downstream Integration

### 10.1 Target Systems

| System | Usage | Key Fields |
|--------|-------|------------|
| Risk Data Warehouse | Storage, reporting | All fields |
| Plato (Risk Engine) | Pure recovery risk | RR02_SENSI, CURRENCY |
| VESPA Reporting | Regulatory reporting | All fields |
| P&L Attribution | Recovery decomposition | RR02_SENSI, RR01_SENSI |
| Model Validation | RR01/RR02 comparison | RR02_SENSI, TRADE_NUM |

### 10.2 Integration Points

| Integration | Protocol | Format |
|-------------|----------|--------|
| Risk DW Load | File-based | CSV |
| Plato Feed | SFTP | CSV (in ZIP) |
| Reporting Extract | Database | Table load |

---

## 11. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [CR RR02 BRD](./cr-rr02-brd.md) | CR-RR02-BRD-001 | Business requirements |
| [CR RR02 IT Config](./cr-rr02-config.md) | CR-RR02-CFG-001 | Technical configuration |
| [CR RR01 IDD](../cr-rr01/cr-rr01-idd.md) | CR-RR01-IDD-001 | With propagation IDD |
| [CR Basis Rate IDD](../cr-basis-rate/cr-basis-rate-idd.md) | CR-BR-IDD-001 | Same source field |
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |

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
| Schema review | On change | As needed |
| Integration review | Quarterly | April 2025 |

---

*End of Document*
