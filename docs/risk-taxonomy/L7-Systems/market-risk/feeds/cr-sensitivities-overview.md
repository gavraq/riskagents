---
# Document Metadata
document_id: CR-SENS-OVW-001
document_name: Credit Sensitivities Feed Suite - Overview Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Market Risk Technology
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds
feed_family: Credit Sensitivities
---

# Credit Sensitivities Feed Suite - Overview Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-SENS-OVW-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Market Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Executive Summary

### 1.1 Purpose

This document provides a comprehensive overview of the Credit Sensitivities feed suite from Murex (VESPA module). It describes the architecture, configuration, and relationships between the 8 credit sensitivity feeds that together provide complete coverage of credit spread risk exposures.

### 1.2 Business Requirements

There is a requirement for:

- **Market risk exposures** and their associated sensitivities for credit risk factors arising from any trading activity executed in Murex with exposure to credit spread risk
- At **trade-level** granularity
- Assigned to **maturity pillars** (each trade may have multiple entries as sensitivities are allocated to adjacent tenor pillars)
- Including **static data** against each trade to facilitate downstream reporting and aggregation
- On a **daily basis** (T+1)
- For each **reporting region** (London, New York, Hong Kong, Singapore)
- Provided via **Managed File Transfer (MFT)** to downstream risk aggregation platforms

**Note**: Sensitivities to non-credit spread risk factors (e.g., Interest Rates, FX, Commodities) are incorporated into separate non-Credit Risk Factor sensitivity feeds.

### 1.3 Feed Suite Summary

The CR Sensitivities suite consists of **8 feeds** generated daily per region:

| # | Feed | File Name | Key Metric | Purpose |
|---|------|-----------|------------|---------|
| 1 | [CR Delta Zero](./cr-delta-zero/) | MxMGB_MR_Credit_CS01_{Region}_{Date}.csv | CS01_ZERO | P&L per 1bp spread (zero rates) |
| 2 | [CR Delta Par](./cr-delta-par/) | MxMGB_MR_Credit_CS01Par_{Region}_{Date}.csv | CS01_PAR | P&L per 1bp spread (par rates) |
| 3 | [CR Basis Rate](./cr-basis-rate/) | MxMGB_MR_Credit_Basis_Rate_{Region}_{Date}.csv | BASIS_SENSI | Basis risk sensitivity |
| 4 | [CR Par CDS Rate](./cr-par-cds-rate/) | MxMGB_MR_Credit_ParCDS_{Region}_{Date}.csv | PAR_CDS_SENSI | CDS-specific risk |
| 5 | [CR Instrument Spread](./cr-instrument-spread/) | MxMGB_MR_Credit_Spread_{Region}_{Date}.csv | SPREAD | Actual spread level |
| 6 | [CR Corr01](./cr-corr01/) | MxMGB_MR_Credit_Corr01_{Region}_{Date}.csv | CREDIT_CORR01 | Correlation sensitivity |
| 7 | [CR RR01](./cr-rr01/) | MxMGB_MR_Credit_RR01_{Region}_{Date}.csv | RR01_SENSI | Recovery sensitivity (with propagation) |
| 8 | [CR RR02](./cr-rr02/) | MxMGB_MR_Credit_RR02_{Region}_{Date}.csv | RR02_SENSI | Recovery sensitivity (without propagation) |

---

## 2. Architecture Overview

### 2.1 Murex Dataflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MUREX VALUATION ENGINE                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│   Processing Script (Feeder)    │ │   Processing Script (Feeder)    │
│     **_MR_VESPA_SENS_FDR        │ │     **_MR_VES_SENSCI_FDR        │
│          (Non-CRDI)             │ │           (CRDI)                │
└───────────────┬─────────────────┘ └───────────────┬─────────────────┘
                │                                   │
                ▼                                   ▼
┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│         Feeder                  │ │         Feeder                  │
│       TF_VESPA_SENS             │ │     TF_VESPA_SENS_CRDI          │
└───────────────┬─────────────────┘ └───────────────┬─────────────────┘
                │                                   │
                ▼                                   ▼
┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│     Simulation View             │ │     Simulation View             │
│   VW_Vespa_Sensitivities        │ │ VW_Vespa_Sensitivities_CRDI     │
└───────────────┬─────────────────┘ └───────────────┬─────────────────┘
                │                                   │
                ▼                                   ▼
┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│      Datamart Table             │ │      Datamart Table             │
│    TBL_VESPA_SENS_REP           │ │   TBL_VESPA_SENSCI_REP          │
└───────────────┬─────────────────┘ └───────────────┬─────────────────┘
                │                                   │
                └───────────────┬───────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Processing Scripts (Extraction)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  **_MR_VESPA_DP_RPT     (CR Delta Par)                                      │
│  **_MR_VESPA_BAS_RPT    (CR Basis Rate)                                     │
│  **_MR_VESPA_D_RPT      (CR Delta Zero)                                     │
│  **_MR_VESPA_PAR_RPT    (CR Par CDS Rate)                                   │
│  **_MR_VESPA_R1_RPT     (CR RR01)                                           │
│  **_MR_VESPA_R2_RPT     (CR RR02)                                           │
│  **_CREDITCORR01_RPT    (CR Corr01)                                         │
│  **_MR_VESPA_SPR_RPT    (CR Instrument Spread)                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              8 CSV Feeds                                     │
│   MxMGB_MR_Credit_CS01_**.csv        MxMGB_MR_Credit_RR01_**.csv             │
│   MxMGB_MR_Credit_CS01Par_**.csv     MxMGB_MR_Credit_RR02_**.csv             │
│   MxMGB_MR_Credit_Basis_Rate_**.csv   MxMGB_MR_Credit_Corr01_**.csv           │
│   MxMGB_MR_Credit_ParCDS_**.csv MxMGB_MR_Credit_Spread_**.csv│
└─────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ZIP Package                                         │
│         MxMGB_MR_Credit_Sens_{Region}_{YYYYMMDD}.zip                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Managed File Transfer (MFT)                               │
│      MurexMGBSensitivitiesToPlato_**    MurexMGBSensitivitiesToRDS_**       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Two Data Flows

The CR Sensitivities suite processes data from two separate streams:

| Stream | Products | Simulation View | Datamart Table |
|--------|----------|-----------------|----------------|
| **Non-CRDI** | CDS, Bonds, CLN, CDO | VW_Vespa_Sensitivities | TBL_VESPA_SENS_REP |
| **CRDI** | Credit Indices (CDX, iTraxx) | VW_Vespa_Sensitivities_CRDI | TBL_VESPA_SENSCI_REP |

**Key Differences**:
- Non-CRDI: Individual issuer-level sensitivities
- CRDI: Index-level sensitivities (filter on Sns Origin = Index)

---

## 3. Market Data Sets

The CR Sensitivities batch uses official end-of-day market data sets:

| Region | Market Data Set | Description |
|--------|-----------------|-------------|
| London (LN) | LNCLOSE → MGB_LN_EOD | London end-of-day |
| Hong Kong (HK) | HKCLOSE → MGB_HK_EOD | Hong Kong end-of-day |
| New York (NY) | NYCLOSE → MGB_NY_EOD | New York end-of-day |
| Singapore (SP) | SPCLOSE → MGB_SP_EOD | Singapore end-of-day |

---

## 4. Simulation View Configuration

### 4.1 VW_Vespa_Sensitivities (Non-CRDI)

The Non-CRDI simulation view calculates **15 outputs** and **15 breakdowns**:

#### Outputs

