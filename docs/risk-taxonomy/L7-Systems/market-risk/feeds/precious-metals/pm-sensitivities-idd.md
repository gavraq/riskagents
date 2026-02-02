# Precious Metals Sensitivities Feed - Interface Design Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | PMS-IDD-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Interface Overview

### 1.1 Interface Summary

| Attribute | Value |
|-----------|-------|
| **Interface Name** | Precious Metals Sensitivities |
| **Interface ID** | MR-IF-PMS |
| **Direction** | Outbound |
| **Source System** | Murex |
| **Target Systems** | Plato, RDS → VESPA |
| **Frequency** | Daily |
| **Transfer Method** | MFT (Managed File Transfer) |

---

## 2. File Specification

### 2.1 File Details

| Attribute | Value |
|-----------|-------|
| **File Format** | CSV |
| **Delimiter** | Comma (,) or Semicolon (;) |
| **Character Encoding** | UTF-8 |
| **Header Row** | Yes |
| **Trailer Row** | No |
| **Record Terminator** | LF |
| **Decimal Separator** | Period (.) |

### 2.2 File Naming Convention

**Individual Sensitivity Files** (13 per region):
```
MxGTS_Sens_PM_{SensType}_{Region}_{YYYYMMDD}.csv
```

**Combined/Merged File**:
```
MxGTS_Sensitivities_{Region}_{YYYYMMDD}.csv
```

| Component | Description | Values |
|-----------|-------------|--------|
| MxGTS | Murex GTS prefix | Fixed |
| Sens_PM | PM Sensitivity | Fixed |
| {SensType} | Sensitivity type | AdDeltaUSD, AdDeltaOZ, SpotDeltaUSD, SpotDeltaOZ, NominalUSD, NominalOZ, Gamma, Theta, Vanna, Volga, Vega, MetalDV01, WeightedVega |
| {Region} | Trading region | LN, HK, NY, SP |
| {YYYYMMDD} | Business date | Date format |

### 2.3 Package Details

| Attribute | Value |
|-----------|-------|
| **Package Format** | ZIP |
| **Package Pattern** | MxGTS_Sensitivities_{Region}_{YYYYMMDD}.zip |
| **Contents** | Combined sensitivities file |
| **Packaging Script** | process_reports.sh |

---

## 3. Field Specification

### 3.1 Field Layout (26 Fields)

| # | Field Name | Description | Type | Length | Mandatory |
|---|------------|-------------|------|--------|-----------|
| 1 | M_TRADE_NUM | Trade ID | Numeric | 10 | Yes |
| 2 | M_PORTFOLIO | Portfolio code | VarChar | 16 | Yes |
| 3 | PKG_NB | Package reference | Numeric | 10 | No |
| 4 | PKG_TYPOLOGY | Package typology | VarChar | 21 | No |
| 5 | M_PL_INSTRU | PnL instrument label | VarChar | 36 | Yes |
| 6 | M_METAL | Precious metal ISO code | VarChar | 21 | Yes |
| 7 | M_FAMILY | Trade family | VarChar | 16 | Yes |
| 8 | M_GROUP | Trade group | VarChar | 5 | Yes |
| 9 | M_TYPE | Trade type | VarChar | 16 | Yes |
| 10 | M_TYPOLOGY | Trade typology | VarChar | 21 | Yes |
| 11 | M_CALL_PUT | Call/Put indicator | VarChar | 20 | No |
| 12 | M_CLASS_LAB | Typology description | VarChar | 16 | Yes |
| 13 | M_CURRENCY | Trade currency | VarChar | 4 | Yes |
| 14 | M_DEAL_MATU | Deal maturity date | Date | 8 | Yes |
| 15 | M_INDEX | Commodity index | VarChar | 21 | Yes |
| 16 | M_LEADING_C | Leading curve | VarChar | 16 | Yes |
| 17 | M_LOCATION | Commodity location | VarChar | 21 | No |
| 18 | DELIVERY_TYPE | Delivery type (UDF) | VarChar | 15 | No |
| 19 | M_MATURITY | Native/Maturity pillar | VarChar | 21 | Yes |
| 20 | M_STRIKE | Strike price | Numeric | 12 | No |
| 21 | M_UNIT | Unit of measure | VarChar | 21 | Yes |
| 22 | M_PILLAR | Constant maturity pillar | VarChar | 64 | Yes |
| 23 | VEGASTK | Vega delta surface pillar | Numeric | 12 | Conditional |
| 24 | SENS_TYPE | Sensitivity type | VarChar | 24 | Yes |
| 25 | SENS_VALUE | Sensitivity value | Numeric | 18 | Yes |

