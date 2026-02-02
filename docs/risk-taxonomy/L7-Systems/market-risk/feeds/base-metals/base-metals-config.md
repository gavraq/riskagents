---
# Document Metadata
document_id: BM-CFG-001
document_name: Base Metals Sensitivities Feed - IT Configuration
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Risk Technology
approving_committee: Risk Technology Change Board

# Parent Reference
parent_document: BM-BRD-001
feed_id: BM-001
---

# Base Metals Sensitivities Feed - IT Configuration

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | BM-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Executive Summary

This document specifies the IT configuration for extracting Base Metals sensitivity data from Murex and delivering it to downstream risk systems. The feed uses Murex's GOM (Generic Object Model) framework with specialized simulation views for commodity Greeks calculation.

---

## 2. System Architecture

### 2.1 High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MUREX TRADING SYSTEM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │   Trades     │───►│  Valuation   │───►│ Sensitivities │                  │
│  │   (Base      │    │   Engine     │    │  Calculation  │                  │
│  │   Metals)    │    │              │    │  (Greeks)     │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                   │
│                                                 │                            │
│                                                 ▼                            │
│                            ┌───────────────────────────────────┐            │
│                            │    VW_SENSITIVITIES_BM            │            │
│                            │    (Simulation View)              │            │
│                            └───────────────────────────────────┘            │
│                                                 │                            │
└─────────────────────────────────────────────────┼────────────────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GOM EXTRACTION LAYER                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    ER_SENSITIVITIES_BM                                │   │
│  │                    (Extraction Request)                               │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │                DE_SENSITIVITIES_BM                              │  │   │
│  │  │                (Data Extractor)                                 │  │   │
│  │  │  ┌──────────────────────────────────────────────────────────┐  │  │   │
│  │  │  │                14 Extraction Files (per region)          │  │  │   │
│  │  │  │  ┌─────────────────┬─────────────────┬────────────────┐  │  │   │   │
│  │  │  │  │ Delta Files (4) │ Gamma Files (2) │ Qty Files (3)  │  │  │   │   │
│  │  │  │  │ AdFwdDeltaMT    │ DAdFwdGammaMT   │ Qty_Lots       │  │  │   │   │
│  │  │  │  │ AdFwdDeltaUS    │ DAdFwdGammaUS   │ Qty_Unit       │  │  │   │   │
│  │  │  │  │ DAdFwdDeltaMT   │                 │ Qty_USD        │  │  │   │   │
│  │  │  │  │ DAdFwdDeltaUS   │                 │                │  │  │   │   │
│  │  │  │  ├─────────────────┼─────────────────┼────────────────┤  │  │   │   │
│  │  │  │  │ Vol Files (5)   │ Time Files (1)  │                │  │  │   │   │
│  │  │  │  │ Vega            │ Theta           │                │  │  │   │   │
│  │  │  │  │ WeightedVega    │                 │                │  │  │   │   │
│  │  │  │  │ Volga           │                 │                │  │  │   │   │
│  │  │  │  │ Vanna           │                 │                │  │  │   │   │
│  │  │  │  └─────────────────┴─────────────────┴────────────────┘  │  │   │   │
│  │  │  └──────────────────────────────────────────────────────────┘  │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                 │                            │
└─────────────────────────────────────────────────┼────────────────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATAMART LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐       │
│  │ SB_SENSI_BM.REP  │───►│   TF_SENS_BM     │───►│  Merged Output   │       │
│  │ (Datamart Table) │    │   (Feeder)       │    │  File            │       │
│  └──────────────────┘    └──────────────────┘    └──────────────────┘       │
│                                                          │                   │
└──────────────────────────────────────────────────────────┼───────────────────┘
                                                           │
                                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DELIVERY LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐         ┌──────────────────┐                          │
│  │       MFT        │────────►│      Plato       │                          │
│  │                  │         │  (Risk Engine)   │                          │
│  │                  │────┐    └──────────────────┘                          │
│  └──────────────────┘    │    ┌──────────────────┐    ┌──────────────────┐  │
│                          └───►│       RDS        │───►│      VESPA       │  │
│                               │                  │    │  (Risk Reporting)│  │
│                               └──────────────────┘    └──────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Overview

| Component | Type | Purpose |
|-----------|------|---------|
| VW_SENSITIVITIES_BM | Simulation View | Calculate base metals Greeks |
| ER_SENSITIVITIES_BM | Extraction Request | Configure extraction parameters |
| DE_SENSITIVITIES_BM | Data Extractor | Extract data from simulation view |
| SB_SENSI_BM.REP | Datamart Table | Staging table for extracted data |
| TF_SENS_BM | Feeder | Transform and output to file |
| merge_files.sh | Shell Script | Merge 14 extraction files into one |

