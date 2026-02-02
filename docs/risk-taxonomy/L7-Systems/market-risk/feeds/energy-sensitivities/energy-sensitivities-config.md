---
# Document Metadata
document_id: EN-CFG-001
document_name: Energy Sensitivities Feed - IT Configuration
version: 1.0
effective_date: 2025-01-03
next_review_date: 2026-01-03
owner: Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: EN-BRD-001  # Energy Sensitivities BRD
feed_id: EN-001
---

# Energy Sensitivities Feed - IT Configuration

**Meridian Global Bank - Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | EN-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 3 January 2025 |
| **Owner** | Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Configuration Overview

### 1.1 Murex Global Operating Model Components

This document describes the Murex GOM configuration for the Energy Sensitivities feed:

| Component | Greeks | Rho |
|-----------|--------|-----|
| **Simulation View** | SV_MRGR_GREEKS | SV_MRGR_RHO |
| **Datamart Table** | TBL_MRGR_GREEKS_REP | TBL_MRGR_RHO_REP |
| **Dynamic Table** | VW_MRGR_GREEKS | VW_MRGR_RHO |
| **Feeders** | TF_MRGR_GREEKS | TF_MRGR_RHO |
| **Data Extractor** | DE_MRGR | DE_MRGR |
| **Extraction Request** | ER_MRGR | ER_MRGR |

### 1.2 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MUREX VESPA MODULE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────┐              ┌─────────────────┐                   │
│  │ SV_MRGR_GREEKS  │              │  SV_MRGR_RHO    │                   │
│  │  6 outputs      │              │  2 outputs      │                   │
│  │  22 breakdowns  │              │  12 breakdowns  │                   │
│  └────────┬────────┘              └────────┬────────┘                   │
│           │                                │                            │
│           ▼                                ▼                            │
│  ┌─────────────────┐              ┌─────────────────┐                   │
│  │ TF_MRGR_GREEKS  │              │  TF_MRGR_RHO    │                   │
│  │   (Feeder)      │              │   (Feeder)      │                   │
│  └────────┬────────┘              └────────┬────────┘                   │
│           │                                │                            │
│           ▼                                ▼                            │
│  ┌─────────────────┐              ┌─────────────────┐                   │
│  │TBL_MRGR_GREEKS  │              │TBL_MRGR_RHO     │                   │
│  │     _REP        │              │     _REP        │                   │
│  └────────┬────────┘              └────────┬────────┘                   │
│           │                                │                            │
│           └────────────────┬───────────────┘                            │
│                            │                                            │
│                            ▼                                            │
│                   ┌─────────────────┐                                   │
│                   │    DE_MRGR      │                                   │
│                   │  (Extractor)    │                                   │
│                   │  UNION ALL      │                                   │
│                   └────────┬────────┘                                   │
│                            │                                            │
│                            ▼                                            │
│                   ┌─────────────────┐                                   │
│                   │    ER_MRGR      │                                   │
│                   │(Extr. Request)  │                                   │
│                   └────────┬────────┘                                   │
│                            │                                            │
└────────────────────────────┼────────────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ MxMGB_MR_Energy │
                    │ _Sens_**_.csv   │
                    └─────────────────┘
