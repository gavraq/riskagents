# Precious Metals Sensitivities Feed - IT Configuration Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | PMS-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Murex Global Operating Model Components

### 1.1 Component Summary

| Component Type | Name | Purpose |
|---------------|------|---------|
| Simulation View | VW_SENSITIVITIES_ALL | Calculate 13 sensitivities + 21 breakdowns |
| Datamart Table | SB_SENSITIVITIES.REP | Store feeder results |
| Feeder | TF_SENS_ALL | Populate datamart from simulation view |
| Data Extractor | DE_SENSITIVITIES_ALL | SQL extraction with parameterized sensitivity |
| Extraction Request | ER_SENSITIVITIES_ALL | Execute extraction for all 13 sensitivities |

---

## 2. Simulation View Configuration

### 2.1 View: VW_SENSITIVITIES_ALL

This is a **shared simulation view** used by multiple commodity sensitivity feeds (Precious Metals, Base Metals).

#### 2.1.1 Outputs (13 Sensitivities)

| Output | Dictionary Path | Settings |
|--------|-----------------|----------|
| Nominal (OZ) | RiskEngine.Results.Outputs.Commodities.Curve Risk.Adapted delta.Value | Unit: OZ.TR, Simplified: Yes |
| Nominal (USD) | RiskEngine.Results.Outputs.Commodities.Curve Risk.Adapted delta.Value(currency) | Currency: USD, Simplified: Yes |
| Adapted Delta (OZ) | RiskEngine.Results.Outputs.Commodities.Curve Risk.Adapted delta.Value | Unit: OZ.TR, Simplified: No |
| Adapted Delta (USD) | RiskEngine.Results.Outputs.Commodities.Curve Risk.Adapted delta.Value(currency) | Currency: USD, Simplified: No |
| Adapted Spot Delta (OZ) | RiskEngine.Results.Outputs.Commodities.Curve Risk.Adapted spot delta.Value | Unit: OZ.TR |
| Adapted Spot Delta (USD) | RiskEngine.Results.Outputs.Commodities.Curve Risk.Adapted spot delta.Value(currency).Value | Currency: USD |
| Com Adapted Gamma (Oz) | RiskEngine.Results.Outputs.Commodities.Curve Risk.Adapted gamma.Value | Unit: OZ.TR |
| Com Vega (USD) | RiskEngine.Results.Outputs.Commodities.Curve Risk.Vega.Value | Currency: USD, Market Exposure Mode: Physical |
| Com Volga | RiskEngine.Results.Outputs.Commodities.Curve Risk.Volga.Value | |
| Com Vanna | RiskEngine.Results.Outputs.Commodities.Curve Risk.Vanna.Value | |
| Com Theta (USD) | RiskEngine.Results.Outputs.Commodities.Curve Risk.Theta.Value | Currency: USD |
| Metal DV01 (USD) | RiskEngine.Results.Outputs.Commodities.Curve Risk.Adapted delta yield.Value | Currency: USD |
| COM_Weighted_Vega | Breakdown formulas.COM_Weighted_Vega | Calculated |

#### 2.1.2 Output Settings Screenshots

**Nominal (OZ) Settings**:
```
Statistics Settings: Default
Expressed in: Specific unit
Display unit with title: No
Commodities:
  Unit: OZ.TR
  Simplified: Yes (checked)
  Equivalent lots: No
  Sensitivities against: Market quotes
  Hedge projection: None
```

**Nominal (USD) Settings**:
```
Statistics Settings: Default
Expressed in: Specific unit
Currency: USD
Display unit with title: No
Commodities:
  Simplified: Yes (checked)
  Spread in market exposure: Excluded
```

**Adapted Delta (OZ) Settings**:
```
Statistics Settings: Default
Expressed in: Specific unit
Display unit with title: No
Commodities:
  Unit: OZ.TR
  Simplified: No (unchecked)  ← Key difference
  Equivalent lots: No
  Sensitivities against: Market quotes
  Hedge projection: None
```

**Com Vega (USD) Settings**:
```
Statistics Settings: Default
Expressed in: Specific unit
Currency: USD
Display unit with title: No
Commodities:
  Market Exposure Mode: Physical
  Spread in market exposure: Excluded
```

#### 2.1.3 Commodities General Settings

```
Label: COM_DEFAULT
Sensitivities:
  Thetas: Analytical
  Gamma cross effect: Off
  Sensitivities hedge curve projection: Father hedge
  Projection on smooth curve pillar: On
  Vega adaptation: No
  Yield curve reaction to currency rate: Keep lease metal rates constant
```

