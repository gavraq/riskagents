# FX Vega Sensitivities - IT Configuration Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | FXV-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Murex Global Operating Model Overview

This document describes the Murex GOM configuration for FX Vega Sensitivities (referred to as "FX Vega StkMat" as the Vega is based on Strike & Maturity).

### 1.1 Component Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FX Vega GOM Component Flow                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────┐                                               │
│  │ Processing Script   │                                               │
│  │ **_QFX_VEG_STKMT_FDR│                                               │
│  └──────────┬──────────┘                                               │
│             │                                                           │
│             ▼                                                           │
│  ┌─────────────────────┐                                               │
│  │ Feeder              │                                               │
│  │ TF_QFX_VEGA_STKMAT  │                                               │
│  └──────────┬──────────┘                                               │
│             │                                                           │
│             ▼                                                           │
│  ┌─────────────────────┐    ┌─────────────────────┐                   │
│  │ Simulation View     │◄───│ Dynamic Table       │                   │
│  │ FX_VEGA_MATURITY    │    │ VW_QFX_VEGA_STKMAT  │                   │
│  └──────────┬──────────┘    └─────────────────────┘                   │
│             │                                                           │
│             ▼                                                           │
│  ┌─────────────────────┐                                               │
│  │ Datamart Table      │                                               │
│  │ SB_QFX_VEGASTK.REP  │                                               │
│  └──────────┬──────────┘                                               │
│             │                                                           │
│             ▼                                                           │
│  ┌─────────────────────┐    ┌─────────────────────┐                   │
│  │ Data Extractor      │    │ Extraction Request  │                   │
│  │ DE_QFX_VEGA_STKMAT  │───►│ ER_QFX_STK_MAT      │                   │
│  └──────────┬──────────┘    └─────────────────────┘                   │
│             │                                                           │
│             ▼                                                           │
│  ┌─────────────────────┐                                               │
│  │ Output File         │                                               │
│  │ MxGTS_Vespa_FX_Vega │                                               │
│  │ _StkMat_**_yyyymmdd │                                               │
│  └─────────────────────┘                                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Market Data Sets

### 2.1 Official Market Data Sets

| Region | Market Data Set | Description |
|--------|-----------------|-------------|
| London | LNCLOSE | London end-of-day market data |
| Hong Kong | HKCLOSE | Hong Kong end-of-day market data |
| New York | NYCLOSE | New York end-of-day market data |
| Sao Paulo | SPCLOSE | Sao Paulo end-of-day market data |

---

## 3. Simulation View Configuration

### 3.1 FX_VEGA_MATURITY Simulation View

| Attribute | Value |
|-----------|-------|
| **View Name** | FX_VEGA_MATURITY |
| **Purpose** | Strike & maturity based FX vega calculation |
| **Mode** | Detailed |
| **Outputs** | 3 (1 active, 2 deprecated) |
| **Breakdowns** | 8 |

### 3.2 Outputs

| Output | Dictionary Path | Definition | Status |
|--------|-----------------|------------|--------|
| **fx_vega_usd** | Risk Engine.Results.Outputs.Fx.Vega.Value | FX vega in USD. Change in market value for 1% move in volatility. Discounted from settlement date to today. Zero day FX spot rate used for USD conversion. | Active |
| FX Default Vega | - | - | **Deprecated** |
| FX Vega Without Splitting | - | - | **Deprecated** |

### 3.3 Breakdowns

| Breakdown | Dictionary Path | Definition |
|-----------|-----------------|------------|
| **Portfolio** | - | Portfolio of the trade |
| **Trade Number** | - | Unique trade identifier |
| **Contract** | Formulas.FX contract.Label | Label of the FX contract (currency pair) |
| **vega_date** | Risk Engine.Results.Outputs.Fx.Vega.Date | Date at which the underlying volatility is interpolated |
| **vega_pillar** | Risk Engine.Results.Outputs.Fx.Vega.Date | References pillars of RISK_VIEW4 maturity set for the risk date |
| **parallel_fx_vega** | Risk Engine.Results.Outputs.Fx.Vega.Strike | Vega strikes (0, 5, 10, 25, 50, 75, 90, 95, 100) of the volatility curve |
| **Instrument** | Risk Engine.Source.Trade.Elements.Body.Body desc.Evaluation.Instrument | Label of the instrument (e.g., Quanto Forward Swap, QFX Range Accrual) |
| **Model** | Risk Engine.Source.Trade.Elements.Body.Body desc.Evaluation.Model | Label of the default model assigned for the instrument |