---

## 3. Murex GOM Configuration

### 3.1 Simulation View

**View Name**: `VW_SENSITIVITIES_BM`

| Property | Value |
|----------|-------|
| **View Type** | Sensitivity Simulation |
| **Asset Class Filter** | Base Metals |
| **Calculation Type** | Full Revaluation |
| **Output Granularity** | Position × Tenor × Strike |

#### 3.1.1 Sensitivity Calculations Enabled

| Sensitivity | Murex Field | Bump Definition |
|-------------|-------------|-----------------|
| Adapted Forward Delta (MT) | ADAPTED_FWD_DELTA_MT | $1/MT price bump |
| Adapted Forward Delta (USD) | ADAPTED_FWD_DELTA_USD | $1/MT price bump |
| Discounted Adapted Forward Delta (MT) | DISC_ADAPTED_FWD_DELTA_MT | $1/MT, discounted |
| Discounted Adapted Forward Delta (USD) | DISC_ADAPTED_FWD_DELTA_USD | $1/MT, discounted |
| Discounted Adapted Forward Gamma (MT) | DISC_ADAPTED_FWD_GAMMA_MT | Second derivative |
| Discounted Adapted Forward Gamma (USD) | DISC_ADAPTED_FWD_GAMMA_USD | Second derivative |
| Quantity (Lots) | QTY_LOTS | Native field |
| Quantity (MT) | QTY_UNIT | Lots × Lot Size |
| Quantity (USD) | QTY_USD | MT × Price |
| Vega | VEGA | 1% relative vol bump |
| Weighted Vega | WEIGHTED_VEGA | Custom calculation |
| Volga | VOLGA | Vol of vol |
| Vanna | VANNA | Cross-Greek |
| Theta | THETA | 1-day time decay |

#### 3.1.2 Weighted Vega Custom Calculation

**Murex Formula Definition**:
```
IF (Vega <> 0.0) THEN
  RESULT := sqrt(30.0 / (Date - GetHorizonDate())) * (1.0/100.0) * Vega * 100.0;
ELSE
  RESULT := 0.0;
END IF;
```

**Parameters**:
- `Date`: Maturity date of the option
- `GetHorizonDate()`: COB valuation date
- `30.0`: Reference period (1 month = 30 days)
- Factor `(1.0/100.0) * 100.0` cancels out (legacy formula)

### 3.2 Pillar Configuration

#### 3.2.1 Tenor Pillar Set (LME Standard)

**Pillar Set Name**: `PS_LME_STANDARD`

| Pillar ID | Label | Days | Description |
|-----------|-------|------|-------------|
| 1 | Cash | 0 | Spot/Cash settlement |
| 2 | 1M | 22 | One month |
| 3 | 3M | 66 | Three months |
| 4 | 6M | 132 | Six months |
| 5 | 1Y | 264 | One year |
| 6 | 18M | 396 | Eighteen months |
| 7 | 2Y | 528 | Two years |
| 8 | 3Y | 792 | Three years |
| 9 | 5Y | 1320 | Five years |
| 10 | 7Y | 1848 | Seven years |
| 11 | 10Y | 2640 | Ten years |

#### 3.2.2 Volatility Strike Pillar Set (Delta-Based)

**Pillar Set Name**: `PS_DELTA_STRIKES`

| Pillar ID | Delta | Description |
|-----------|-------|-------------|
| 1 | 10 | 10-delta (deep OTM) |
| 2 | 25 | 25-delta (OTM) |
| 3 | 50 | 50-delta (ATM) |
| 4 | 75 | 75-delta (ITM) |
| 5 | 90 | 90-delta (deep ITM) |

### 3.3 Extraction Request

**Request Name**: `ER_SENSITIVITIES_BM`

| Property | Value |
|----------|-------|
| **Simulation View** | VW_SENSITIVITIES_BM |
| **Data Extractor** | DE_SENSITIVITIES_BM |
| **Output Format** | CSV (pipe-delimited) |
| **Include Header** | Yes |
| **Date Format** | YYYYMMDD |
| **Decimal Precision** | 10 |

### 3.4 Data Extractor Configuration

**Extractor Name**: `DE_SENSITIVITIES_BM`

| Property | Value |
|----------|-------|
| **Source View** | VW_SENSITIVITIES_BM |
| **Output Directory** | /murex/extracts/basemetals/ |
| **File Naming** | MxMGB_Sens_BM_{Type}_{Region}_{Date}.csv |
| **Compression** | None |

---

## 4. Regional Configuration

### 4.1 Regional Processing Overview

