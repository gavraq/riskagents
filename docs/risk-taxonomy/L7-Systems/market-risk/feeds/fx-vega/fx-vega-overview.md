# FX Vega Sensitivities - Feed Overview

## Executive Summary

The FX Vega Sensitivities feed provides trade-level foreign exchange volatility risk exposures from Murex to downstream market risk systems. This feed captures non-linear FX risk (options) with sensitivities assigned to maturity pillars and strike levels, enabling accurate FX options risk reporting and hedging decisions.

## Feed Identity

| Attribute | Value |
|-----------|-------|
| **Feed Name** | FX Vega Sensitivities (Strike & Maturity) |
| **Feed ID** | MR-FX-VEGA |
| **Asset Class** | Foreign Exchange |
| **Risk Type** | Vega (Volatility) |
| **Source System** | Murex |
| **Target Systems** | Plato, RDS, VaR Engine |
| **Frequency** | Daily |
| **Business Owner** | Market Risk |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      FX Vega Architecture                                    │
│               (Single-Source with Strike & Maturity Bucketing)              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                 PROCESSING SCRIPT (Regional)                        │   │
│  │                                                                      │   │
│  │  **_QFX_VEG_STKMT_FDR                                               │   │
│  │  (LN_, HK_, NY_, SP_ prefixes)                                      │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         FEEDER                                       │   │
│  │                                                                      │   │
│  │  Feeder: TF_QFX_VEGA_STKMAT                                         │   │
│  │  Batches: BF_QFX_VG_ST_{Region}                                     │   │
│  │  Global Filter: GF_{Region}_PFOLIOS_RD                              │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    SIMULATION VIEW                                   │   │
│  │                                                                      │   │
│  │  View: FX_VEGA_MATURITY                                             │   │
│  │       │                                                              │   │
│  │       ├─── Outputs: fx_vega_usd, FX Default Vega (deprecated),     │   │
│  │       │             FX Vega Without Splitting (deprecated)          │   │
│  │       │                                                              │   │
│  │       └─── Breakdowns: 8 (Portfolio, Trade Number, Contract,       │   │
│  │                          vega_date, vega_pillar, parallel_fx_vega, │   │
│  │                          Instrument, Model)                         │   │
│  │                                                                      │   │
│  │  Dynamic Table: VW_QFX_VEGA_STKMAT                                  │   │
│  │  Datamart Table: SB_QFX_VEGASTK.REP                                 │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    DATA EXTRACTOR                                    │   │
│  │                                                                      │   │
│  │  Data Extractor: DE_QFX_VEGA_STKMAT                                 │   │
│  │  Extraction Request: ER_QFX_STK_MAT                                 │   │
│  │                                                                      │   │
│  │  SQL Logic:                                                          │   │
│  │   • Join to TBL_FX_CNT_REP for quotation mode                       │   │
│  │   • Join to SB_TP_REP for legal entity filter                       │   │
│  │   • CASE logic for instrument type mapping                          │   │
│  │   • Call/Put/ATM determination from strike level                    │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         OUTPUT FILE                                  │   │
│  │                                                                      │   │
│  │  Pattern: MxGTS_Vespa_FX_Vega_StkMat_{Region}_{YYYYMMDD}.csv       │   │
│  │  Fields: 11 (PORTFOLIO, TRADE_NUMBER, INSTRUMENT, etc.)            │   │
│  │  Delivery: MFT to Plato and RDS                                     │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Key Characteristics

### Single-Source Architecture

| Component | Name | Description |
|-----------|------|-------------|
| **Simulation View** | FX_VEGA_MATURITY | Strike & maturity based vega calculation |
| **Dynamic Table** | VW_QFX_VEGA_STKMAT | Filtered view with transaction type filtering |
| **Datamart Table** | SB_QFX_VEGASTK.REP | Storage for vega sensitivities |
| **Data Extractor** | DE_QFX_VEGA_STKMAT | SQL-based extraction with mappings |

### Vega Calculation Definition

| Measure | Definition | Details |
|---------|------------|---------|
| **fx_vega_usd** | FX Vega in USD | Change in market value for 1% move in volatility. Discounted from settlement date to today. Zero day FX spot rate used for USD conversion. |

### Maturity Pillar Set (RISK_VIEW4)

The vega sensitivities are bucketed into standard maturity pillars:

| Short Term | Medium Term | Long Term |
|------------|-------------|-----------|
| O/N, T/N, 1W, 2W | 1M, 2M, 3M, 6M, 9M | 1Y, 18M, 2Y, 3Y, 4Y, 5Y |
| | | 6Y, 7Y, 8Y, 9Y, 10Y, 12Y |
| | | 15Y, 20Y, 25Y, 30Y, 35Y |

**Pillar Assignment Logic**: When a cash flow falls between pillar dates, the sensitivity is split between adjacent pillars weighted by distance from each pillar date.

### Vega Strike Levels

| Strike Type | Determination | Description |
|-------------|---------------|-------------|
| **Call** | VEGA_STK < 50 | Out-of-the-money call |
| **ATM** | VEGA_STK = 50 | At-the-money |
| **Put** | VEGA_STK > 50 | Out-of-the-money put |

Strike values represent delta levels (0, 5, 10, 25, 50, 75, 90, 95, 100).

## Processing Flow

### Regional Processing

| Region | Processing Script | Batch | Portfolio Nodes |
|--------|-------------------|-------|-----------------|
| LDN | LN_QFX_VEG_STKMT_FDR | BF_QFX_VG_ST_LN | FXDLN, IRLN, LMLN, PMLN |
| HKG | HK_QFX_VEG_STKMT_FDR | BF_QFX_VG_ST_HK | LMHK, PMSG |
| NYK | NY_QFX_VEG_STKMT_FDR | BF_QFX_VG_ST_NY | LMNY, PMNY |
| SAO | SP_QFX_VEG_STKMT_FDR | BF_QFX_VG_ST_SP | LMSP |

