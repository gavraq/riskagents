# FX Delta Sensitivities - IT Configuration Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | FXD-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Murex Global Operating Model Components

### 1.1 Component Summary

| Component Type | STB Stream | Non-STB Stream |
|----------------|------------|----------------|
| **Simulation View** | STB_Fx_Delta_ONLY | FXDELTAPOSRPT |
| **Datamart Table** | A_FXPOS_STBDELTA.REP | A_FXPOSITIONDEL.REP |
| **Feeder** | A_FXPOS_STBDELTA | A_FXPOSITIONDELTA |
| **Dynamic Table** | A_FXPOS_STBDELTA | A_FXPOSITIONDELTA |
| **Data Extractor** | DE_FXPOSTL | DE_FXPOSTL |
| **Extraction Request** | FXPOSITONTL | FXPOSITONTL |

---

## 2. Structured Bonds (STB) Configuration

### 2.1 Simulation View: STB_Fx_Delta_ONLY

#### Filters

| Filter | Condition | Purpose |
|--------|-----------|---------|
| Flow Currency | ≠ US1 AND ≠ USD | Exclude USD-denominated flows (no FX risk) |
| Sec Type | = Structured | Include only structured bonds |

#### Outputs (1 active + 6 hidden)

| Output | Dictionary Path | Definition | Hidden |
|--------|-----------------|------------|--------|
| **Past and Future Flows** | Risk Engine.Results.Flows.Cash flows.Past and Future Flows.Financed | Past and future cashflows converted to USD using zero-day spot rate. Financing and discounting disabled. | No |
| Unit | - | Unit of Past and Future Flows (USD) | Yes |
| **FX delta_STB** | Risk Engine.Results.Outputs.Fx.Delta.Value | Spot Delta Hedge in USD. dHedge@spot/dS capitalized from horizon to Spot with FX curves. Projected on "STD FAMILY" (USD vs all other currencies). | No |
| Unit | - | Unit of FX delta_STB (USD) | Yes |
| **FX Delta USD** | Formula-based | Derived FX delta (see formula below) | No |
| FX Discount Delta | - | Hidden technical field | Yes |
| FX Projection Discount Delta | - | Hidden technical field | Yes |

#### FX Delta USD Formula

```
IF (Flow_Currency <> "USD") THEN {
    IF (Past_and_Future_Flows == 0.0) THEN {
        FX_Delta_USD := FX_delta_STB
    }
    ELSE {
        FX_Delta_USD := Past_and_Future_Flows
    }
};
```

**Logic**: For STB products, use cashflow-based delta if available (most common case), otherwise fall back to risk engine delta.

#### Breakdowns (10)

| Breakdown | Dictionary Path | Definition |
|-----------|-----------------|------------|
| Structured Bond Note | Formulas.PL security/future.Displayed label | Label of the security |
| Flow Currency | Risk Engine.Results.Flows.Cash flows.Past and Future Flows.Currency | Currency of the flows |
| Strategy | - | Trading strategy |
| Trade Number | - | Murex trade ID |
| Portfolio | - | Trading book |
| Portfolio Legal Entity | - | Legal entity of portfolio |
| Label | - | Product label |
| Status | - | Trade status |
| Closing Entity | - | Closing entity |
| Sec Type | - | Security type |

#### Output Settings (FX delta_STB)

| Setting | Value |
|---------|-------|
| Expressed in | Specific unit |
| Currency | USD |
| Display unit with title | No |
| Delta definition | dHedge@spot/dS |
| Delta at bucket/date | Follows delta definition |
| Fx option delta | Yes |
| Flow | Yes |
| Mkt value | Yes |
| Family projection | On |
| Family | STD FAMILY |
| Accrual mode | No |

---

## 3. Non-Structured Products Configuration

### 3.1 Simulation View: FXDELTAPOSRPT

#### Outputs (4 active + 8 hidden)