### 3.2 Field Details

#### Field 1: M_TRADE_NUM
| Attribute | Value |
|-----------|-------|
| **Description** | Unique trade identifier in Murex |
| **Data Type** | Numeric |
| **Length** | 10 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL |
| **Example** | 4E+07 (scientific notation), 40000001 |

#### Field 2: M_PORTFOLIO
| Attribute | Value |
|-----------|-------|
| **Description** | Trading book portfolio code |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL |
| **Example** | PMSGSGB |

#### Field 3: PKG_NB
| Attribute | Value |
|-----------|-------|
| **Description** | Package reference number for structured deals |
| **Data Type** | Numeric |
| **Length** | 10 |
| **Mandatory** | No |
| **Source** | M_PACKAGE in SB_TP_REP |
| **Example** | 0, 12345 |

#### Field 4: PKG_TYPOLOGY
| Attribute | Value |
|-----------|-------|
| **Description** | Typology of the package |
| **Data Type** | VarChar |
| **Length** | 21 |
| **Mandatory** | No |
| **Source** | M_PKG_TYPO in SB_TP_REP |
| **Example** | (blank for non-packaged) |

#### Field 5: M_PL_INSTRU
| Attribute | Value |
|-----------|-------|
| **Description** | Label of the PnL instrument |
| **Data Type** | VarChar |
| **Length** | 36 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL |
| **Example** | COMSpotForward CNH |

#### Field 6: M_METAL
| Attribute | Value |
|-----------|-------|
| **Description** | Precious metal ISO code |
| **Data Type** | VarChar |
| **Length** | 21 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL (Formulas.Product.Label) |
| **Valid Values** | XAU (Gold), XAG (Silver), XPT (Platinum), XPD (Palladium) |
| **Example** | XAU, XAG |

#### Field 7: M_FAMILY
| Attribute | Value |
|-----------|-------|
| **Description** | Trade family classification |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL |
| **Example** | COM |

#### Field 8: M_GROUP
| Attribute | Value |
|-----------|-------|
| **Description** | Trade group classification |
| **Data Type** | VarChar |
| **Length** | 5 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL |
| **Example** | SPOT, SWAP, OPT |

#### Field 9: M_TYPE
| Attribute | Value |
|-----------|-------|
| **Description** | Trade type classification |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL |
| **Example** | PM - SPOT UA, PM - FWD, PM - Fwd put |

#### Field 10: M_TYPOLOGY
| Attribute | Value |
|-----------|-------|
| **Description** | Trade typology code |
| **Data Type** | VarChar |
| **Length** | 21 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL |
| **Valid Values** | PM - FUT, PM - FWD AL, PM - ASIAN OPT OTC, etc. |
| **Example** | PM - SPOT UA |

#### Field 11: M_CALL_PUT
| Attribute | Value |
|-----------|-------|
| **Description** | Call or Put indicator for options |
| **Data Type** | VarChar |
| **Length** | 20 |
| **Mandatory** | No (blank for non-options) |
| **Source** | VW_SENSITIVITIES_ALL (Formulas.Call/Put) |
| **Valid Values** | CALL, PUT, (blank) |
| **Example** | CALL |

#### Field 12: M_CLASS_LAB
| Attribute | Value |
|-----------|-------|
| **Description** | PL Key Category name |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL (Formulas.PL Key.Category.Complete Name) |
| **Example** | COM Simple option, COMSpotForward CNH |

#### Field 13: M_CURRENCY
| Attribute | Value |
|-----------|-------|
| **Description** | Trade currency |
| **Data Type** | VarChar |
| **Length** | 4 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL |
| **Example** | USD, AUD, JPY |

#### Field 14: M_DEAL_MATU
| Attribute | Value |
|-----------|-------|
| **Description** | Maturity date of the trade |
| **Data Type** | Date |
| **Length** | 8 |
| **Format** | YYYYMMDD or DD/MM/YYYY |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL (Formulas.Maturity) |
| **Example** | 09/04/2022, 06/04/2023 |

#### Field 15: M_INDEX
| Attribute | Value |
|-----------|-------|
| **Description** | Underlying commodity index label |
| **Data Type** | VarChar |
| **Length** | 21 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL (Formulas.Index.Label) |
| **Example** | AU.LBMA, AG.LBMA |