**Note**: Hong Kong/Singapore region excludes FXHKSBL portfolio node.

### Transaction Filtering

The dynamic table VW_QFX_VEGA_STKMAT filters to:
- Transaction types: Interest rate swaps, Default swaps
- Deal status: Not DEAD
- Products in scope: QFX Range Accruals, Quanto Forward Swaps, and other exotic instruments with FX vega sensitivity

### Instrument Type Mapping

| Murex Instrument | Mapped Type |
|------------------|-------------|
| QFX Range Accrua | IRD_IRS_RA |
| Quanto Forward S | IRD_IRS_FX |
| QIR Range Accrua | IRD_IRS_RA |
| Insurance Instru | CRD_CDS_INS |
| Guarantee Instru | CRD_CDS_GUA |

## Data Flow Summary

```
Market Data (LNCLOSE, HKCLOSE, NYCLOSE, SPCLOSE)
       │
       ▼
┌─────────────────┐
│ Valuation Batch │
└─────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ FX_VEGA_MATURITY Simulation View                        │
│                                                         │
│  Outputs:                                               │
│   • fx_vega_usd (primary)                              │
│   • FX Default Vega (deprecated)                       │
│   • FX Vega Without Splitting (deprecated)             │
│                                                         │
│  Breakdowns:                                            │
│   • Portfolio, Trade Number, Contract                  │
│   • vega_date, vega_pillar, parallel_fx_vega          │
│   • Instrument, Model                                  │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ Feeder: TF_QFX_VEGA_STKMAT                              │
│ Dynamic Table: VW_QFX_VEGA_STKMAT                       │
│                                                         │
│ Filters:                                                │
│  • Transaction types (IRS, CDS)                        │
│  • Status ≠ DEAD                                       │
│  • Portfolio nodes (L4)                                │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ Datamart: SB_QFX_VEGASTK.REP                            │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ Data Extractor: DE_QFX_VEGA_STKMAT                      │
│ Extraction Request: ER_QFX_STK_MAT                      │
│                                                         │
│ SQL Logic:                                              │
│  • Join TBL_FX_CNT_REP for quotation mode              │
│  • Join SB_TP_REP for legal entity filter              │
│  • CASE mapping for instrument types                   │
│  • Call/Put/ATM from strike level                      │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ CSV File                                                │
│ MxGTS_Vespa_FX_Vega_StkMat_{Region}_{YYYYMMDD}.csv     │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ ZIP Package                                             │
│ MxGTS_Vespa_Sensitivities_{Region}_{YYYYMMDD}.zip      │
└─────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ MFT Delivery                                            │
│ Plato, RDS                                              │
└─────────────────────────────────────────────────────────┘
```

## Comparison with Other FX Feeds

| Attribute | FX Vega | FX Delta |
|-----------|---------|----------|
| **Products** | Non-linear (options, exotics) | Linear (spots, forwards, swaps) |
| **Risk Factor** | FX volatility | Spot FX rates |
| **Simulation Views** | FX_VEGA_MATURITY | STB_Fx_Delta_ONLY, FXDELTAPOSRPT |
| **Architecture** | Single source | Dual source with UNION ALL |
| **Pillar Assignment** | Yes (maturity + strike) | No |
| **Output Fields** | 11 | 8 |
| **Complexity** | Medium (strike/maturity grid) | High (3-block SQL) |

## Comparison with IR Vega Feed

| Attribute | FX Vega | IR Vega |
|-----------|---------|---------|
| **Underlying** | FX volatility surface | IR volatility (swaption/cap) |
| **Simulation View** | FX_VEGA_MATURITY | IRVEGA_RPT |
| **Strike Dimension** | FX delta strikes (0-100) | Swaption strikes (ATM, OTM) |
| **Pillar Set** | RISK_VIEW4 | RISK_VIEW4 |
| **CP Flag** | Call/Put/ATM from strike | Derived from vega type |

## Known Issues and Recommendations

### Portfolio Node Inconsistency (Hong Kong)
- **Issue**: FXHKSBL portfolio node is not included in Hong Kong region
- **Impact**: Potential gap in FX options coverage for HK
- **Recommendation**: Review and document business rationale for exclusion

### Deprecated Outputs
- **Issue**: FX Default Vega and FX Vega Without Splitting are deprecated
- **Recommendation**: Remove from simulation view in next update cycle

### Incomplete Breakdown Documentation
- **Issue**: PDF notes "Need to update table to include relevant breakdowns from IR Sensitivity feed document"
- **Recommendation**: Complete breakdown documentation with full definitions

### Legal Entity Filtering
- **Issue**: SA legal entity exclusion logic documented as "to be documented more fully"
- **Recommendation**: Complete documentation of legal entity filtering rules

## Related Documentation

| Document | Description |
|----------|-------------|
| [FX Vega BRD](./fx-vega-brd.md) | Business requirements |
| [FX Vega IT Config](./fx-vega-config.md) | Murex GOM configuration |
| [FX Vega IDD](./fx-vega-idd.md) | Interface design document |
| [FX Delta Overview](../fx-delta/fx-delta-overview.md) | Related FX linear feed |
| [IR Vega Overview](../ir-vega/ir-vega-overview.md) | Related IR options feed |

---

*Document Version: 1.0 | Last Updated: 2025-01-13 | Owner: Market Risk Technology*