```

---

## 2. Simulation View Configuration

### 2.1 SV_MRGR_GREEKS

| Property | Value |
|----------|-------|
| **View Name** | SV_MRGR_GREEKS |
| **View Type** | Simulation |
| **Outputs** | 6 |
| **Breakdowns** | 22 |

#### 2.1.1 Outputs

| # | Output | Dictionary Path |
|---|--------|-----------------|
| 1 | Price | RiskEngine.Results.Outputs.Commodities.Curve Risk.Delta.Price |
| 2 | Delta | RiskEngine.Results.Outputs.Commodities.Curve Risk.Delta.Value |
| 3 | Adapted delta | RiskEngine.Results.Outputs.Commodities.Curve Risk.Adapted delta.Value |
| 4 | Gamma | RiskEngine.Results.Outputs.Commodities.Curve Risk.Gamma.Value |
| 5 | Theta | RiskEngine.Results.Outputs.Commodities.Curve Risk.Theta.Value |
| 6 | Vega | RiskEngine.Results.Outputs.Commodities.Curve Risk.Vega.Value |

#### 2.1.2 Breakdowns

| # | Breakdown | Dictionary Path | Type |
|---|-----------|-----------------|------|
| 1 | Portfolio | Formulas.Portfolio | Hierarchy |
| 2 | Family | Formulas.Family | Static |
| 3 | Group | Formulas.Group | Static |
| 4 | Type | Formulas.Type | Static |
| 5 | Trade number | Formulas.Trade number | Static |
| 6 | Global ID | Formulas.Global ID | Static |
| 7 | Deal Maturity | Formulas.Deal Maturity | Date |
| 8 | Typology | Formulas.Typology | Static |
| 9 | Label | Formulas.Label (×4) | Static |
| 10 | PILLARS | Formulas.PILLARS | Static |
| 11 | Curve name | Formulas.Curve name | Static |
| 12 | Maturity | Formulas.Maturity | Date |
| 13 | Market price | Formulas.Market price | Numeric |
| 14 | Currency | Formulas.Currency | Static |
| 15 | Unit | Formulas.Index.Quotation.Unit | Static |
| 16 | PL Instrument | Formulas.PL Instrument | Static |
| 17 | Status | Formulas.Status | Static |
| 18 | Val Status | Formulas.Val Status | Static |
| 19 | Underlying | Formulas.Underlying | Static |

### 2.2 SV_MRGR_RHO

| Property | Value |
|----------|-------|
| **View Name** | SV_MRGR_RHO |
| **View Type** | Simulation |
| **Outputs** | 2 |
| **Breakdowns** | 12 |

#### 2.2.1 Outputs

| # | Output | Dictionary Path |
|---|--------|-----------------|
| 1 | Yield zero rate | RiskEngine.Results.Outputs.Interest rates.Delta.Zero.Rate |
| 2 | DV01 (zero) | RiskEngine.Results.Outputs.Interest rates.Delta.Zero.Value |

#### 2.2.2 Breakdowns

| # | Breakdown | Dictionary Path | Type |
|---|-----------|-----------------|------|
| 1 | Curve name | RiskEngine.Results.Outputs.Interest rates.Delta.Zero.Curve key.Curve name | Static |
| 2 | Portfolio | Formulas.Portfolio | Hierarchy |
| 3 | Family | Formulas.Family | Static |
| 4 | Group | Formulas.Group | Static |
| 5 | Type | Formulas.Type | Static |
| 6 | Trade Number | Formulas.Trade Number | Static |
| 7 | Global ID | Formulas.Global ID | Static |
| 8 | PL Instrument | Formulas.PL Instrument | Static |
| 9 | Currency | Formulas.Currency | Static |
| 10 | Typology | Formulas.Typology | Static |
| 11 | Deal Maturity | Formulas.Deal Maturity | Date |
| 12 | Date | RiskEngine.Results.Outputs.Interest rates.Delta.Zero.Date | Date |

#### 2.2.3 Maturity Set Configuration

| Property | Value |
|----------|-------|
| **Maturity Set** | SV_MRGR_IR |
| **Display Mode** | Label |
| **Bucket Type** | Pillars |
| **Split Mode** | Surrounding pillars |

**Pillars**: O/N, T/N, 1W, 2W, 1M, 2M, 3M, 4M, 5M, 6M, 7M, 8M, 9M, 10M, 11M, 1Y, 2Y, 3Y, 4Y, 5Y, 7Y, 10Y, 15Y, 20Y, 25Y, 30Y

---

## 3. Feeder Configuration

### 3.1 Greeks Feeders

#### 3.1.1 Regional Configuration

| Region | Processing Script | Batch | Global Filter |
|--------|-------------------|-------|---------------|
| HK | HK_MRGR_GRKS_FDR | BF_MRGR_GRKS_HK | GF_HK_FOLIOS_CMGRK |
| LN | LN_MRGR_GRKS_FDR | BF_MRGR_GRKS_LN | GF_LN_FOLIOS_CMGRK |
| NY | NY_MRGR_GRKS_FDR | BF_MRGR_GRKS_NY | GF_NY_PFOLIO_CMGRK |
| SP | SP_MRGR_GRKS_FDR | BF_MRGR_GRKS_SP | GF_SP_FOLIOS_CMGRK |

#### 3.1.2 Portfolio Nodes (Greeks)

| Region | Portfolio Nodes |
|--------|-----------------|
| HK | LMHK, PMSG |
| LN | FXDLN, IRLN, LMLN, PMLN |
| NY | LMNY |
| SP | LMSP |

**Note**: Precious metal portfolios PMNY and PMSG are **excluded** from Greeks feeders.

#### 3.1.3 Feeder Target

| Property | Value |
|----------|-------|
| **Feeder** | TF_MRGR_GREEKS |
| **Datamart Table** | TBL_MRGR_GREEKS_REP |
| **Dynamic Table** | VW_MRGR_GREEKS |
| **Simulation View** | SV_MRGR_GREEKS |

### 3.2 Rho Feeders

#### 3.2.1 Regional Configuration

| Region | Processing Script | Batch | Global Filter |
|--------|-------------------|-------|---------------|
| HK | HK_MRGR_RHO_FDR | BF_MRGR_RHO_HK | GF_HK_FOLIOS_RD_RHO |
| LN | LN_MRGR_RHO_FDR | BF_MRGR_RHO_LN | GF_LN_FOLIOS_RD_RHO |
| NY | NY_MRGR_RHO_FDR | BF_MRGR_RHO_NY | GF_NY_FOLIOS_RD_RHO |
| SP | SP_MRGR_RHO_FDR | BF_MRGR_RHO_SP | GF_SP_FOLIOS_RD_RHO |

#### 3.2.2 Portfolio Nodes (Rho)

| Region | Portfolio Nodes |
|--------|-----------------|
| HK | LMHK, PMSG |
| LN | FXDLN, IRLN, LMLN, PMLN |
| NY | LMNY, PMNY |
| SP | LMSP |

**Note**: Precious metal portfolios PMNY and PMSG are **included** in Rho feeders.

#### 3.2.3 Feeder Target

| Property | Value |
|----------|-------|
| **Feeder** | TF_MRGR_RHO |
| **Datamart Table** | TBL_MRGR_RHO_REP |
| **Dynamic Table** | VW_MRGR_RHO |
| **Simulation View** | SV_MRGR_RHO |

### 3.3 Product Filtering (Global Filters)

All global filters include commodity product filtering using Family/Group/Type:

```
COM|ASIAN|
COM|ASIAN|CLR
COM|FUT|
COM|FWD|
COM|OFUT|LST
COM|OFUT|OTC
COM|OPT|SMP
COM|OPT|SWAP
COM|SPOT|
COM|SWAP|
COM|SWAP|CLR
COM|SWAP|PHYS
```

---

## 4. Datamart Tables

### 4.1 TBL_MRGR_GREEKS_REP

| Column | Type | Description |
|--------|------|-------------|
| M_PORTFOLIO | VARCHAR2(20) | Trading portfolio |
| M_PL_INSTRU | VARCHAR2(30) | PL Instrument |
| M_CURVE_NAM | VARCHAR2(50) | Commodity curve name |
| M_PILLARS | VARCHAR2(10) | Tenor pillar |
| M_UNIT | VARCHAR2(21) | Quotation unit |
| M_PRICE | NUMBER(16,6) | Commodity price |
| M_DELTA | NUMBER(15,6) | Standard delta |
| M_ADAPTED_D | NUMBER(15,6) | Adapted delta |
| M_GAMMA | NUMBER(15,6) | Gamma |
| M_THETA | NUMBER(15,6) | Theta |
| M_VEGA | NUMBER(15,6) | Vega |
| M_CURRENCY | VARCHAR2(4) | Currency |
| M_TRADE_NUM | NUMBER(10) | Trade number |
| M_FAMILY | VARCHAR2(16) | Family |
| M_GROUP | VARCHAR2(5) | Group |
| M_TYPOLOGY | VARCHAR2(21) | Typology |
| M_UNDERLYIN | VARCHAR2(30) | Underlying |
| M_MARKET_PR | NUMBER(16,6) | Market price |
| M_LABEL2 | VARCHAR2(30) | Product label |
| M_U_PROJ_NAM | VARCHAR2(30) | CER project name |
| M_REF_DATA | NUMBER(10) | Reference data key |

### 4.2 TBL_MRGR_RHO_REP

| Column | Type | Description |
|--------|------|-------------|
| M_PORTFOLIO | VARCHAR2(20) | Trading portfolio |
| M_CURRENCY | VARCHAR2(4) | Currency |
| M_DATE | VARCHAR2(10) | Pillar date |
| M_DV01__ZER | NUMBER(16,4) | DV01 (zero) |
| M_TRADE_NUM | NUMBER(10) | Trade number |
| M_FAMILY | VARCHAR2(16) | Family |
| M_GROUP | VARCHAR2(5) | Group |
| M_TYPOLOGY | VARCHAR2(21) | Typology |
| M_REF_DATA | NUMBER(10) | Reference data key |

---

## 5. Extraction Configuration

### 5.1 Data Extractor

| Property | Value |
|----------|-------|
| **Extractor Name** | DE_MRGR |
| **Type** | SQL |
| **Source Tables** | TBL_MRGR_GREEKS_REP, TBL_MRGR_RHO_REP |
| **Join Tables** | SB_PF_REP, SB_TP_REP, SB_TP_BD_REP |

### 5.2 Extraction Request

| Property | Value |
|----------|-------|
| **Request Name** | ER_MRGR |
| **Output Format** | CSV |
| **Delimiter** | Semicolon (;) |
| **Encoding** | UTF-8 |

### 5.3 Regional Extraction Batches

| Region | Processing Script | Batch | Output File |
|--------|-------------------|-------|-------------|
| HK | HK_MRGRNLI_RPT | BE_MRGRNLI_HK | MxMGB_MR_Energy_Sens_HK_yyyymmdd.csv |
| LN | LN_MRGRNLI_RPT | BE_MRGRNLI_LN | MxMGB_MR_Energy_Sens_LN_yyyymmdd.csv |
| NY | NY_MRGRNLI_RPT | BE_MRGRNLI_NY | MxMGB_MR_Energy_Sens_NY_yyyymmdd.csv |
| SP | SP_MRGRNLI_RPT | BE_MRGRNLI_SP | MxMGB_MR_Energy_Sens_SP_yyyymmdd.csv |

### 5.4 Extraction Parameters

| Parameter | Description | Usage |
|-----------|-------------|-------|
| @MxParentNode | Portfolio parent node | Portfolio hierarchy filtering |
| @RiskType | Risk type (LINEAR/NON-LINEAR) | Product classification filtering |
| @MxDataSetKey | Market data set reference | Regional data set selection |

### 5.5 Extraction SQL Overview

The extraction uses a **UNION ALL** structure combining Greeks and Rho:

```sql
SELECT /* Common columns */
FROM (
    -- Greeks subquery
    SELECT /* Greeks columns, TXV_RHO = 0 */
    FROM TBL_MRGR_GREEKS_REP GREEKS
    INNER JOIN SB_PF_REP PF ON ...
    LEFT JOIN SB_TP_REP TP ON ...
    LEFT JOIN SB_TP_BD_REP TP_BD ON ...
    WHERE PF.M_H_FATHER = @MxParentNode

    UNION ALL

    -- Rho subquery
    SELECT /* Rho columns, Greeks = 0 */
    FROM TBL_MRGR_RHO_REP IR
    INNER JOIN SB_PF_REP PF ON ...
    LEFT JOIN SB_TP_REP TP ON ...
    WHERE PF.M_H_FATHER = @MxParentNode
    GROUP BY ...
    HAVING sum(M_DV01__ZER*100) <> 0
) MRGR
WHERE RISK_TYPE = @RiskType
GROUP BY ...
HAVING sum(TXV_DELTA) <> 0 OR sum(TXV_GAMMA) <> 0
    OR sum(TXV_VEGA) <> 0 OR sum(TXV_THETA) <> 0
    OR sum(TXV_RHO) <> 0
