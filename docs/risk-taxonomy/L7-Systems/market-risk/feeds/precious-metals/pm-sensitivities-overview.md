# Precious Metals Sensitivities Feed - Architecture Overview

**Meridian Global Bank - Market Risk Technology**

---

## 1. Executive Summary

The Precious Metals (PM) Sensitivities Feed provides trade-level commodity risk factor sensitivities for all precious metals trading activity executed in Murex. Unlike the single-sensitivity IR and FX feeds, this feed delivers **13 distinct sensitivity measures** in a unified output, enabling comprehensive risk analysis across delta, gamma, vega, and higher-order greeks.

### Key Characteristics

| Attribute | Value |
|-----------|-------|
| **Asset Class** | Commodities - Precious Metals |
| **Source System** | Murex (VESPA Module) |
| **Simulation View** | VW_SENSITIVITIES_ALL (shared with other commodity feeds) |
| **Sensitivities** | 13 types |
| **Breakdowns** | 21 attributes |
| **Regions** | London, Hong Kong, New York, São Paulo |
| **Frequency** | Daily (EOD) |
| **Target Systems** | Plato, RDS → VESPA |

---

## 2. Sensitivity Types

### 2.1 Delta Sensitivities (6 measures)

| Sensitivity | Field Name | Unit | Discounted | Description |
|-------------|------------|------|------------|-------------|
| Forward Delta | Nominal (USD) | USD | No | Change in value for $1 forward price move |
| Forward Delta | Nominal (OZ) | OZ.TR | No | Native unit equivalent for $1 forward price move |
| Forward Delta Adapted | Adapted Delta (USD) | USD | Yes | Includes smile impact, discounted to today |
| Forward Delta Adapted | Adapted Delta (OZ) | OZ.TR | Yes | Native unit, includes smile impact |
| Spot Delta Adapted | Adapted Spot Delta (USD) | USD | Yes | Change in value for $1 spot price move |
| Spot Delta Adapted | Adapted Spot Delta (OZ) | OZ.TR | Yes | Native unit spot delta |

### 2.2 Second-Order and Volatility Sensitivities (6 measures)

| Sensitivity | Field Name | Definition |
|-------------|------------|------------|
| Gamma | Com Adapted Gamma (Oz) | Change in Adapted Delta for $1 price move |
| Vega | Com Vega (USD) | Change in value for 1% volatility move |
| Volga | Com Volga | Sensitivity of Vega to volatility (1% move) |
| Vanna | Com Vanna | Sensitivity of Delta to volatility (1% move) |
| Theta | Com Theta (USD) | Sensitivity to time decay |
| Lease Rate Risk | Metal DV01 (USD) | Change in P&L for 1bp lease rate shift |

### 2.3 Calculated Sensitivity (1 measure)

| Sensitivity | Field Name | Definition |
|-------------|------------|------------|
| Weighted Vega | COM_Weighted_Vega | Time-weighted vega (1M = baseline weight 1.0) |

**Weighted Vega Formula**:
```
IF (Vega <> 0.0) THEN
    RESULT := sqrt(30.0 / (Date - GetHorizonDate())) * (1.0/100.0) * Vega * 100.0
```

---

## 3. Architecture Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PRECIOUS METALS SENSITIVITIES                         │
│                           Data Flow Architecture                             │
└─────────────────────────────────────────────────────────────────────────────┘

                         ┌──────────────────────┐
                         │  Processing Script   │
                         │    **_SENS_FDR       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       Feeder         │
                         │    TF_SENS_ALL       │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│   Simulation View   │ │   Datamart Table    │ │     Extraction      │
│ VW_SENSITIVITIES_ALL│ │ SB_SENSITIVITIES.REP│ │ DE_SENSITIVITIES_ALL│
│                     │ │                     │ │                     │
│  • 13 Outputs       │ │  Stores results     │ │  SQL with params:   │
│  • 21 Breakdowns    │ │  from feeders       │ │  @MxSensType        │
│                     │ │                     │ │  @MxSensValue       │
└─────────────────────┘ └─────────────────────┘ │  @MxSQLExpression   │
                                                └──────────┬──────────┘
                                                           │
                         ┌─────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  13 Sensitivity Files │
              │  (per region/day)     │
              │                       │
              │ MxGTS_Sens_PM_*.csv   │
              └──────────┬────────────┘
                         │
                         ▼ merge_files.sh
              ┌──────────────────────┐
              │   Combined Report    │
              │ MxGTS_Sensitivities_ │
              │   **_yyyymmdd.csv    │
              └──────────┬───────────┘
                         │
                         ▼ process_reports.sh
              ┌──────────────────────┐
              │    ZIP Package       │
              │ MxGTS_Sensitivities_ │
              │   **_yyyymmdd.zip    │
              └──────────┬───────────┘
                         │
           ┌─────────────┴─────────────┐
           │                           │
           ▼                           ▼
    ┌────────────┐              ┌────────────┐
    │   PLATO    │              │    RDS     │
    │            │              │     ↓      │
    │ Risk Agg   │              │   VESPA    │
    └────────────┘              └────────────┘