#### 2.1.4 Breakdowns (21 Attributes)

| Breakdown | Dictionary Path | Description |
|-----------|-----------------|-------------|
| Trade Number | Standard | Trade ID |
| Portfolio | Standard | Trading book |
| Metal | Formulas.Product.Label | PM ISO code (XAU, etc.) |
| Call/Put | Formulas.Call/Put | Option type |
| Strike | Formulas.Strike | Option strike |
| Deal Maturity | Formulas.Maturity | Trade maturity |
| PL Instrument | Standard | PnL instrument label |
| Index | Formulas.Index.Label | Commodity index |
| Family | Standard | Trade family |
| Group | Standard | Trade group |
| Type | Standard | Trade type |
| Typology | Standard | Trade typology |
| Class Label | Formulas.PL Key.Category.Complete Name | PL Key category |
| Leading curve | RiskEngine.Results.Outputs.Commodities.Curve Risk.Adapted delta.Leading curve.Leading curve | Aggregation curve |
| Location | Formulas.Location.Label | Commodity location |
| Currency | Standard | Trade currency |
| Maturity Contract | Standard | Contract maturity |
| Native Pillar | Formulas.Pillar.Label | Native curve pillar |
| Pillar | Formulas.Risk date | Bucketed maturity pillar |
| Unit | Formulas.Index.Quotation.Unit | Quotation unit |
| VEGASTK | RiskEngine.Results.Outputs.Commodities.Curve Risk.Vega.Pillar.Strike | Vega surface delta pillar |

#### 2.1.5 Pillar Breakdown Settings

```
Mat. Source: Maturity Set
Disp. maturity set: PM RISK
Bucket type: Pillars
Reduced label: Yes
Standard labels: Yes
Display Mode: Label
Add dates: No
All Pillars: No
Split Mode: Surrounding pillars
Shifter: (configured)
Truncate Flows: No
```

#### 2.1.6 Weighted Vega Breakdown Formula

```
IF (Vega <> 0.0) THEN
    RESULT := sqrt(30.0 / (Date - GetHorizonDate())) * (1.0/100.0) * Vega * 100.0;
```

Where:
- `Date` = maturity of the deal
- `GetHorizonDate()` = environment/reporting date (typically T-1)

---

## 3. Feeder Configuration

### 3.1 Feeder: TF_SENS_ALL

| Attribute | Value |
|-----------|-------|
| Type | Trading |
| Simulation View | VW_SENSITIVITIES_ALL |
| Datamart Table | SB_SENSITIVITIES.REP |

### 3.2 Feeder Batches by Region

| Region | Processing Script | Batch | Global Filter | Portfolio Nodes |
|--------|------------------|-------|---------------|-----------------|
| HKG | HK_SENS_FDR | BF_SENS_HK | GF_HK_PFOLIOS_RD | LMHK, PMSG |
| LDN | LN_SENS_FDR | BF_SENS_LN | GF_LN_PFOLIOS_RD | FXDLN, IRLN, LMLN, PMLN |
| NYK | NY_SENS_FDR | BF_SENS_NY | GF_NY_PFOLIOS_RD | LMNY, PMNY |
| SAO | SP_SENS_FDR | BF_SENS_SP | GF_SP_PFOLIOS_RD | LMSP |

### 3.3 Portfolio Filtering Logic

The feeder scope includes Level 4 portfolio nodes that contain deals sensitive to PM:
- **Included**: LM* (London Metals), PM* (Precious Metals), PMSG (Singapore PM)
- **Excluded**: IR* (Interest Rates), FX* (Foreign Exchange) - sensitivity covered in other feeds

---

## 4. Market Data Sets

| Region | Market Data Set | Description |
|--------|-----------------|-------------|
| LDN | LNCLOSE | London official close |
| HKG | HKCLOSE | Hong Kong official close |
| NYK | NYCLOSE | New York official close |
| SAO | SPCLOSE | São Paulo official close |

---

## 5. Extraction Configuration

### 5.1 Extraction Request: ER_SENSITIVITIES_ALL

| Attribute | Value |
|-----------|-------|
| Data Extractor | DE_SENSITIVITIES_ALL |
| Output Directory | ./reports/today/eod |

### 5.2 Extraction Batches by Region

| Region | Processing Script | Batch |
|--------|------------------|-------|
| HKG | HK_SENS_RPT | BE_SENS_HK |
| LDN | LN_SENS_RPT | BE_SENS_HK |
| NYK | NY_SENS_RPT | BE_SENS_HK |
| SAO | SP_SENS_RPT | BE_SENS_HK |