ORDER BY TP_PFOLIO, XV_INSTR, XV_CALMAT, XV_UNIT
```

---

## 6. Post-Processing

### 6.1 File Merge Script

| Property | Value |
|----------|-------|
| **Script Name** | merge_files.sh |
| **Config File** | MERGE_MRGRNLI_RPT.cfg |
| **Purpose** | Merge regional files before delivery |

**Note**: The merge configuration currently only mentions NY region. Other regions may not be included in the final merged file. This should be reviewed for regional completeness.

### 6.2 Output Directory

| Property | Value |
|----------|-------|
| **Directory** | ./reports/today/eod |
| **File Pattern** | MxMGB_MR_Energy_Sens_{Region}_{YYYYMMDD}.csv |

---

## 7. Market Data Sets

| Region | Market Data Set | Description |
|--------|-----------------|-------------|
| LN | MGB_LN_EOD | London end-of-day prices |
| HK | MGB_HK_EOD | Hong Kong end-of-day prices |
| NY | MGB_NY_EOD | New York end-of-day prices |
| SP | MGB_SP_EOD | Singapore end-of-day prices |

---

## 8. Batch Event Schedule

### 8.1 Feeder Batches

| Batch | Start Time (GMT) | Dependencies |
|-------|------------------|--------------|
| BF_MRGR_GRKS_LN | 03:00 | Valuation complete |
| BF_MRGR_RHO_LN | 03:00 | Valuation complete |
| BF_MRGR_GRKS_HK | 03:00 | Valuation complete |
| BF_MRGR_RHO_HK | 03:00 | Valuation complete |
| BF_MRGR_GRKS_NY | 03:00 | Valuation complete |
| BF_MRGR_RHO_NY | 03:00 | Valuation complete |
| BF_MRGR_GRKS_SP | 03:00 | Valuation complete |
| BF_MRGR_RHO_SP | 03:00 | Valuation complete |

### 8.2 Extraction Batches

| Batch | Start Time (GMT) | Dependencies |
|-------|------------------|--------------|
| BE_MRGRNLI_LN | 04:00 | BF_MRGR_GRKS_LN, BF_MRGR_RHO_LN |
| BE_MRGRNLI_HK | 04:00 | BF_MRGR_GRKS_HK, BF_MRGR_RHO_HK |
| BE_MRGRNLI_NY | 04:00 | BF_MRGR_GRKS_NY, BF_MRGR_RHO_NY |
| BE_MRGRNLI_SP | 04:00 | BF_MRGR_GRKS_SP, BF_MRGR_RHO_SP |

---

## 9. Delivery Configuration

### 9.1 MFT Details

| Property | Value |
|----------|-------|
| **MFT ID** | MurexMGBMrgrnliToVespa |
| **Protocol** | SFTP |
| **Target Systems** | Plato, RDS |
| **Delivery Time** | 05:30 GMT |

### 9.2 File Packaging

| Property | Value |
|----------|-------|
| **Archive Format** | ZIP |
| **File Pattern** | MxMGB_MR_Energy_Sens_{Region}_{YYYYMMDD}.zip |

---

## 10. Related Documents

| Document | ID | Relationship |
|----------|-----|-------------|
| [Energy Sensitivities Overview](./energy-sensitivities-overview.md) | EN-OVW-001 | Parent document |
| [Energy Sensitivities BRD](./energy-sensitivities-brd.md) | EN-BRD-001 | Business requirements |
| [Energy Sensitivities IDD](./energy-sensitivities-idd.md) | EN-IDD-001 | Interface design |
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Feed family parent |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-03 | Initial version | Risk Technology |

### 11.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Technical review | Annual | January 2026 |
| Configuration audit | Quarterly | April 2025 |

---

*End of Document*