```

---

## 4. Multi-File Generation

Unlike IR/FX feeds that produce a single file, PM Sensitivities generates **13 separate files** that are merged:

| File | Sensitivity Type |
|------|------------------|
| MxGTS_Sens_PM_AdDeltaUSD | Adapted Delta (USD) |
| MxGTS_Sens_PM_AdDeltaOZ | Adapted Delta (OZ) |
| MxGTS_Sens_PM_SpotDeltaUSD | Adapted Spot Delta (USD) |
| MxGTS_Sens_PM_SpotDeltaOZ | Adapted Spot Delta (OZ) |
| MxGTS_Sens_PM_NominalUSD | Nominal/Forward Delta (USD) |
| MxGTS_Sens_PM_NominalOZ | Nominal/Forward Delta (OZ) |
| MxGTS_Sens_PM_Gamma | Adapted Gamma |
| MxGTS_Sens_PM_Theta | Theta |
| MxGTS_Sens_PM_Vanna | Vanna |
| MxGTS_Sens_PM_Volga | Volga |
| MxGTS_Sens_PM_Vega | Vega |
| MxGTS_Sens_PM_MetalDV01 | Metal DV01 / Lease Rate Risk |
| MxGTS_Sens_PM_WeightedVega | Weighted Vega |

---

## 5. Pillaring Methodology

### 5.1 Tenor Pillaring

Risk is bucketed to maturity pillars using fractional allocation:

```
Fractional Risk Pillar 1 = (Pillar Date 2 - T) / (Pillar Date 2 - Pillar Date 1)
Fractional Risk Pillar 2 = 1 - Fractional Risk Pillar 1
```

**PM RISK Maturity Set**:
| Pillar | Example Date (Ref: 7 Jun 2023) |
|--------|-------------------------------|
| TODAY | 07 Jun 2023 |
| TOM | 08 Jun 2023 |
| SPOT | 09 Jun 2023 |
| 1W | 14 Jun 2023 |
| 1M | 07 Jul 2023 |
| 2M | 07 Aug 2023 |
| 3M | 07 Sep 2023 |
| ... | ... |
| 10Y | 07 Jun 2033 |

### 5.2 Volatility Surface Pillaring (Vega only)

Vega is also allocated across delta-based volatility surface pillars:

| Delta Pillar | Description |
|--------------|-------------|
| 5 | Deep OTM Call |
| 10 | OTM Call |
| 25 | OTM Call |
| 50 | ATM |
| 75 | OTM Put (25-delta put) |
| 90 | OTM Put (10-delta put) |
| 95 | Deep OTM Put |

**Key Note**: Vega is allocated to **all points** on the volatility surface, not just adjacent pillars. This represents a hypothetical distribution of risk.

---

## 6. Filtering Architecture

### 6.1 Feeder Level - Portfolio Filtering

| Region | Portfolio Nodes | Exclusions |
|--------|-----------------|------------|
| HKG | LMHK, PMSG | IR*, FX* |
| LDN | FXDLN, IRLN, LMLN, PMLN | IR*, FX* |
| NYK | LMNY, PMNY | IR*, FX* |
| SAO | LMSP | IR*, FX* |

### 6.2 Extraction Level - Typology Filtering

Only deals where **M_H_CATEGORY = 'PRECIOUS'** in SB_TYPOLOGY_REP are included.

PM Typologies include:
- PM - ASIAN OPT OTC
- PM - EFP
- PM - FUT
- PM - FUT CARRY
- PM - FUT OPT LST
- PM - FWD ADJ
- PM - FWD AL
- PM - FWD AL PP FIX
- PM - FWD AVG
- PM - FWD CARRY
- PM - FWD MTF ROLL
- (and others)

---

## 7. Comparison with IR/FX Feeds

| Aspect | IR/FX Feeds | PM Sensitivities |
|--------|-------------|------------------|
| Sensitivities per file | 1 | 13 (merged) |
| Simulation view | Dedicated per feed | Shared (VW_SENSITIVITIES_ALL) |
| Filtering | Index family | Typology category |
| Vega pillaring | Strike-based | Delta-based surface |
| Unit expression | Currency only | Currency + Native (OZ.TR) |
| Calculated fields | None | Weighted Vega |
| Lease rate risk | N/A | Metal DV01 included |

---

## 8. Market Data Sets

| Region | Market Data Set |
|--------|-----------------|
| LDN | LNCLOSE |
| HKG | HKCLOSE |
| NYK | NYCLOSE |
| SAO | SPCLOSE |

---

## 9. Related Documentation

| Document | Description |
|----------|-------------|
| [pm-sensitivities-brd.md](pm-sensitivities-brd.md) | Business requirements |
| [pm-sensitivities-config.md](pm-sensitivities-config.md) | Murex GOM configuration |
| [pm-sensitivities-idd.md](pm-sensitivities-idd.md) | Interface design |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