### 3.4 Maturity Set Configuration (RISK_VIEW4)

| Setting | Value |
|---------|-------|
| **Mat. Source** | Maturity Set |
| **Disp. maturity set** | RISK_VIEW4 |
| **Bucket type** | Pillars |
| **Reduced label** | Yes |
| **Standard labels** | Yes |
| **Display Mode** | Label |
| **Split Mode** | Nearest pillar |

**RISK_VIEW4 Pillars**:
O/N, T/N, 1W, 2W, 1M, 2M, 3M, 6M, 9M, 1Y, 18M, 2Y, 3Y, 4Y, 5Y, 6Y, 7Y, 8Y, 9Y, 10Y, 12Y, 15Y, 20Y, 25Y, 30Y, 35Y

**Pillar Assignment**: Sensitivities are "bucketed" into pillars. When a cash flow falls between pillar dates, the contribution is split between adjacent pillars weighted by distance from each pillar date. Pillar dates are computed dynamically from the reference date.

---

## 4. Feeder Configuration

### 4.1 Feeder Component

| Attribute | Value |
|-----------|-------|
| **Feeder Name** | TF_QFX_VEGA_STKMAT |
| **Dynamic Table** | VW_QFX_VEGA_STKMAT |
| **Datamart Table** | SB_QFX_VEGASTK.REP |
| **Simulation View** | FX_VEGA_MATURITY |

### 4.2 Regional Feeder Configuration

| Region | Processing Script | Batch | Global Filter | Portfolio Nodes |
|--------|-------------------|-------|---------------|-----------------|
| HKG | HK_QFX_VEG_STKMT_FDR | BF_QFX_VG_ST_HK | GF_HK_PFOLIOS_RD | LMHK, PMSG |
| LDN | LN_QFX_VEG_STKMT_FDR | BF_QFX_VG_ST_LN | GF_LN_PFOLIOS_RD | FXDLN, IRLN, LMLN, PMLN |
| NYK | NY_QFX_VEG_STKMT_FDR | BF_QFX_VG_ST_NY | GF_NY_PFOLIOS_RD | LMNY, PMNY |
| SAO | SP_QFX_VEG_STKMT_FDR | BF_QFX_VG_ST_SP | GF_SP_PFOLIOS_RD | LMSP |

### 4.3 Portfolio Filtering (Level 4 Nodes)

| Region | Portfolio Nodes | Notes |
|--------|-----------------|-------|
| London | FXDLN, IRLN, LMLN, PMLN | Full coverage |
| New York | PMNY, LMNY | Full coverage |
| Hong Kong/Singapore | PMSG, LMHK | **FXHKSBL not selected** |
| Sao Paulo | LMSP | Full coverage |

### 4.4 Transaction Filtering

The dynamic table VW_QFX_VEGA_STKMAT applies the following filters:

| Filter | Value | Description |
|--------|-------|-------------|
| **Transaction Types** | Interest rate swaps, Default swaps | Only these transaction types included |
| **Deal Status** | Not DEAD | Excludes dead deals |
| **Simulation Mode** | Detailed | Full trade-level granularity |

**Products in Scope**: QFX Range Accruals, Quanto Forward Swaps, and other exotic instruments with FX vega sensitivity.

---

## 5. Data Extractor Configuration

### 5.1 Extraction Components