| Output | Dictionary Path | Definition |
|--------|-----------------|------------|
| **Asset spread (par)** | Formulas.PL security/future.Long future.Cheapest data.Market data.Spread.Asset swap (par).Value | Future asset swap spread based on CTD bond |
| **CR01 (zero)** | RiskEngine.Results.Outputs.Credit.Delta.Zero.Value | Credit risk in USD - derivative of NPV w.r.t. credit spreads (zero basis) |
| **CR01 (par)** | RiskEngine.Results.Outputs.Credit.Delta.Par.Value | Credit risk in USD - derivative of NPV w.r.t. credit spreads (par basis) |
| **CR01 (par) quotation** | RiskEngine.Results.Outputs.Credit.Delta.Par quotation.Value | Credit risk in USD - derivative of NPV w.r.t. market quotes |
| **Recovery rate sens.** | RiskEngine.Results.Outputs.Credit.Recovery rate sens.Value | Recovery rate sensitivity WITH propagation |
| **Recovery rate 2** | RiskEngine.Results.Outputs.Credit.Recovery rate 2.Value | Recovery rate sensitivity WITHOUT propagation |
| **Credit par rate** | RiskEngine.Results.Outputs.Credit.Delta.Par.Rate | Credit market rate from market data |
| **Equ Par Spread** | RiskEngine.Results.Outputs.Credit.Delta.Par.Equ Par Spread | Equivalent par spread of credit curve |
| **Value** | RiskEngine.Results.Outputs.Credit.Interpolated spread.Value | Interpolated default spread |
| **Eval spread** | Formulas.PL security/future.Bond.Market data.Spread.Quoted.Value | Bond evaluation spread |
| **Capital factor** | RiskEngine.Results.Flows.Security flows.Security/future.Bond.Market data.Capital factor | Amortization factor x indexation factor |
| **Zero spread** | Formulas.PL security/future.Bond.Market data.Spread.Zero.Value | Bond zero coupon spread |
| **CR01 (par) quotation local curr** | RiskEngine.Results.Outputs.Credit.Delta.Par quotation.Value | CR01 in local currency (par quotation) |
| **CR01 (zero) local curr** | RiskEngine.Results.Outputs.Credit.Delta.Zero.Value | CR01 in local currency (zero) |
| **Corr01** | RiskEngine.Results.Outputs.Credit.Corr01.Corr01 | Sensitivity to average correlation (Monte Carlo) |

#### Breakdowns

| Breakdown | Dictionary Path | Definition |
|-----------|-----------------|------------|
| **Issuer** | Formulas.Issuer.Issuer name | Issuer label of the security |
| **Curve name (zero)** | Formulas.Issuer.Issuer name | Credit curve for delta zero |
| **Curve name (par)** | RiskEngine.Results.Outputs.Credit.Delta.Par.Credit key.Curve key.Curve name | Credit curve for delta par |
| **Date (zero)** | RiskEngine.Results.Outputs.Credit.Delta.Zero.Date | Tenor pillar date (zero basis) |
| **Currency** | RiskEngine.Results.Outputs.Credit.Recovery rate 2.Credit key.Currency | Currency of sensitivities |
| **Currency2** | RiskEngine.Results.Outputs.Credit.Recovery rate 2.Credit key.Currency | Duplicate currency field |
| **Country** | Formulas.Credit key.Issuer.Country.Description | Country of the issuer |
| **Rate** | RiskEngine.Results.Outputs.Credit.Recovery rate sens.Recovery rate.Rate | Recovery rate of the issuer |

*Additional breakdowns include trade attributes (Trade Number, Family, Group, Type, Typology, Portfolio, PL Instrument).*

### 4.2 VW_Vespa_Sensitivities_CRDI (CRDI)

The CRDI simulation view calculates **7 outputs** and **11 breakdowns**:

**Note**: A filter is applied to ensure only CRDI products are included: `Sns origin = Index`

#### Outputs

| Output | Dictionary Path | Definition |
|--------|-----------------|------------|
| **CR01 (zero)** | RiskEngine.Results.Outputs.Credit.Delta.Zero.Value | Credit risk in USD (zero basis) |
| **CR01 (par)** | RiskEngine.Results.Outputs.Credit.Delta.Par.Value | Credit risk in USD (par basis) |
| **CR01 (par) quotation** | RiskEngine.Results.Outputs.Credit.Delta.Par quotation.Value | Credit risk in USD (market quotes) |
| **Recovery rate sens.** | RiskEngine.Results.Outputs.Credit.Recovery rate sens.Value | Recovery sensitivity WITH propagation |
| **Recovery rate 2** | RiskEngine.Results.Outputs.Credit.Recovery rate 2.Value | Recovery sensitivity WITHOUT propagation |
| **CR01 (par) quotation local curr** | RiskEngine.Results.Outputs.Credit.Delta.Par quotation.Value | CR01 in local currency |
| **CR01 (zero) local curr** | RiskEngine.Results.Outputs.Credit.Delta.Zero.Value | CR01 in local currency (zero) |

#### Breakdowns