| Output | Dictionary Path | Definition | Hidden |
|--------|-----------------|------------|--------|
| **FXDELTA** | Risk Engine.Results.Outputs.Fx.Delta.Value | Spot Delta Hedge in USD. Projected on FXDELTA family (USD vs all other currencies). | No |
| **FXDELTA2** | Risk Engine.Results.Outputs.Fx.Delta.Value | Discounted delta in USD (dValue@horizon/dS0). Projected on FXDELTA family. | No |
| **FXDELTA_ZAR** | Risk Engine.Results.Outputs.Fx.Delta.Value | Spot Delta Hedge in ZAR. Projected on "STD FAMILY ZAR" (ZAR vs all currencies). **DEPRECATED** | No |
| **FXDELTA_ZAR2** | Risk Engine.Results.Outputs.Fx.Delta.Value | Discounted delta in ZAR. **DEPRECATED** | No |
| Closing Entity | - | Closing entity | No |
| FX Discount Delta | - | Hidden technical field | Yes |
| FX Projection Discount Delta | - | Hidden technical field (x4) | Yes |

#### Output Settings (FXDELTA)

| Setting | Value |
|---------|-------|
| Expressed in | Specific unit |
| Currency | USD |
| Display unit with title | No |
| Delta definition | dHedge@spot/dS |
| Delta at bucket/date | Follows delta definition |
| Fx option delta | Yes |
| Flow | Yes |
| Mkt value | Yes |
| Family projection | On |
| Family | FXDELTA |
| Accrual mode | No |

#### Output Settings (FXDELTA2 - Discounted)

| Setting | Value |
|---------|-------|
| Delta definition | dValue@horizon/dS0 |
| All other settings | Same as FXDELTA |

#### Breakdowns (7)

| Breakdown | Dictionary Path | Definition |
|-----------|-----------------|------------|
| **FXQUOT** | Risk Engine.Results.Outputs.Fx.Delta.FX contract.FX quotation | FX quotation of the FX contract |
| Portfolio | - | Trading book |
| Legal Entity | - | Legal entity |
| NB | - | Trade number |
| Status | - | Trade status |
| Currency | - | Deal currency |
| Label | - | Product label |

---

## 4. Feeder Configuration

### 4.1 STB Feeders by Region

| Region | Processing Script | Batches of Feeders | Global Filter | Portfolio Nodes |
|--------|-------------------|-------------------|---------------|-----------------|
| **HKG** | BF_FXPOSDLT_HK | BF_FXPOSDLT_HK | BF_STBDELTA_HK | FXHKSBL, LMHKSBL, PMSG |
| **LDN** | BF_FXPOSDLTA_LN | BF_FXPOSDLTA_LN | BF_STBDELT_A_LN | LMLNSBL, PMLN |
| | BF_FXPOSDLTB_LN | BF_FXPOSDLTB_LN | BF_STBDELT_B_LN | FXDLNSBL, FXLNSBL, IFXMMLNIC, IFXMMLNLH |
| | BF_FXPOSDLTC_LN | BF_FXPOSDLTC_LN | BF_STBDELT_C_LN | IRLNSBL |
| **NYK** | BF_FXPOSDLT_NY | BF_FXPOSDLT_NY | BF_STBDELTA_NY | FXNYSBL, LMNYSBL, PMNY |
| **SAO** | BF_FXPOSDLT_SP | BF_FXPOSDLT_SP | BF_STBDELTA_SP | LMSPBSI, LMSPFIA, LMSPFND, LMSPSBL |

**Note**: London uses 3 batches for legacy reasons (historical Murex processing constraints).

### 4.2 Non-STB Feeders by Region

| Region | Processing Script | Batches of Feeders | Global Filter | Portfolio Nodes |
|--------|-------------------|-------------------|---------------|-----------------|
| **HKG** | HK_FXPOS_FDR | BF_FXPOSTL_HK | BF_FXPOSTL_HK | FXHKSBL, LMHKSBL, PMSG |
| **LDN** | LN_FXPOS_FDR | BF_FXPOSTL_LN | BF_FXPOSTL_LN | FXDLNSBL, FXLNSBL, IFXMMLNIC, IFXMMLNLH, IRLNSBL, JBSBSA, LMLNSBL, PMLN |
| **NYK** | NY_FXPOS_FDR | BF_FXPOSTL_NY | BF_FXPOSTL_NY | FXNYSBL, LMNYSBL, PMNY |
| **SAO** | SP_FXPOS_FDR | BF_FXPOSTL_SP | BF_FXPOSTL_SP | LMSPBSI, LMSPFIA, LMSPFND, LMSPSBL |