| Region | Processing Script | Batch Job | Global Filter | Portfolio Node | Status |
|--------|-------------------|-----------|---------------|----------------|--------|
| **LN** | LN_SENS_BM_FDR | BF_SENS_BM_LN | GF_BM_PFOLIOS_LN | BMLN | Active |
| HK | HK_SENS_BM_FDR | BF_SENS_BM_HK | GF_BM_PFOLIOS_HK | PMHK | Dormant |
| NY | NY_SENS_BM_FDR | BF_SENS_BM_NY | GF_BM_PFOLIOS_NY | PMNY | Dormant |
| SP | SP_SENS_BM_FDR | BF_SENS_BM_SP | GF_BM_PFOLIOS_SP | LMSP | Dormant |

### 4.2 Global Filters

#### 4.2.1 London Filter (Primary)

**Filter Name**: `GF_BM_PFOLIOS_LN`

```sql
WHERE portfolio_node IN (
  SELECT node_id FROM hierarchy
  WHERE root_node = 'BMLN'
)
AND book_type = 'TRADING'
AND trade_status = 'LIVE'
AND asset_class = 'BASE_METALS'
```

### 4.3 Market Data Sets

| Region | Market Data Set | Snapshot Time | Current Usage |
|--------|-----------------|---------------|---------------|
| **LN** | LNCLOSE | 18:30 GMT | Primary (all trades) |
| HK | HKCLOSE | 10:30 GMT | Not used |
| NY | NYCLOSE | 22:00 GMT | Not used |
| SP | SPCLOSE | 10:30 GMT | Not used |

---

## 5. Extraction Files

### 5.1 File Inventory (14 Files per Region)

Each region produces 14 separate extraction files which are merged into a single output file:

| # | File Name Pattern | Sensitivity Type | Unit |
|---|-------------------|------------------|------|
| 1 | MxMGB_Sens_BM_AdFwdDeltaMT_{Region}_{Date}.csv | Adapted Forward Delta | MT |
| 2 | MxMGB_Sens_BM_AdFwdDeltaUS_{Region}_{Date}.csv | Adapted Forward Delta | USD |
| 3 | MxMGB_Sens_BM_DAdFwdDeltaMT_{Region}_{Date}.csv | Disc Adapted Forward Delta | MT |
| 4 | MxMGB_Sens_BM_DAdFwdDeltaUS_{Region}_{Date}.csv | Disc Adapted Forward Delta | USD |
| 5 | MxMGB_Sens_BM_DAdFwdGammaMT_{Region}_{Date}.csv | Disc Adapted Forward Gamma | MT |
| 6 | MxMGB_Sens_BM_DAdFwdGammaUS_{Region}_{Date}.csv | Disc Adapted Forward Gamma | USD |
| 7 | MxMGB_Sens_BM_Qty_Lots_{Region}_{Date}.csv | Quantity | Lots |
| 8 | MxMGB_Sens_BM_Qty_Unit_{Region}_{Date}.csv | Quantity | MT |
| 9 | MxMGB_Sens_BM_Qty_USD_{Region}_{Date}.csv | Quantity | USD |
| 10 | MxMGB_Sens_BM_Theta_{Region}_{Date}.csv | Theta | USD |
| 11 | MxMGB_Sens_BM_Vanna_{Region}_{Date}.csv | Vanna | USD |
| 12 | MxMGB_Sens_BM_Vega_{Region}_{Date}.csv | Vega | USD |
| 13 | MxMGB_Sens_BM_Volga_{Region}_{Date}.csv | Volga | USD |
| 14 | MxMGB_Sens_BM_WeightedVega_{Region}_{Date}.csv | Weighted Vega | USD |

### 5.2 File Merge Process

**Script**: `merge_files.sh`

```bash
#!/bin/bash
# Merge 14 Base Metals sensitivity files into single output
# Usage: merge_files.sh <region> <date>

REGION=$1
DATE=$2
INPUT_DIR="/murex/extracts/basemetals/${REGION}"
OUTPUT_DIR="/murex/feeds/basemetals"
OUTPUT_FILE="MxMGB_Sens_BM_Combined_${REGION}_${DATE}.csv"

# Create header from first file
head -1 ${INPUT_DIR}/MxMGB_Sens_BM_AdFwdDeltaMT_${REGION}_${DATE}.csv > ${OUTPUT_DIR}/${OUTPUT_FILE}

# Append data from all 14 files (skip headers)
for file in ${INPUT_DIR}/MxMGB_Sens_BM_*_${REGION}_${DATE}.csv; do
  tail -n +2 "$file" >> ${OUTPUT_DIR}/${OUTPUT_FILE}
done

# Generate row count for reconciliation
wc -l ${OUTPUT_DIR}/${OUTPUT_FILE} > ${OUTPUT_DIR}/${OUTPUT_FILE}.count

echo "Merged output: ${OUTPUT_DIR}/${OUTPUT_FILE}"
```