### 5.3 Data Extractor: DE_SENSITIVITIES_ALL

The extraction uses **parameterized SQL** to generate 13 separate files, one per sensitivity type.

#### 5.3.1 SQL Parameters

| Parameter | Description | Example Value |
|-----------|-------------|---------------|
| @MxSQLExpression | Filter to exclude null results | `SENSI.M_ADAPTED_1 <> 0` |
| @MxSensType | Sensitivity type label | `'Adapted Delta (USD)'` |
| @MxSensValue | Sensitivity value column | `SENSI.M_ADAPTED_1` |
| @MxDataSetKey | Reference data set key | (system generated) |

#### 5.3.2 Complete Extraction SQL

```sql
SELECT
    SENSI.M_TRADE_NUM,
    SENSI.M_PORTFOLIO,
    TP.M_PACKAGE AS PKG_NB,
    TP.M_PKG_TYPO AS PKG_TYPOLOGY,
    SENSI.M_PL_INSTRU,
    SENSI.M_METAL,
    SENSI.M_FAMILY,
    SENSI.M_GROUP,
    SENSI.M_TYPE,
    SENSI.M_TYPOLOGY,
    SENSI.M_CALL_PUT,
    SENSI.M_CLASS_LAB,
    SENSI.M_CURRENCY,
    SENSI.M_DEAL_MATU,
    SENSI.M_INDEX,
    SENSI.M_LEADING_C,
    SENSI.M_LOCATION,
    UDF.M_DELIV_TYP AS DELIVERY_TYPE,
    NVL(RTRIM(SENSI.M_MATURITY_), SENSI.M_NATIVE_PI) AS M_MATURITY,
    SENSI.M_STRIKE,
    SENSI.M_UNIT,
    SENSI.M_PILLAR,
    CASE
        WHEN (@MxSensType:C <> 'Vega' AND @MxSensType:C <> 'Weighted Vega')
        THEN ' '
        ELSE to_char(SENSI.M_VEGASTK)
    END AS VEGASTK,
    @MxSensType:C AS SENS_TYPE,
    @MxSensValue:N AS SENS_VALUE
FROM DM.SB_SENSITIVITIES_REP SENSI
LEFT JOIN DM.SB_UDF_REP UDF
    ON SENSI.M_REF_DATA = UDF.M_REF_DATA
    AND SENSI.M_TRADE_NUM = UDF.M_NB
LEFT JOIN DM.SB_TP_REP TP
    ON SENSI.M_REF_DATA = TP.M_REF_DATA
    AND SENSI.M_TRADE_NUM = TP.M_NB
    AND SENSI.M_PORTFOLIO = TP.M_TP_PFOLIO
LEFT JOIN DM.SB_TYPOLOGY_REP TYP
    ON RTRIM(SENSI.M_TYPOLOGY) = RTRIM(TYP.M_LABEL)
    AND SENSI.M_REF_DATA = TYP.M_REF_DATA
WHERE @MxSQLExpression:C
    AND SENSI.M_REF_DATA = @MxDataSetKey:N
    AND TYP.M_H_CATEGORY = 'PRECIOUS'
```

#### 5.3.3 Key SQL Components

| Component | Purpose |
|-----------|---------|
| `SB_SENSITIVITIES_REP` | Main sensitivity outputs table |
| `SB_UDF_REP` | Trade UDF table (delivery type) |
| `SB_TP_REP` | Trade package table (package number, typology) |
| `SB_TYPOLOGY_REP` | Typology reference (for PRECIOUS filter) |

#### 5.3.4 Typology Filter

The extraction filters by **M_H_CATEGORY = 'PRECIOUS'** from the typology hierarchy:

```
Hierarchy → Classification → Levels
  ├── PM - ASIAN OPT OTC    [Category: PRECIOUS]
  ├── PM - EFP              [Category: PRECIOUS]
  ├── PM - FUT              [Category: PRECIOUS]
  ├── PM - FUT CARRY        [Category: PRECIOUS]
  ├── PM - FUT OPT LST      [Category: PRECIOUS]
  ├── PM - FWD ADJ          [Category: PRECIOUS]
  ├── PM - FWD AL           [Category: PRECIOUS]
  ├── PM - FWD AL PP FIX    [Category: PRECIOUS]
  ├── PM - FWD AVG          [Category: PRECIOUS]
  ├── PM - FWD CARRY        [Category: PRECIOUS]
  └── PM - FWD MTF ROLL     [Category: PRECIOUS]
```

### 5.4 Parameter Mapping by Sensitivity

