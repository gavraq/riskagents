# FX Delta Sensitivities - Feed Overview

## Executive Summary

The FX Delta Sensitivities feed provides trade-level foreign exchange spot delta risk exposures from Murex to downstream market risk systems. This feed captures linear FX risk for all non-option products, enabling accurate FX position reporting and hedging decisions.

## Feed Identity

| Attribute | Value |
|-----------|-------|
| **Feed Name** | FX Delta Sensitivities |
| **Feed ID** | MR-FX-DELTA |
| **Asset Class** | Foreign Exchange |
| **Risk Type** | Delta (Spot) |
| **Source System** | Murex |
| **Target Systems** | Plato, RDS, VaR Engine |
| **Frequency** | Daily |
| **Business Owner** | Market Risk |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FX Delta Architecture                                │
│                    (Dual-Source with UNION ALL Merge)                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    STRUCTURED BONDS (STB)                            │   │
│  │                                                                      │   │
│  │  Simulation View: STB_Fx_Delta_ONLY                                 │   │
│  │       │                                                              │   │
│  │       ├─── Outputs: Past_and_Future_Flows, FX_delta_STB,           │   │
│  │       │             FX_Delta_USD (formula-based)                    │   │
│  │       │                                                              │   │
│  │       ├─── Filters: Flow Currency ≠ US1/USD, Sec Type = Structured │   │
│  │       │                                                              │   │
│  │       └─── Breakdowns: 10 (Portfolio, Legal Entity, etc.)          │   │
│  │                                                                      │   │
│  │  Feeder: A_FXPOS_STBDELTA                                           │   │
│  │  Datamart Table: A_FXPOS_STBDELTA.REP                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    │ LEFT JOIN                              │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │               NON-STRUCTURED PRODUCTS                                │   │
│  │                                                                      │   │
│  │  Simulation View: FXDELTAPOSRPT                                     │   │
│  │       │                                                              │   │
│  │       ├─── Outputs: FXDELTA, FXDELTA2, FXDELTA_ZAR, FXDELTA_ZAR2   │   │
│  │       │             (4 outputs + 8 hidden)                          │   │
│  │       │                                                              │   │
│  │       └─── Breakdowns: 7 (FXQUOT, Portfolio, Legal Entity, etc.)   │   │
│  │                                                                      │   │
│  │  Feeder: A_FXPOSITIONDELTA                                          │   │
│  │  Datamart Table: A_FXPOSITIONDEL.REP                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    │ UNION ALL (3-block SQL)               │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    DATA EXTRACTOR: DE_FXPOSTL                        │   │
│  │                                                                      │   │
│  │  Extraction Request: FXPOSITONTL                                    │   │
│  │                                                                      │   │
│  │  Three-Part UNION ALL Logic:                                        │   │
│  │   1. Live Deals - STB + Non-STB joined                              │   │
│  │   2. Dead/Purged Deals - Trade Number = 0                           │   │
│  │   3. Legacy STB-only - Fallback for orphan STB trades               │   │
│  │                                                                      │   │
│  │  Reference Table: TBL_FX_CNT_REP (FX Contract definitions)          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         OUTPUT FILE                                  │   │
│  │                                                                      │   │
│  │  Pattern: MxMGB_MR_FX_Pos_{Region}_{YYYYMMDD}.csv                   │   │
│  │  Fields: 8 (TRADENUMBER, PORTFOLIO, CURRENCY_PAIR, FXDELTA, etc.)  │   │
│  │  Delivery: MFT to Plato and RDS                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Key Characteristics

### Dual-Source Architecture

| Source | Simulation View | Datamart Table | Products |
|--------|-----------------|----------------|----------|
| **Structured Bonds** | STB_Fx_Delta_ONLY | A_FXPOS_STBDELTA.REP | CLN Leveraged, Deposit Note, FX Linked Note, FX Passthrough, Passthrough |
| **Non-Structured** | FXDELTAPOSRPT | A_FXPOSITIONDEL.REP | FX Spots, Forwards, NDFs, Cross-Currency Swaps |

### Delta Calculation Types

| Delta Type | Definition | Usage |
|------------|------------|-------|
| **Spot Delta Hedge** (dHedge@spot/dS) | PL variation as of Spot for Spot price variations | Primary delta measure |
| **Discounted Delta** (dValue@horizon/dS0) | PL variation as of horizon for discounted spot variations | Secondary measure |

### FX Family Projection

| Family | Description | Output |
|--------|-------------|--------|
| **FXDELTA** | USD vs all other currencies | FXDELTA, FXDELTA2 |
| **STD FAMILY** | USD vs all other currencies | FX_delta_STB |
| **STD FAMILY ZAR** | ZAR vs all other currencies | FXDELTA_ZAR, FXDELTA_ZAR2 (deprecated) |