---

## 6. Datamart Configuration

### 6.1 Datamart Table

**Table Name**: `SB_SENSI_BM.REP`

| Column | Data Type | Description |
|--------|-----------|-------------|
| EXTRACTION_DATE | DATE | Date of extraction |
| TRADE_ID | VARCHAR(50) | Murex trade identifier |
| POSITION_ID | VARCHAR(50) | Position identifier |
| BOOK_CODE | VARCHAR(20) | Trading book code |
| DESK_CODE | VARCHAR(20) | Trading desk code |
| DIVISION_CODE | VARCHAR(20) | Division code |
| ENTITY_CODE | VARCHAR(20) | Legal entity code |
| METAL_CODE | VARCHAR(10) | Base metal code (CU, AL, etc.) |
| METAL_NAME | VARCHAR(50) | Full metal name |
| PRODUCT_TYPE | VARCHAR(30) | Product classification |
| OPTION_TYPE | VARCHAR(10) | Call/Put indicator |
| MATURITY_DATE | DATE | Option/forward maturity |
| PILLAR_DATE | DATE | Assigned pillar date |
| PILLAR_LABEL | VARCHAR(10) | Pillar label (Cash, 1M, etc.) |
| DELTA_PILLAR | NUMBER(3) | Delta strike pillar (10-90) |
| SENSITIVITY_TYPE | VARCHAR(30) | Type of sensitivity |
| SENSITIVITY_VALUE | NUMBER(20,10) | Sensitivity value |
| SENSITIVITY_UNIT | VARCHAR(10) | Unit (USD, MT, Lots) |
| MARKET_DATA_SET | VARCHAR(20) | Market data set used |
| CALCULATION_DATE | DATE | Date of calculation |
| REGION_CODE | VARCHAR(5) | Processing region |

### 6.2 Feeder Configuration

**Feeder Name**: `TF_SENS_BM`

| Property | Value |
|----------|-------|
| **Source Table** | SB_SENSI_BM.REP |
| **Output Format** | CSV (pipe-delimited) |
| **Output Directory** | /murex/feeds/basemetals/ |
| **File Name Pattern** | MxMGB_Sens_BM_{Type}_{Region}_{Date}.csv |
| **Include Header** | Yes |
| **Sort Order** | TRADE_ID, SENSITIVITY_TYPE, PILLAR_DATE |

---

## 7. Batch Processing

### 7.1 Batch Job Sequence

| Step | Job Name | Description | Dependency | Duration |
|------|----------|-------------|------------|----------|
| 1 | BJ_VALUATION_BM | Run base metals valuation | Market data loaded | 45 min |
| 2 | BJ_SENS_CALC_BM | Calculate sensitivities | BJ_VALUATION_BM | 30 min |
| 3 | BF_SENS_BM_LN | Extract London sensitivities | BJ_SENS_CALC_BM | 20 min |
| 4 | BJ_MERGE_BM_LN | Merge 14 files | BF_SENS_BM_LN | 5 min |
| 5 | BJ_DELIVER_BM | Transfer to downstream | BJ_MERGE_BM_LN | 10 min |

### 7.2 Batch Schedule

| Job | Schedule | Start Time | SLA |
|-----|----------|------------|-----|
| BJ_VALUATION_BM | Daily | 19:00 GMT | 20:00 |
| BJ_SENS_CALC_BM | Daily | 20:00 GMT | 21:00 |
| BF_SENS_BM_LN | Daily | 21:00 GMT | 22:00 |
| BJ_MERGE_BM_LN | Daily | 22:00 GMT | 22:30 |
| BJ_DELIVER_BM | Daily | 22:30 GMT | 05:30 |

### 7.3 Error Handling

| Error Type | Action | Alert |
|------------|--------|-------|
| Valuation failure | Retry once, then escalate | Pager: L2 Support |
| Extraction failure | Retry once, use T-1 if fails | Email: Risk Ops |
| Merge failure | Manual intervention | Email: Risk Technology |
| Delivery failure | Retry 3 times | Pager: MFT Support |

---

## 8. SQL Extraction Queries

### 8.1 Main Extraction Query