| File | @MxSensType | @MxSensValue | @MxSQLExpression |
|------|-------------|--------------|------------------|
| MxGTS_Sens_PM_AdDeltaUSD | 'Adapted Delta (USD)' | SENSI.M_ADAPTED_1 | SENSI.M_ADAPTED_1 <> 0 |
| MxGTS_Sens_PM_AdDeltaOZ | 'Adapted Delta (OZ)' | SENSI.M_ADAPTED_OZ | SENSI.M_ADAPTED_OZ <> 0 |
| MxGTS_Sens_PM_SpotDeltaUSD | 'Adapted Spot Delta (USD)' | SENSI.M_SPOT_USD | SENSI.M_SPOT_USD <> 0 |
| MxGTS_Sens_PM_SpotDeltaOZ | 'Adapted Spot Delta (OZ)' | SENSI.M_SPOT_OZ | SENSI.M_SPOT_OZ <> 0 |
| MxGTS_Sens_PM_NominalUSD | 'Nominal (USD)' | SENSI.M_NOMINAL_1 | SENSI.M_NOMINAL_1 <> 0 |
| MxGTS_Sens_PM_NominalOZ | 'Nominal (OZ)' | SENSI.M_NOMINAL_OZ | SENSI.M_NOMINAL_OZ <> 0 |
| MxGTS_Sens_PM_Gamma | 'Adapted Gamma (OZ)' | SENSI.M_GAMMA | SENSI.M_GAMMA <> 0 |
| MxGTS_Sens_PM_Theta | 'Theta (USD)' | SENSI.M_THETA | SENSI.M_THETA <> 0 |
| MxGTS_Sens_PM_Vanna | 'Vanna' | SENSI.M_VANNA | SENSI.M_VANNA <> 0 |
| MxGTS_Sens_PM_Volga | 'Volga' | SENSI.M_VOLGA | SENSI.M_VOLGA <> 0 |
| MxGTS_Sens_PM_Vega | 'Vega' | SENSI.M_VEGA | SENSI.M_VEGA <> 0 |
| MxGTS_Sens_PM_MetalDV01 | 'Metal DV01 (USD)' | SENSI.M_DV01 | SENSI.M_DV01 <> 0 |
| MxGTS_Sens_PM_WeightedVega | 'Weighted Vega' | SENSI.M_WVEGA | SENSI.M_WVEGA <> 0 |

---

## 6. Post-Processing Scripts

### 6.1 merge_files.sh

Merges the 13 individual sensitivity files into a combined report:

```bash
# Input: 13 files per region
# Output: MxGTS_Sensitivities_**_yyyymmdd.csv
```

### 6.2 process_reports.sh

Compresses and packages for MFT delivery:

```bash
# Input: MxGTS_Sensitivities_**_yyyymmdd.csv + other sensitivity files
# Output: ZIP package for transfer
```

---

## 7. PM RISK Maturity Set

### 7.1 Pillar Configuration

| Label | Reference Date Example (7 Jun 2023) |
|-------|-------------------------------------|
| TODAY | 07 Jun 2023 |
| TOM | 08 Jun 2023 |
| SPOT | 09 Jun 2023 |
| 1W | 14 Jun 2023 |
| 1M | 07 Jul 2023 |
| 2M | 07 Aug 2023 |
| 3M | 07 Sep 2023 |
| 4M | 07 Oct 2023 |
| 5M | 07 Nov 2023 |
| 6M | 07 Dec 2023 |
| 9M | 07 Mar 2024 |
| 1Y | 07 Jun 2024 |
| 18M | 07 Dec 2024 |
| 2Y | 07 Jun 2025 |
| 3Y | 07 Jun 2026 |
| 4Y | 07 Jun 2027 |
| 5Y | 07 Jun 2028 |
| 10Y | 07 Jun 2033 |

### 7.2 Pillar Date Calculation

Pillar dates are computed dynamically from the reference date of the environment.

---

## 8. Vega Delta Surface Pillars

For Vega and Weighted Vega, exposures are distributed across 7 delta pillars:

| Delta Pillar | Option Type |
|--------------|-------------|
| 5 | Deep OTM Call |
| 10 | OTM Call |
| 25 | OTM Call |
| 50 | ATM |
| 75 | OTM Put (25-delta) |
| 90 | OTM Put (10-delta) |
| 95 | Deep OTM Put |

---

## 9. Change History

| Version | Date | Author | Change Description |
|---------|------|--------|-------------------|
| 1.0 | 2025-01-13 | Risk Technology | Initial document |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