| Region | Processing Script | Batch | Data Extractor | Extraction Request |
|--------|-------------------|-------|----------------|-------------------|
| HKG | HK_QFX_VEG_STKMT_RPT | BE_QFX_VG_ST_HK | DE_QFX_VEGA_STKMAT | ER_QFX_STK_MAT |
| LDN | LN_QFX_VEG_STKMT_RPT | BE_QFX_VG_ST_LN | DE_QFX_VEGA_STKMAT | ER_QFX_STK_MAT |
| NYK | NY_QFX_VEG_STKMT_RPT | BE_QFX_VG_ST_NY | DE_QFX_VEGA_STKMAT | ER_QFX_STK_MAT |
| SAO | SP_QFX_VEG_STKMT_RPT | BE_QFX_VG_ST_SP | DE_QFX_VEGA_STKMAT | ER_QFX_STK_MAT |

### 5.2 Extraction SQL Request

```sql
SELECT  SBL.M_PORTFOLIO,
        SBL.M_TRADE_NUM,
        SBL.M_LABEL,
        CASE WHEN SBL.M_INSTRUMEN = 'QFX Range Accrua'
             THEN 'IRD_IRS_RA'
             WHEN SBL.M_INSTRUMEN = 'Quanto Forward S'
             THEN 'IRD_IRS_FX'
             WHEN SBL.M_INSTRUMEN = 'QIR Range Accrua'
             THEN 'IRD_IRS_RA'
             WHEN SBL.M_INSTRUMEN = 'Insurance Instru'
             THEN 'CRD_CDS_INS'
             WHEN SBL.M_INSTRUMEN = 'Guarantee Instru'
             THEN 'CRD_CDS_GUA'
             ELSE ''
        END as INSTRUMENT_TYPE,
        SUBSTR(FX.M_QUOTMODE0,1,3),
        CASE
             WHEN SBL.M_VEGA_STK < 50.0 THEN 'Call'
             WHEN SBL.M_VEGA_STK > 50.0 THEN 'Put'
             ELSE 'ATM'
        END,
        SBL.M_VEGA_MAT,
        SUBSTR(TO_CHAR(SBL.M_VEGA_MATD,'mm/dd/yyyy'),7,10)
             || '-' || SUBSTR(TO_CHAR(SBL.M_VEGA_MATD,'mm/dd/yyyy'),1,2)
             || '-' || CAST(EXTRACT(DAY FROM
                       TO_TIMESTAMP(TO_CHAR(SBL.M_VEGA_MATD,'YYYY-MM-DD HH24:MI:SS'),
                       'YYYY-MM-DD HH24:MI:SS')) AS VARCHAR2(30)),
        SBL.M_VEGA_STK,
        SBL.M_VEGA_USD,
        'USD'
FROM    DM.SB_QFX_VEGASTK_REP SBL
LEFT OUTER JOIN DM.TBL_FX_CNT_REP FX
        ON SBL.M_LABEL = FX.M_LABEL
        AND SBL.M_REF_DATA = FX.M_REF_DATA
JOIN    DM.SB_TP_REP TP
        ON TP.M_REF_DATA = SBL.M_REF_DATA
        AND TP.M_NB = SBL.M_TRADE_NUM
        AND TP.M_TP_LENTDSP = @LegalEntity:C
WHERE   M_VEGA_MAT IS NOT NULL
        AND M_VEGA_STK > 0
        AND SBL.M_REF_DATA = @MxDataSetKey:N
ORDER BY SBL.M_PORTFOLIO,
         SBL.M_TRADE_NUM,
         SBL.M_LABEL,
         SBL.M_VEGA_MATD,
         SBL.M_VEGA_STK
```

### 5.3 SQL Logic Explanation

| Component | Purpose |
|-----------|---------|
| **Main Table** | SB_QFX_VEGASTK_REP - FX vega datamart |
| **TBL_FX_CNT_REP Join** | Get first currency of default spot quotation mode (USD/JPY) |
| **SB_TP_REP Join** | Filter by legal entity parameter |
| **CASE (Instrument)** | Map Murex instruments to standardized type codes |
| **CASE (Call/Put)** | Determine option type from strike level |
| **Date Formatting** | Convert M_VEGA_MATD to YYYY-MM-DD format |
| **WHERE Filters** | Exclude null maturity, strike ≤ 0, filter by data set |
| **ORDER BY** | Sort by portfolio, trade, label, date, strike |

### 5.4 Instrument Type Mapping