| Breakdown | Dictionary Path | Definition |
|-----------|-----------------|------------|
| **Sns Origin (hidden)** | RiskEngine.Results.Outputs.Credit.Delta.Par.Credit key.Sns Origin | Source of sensitivity (Issuer or Index) |
| **Date** | RiskEngine.Results.Outputs.Credit.Delta.Par.Date | Tenor pillar date (par basis) |
| **Currency** | RiskEngine.Results.Outputs.Credit.Recovery rate 2.Credit key.Currency | Currency of sensitivities |
| **Currency2** | RiskEngine.Results.Outputs.Credit.Recovery rate 2.Credit key.Currency | Duplicate currency field |

*Additional breakdowns include trade attributes (Trade Number, Family, Group, Type, Typology, Portfolio, PL Instrument).*

---

## 5. Feeder Configuration

### 5.1 Non-CRDI Feeders

| Region | Processing Script | Batch | Global Filter | Portfolio Nodes | Feeder | Datamart Table |
|--------|-------------------|-------|---------------|-----------------|--------|----------------|
| LN | LN_MR_VESPA_SENS_FDR | BF_VESPASENS_LN | GF_LN_PFOLIOS_RD | FXDLN, IRLN, LMLN, PMLN | TF_VESPA_SENS | TBL_VESPA_SENS_REP |
| HK | HK_MR_VESPA_SENS_FDR | BF_VESPASENS_HK | GF_HK_PFOLIOS_RD | LMHK, PMSG | TF_VESPA_SENS | TBL_VESPA_SENS_REP |
| NY | NY_MR_VESPA_SENS_FDR | BF_VESPASENS_NY | GF_NY_PFOLIOS_RD | LMNY, PMNY | TF_VESPA_SENS | TBL_VESPA_SENS_REP |
| SP | SP_MR_VESPA_SENS_FDR | BF_VESPASENS_SP | GF_SP_PFOLIOS_RD | LMSP | TF_VESPA_SENS | TBL_VESPA_SENS_REP |

### 5.2 CRDI Feeders

| Region | Processing Script | Batch | Global Filter | Portfolio Nodes | Feeder | Datamart Table |
|--------|-------------------|-------|---------------|-----------------|--------|----------------|
| LN | LN_MR_VES_SENSCI_FDR | BF_VESPCRDI_LN | GF_LN_PFOLIOS_RD | FXDLN, IRLN, LMLN, PMLN | TF_VESPA_SENS_CRDI | TBL_VESPA_SENSCI_REP |
| HK | HK_MR_VES_SENSCI_FDR | BF_VESPCRDI_HK | GF_HK_PFOLIOS_RD | LMHK, PMSG | TF_VESPA_SENS_CRDI | TBL_VESPA_SENSCI_REP |
| NY | NY_MR_VES_SENSCI_FDR | BF_VESPCRDI_NY | GF_NY_PFOLIOS_RD | LMNY, PMNY | TF_VESPA_SENS_CRDI | TBL_VESPA_SENSCI_REP |
| SP | SP_MR_VES_SENSCI_FDR | BF_VESPCRDI_SP | GF_SP_PFOLIOS_RD | LMSP | TF_VESPA_SENS_CRDI | TBL_VESPA_SENSCI_REP |

### 5.3 Portfolio Filtering

Level 4 portfolio nodes selected per region:

| Region | Portfolio Nodes |
|--------|-----------------|
| London | FXDLN, IRLN, LMLN, PMLN |
| Hong Kong/Singapore | PMSG, LMHK |
| New York | PMNY, LMNY |
| Sao Paulo | LMSP |

---

## 6. Feed Specifications Summary

### 6.1 Field Count by Feed

| Feed | Total Fields | Non-CRDI Fields | CRDI Fields | Structure |
|------|--------------|-----------------|-------------|-----------|
| CR Delta Zero | 19 | 19 | 19 | UNION |
| CR Delta Par | 19 | 19 | 19 | UNION |
| CR Basis Rate | 20 | 20 | 20 | UNION |
| CR Par CDS Rate | 20 | 20 | 20 | UNION |
| CR Instrument Spread | 19 | 19 | 19 | UNION |
| CR Corr01 | 13 | 13 | N/A | Non-CRDI only |
| CR RR01 | 20 | 20 | 20 | UNION |
| CR RR02 | 20 | 20 | 20 | UNION |

### 6.2 Key Metrics by Feed