#### Field 16: M_LEADING_C
| Attribute | Value |
|-----------|-------|
| **Description** | Leading curve for risk aggregation |
| **Data Type** | VarChar |
| **Length** | 16 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL (RiskEngine.Results.Outputs.Commodities.Curve Risk.Adapted delta.Leading curve) |
| **Example** | AU.LBMA, AG.LBMA |

#### Field 17: M_LOCATION
| Attribute | Value |
|-----------|-------|
| **Description** | Commodity location |
| **Data Type** | VarChar |
| **Length** | 21 |
| **Mandatory** | No |
| **Source** | VW_SENSITIVITIES_ALL (Formulas.Location.Label) |
| **Example** | LONDON, INTRANSIT, UNALLOCATED |

#### Field 18: DELIVERY_TYPE
| Attribute | Value |
|-----------|-------|
| **Description** | Delivery type from trade UDF |
| **Data Type** | VarChar |
| **Length** | 15 |
| **Mandatory** | No |
| **Source** | M_DELIV_TYP in SB_UDF_REP |
| **Valid Values** | PHYSICAL_IMS, UNALLOCATED |
| **Example** | UNALLOCATED |

#### Field 19: M_MATURITY
| Attribute | Value |
|-----------|-------|
| **Description** | Native pillar or maturity label |
| **Data Type** | VarChar |
| **Length** | 21 |
| **Mandatory** | Yes |
| **Source** | NVL(RTRIM(M_MATURITY_), M_NATIVE_PI) from VW_SENSITIVITIES_ALL |
| **Business Rule** | Use M_MATURITY_ if not null, otherwise use M_NATIVE_PI |
| **Example** | SPOT, TODAY, TDY, 3M, 1M |

#### Field 20: M_STRIKE
| Attribute | Value |
|-----------|-------|
| **Description** | Strike price for options |
| **Data Type** | Numeric |
| **Length** | 12 |
| **Mandatory** | No (blank for non-options) |
| **Source** | VW_SENSITIVITIES_ALL (Formulas.Strike) |
| **Example** | 0, 1850.00, 27.5 |

#### Field 21: M_UNIT
| Attribute | Value |
|-----------|-------|
| **Description** | Quotation unit of measure |
| **Data Type** | VarChar |
| **Length** | 21 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL (Formulas.Index.Quotation.Unit) |
| **Example** | OZ TR (Troy Ounce), MMBTU |

#### Field 22: M_PILLAR
| Attribute | Value |
|-----------|-------|
| **Description** | Constant maturity pillar for bucketing |
| **Data Type** | VarChar |
| **Length** | 64 |
| **Mandatory** | Yes |
| **Source** | VW_SENSITIVITIES_ALL (Formulas.Risk date with PM RISK maturity set) |
| **Valid Values** | TODAY, TOM, SPOT, 1W, 1M, 2M, 3M, 4M, 5M, 6M, 9M, 1Y, 18M, 2Y, 3Y, 4Y, 5Y, 10Y |
| **Example** | SPOT, 1M, 3M |

#### Field 23: VEGASTK
| Attribute | Value |
|-----------|-------|
| **Description** | Vega delta surface pillar |
| **Data Type** | Numeric |
| **Length** | 12 |
| **Mandatory** | Conditional (only for Vega and Weighted Vega) |
| **Source** | VW_SENSITIVITIES_ALL (RiskEngine.Results.Outputs.Commodities.Curve Risk.Vega.Pillar.Strike) |
| **Valid Values** | 0, 5, 10, 25, 50, 75, 90, 95 |
| **Business Rule** | Populated only when SENS_TYPE = 'Vega' or 'Weighted Vega'; blank otherwise |
| **Example** | 50, 25, (blank) |

#### Field 24: SENS_TYPE
| Attribute | Value |
|-----------|-------|
| **Description** | Type of sensitivity value |
| **Data Type** | VarChar |
| **Length** | 24 |
| **Mandatory** | Yes |
| **Source** | @MxSensType parameter |
| **Valid Values** | Adapted Delta (OZ), Adapted Delta (USD), Adapted Spot Delta (OZ), Adapted Spot Delta (USD), Nominal (OZ), Nominal (USD), Adapted Gamma (OZ), Theta (USD), Vanna, Volga, Vega, Metal DV01 (USD), Weighted Vega |
| **Example** | Adapted Delta (OZ) |