**Note**: Non-STB uses single batch per region. JBSBSA portfolio included in scope but filtered at extraction.

---

## 5. Extraction Configuration

### 5.1 Extraction by Region

| Region | Processing Script | Batches of Extraction | Single Extraction | Extraction Request |
|--------|-------------------|----------------------|-------------------|-------------------|
| HKG | HK_VSPA_FXPOS_RPT | BE_FXPOSTL_HK | DE_FXPOSTL | FXPOSITONTL |
| LDN | LN_VSPA_FXPOS_RPT | BE_FXPOSTL_LN | DE_FXPOSTL | FXPOSITONTL |
| NYK | NY_VSPA_FXPOS_RPT | BE_FXPOSTL_NY | DE_FXPOSTL | FXPOSITONTL |
| SAO | SP_VSPA_FXPOS_RPT | BE_FXPOSTL_SP | DE_FXPOSTL | FXPOSITONTL |

### 5.2 SQL Extraction Logic (Three-Block UNION ALL)

The extraction uses a complex 3-block UNION ALL structure:

#### Block 1: Live Deals (STB + Non-STB Joined)

```sql
-- Condition: M_STATUS in ('LIVE', 'MKT_OP')
-- Source: A_FXPOSITIONDEL_REP LEFT JOIN A_FXPOS_STBDELTA_REP

-- FX Delta selection logic:
CASE WHEN stb.M_TRADE_NUM IS NOT NULL
    THEN stb.M_FX_DELTA1
    ELSE pos.M_FXDELTA
END AS M_FXDELTA

-- Currency pair construction:
CASE WHEN stb.M_TRADE_NUM IS NOT NULL AND stb.M_LABEL NOT IN ('IRD - FX LINKED NOTE')
    THEN CASE WHEN stb.M_CURRENCY = stb.M_FLOW_CURR
        THEN stb.M_CURRENCY || '-' || stb.M_UNIT
        ELSE stb.M_CURRENCY || '-' || stb.M_FLOW_CURR
    END
WHEN stb.M_LABEL IN ('IRD - FX LINKED NOTE')
    THEN stb.M_FLOW_CURR || '-' || stb.M_UNIT
ELSE M_FXQUOT
END AS M_QUOTMODE0
```

#### Block 2: Dead/Purged Deals

```sql
-- Condition: M_STATUS NOT IN ('LIVE', 'MKT_OP') OR M_STATUS IS NULL
-- Source: A_FXPOSITIONDEL_REP only

SELECT CAST(0 AS NUMBER(10,0)) AS M_NB,  -- Trade number set to 0
       M_PORTFOLIO,
       M_CLOSING_E,
       M_LEGAL_ENT,
       SUM(M_FXDELTA),                    -- Aggregated delta
       SUM(M_FXDELTA_Z),
       '' AS M_STATUS,
       M_QUOTMODE0
FROM A_FXPOSITIONDEL_REP
WHERE M_STATUS NOT IN ('LIVE', 'MKT_OP') OR M_STATUS IS NULL
GROUP BY M_PORTFOLIO, M_QUOTMODE0, M_CLOSING_E, M_LEGAL_ENT
```

#### Block 3: Legacy STB (Orphan Trades)

```sql
-- Condition: M_STATUS in ('LIVE', 'MKT_OP')
-- Source: A_FXPOS_STBDELTA_REP where trade NOT in A_FXPOSITIONDEL_REP

-- This block usually returns no results as Non-STB scope includes STB scope
SELECT M_NB, M_PORTFOLIO, ...
FROM A_FXPOS_STBDELTA_REP stb
WHERE stb.M_TRADE_NUM NOT IN (SELECT M_NB FROM A_FXPOSITIONDEL_REP)
  AND M_STATUS IN ('LIVE', 'MKT_OP')
```

#### Final Aggregation