| Feed | Source Field | Output Field | Unit |
|------|--------------|--------------|------|
| CR Delta Zero | M_ZERO_ | CS01_ZERO | Local currency |
| CR Delta Par | M_PAR | CS01_PAR | Local currency |
| CR Basis Rate | M_RECOVERY1 | BASIS_SENSI | Local currency |
| CR Par CDS Rate | M_PAR_CDS | PAR_CDS_SENSI | Local currency |
| CR Instrument Spread | M_ZERO_SPRE / 100 | SPREAD | Decimal (%) |
| CR Corr01 | M_CORR01 | CREDIT_CORR01 | Local currency |
| CR RR01 | M_RECOVERY_ | RR01_SENSI | Local currency |
| CR RR02 | M_RECOVERY1 | RR02_SENSI | Local currency |

### 6.3 Special Handling Notes

| Feed | Special Handling |
|------|------------------|
| CR Delta Zero | Standard UNION structure |
| CR Delta Par | Standard UNION structure |
| CR Basis Rate | Includes RESTRUCT field |
| CR Par CDS Rate | Includes RESTRUCT field |
| CR Instrument Spread | SPREAD divided by 100 (CM-6402) |
| CR Corr01 | Non-CRDI only (Monte Carlo products), dual credit curves |
| CR RR01 | Recovery WITH propagation (recalibrates spread) |
| CR RR02 | Recovery WITHOUT propagation (same source as Basis Rate) |

---

## 7. Extraction and Delivery

### 7.1 Extraction Processing

| Feed | Processing Script Pattern | Data Extractor | Extraction Request |
|------|---------------------------|----------------|-------------------|
| CR Delta Zero | **_MR_VESPA_D_RPT | DE_VESPA_CR_DELTAPAR | ER_VESPA_CR_Delta_Zero |
| CR Delta Par | **_MR_VESPA_DP_RPT | DE_VESPA_CR_DELTAPAR | ER_VESPA_CR_Delta_Par |
| CR Basis Rate | **_MR_VESPA_BAS_RPT | DE_VESPA_CR_BASIS | ER_VESPA_CR_Basis |
| CR Par CDS Rate | **_MR_VESPA_PAR_RPT | DE_VESPA_CR_PAR_CDS | ER_VESPA_CR_Par_CDS |
| CR Instrument Spread | **_MR_VESPA_SPR_RPT | DE_VESPA_CR_SPREAD | ER_VESPA_CR_Instrument_Spread |
| CR Corr01 | **_MR_VESPA_CORR01_RPT | DE_VESPA_CR_CORR01 | ER_VESPA_CR_Corr01 |
| CR RR01 | **_MR_VESPA_R1_RPT | DE_VESPA_CR_RR01 | ER_VESPA_CR_RR01 |
| CR RR02 | **_MR_VESPA_R2_RPT | DE_VESPA_CR_RR02 | ER_VESPA_CR_RR02 |

### 7.2 Output Directory

All feeds are generated to: `./reports/today/eod/`

### 7.3 Packaging

Files are packaged into a single ZIP:
```
MxMGB_MR_Credit_Sens_{Region}_{YYYYMMDD}.zip
```

### 7.4 Delivery via MFT

| Destination | MFT ID Pattern |
|-------------|----------------|
| Plato | MurexMGBSensitivitiesToPlato_{Region} |
| Risk Data Warehouse | MurexMGBSensitivitiesToRDS_{Region} |

---

## 8. Processing Schedule

### 8.1 Daily Timeline (GMT)

| Time | Event | Description |
|------|-------|-------------|
| 18:00 | Market Data Close | Credit curves calibrated |
| 21:00 | Valuation Batch Complete | All trades valued |
| 03:00 | Extraction Start | Regional batch processing |
| 04:00 | Extraction Complete | All 8 feeds generated |
| 05:00 | Packaging | ZIP file created |
| 05:30 | MFT Delivery | Files sent to Plato/RDS |

### 8.2 Regional Processing

| Region | Extraction Start | Extraction End | Delivery |
|--------|------------------|----------------|----------|
| LN | 03:00 GMT | 04:00 GMT | 05:30 GMT |
| HK | 21:00 HKT | 22:00 HKT | 23:30 HKT |
| NY | 22:00 EST | 23:00 EST | 00:30 EST+1 |
| SP | 21:00 SGT | 22:00 SGT | 23:30 SGT |