#### Field 25: SENS_VALUE
| Attribute | Value |
|-----------|-------|
| **Description** | Sensitivity value |
| **Data Type** | Numeric |
| **Length** | 18 |
| **Precision** | Variable (up to 6 decimal places) |
| **Mandatory** | Yes |
| **Source** | @MxSensValue parameter from VW_SENSITIVITIES_ALL |
| **Example** | 6.43, 32151, -48, 1403.6 |

---

## 4. Sample Data

### 4.1 Header Row
```
M_TRADE_NUM,M_PORTFOLIO,PKG_NB,PKG_TYPOLOGY,M_PL_INSTRU,M_METAL,M_FAMILY,M_GROUP,M_TYPE,M_TYPOLOGY,M_CALL_PUT,M_CLASS_LAB,M_CURRENCY,M_DEAL_MATU,M_INDEX,M_LEADING_C,M_LOCATION,DELIVERY_TYPE,M_MATURITY,M_STRIKE,M_UNIT,M_PILLAR,VEGASTK,SENS_TYPE,SENS_VALUE
```

### 4.2 Sample Records

```csv
4E+07,PMSGSGB,0,,XAU,XAU,COM,SPOT,PM - SPOT UA,COMSpotForward CNH,,,AU.LBMA,09/04/2022,AU.LBMA,AU.LBMA,LONDON,UNALLOCATED,SPOT,0,OZ TR,SPOT,,Adapted Delta (OZ),6.43
4E+07,PMSGSGB,0,,XAU,XAU,COM,SPOT,PM - SPOT UA,COMSpotForward CNH,,,AU.LBMA,09/04/2022,AU.LBMA,AU.LBMA,LONDON,UNALLOCATED,SPOT,0,OZ TR,SPOT,,Adapted Delta (USD),6.43
4E+07,PMSGSGB,0,,XAU,XAU,COM,SWAP,PM - FWD XCCY A,COMPhysicalFor,,,AU.LBMA,04/04/2023,AU.LBMA,AU.LBMA,INTRANSIT,PHYSICAL_IMS,TDY,0,OZ TR,TODAY,,Adapted Delta (OZ),32151
4E+07,PMSGSGB,0,,XAU,XAU,COM,SWAP,PM - FWD XCCY A,COMPhysicalFor,JPY,,,AU.LBMA,06/04/2023,AU.LBMA,AU.LBMA,INTRANSIT,PHYSICAL_IMS,SPOT,0,OZ TR,SPOT,,Adapted Delta (OZ),3215
4E+07,PMSGSGB,0,,XAG,XAG,COM,OPT,PM - Fwd put,COMSimple optn,USD,CALL,AG.LBMA,04/03/2023,AG.LBMA,AG.LBMA,LONDON,UNALLOCATED,6M,27.5,OZ TR,9M,50,Vega,643.01
4E+07,PMSGSGB,0,,XAG,XAG,COM,OPT,PM - Fwd put,COMSimple optn,USD,CALL,AG.LBMA,04/03/2023,AG.LBMA,AG.LBMA,LONDON,UNALLOCATED,6M,27.5,OZ TR,9M,25,Vega,1403.6
4E+07,PMSGSGB,0,,XAG,XAG,COM,OPT,PM - Fwd put,COMSimple optn,USD,CALL,AG.LBMA,04/03/2023,AG.LBMA,AG.LBMA,LONDON,UNALLOCATED,6M,27.5,OZ TR,9M,,Adapted Delta (USD),6361
```

**Note**: Each trade may have multiple records:
- Different sensitivity types (13 possible)
- Different tenor pillars (fractional allocation)
- Different delta surface pillars (for Vega/Weighted Vega only)

---

## 5. Data Quality Rules

### 5.1 Validation Rules

| Rule ID | Field | Rule | Severity | Action |
|---------|-------|------|----------|--------|
| DQ-PMS-001 | M_TRADE_NUM | Must be numeric | Critical | Reject |
| DQ-PMS-002 | M_PORTFOLIO | Must not be null | Critical | Reject |
| DQ-PMS-003 | M_METAL | Must be valid PM code (XAU, XAG, XPT, XPD) | High | Warning |
| DQ-PMS-004 | SENS_VALUE | Must be numeric | Critical | Reject |
| DQ-PMS-005 | SENS_TYPE | Must be valid sensitivity type | Critical | Reject |
| DQ-PMS-006 | M_PILLAR | Must be valid PM RISK pillar | High | Warning |
| DQ-PMS-007 | VEGASTK | Must be in (0,5,10,25,50,75,90,95) when populated | High | Warning |
| DQ-PMS-008 | M_TYPOLOGY | Must have PRECIOUS category | Critical | Reject |