```sql
-- Delta sign handling
SELECT M_NB AS TRADENUMBER,
       M_PORTFOLIO AS PORTFOLIO,
       M_QUOTMODE0 AS CURRENCY_PAIR,
       CAST(CASE WHEN MAX(M_FXDELTA) != 0
                 THEN MAX(M_FXDELTA)
                 ELSE MIN(M_FXDELTA)
            END AS NUMBER(22,2)) AS FXDELTA,
       'USD' AS FXDELTA_CURR,
       ...
FROM (UNION ALL of 3 blocks)
JOIN TBL_FX_CNT_REP cnt ON currency pair matching
WHERE M_LEGAL_ENT <> 'SBSA'  -- Exclude SBSA
GROUP BY M_NB, M_PORTFOLIO, M_QUOTMODE0, FXDELTA_CURR, FXDELTA_CURR2, M_CLOSING_E
ORDER BY 2, 5, 1
```

### 5.3 Reference Table: TBL_FX_CNT_REP

Used to standardize currency pair quotation modes:

| Column | Description |
|--------|-------------|
| M_BASE | Base currency |
| M_UNDERLNG | Underlying currency |
| M_TYPE | Contract type (OTC) |

---

## 6. Market Data Sets

| Region | Market Data Set | Description |
|--------|-----------------|-------------|
| LDN | LNCLOSE | London close prices |
| HKG | HKCLOSE | Hong Kong close prices |
| NYK | NYCLOSE | New York close prices |
| SAO | SPCLOSE | Sao Paulo close prices |

---

## 7. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    MUREX VALUATION ENGINE                       │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┴───────────────────┐
          │                                       │
          ▼                                       ▼
┌─────────────────────┐               ┌─────────────────────┐
│   STB_Fx_Delta_ONLY │               │   FXDELTAPOSRPT     │
│   Simulation View   │               │   Simulation View   │
│                     │               │                     │
│ Outputs:            │               │ Outputs:            │
│ - Past/Future Flows │               │ - FXDELTA (USD)     │
│ - FX_delta_STB      │               │ - FXDELTA2 (disc)   │
│ - FX_Delta_USD      │               │ - FXDELTA_ZAR       │
│                     │               │ - FXDELTA_ZAR2      │
│ Filters:            │               │                     │
│ - Flow CCY ≠ USD    │               │ Breakdowns:         │
│ - Sec Type=Struct   │               │ - FXQUOT            │
└─────────────────────┘               │ - Portfolio         │
          │                           │ - Legal Entity      │
          ▼                           └─────────────────────┘
┌─────────────────────┐                         │
│   A_FXPOS_STBDELTA  │                         ▼
│   Feeder            │               ┌─────────────────────┐
│                     │               │   A_FXPOSITIONDELTA │
│   LDN: 3 batches    │               │   Feeder            │
│   Others: 1 batch   │               │                     │
└─────────────────────┘               │   All regions:      │
          │                           │   1 batch           │
          ▼                           └─────────────────────┘
┌─────────────────────┐                         │
│ A_FXPOS_STBDELTA.REP│                         ▼
│   Datamart Table    │               ┌─────────────────────┐
└─────────────────────┘               │ A_FXPOSITIONDEL.REP │
          │                           │   Datamart Table    │
          │                           └─────────────────────┘
          │                                     │
          └──────────────┬──────────────────────┘
                         │
                         ▼
          ┌─────────────────────────────────────┐
          │         DE_FXPOSTL                  │
          │         Data Extractor              │
          │                                     │
          │  SQL: 3-block UNION ALL             │
          │  - Live deals (STB + Non-STB join)  │
          │  - Dead deals (Trade# = 0)          │
          │  - Legacy STB (orphans)             │
          │                                     │
          │  Reference: TBL_FX_CNT_REP          │
          │  Filter: Legal Entity ≠ SBSA       │
          └─────────────────────────────────────┘
                         │
                         ▼
          ┌─────────────────────────────────────┐
          │         FXPOSITONTL                 │
          │         Extraction Request          │
          └─────────────────────────────────────┘
                         │
                         ▼
          ┌─────────────────────────────────────┐
          │   MxMGB_MR_FX_Pos_{Region}_{Date}   │
          │         Output File                 │
          └─────────────────────────────────────┘
```

---

## 8. Configuration Change Log

| Date | Change | Author | Approved By |
|------|--------|--------|-------------|
| 2025-01-13 | Initial documentation | Risk Technology | |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