```sql
SELECT
  e.extraction_date,
  t.trade_id,
  t.position_id,
  h.book_code,
  h.desk_code,
  h.division_code,
  h.entity_code,
  u.metal_code,
  u.metal_name,
  t.product_type,
  t.option_type,
  t.maturity_date,
  p.pillar_date,
  p.pillar_label,
  s.delta_pillar,
  s.sensitivity_type,
  s.sensitivity_value,
  s.sensitivity_unit,
  e.market_data_set,
  e.calculation_date,
  e.region_code
FROM
  SB_SENSI_BM.REP s
  JOIN extraction_run e ON s.extraction_id = e.extraction_id
  JOIN trade t ON s.trade_id = t.trade_id
  JOIN hierarchy h ON t.book_code = h.book_code
  JOIN underlying u ON t.underlying_id = u.underlying_id
  JOIN pillar_mapping p ON s.maturity_date BETWEEN p.start_date AND p.end_date
WHERE
  e.extraction_date = :COB_DATE
  AND e.region_code = :REGION
  AND s.sensitivity_value <> 0
ORDER BY
  t.trade_id,
  s.sensitivity_type,
  p.pillar_date,
  s.delta_pillar;
```

### 8.2 Hierarchy Resolution Query (Bookman)

```sql
SELECT
  b.book_code,
  b.book_name,
  d.desk_code,
  d.desk_name,
  div.division_code,
  div.division_name,
  e.entity_code,
  e.entity_name
FROM
  bookman_book b
  JOIN bookman_desk d ON b.desk_id = d.desk_id
  JOIN bookman_division div ON d.division_id = div.division_id
  JOIN bookman_entity e ON div.entity_id = e.entity_id
WHERE
  b.book_code = :BOOK_CODE
  AND b.effective_date <= :COB_DATE
  AND (b.expiry_date IS NULL OR b.expiry_date > :COB_DATE);
```

### 8.3 Metal Reference Query

```sql
SELECT
  metal_code,
  metal_name,
  lme_code,
  lot_size_mt,
  currency,
  price_unit
FROM
  ref_base_metals
WHERE
  active_flag = 'Y';
```

---

## 9. Delivery Configuration

### 9.1 MFT Transfer

| Property | Value |
|----------|-------|
| **Protocol** | SFTP |
| **Source Path** | /murex/feeds/basemetals/ |
| **File Pattern** | MxMGB_Sens_BM_Combined_*.csv |
| **Compression** | GZIP |
| **Encryption** | PGP (recipient key) |

### 9.2 Target Systems

| Target | Path | Format | Frequency |
|--------|------|--------|-----------|
| **Plato** | /plato/inbound/basemetals/ | CSV (pipe) | Daily |
| **RDS** | /rds/inbound/sensitivities/ | CSV (pipe) | Daily |
| **VESPA** | Via RDS forward | CSV (pipe) | Daily |

### 9.3 Control File

A control file accompanies each data file:

**File Name**: `MxMGB_Sens_BM_Combined_{Region}_{Date}.ctl`

```
FILE_NAME=MxMGB_Sens_BM_Combined_LN_20250102.csv.gz.pgp
ROW_COUNT=125847
CHECKSUM=a1b2c3d4e5f6...
EXTRACTION_DATE=20250102
REGION=LN
GENERATION_TIME=2025-01-02T22:15:00Z
```

---

## 10. Monitoring and Alerting

### 10.1 Monitoring Points

| Checkpoint | Expected | Alert Threshold |
|------------|----------|-----------------|
| Valuation complete | 20:00 GMT | +30 min |
| Sensitivity calculation | 21:00 GMT | +30 min |
| Extraction complete | 22:00 GMT | +30 min |
| File merge complete | 22:30 GMT | +15 min |
| Delivery to Plato | 05:30 GMT | +30 min |
| Row count | >100,000 | <90,000 or >150,000 |

### 10.2 Alert Distribution

| Severity | Recipients | Method |
|----------|------------|--------|
| Critical | L2 Support, Risk Ops | Pager, SMS |
| High | Risk Technology | Email, Slack |
| Medium | Operations | Email |
| Low | Monitoring Dashboard | Dashboard only |

---

## 11. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Base Metals BRD](./base-metals-brd.md) | BM-BRD-001 | Business requirements |
| [Base Metals IDD](./base-metals-idd.md) | BM-IDD-001 | Interface specification |
| [Sensitivities IT Config](../sensitivities/sensitivities-config.md) | SENS-CFG-001 | General sensitivities |
| [Bookman Hierarchy Guide](../../reference/bookman-guide.md) | REF-003 | Hierarchy management |

---

## 12. Document Control

### 12.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-02 | Initial version | Risk Technology Change Board |

### 12.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Configuration audit | Quarterly | April 2025 |
| Performance review | Monthly | February 2025 |

---

*End of Document*