### 5.2 Completeness Checks

| Check | Description | Threshold |
|-------|-------------|-----------|
| Record Count | Day-over-day variance | ±20% |
| Sensitivity Type Coverage | All 13 types present | 100% |
| Metal Coverage | All traded metals included | 100% |
| Zero Value Count | Records with SENS_VALUE = 0 | Should be 0 (filtered) |
| Portfolio Coverage | All PM portfolios | 100% |

### 5.3 Cross-Field Validations

| Rule | Description |
|------|-------------|
| VEGASTK populated | Only when SENS_TYPE in ('Vega', 'Weighted Vega') |
| M_CALL_PUT populated | Only for option products (M_GROUP = 'OPT') |
| M_STRIKE populated | Only for option products |

---

## 6. Interface Dependencies

### 6.1 Upstream Dependencies

| System | Data | Timing | Impact if Delayed |
|--------|------|--------|-------------------|
| Market Data | PM curves, volatility surfaces | 18:00 GMT | Sensitivity calculation fails |
| Market Data | FX spot rates | 18:00 GMT | USD conversion fails |
| Valuation Batch | PM sensitivity calculations | 21:00 GMT | Feed cannot run |
| Reference Data | SB_TYPOLOGY_REP | Static | Typology filter fails |
| Reference Data | SB_UDF_REP | Static | Delivery type missing |

### 6.2 Downstream Consumers

| System | Purpose | Frequency |
|--------|---------|-----------|
| Plato | Risk aggregation | Daily |
| RDS → VESPA | VaR calculation | Daily |
| Limit System | PM position monitoring | Daily |
| Risk Control | Daily risk reports | Daily |

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
| Missing sensitivity type | DQ rules | Alert | Risk Control |
| Merge script failure | Script log | Alert | Risk Tech L2 |

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
| Total Adapted Delta USD | Murex | Feed | ±$1,000 |
| Total Vega USD | Murex | Feed | ±$500 |
| Record Count | Murex | Feed | ±5% |
| Trade Count | Murex | Feed | 100% |

### 9.2 Sensitivity Type Reconciliation

For each sensitivity type:
- Sum across all trades must match Murex Risk Engine total
- Sum across pillars must equal trade-level sensitivity
- Sum across delta surface (for Vega) must equal trade-level vega

---

## 10. Change History

| Version | Date | Author | Change Description |
|---------|------|--------|-------------------|
| 1.0 | 2025-01-13 | Risk Technology | Initial document |

---

## Appendix A: Sensitivity Type Reference

| SENS_TYPE | Murex Output | Unit | Discounted | Smile |
|-----------|--------------|------|------------|-------|
| Nominal (OZ) | Adapted delta.Value | OZ.TR | No | No |
| Nominal (USD) | Adapted delta.Value(currency) | USD | No | No |
| Adapted Delta (OZ) | Adapted delta.Value | OZ.TR | Yes | Yes |
| Adapted Delta (USD) | Adapted delta.Value(currency) | USD | Yes | Yes |
| Adapted Spot Delta (OZ) | Adapted spot delta.Value | OZ.TR | Yes | Yes |
| Adapted Spot Delta (USD) | Adapted spot delta.Value(currency) | USD | Yes | Yes |
| Adapted Gamma (OZ) | Adapted gamma.Value | OZ.TR | Yes | Yes |
| Vega | Vega.Value | USD | Yes | No |
| Volga | Volga.Value | USD | Yes | N/A |
| Vanna | Vanna.Value | USD | Yes | N/A |
| Theta (USD) | Theta.Value | USD | Yes | N/A |
| Metal DV01 (USD) | Adapted delta yield.Value | USD | Yes | N/A |
| Weighted Vega | Breakdown formula | USD | Yes | No |

---

## Appendix B: PM RISK Maturity Set

| Pillar Label | Description |
|--------------|-------------|
| TODAY | Current date |
| TOM | Tomorrow |
| SPOT | Spot date (T+2) |
| 1W | 1 Week |
| 1M | 1 Month |
| 2M | 2 Months |
| 3M | 3 Months |
| 4M | 4 Months |
| 5M | 5 Months |
| 6M | 6 Months |
| 9M | 9 Months |
| 1Y | 1 Year |
| 18M | 18 Months |
| 2Y | 2 Years |
| 3Y | 3 Years |
| 4Y | 4 Years |
| 5Y | 5 Years |
| 10Y | 10 Years |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