---

## 9. Target Systems

### 9.1 Downstream Consumers

| System | Purpose | Critical Feeds |
|--------|---------|----------------|
| **Plato** | FRTB risk calculations | All 8 feeds |
| **Risk Data Warehouse** | Storage, reporting | All 8 feeds |
| **VESPA Reporting** | Regulatory reporting | All 8 feeds |
| **P&L Attribution** | P&L decomposition | CR Instrument Spread, RR01, RR02 |
| **Model Validation** | Sensitivity comparison | RR01 vs RR02, Zero vs Par |

### 9.2 Integration Summary

| Integration | Protocol | Format |
|-------------|----------|--------|
| Plato | SFTP via MFT | CSV in ZIP |
| Risk DW | SFTP via MFT | CSV in ZIP |
| VESPA Reporting | Database load | Table format |

---

## 10. Feed Documentation Index

### 10.1 Individual Feed Documents

Each feed has 3-tier documentation:

| Feed | BRD | IT Config | IDD |
|------|-----|-----------|-----|
| CR Delta Zero | [cr-delta-zero-brd.md](./cr-delta-zero/cr-delta-zero-brd.md) | [cr-delta-zero-config.md](./cr-delta-zero/cr-delta-zero-config.md) | [cr-delta-zero-idd.md](./cr-delta-zero/cr-delta-zero-idd.md) |
| CR Delta Par | [cr-delta-par-brd.md](./cr-delta-par/cr-delta-par-brd.md) | [cr-delta-par-config.md](./cr-delta-par/cr-delta-par-config.md) | [cr-delta-par-idd.md](./cr-delta-par/cr-delta-par-idd.md) |
| CR Basis Rate | [cr-basis-rate-brd.md](./cr-basis-rate/cr-basis-rate-brd.md) | [cr-basis-rate-config.md](./cr-basis-rate/cr-basis-rate-config.md) | [cr-basis-rate-idd.md](./cr-basis-rate/cr-basis-rate-idd.md) |
| CR Par CDS Rate | [cr-par-cds-rate-brd.md](./cr-par-cds-rate/cr-par-cds-rate-brd.md) | [cr-par-cds-rate-config.md](./cr-par-cds-rate/cr-par-cds-rate-config.md) | [cr-par-cds-rate-idd.md](./cr-par-cds-rate/cr-par-cds-rate-idd.md) |
| CR Instrument Spread | [cr-instrument-spread-brd.md](./cr-instrument-spread/cr-instrument-spread-brd.md) | [cr-instrument-spread-config.md](./cr-instrument-spread/cr-instrument-spread-config.md) | [cr-instrument-spread-idd.md](./cr-instrument-spread/cr-instrument-spread-idd.md) |
| CR Corr01 | [cr-corr01-brd.md](./cr-corr01/cr-corr01-brd.md) | [cr-corr01-config.md](./cr-corr01/cr-corr01-config.md) | [cr-corr01-idd.md](./cr-corr01/cr-corr01-idd.md) |
| CR RR01 | [cr-rr01-brd.md](./cr-rr01/cr-rr01-brd.md) | [cr-rr01-config.md](./cr-rr01/cr-rr01-config.md) | [cr-rr01-idd.md](./cr-rr01/cr-rr01-idd.md) |
| CR RR02 | [cr-rr02-brd.md](./cr-rr02/cr-rr02-brd.md) | [cr-rr02-config.md](./cr-rr02/cr-rr02-config.md) | [cr-rr02-idd.md](./cr-rr02/cr-rr02-idd.md) |

### 10.2 Related Documents

| Document | ID | Description |
|----------|-----|-------------|
| [Feeds Overview](./feeds-overview.md) | MR-L7-003 | Parent feeds document |
| [Data Dictionary](../data-dictionary.md) | MR-L7-002 | Field definitions |
| [IR Sensitivities Overview](./ir-sensitivities-overview.md) | IR-SENS-OVW-001 | Interest rate feeds |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-02 | Initial version | Risk Technology |

### 11.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Technical review | Annual | January 2026 |
| Architecture review | On major change | As needed |
| Integration review | Quarterly | April 2025 |

---

*End of Document*