| Murex Instrument | Mapped Type | Description |
|------------------|-------------|-------------|
| QFX Range Accrua | IRD_IRS_RA | Quanto FX Range Accrual |
| Quanto Forward S | IRD_IRS_FX | Quanto Forward Swap |
| QIR Range Accrua | IRD_IRS_RA | Quanto IR Range Accrual |
| Insurance Instru | CRD_CDS_INS | Insurance Instrument |
| Guarantee Instru | CRD_CDS_GUA | Guarantee Instrument |
| (Other) | '' | Empty string |

### 5.5 Call/Put/ATM Logic

| Condition | Output | Description |
|-----------|--------|-------------|
| M_VEGA_STK < 50.0 | Call | Out-of-the-money call |
| M_VEGA_STK > 50.0 | Put | Out-of-the-money put |
| M_VEGA_STK = 50.0 | ATM | At-the-money |

---

## 6. Reference Tables

### 6.1 TBL_FX_CNT_REP

| Attribute | Description |
|-----------|-------------|
| **Purpose** | FX contract definitions and quotation modes |
| **Key Fields** | M_LABEL, M_REF_DATA, M_QUOTMODE0 |
| **Usage** | Extract first currency of default spot quotation mode |

### 6.2 SB_TP_REP

| Attribute | Description |
|-----------|-------------|
| **Purpose** | Trade repository for legal entity lookup |
| **Key Fields** | M_REF_DATA, M_NB, M_TP_LENTDSP |
| **Usage** | Filter trades by legal entity parameter |

---

## 7. Output File Configuration

### 7.1 File Details

| Attribute | Value |
|-----------|-------|
| **File Pattern** | MxGTS_Vespa_FX_Vega_StkMat_{Region}_{YYYYMMDD}.csv |
| **Output Directory** | ./reports/today/eod |
| **Package Pattern** | MxGTS_Vespa_Sensitivities_{Region}_{YYYYMMDD}.zip |
| **Packaging Script** | process_reports.sh |

### 7.2 Regional File Names

| Region | File Name Pattern |
|--------|-------------------|
| London | MxGTS_Vespa_FX_Vega_StkMat_LN_{YYYYMMDD}.csv |
| Hong Kong | MxGTS_Vespa_FX_Vega_StkMat_HK_{YYYYMMDD}.csv |
| New York | MxGTS_Vespa_FX_Vega_StkMat_NY_{YYYYMMDD}.csv |
| Sao Paulo | MxGTS_Vespa_FX_Vega_StkMat_SP_{YYYYMMDD}.csv |

---

## 8. Delivery Configuration

### 8.1 MFT Configuration

| Target | MFT ID Pattern |
|--------|----------------|
| Plato | MurexGTSSensitivitiesToPlato_{Region} |
| RDS | MurexGTSSensitivitiesToRDS_{Region} |

### 8.2 Regional MFT IDs

| Region | Plato MFT ID | RDS MFT ID |
|--------|--------------|------------|
| LDN | MurexGTSSensitivitiesToPlato_LN | MurexGTSSensitivitiesToRDS_LN |
| HKG | MurexGTSSensitivitiesToPlato_HK | MurexGTSSensitivitiesToRDS_HK |
| NYK | MurexGTSSensitivitiesToPlato_NY | MurexGTSSensitivitiesToRDS_NY |
| SAO | MurexGTSSensitivitiesToPlato_SP | MurexGTSSensitivitiesToRDS_SP |

---

## 9. Configuration Summary

| Component | FX Vega Configuration |
|-----------|----------------------|
| **Simulation View** | FX_VEGA_MATURITY |
| **Dynamic Table** | VW_QFX_VEGA_STKMAT |
| **Datamart Table** | SB_QFX_VEGASTK.REP |
| **Feeder** | TF_QFX_VEGA_STKMAT |
| **Data Extractor** | DE_QFX_VEGA_STKMAT |
| **Extraction Request** | ER_QFX_STK_MAT |
| **Output Fields** | 11 |
| **Maturity Set** | RISK_VIEW4 (26 pillars) |
| **Strike Levels** | 0-100 delta |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