## Processing Flow

### Regional Processing

| Region | Processing Script | Market Data Set | Feeder Batches |
|--------|-------------------|-----------------|----------------|
| LDN | LN_FXPOS_FDR | LNCLOSE | 3 (STB) + 1 (Non-STB) |
| HKG | HK_FXPOS_FDR | HKCLOSE | 1 (STB) + 1 (Non-STB) |
| NYK | NY_FXPOS_FDR | NYCLOSE | 1 (STB) + 1 (Non-STB) |
| SAO | SP_FXPOS_FDR | SPCLOSE | 1 (STB) + 1 (Non-STB) |

### Three-Block UNION ALL Logic

The extraction SQL aggregates data from three sources:

```
Block 1: Live Deals (M_STATUS in ('LIVE', 'MKT_OP'))
├── STB data joined to Non-STB data
├── FX delta from appropriate source
└── Grouped by: Trade, Portfolio, Currency Pair, Closing Entity

Block 2: Dead/Purged Deals (M_STATUS not in ('LIVE', 'MKT_OP') OR IS NULL)
├── Non-STB data only
├── Trade Number set to 0
└── Aggregated by: Portfolio, Currency Pair, Closing Entity

Block 3: Legacy STB (M_STATUS in ('LIVE', 'MKT_OP'))
├── STB trades NOT in Non-STB table
├── Usually returns no results (fallback only)
└── Full trade detail preserved
```

## Comparison with Other FX Feeds

| Attribute | FX Delta | FX Vega |
|-----------|----------|---------|
| **Products** | Linear (non-option) | Options |
| **Risk Factor** | Spot FX rates | FX volatility |
| **Simulation Views** | STB_Fx_Delta_ONLY, FXDELTAPOSRPT | FXVEGA_RPT |
| **Complexity** | Dual-source + 3-block SQL | Single source |
| **Output Fields** | 8 | ~15 |

## Data Flow Summary

```
Market Data (LNCLOSE, etc.)
       │
       ▼
┌─────────────────┐
│ Valuation Batch │
└─────────────────┘
       │
       ├──────────────────────────────────────┐
       ▼                                      ▼
┌─────────────────┐                   ┌─────────────────┐
│ STB Feeder      │                   │ Non-STB Feeder  │
│ A_FXPOS_STBDELTA│                   │ A_FXPOSITIONDELTA│
└─────────────────┘                   └─────────────────┘
       │                                      │
       ▼                                      ▼
┌─────────────────┐                   ┌─────────────────┐
│ A_FXPOS_STBDELTA│                   │ A_FXPOSITIONDEL │
│ .REP            │                   │ .REP            │
└─────────────────┘                   └─────────────────┘
       │                                      │
       └──────────────┬───────────────────────┘
                      │
                      ▼
            ┌─────────────────┐
            │ UNION ALL SQL   │
            │ DE_FXPOSTL      │
            └─────────────────┘
                      │
                      ▼
            ┌─────────────────┐
            │ CSV File        │
            │ MxMGB_MR_FX_Pos_│
            └─────────────────┘
                      │
                      ▼
            ┌─────────────────┐
            │ MFT Delivery    │
            │ Plato, RDS      │
            └─────────────────┘
```

## Known Issues and Recommendations

### London Three-Batch STB Configuration
- **Issue**: LDN uses 3 separate STB feeder batches due to historical Murex constraints
- **Recommendation**: Evaluate consolidation in current Murex version

### Portfolio Level Filtering
- **Issue**: Mix of Level 4 and Level 5 portfolio nodes across regions
- **Recommendation**: Standardize to Level 4 portfolio nodes only

### Deprecated ZAR Fields
- **Issue**: FXDELTA_ZAR, FXDELTA_CURR2, ZAR_PROCESSING are JBSBSA-related legacy fields
- **Recommendation**: Remove in next feed update cycle

### Dead Deal Handling
- **Issue**: Dead/purged deals aggregated with Trade Number = 0
- **Impact**: Cannot trace individual dead trades
- **Recommendation**: Document business rationale for aggregation

## Related Documentation

| Document | Description |
|----------|-------------|
| [FX Delta BRD](./fx-delta-brd.md) | Business requirements |
| [FX Delta IT Config](./fx-delta-config.md) | Murex GOM configuration |
| [FX Delta IDD](./fx-delta-idd.md) | Interface design document |
| [FX Vega Overview](../fx-vega/fx-vega-overview.md) | Related FX option feed |

---

*Document Version: 1.0 | Last Updated: 2025-01-13 | Owner: Market Risk Technology*
