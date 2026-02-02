---
# Document Metadata
document_id: CR-DP-CFG-001
document_name: CR Delta Par Feed - IT Configuration Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Steering Committee

# Parent Reference
parent_document: CR-DP-BRD-001
feed_id: CR-DP-001
---

# CR Delta Par Feed - IT Configuration Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-DP-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Related BRD** | CR-DP-BRD-001 |

---

## 1. Configuration Overview

This document specifies the technical configuration for the CR Delta Par feed within the Murex Global Operating Model (GOM). The feed extracts par spread sensitivities (CR01 Par) using the M_CR01__PA2 and M_CR01__PA1 fields.

### 1.1 Component Summary

| Component Type | Name | Purpose |
|---------------|------|---------|
| Simulation Views | VW_Vespa_Sensitivities, VW_Vespa_Sensitivities_CRDI | Source sensitivity data |
| Datamart Tables | TBL_VESPA_SENS_REP, TBL_VESPA_SENSCI_REP | Staging for extraction |
| Reference Tables | SB_CP_REP, TBL_CRD_RECOVERY_REP, SB_TP_* | Static data |
| Feeders | FD_VESPA_SENS, FD_VESPA_SENSCI | Populate datamart tables |
| Data Extractors | DE_VESPA_CR_DELTAPAR | Extract to CSV |
| Extraction Requests | ER_VESPA_CR_DELTAPAR | Execute extraction |
| Processing Scripts | **_MR_VESPA_DP_RPT | Post-processing |
| Batch Events | BE_VESPA_DP_** | Scheduled execution |

---

## 2. Murex GOM Configuration

### 2.1 Simulation Views

#### 2.1.1 Non-CRDI: VW_Vespa_Sensitivities

| Property | Value |
|----------|-------|
| **View Name** | VW_Vespa_Sensitivities |
| **Purpose** | Par credit sensitivities for single-name products |
| **Key Sensitivity Fields** | M_CR01__PA2 (local), M_CR01__PA1 (USD) |
| **Output** | CR01 Par - Par spread sensitivity |

**Filter Criteria (Standard Non-CRDI)**:
```sql
STP_STATUS IN ('RELE', 'VERI', 'STTL')
AND LEGAL_ENTITY = 'MGB'
AND CREDIT_DELTA_DATE IS NOT NULL
AND ISSUER IS NOT NULL
AND M_GROUP <> 'CRDI'
AND M_TYPOLOGY NOT IN ('CRD - GUARANTEE', 'CRD - INSURANCE')
```

**Filter Criteria (Insurance/Guarantee)**:
```sql
STP_STATUS IN ('RELE', 'VERI', 'STTL')
AND LEGAL_ENTITY = 'MGB'
AND CREDIT_DELTA_DATE IS NOT NULL
AND ISSUER IS NOT NULL
AND M_TYPOLOGY IN ('CRD - GUARANTEE', 'CRD - INSURANCE')
```

#### 2.1.2 CRDI: VW_Vespa_Sensitivities_CRDI

| Property | Value |
|----------|-------|
| **View Name** | VW_Vespa_Sensitivities_CRDI |
| **Purpose** | Par credit sensitivities for credit index products |
| **Key Sensitivity Fields** | M_CR01__PA2 (local), M_CR01__PA1 (USD) |
| **Output** | CR01 Par - Index-level par spread sensitivity |

**Filter Criteria**:
```sql
STP_STATUS IN ('RELE', 'VERI', 'STTL')
AND LEGAL_ENTITY = 'MGB'
AND M_GROUP = 'CRDI'
```

### 2.2 Sensitivity Calculation

#### 2.2.1 CR01 Par Calculation Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Sensitivity Type** | CR01 (Par) | Par spread sensitivity |
| **Source Fields** | M_CR01__PA2 (local), M_CR01__PA1 (USD) | Murex simulation fields |
| **Bump Size** | 1 basis point | Par spread shock |
| **Curve Type** | Par Spread Curve | Market-observable spreads |
| **Calculation** | Full Revaluation | Complete MTM recalculation |

**Comparison with CR01 Zero**:
| Aspect | CR01 Par (This Feed) | CR01 Zero |
|--------|---------------------|-----------|
| Source Field (Local) | M_CR01__PA2 | M_CR01 |
| Source Field (USD) | M_CR01__PA1 | M_CR01_USD |
| Curve Type | Par spread | Zero/default spread |

### 2.3 Datamart Tables

#### 2.3.1 TBL_VESPA_SENS_REP (Non-CRDI)

| Property | Value |
|----------|-------|
| **Table Name** | TBL_VESPA_SENS_REP |
| **Schema** | DATAMART |
| **Refresh Mode** | Truncate and Load |
| **Partition** | By ASOF_DATE |

#### 2.3.2 TBL_VESPA_SENSCI_REP (CRDI)

| Property | Value |
|----------|-------|
| **Table Name** | TBL_VESPA_SENSCI_REP |
| **Schema** | DATAMART |
| **Refresh Mode** | Truncate and Load |
| **Partition** | By ASOF_DATE |

### 2.4 Reference Tables

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **SB_CP_REP** | Counterparty definition | M_U_CIF_ID, M_U_GLOBID, M_U_RSK_CTRY |
| **TBL_CRD_RECOVERY_REP** | Credit recovery details | M_REF_OBLI1, M_REF_OBLIG, M_RESTRUCTU |
| **SB_TP_REP** | Transaction details | M_TP_DTEEXP, M_TP_NOMINAL, M_TP_BUY |
| **SB_TP_EXT_REP** | Extended transaction data | M_TP_SECMKT |
| **SB_TP_BD_REP** | Bond-specific transaction data | M_TP_RTCCP02, M_TP_RTCAPI0, M_TP_SECLOT |
| **SB_SE_HEAD_REP** | Security header | M_SE_CODE |
| **TBL_SE_ROOT_REP** | Security root | M_SE_MARKE |
| **SB_CRI_DEF_REP** | Credit Index definition | M_INDEX_LBL |

### 2.5 Feeders

#### 2.5.1 FD_VESPA_SENS (Non-CRDI)

| Property | Value |
|----------|-------|
| **Feeder Name** | FD_VESPA_SENS |
| **Source** | VW_Vespa_Sensitivities |
| **Target** | TBL_VESPA_SENS_REP |
| **Mode** | Full Refresh |

#### 2.5.2 FD_VESPA_SENSCI (CRDI)

| Property | Value |
|----------|-------|
| **Feeder Name** | FD_VESPA_SENSCI |
| **Source** | VW_Vespa_Sensitivities_CRDI |
| **Target** | TBL_VESPA_SENSCI_REP |
| **Mode** | Full Refresh |

---

## 3. Data Extraction Configuration

### 3.1 Data Extractor: DE_VESPA_CR_DELTAPAR

| Property | Value |
|----------|-------|
| **Extractor Name** | DE_VESPA_CR_DELTAPAR |
| **Type** | SQL-based Extraction |
| **Output Format** | CSV |
| **Delimiter** | Semicolon (;) |
| **Header** | Yes |
| **Encoding** | UTF-8 |

### 3.2 Extraction SQL Structure

The extraction uses a three-way UNION ALL structure:

```sql
-- ========================================
-- PART 1: Non-CRDI (excluding Insurance/Guarantee)
-- ========================================
SELECT
    VSP.M_TRADE_NUM AS TRADE_NUM,
    VSP.M_FAMILY AS FAMILY,
    VSP.M_GROUP AS GRP,
    VSP.M_TYPE AS TYP,
    VSP.M_TYPOLOGY AS TYPOLOGY,
    VSP.M_PORTFOLIO AS PORTFOLIO,
    VSP.M_PL_INSTRU AS INSTRUMENT,
    CASE WHEN VSP.M_ISSUER IS NULL
         THEN VSP.M_PL_INSTRU
         ELSE VSP.M_ISSUER END AS ISSUER,
    VSP.M_CURVE_NA1 AS CURVE_NAME,
    VSP.M_DATE__ZER AS DAT,
    VSP.M_RATE AS RECOVERY_RATE,
    VSP.M_CR01__PA2 AS CR01_par_quotation,
    VSP.M_CURRENCY AS CURRENCY,
    cast(CP.M_U_CIF_ID as varchar(10)) AS CIF,
    CP.M_U_GLOBID AS GLOBUS_ID,
    CP.M_U_RSK_CTRY AS COUNTRY,
    CASE WHEN VSP.M_GROUP = 'BOND'
         THEN SE_HEAD.M_SE_CODE
         ELSE rtrim(OBL.M_REF_OBLI1) END AS ISIN,
    TP.M_TP_DTEEXP AS MATURITY,
    OBL.M_REF_OBLIG AS UNDERLYING,
    CASE WHEN OBL.M_RESTRUCTU = 'Yes'
         THEN OBL.M_RESTRUCTU
         ELSE 'NONE' END AS RESTRUCT,
    -- Complex NOTIONAL calculation
    CASE
        WHEN VSP.M_FAMILY = 'IRD' AND VSP.M_GROUP = 'RTRN' AND VSP.M_TYPE = 'SWAP'
        THEN TP_BD.M_TP_RTCAPI0 * TP_BD.M_TP_SECLOT
        WHEN VSP.M_GROUP IN ('BOND', 'CDS')
        THEN CASE WHEN VSP.M_GROUP = 'BOND'
                  THEN TP_BD.M_TP_RTCCP02
                  ELSE abs(TP_BD.M_TP_RTCCP02) END
        ELSE CASE WHEN ltrim(TP.M_TP_BUY) = 'S'
                  THEN (-1) * TP.M_TP_NOMINAL
                  ELSE TP.M_TP_NOMINAL END
    END AS NOTIONAL,
    -- MARKET field logic
    CASE
        WHEN VSP.M_FAMILY IN ('IRD', 'EQD') THEN TP_EXT.M_TP_SECMKT
        WHEN VSP.M_FAMILY = 'CRD' AND VSP.M_GROUP = 'CDS'
        THEN (SELECT DISTINCT ROOT.M_SE_MARKE
              FROM DM.TBL_SE_ROOT_REP ROOT
              WHERE ROOT.M_SE_LABEL = OBL.M_REF_OBLI2
              AND ROOT.M_SE_DED IS NULL
              AND ROOT.M_REF_DATA = @MxDataSetKey:N)
        ELSE ''
    END AS MARKET,
    VSP.M_CR01__PA1 AS CR01_par_quotation_USD
FROM DM.TBL_VESPA_SENS_REP VSP
LEFT JOIN DM.SB_CP_REP CP ON VSP.M_ISSUER = CP.M_DSP_LABEL
    AND CP.M_REF_DATA = VSP.M_REF_DATA
LEFT JOIN DM.TBL_CRD_RECOVERY_REP OBL ON VSP.M_TRADE_NUM = OBL.M_NB
    AND VSP.M_REF_DATA = OBL.M_REF_DATA AND VSP.M_GROUP = 'CDS'
JOIN DM.SB_TP_REP TP ON TP.M_REF_DATA = VSP.M_REF_DATA
    AND VSP.M_TRADE_NUM = TP.M_NB
JOIN DM.SB_TP_EXT_REP TP_EXT ON TP_EXT.M_REF_DATA = VSP.M_REF_DATA
    AND VSP.M_TRADE_NUM = TP_EXT.M_NB
JOIN DM.SB_TP_BD_REP TP_BD ON TP_BD.M_REF_DATA = VSP.M_REF_DATA
    AND VSP.M_TRADE_NUM = TP_BD.M_NB
LEFT JOIN DM.SB_SE_HEAD_REP SE_HEAD ON SE_HEAD.M_SE_D_LABEL = TP.M_INSTRUMENT
    AND SE_HEAD.M_REF_DATA = TP.M_REF_DATA
WHERE VSP.M_REF_DATA = @MxDataSetKey:N
    AND TP.M_TP_LENTDSP = @LegalEntity:C
    AND TP.M_STP_STATUS IN ('RELE', 'VERI', 'STTL')
    AND rtrim(VSP.M_DATE__ZER) IS NOT NULL
    AND rtrim(VSP.M_ISSUER) IS NOT NULL
    AND VSP.M_GROUP <> 'CRDI'
    AND VSP.M_TYPOLOGY NOT IN ('CRD - GUARANTEE', 'CRD - INSURANCE')

UNION ALL

-- ========================================
-- PART 2: Insurance and Guarantee Products
-- ========================================
SELECT
    -- Same field structure as Part 1
    -- Additional join condition: OBL.M_INSTRUMEN = OBL.M_ISSUER
FROM DM.TBL_VESPA_SENS_REP VSP
-- Same joins with additional constraint
WHERE VSP.M_TYPOLOGY IN ('CRD - GUARANTEE', 'CRD - INSURANCE')

UNION ALL

-- ========================================
-- PART 3: Credit Index Products (CRDI)
-- ========================================
SELECT
    VSP.M_TRADE_NUM AS TRADE_NUM,
    VSP.M_FAMILY AS FAMILY,
    VSP.M_GROUP AS GRP,
    VSP.M_TYPE AS TYP,
    VSP.M_TYPOLOGY AS TYPOLOGY,
    VSP.M_PORTFOLIO AS PORTFOLIO,
    VSP.M_PL_INSTRU AS INSTRUMENT,
    VSP.M_PL_INSTRU AS ISSUER,           -- Index label
    VSP.M_PL_INSTRU AS CURVE_NAME,       -- Index label
    VSP.M_DATE AS DAT,
    0 AS RECOVERY_RATE,                   -- Set to 0 for indices
    VSP.M_CR01__PA2 AS CR01_par_quotation,
    VSP.M_CURRENCY AS CURRENCY,
    cast(0 as varchar(10)) AS CIF,        -- Not applicable
    '' AS GLOBUS_ID,                      -- Not applicable
    '' AS COUNTRY,                        -- Multi-country
    '' AS ISIN,                           -- Not applicable
    TP.M_TP_DTEEXP AS MATURITY,
    '' AS UNDERLYING,                     -- Not applicable
    'NONE' AS RESTRUCT,                   -- Not applicable
    abs(TP_BD.M_TP_RTCCP02) AS NOTIONAL,
    '' AS MARKET,                         -- Not applicable
    VSP.M_CR01__PA1 AS CR01_par_quotation_USD
FROM DM.TBL_VESPA_SENSCI_REP VSP
JOIN DM.SB_TP_REP TP ON TP.M_REF_DATA = VSP.M_REF_DATA
    AND VSP.M_TRADE_NUM = TP.M_NB
JOIN SB_TP_BD_REP TP_BD ON TP_BD.M_REF_DATA = VSP.M_REF_DATA
    AND VSP.M_TRADE_NUM = TP_BD.M_NB
LEFT JOIN DM.SB_CRI_DEF_REP CRI ON VSP.M_PL_INSTRU = CRI.M_INDEX_LBL
    AND CRI.M_REF_DATA = VSP.M_REF_DATA
WHERE VSP.M_REF_DATA = @MxDataSetKey:N
    AND TP.M_TP_LENTDSP = @LegalEntity:C
    AND TP.M_STP_STATUS IN ('RELE', 'VERI', 'STTL')
    AND VSP.M_GROUP = 'CRDI'
```

### 3.3 Extraction Request: ER_VESPA_CR_DELTAPAR

| Property | Value |
|----------|-------|
| **Request Name** | ER_VESPA_CR_DELTAPAR |
| **Data Extractor** | DE_VESPA_CR_DELTAPAR |
| **Output Directory** | /data/feeds/vespa/cr_delta_par/ |
| **File Pattern** | MxMGB_MR_Credit_CS01Par_{REGION}_{YYYYMMDD}.csv |

### 3.4 Output File Configuration

| Property | Value |
|----------|-------|
| **File Name Pattern** | MxMGB_MR_Credit_CS01Par_{REGION}_{YYYYMMDD}.csv |
| **Example** | MxMGB_MR_Credit_CS01Par_LN_20250102.csv |
| **Field Count** | 23 |
| **Delimiter** | Semicolon (;) |
| **Record Terminator** | LF |
| **Quoting** | None (semicolon separated) |

---

## 4. Processing Scripts

### 4.1 Regional Processing Scripts

| Region | Script Name | Purpose |
|--------|-------------|---------|
| London | LN_MR_VESPA_DP_RPT | Process LN par credit delta |
| Hong Kong | HK_MR_VESPA_DP_RPT | Process HK par credit delta |
| New York | NY_MR_VESPA_DP_RPT | Process NY par credit delta |
| Singapore | SP_MR_VESPA_DP_RPT | Process SP par credit delta |

### 4.2 Script Functionality

```bash
#!/bin/bash
# **_MR_VESPA_DP_RPT Processing Script Template

# 1. Validate input files
validate_input_files()

# 2. Apply data quality checks
check_mandatory_fields()
validate_cr01_par_values()
check_currency_codes()

# 3. Apply FX conversion (if needed)
apply_fx_rates()

# 4. Generate output file
generate_output_file()

# 5. Archive source files
archive_processed_files()

# 6. Package with other sensitivities
package_to_zip()  # MxMGB_MR_Credit_Sens_Region_YYYYMMDD.zip

# 7. Trigger downstream notifications
notify_downstream_systems()
```

### 4.3 Data Quality Checks

| Check | Rule | Action |
|-------|------|--------|
| Mandatory Fields | All required fields populated | Reject record |
| CR01 Par Range | CR01 Par within reasonable bounds | Flag for review |
| Currency Validation | Valid ISO currency code | Reject record |
| Issuer Check | Non-CRDI must have issuer | Use PL Instrument |
| Duplicate Check | No duplicate trade/curve/date combinations | Take latest |

---

## 5. Batch Configuration

### 5.1 Batch Events

| Batch Event | Region | Schedule | Dependencies |
|-------------|--------|----------|--------------|
| BE_VESPA_DP_LN | London | 04:30 GMT | BE_VALUATION_LN |
| BE_VESPA_DP_HK | Hong Kong | 20:30 GMT (T) | BE_VALUATION_HK |
| BE_VESPA_DP_NY | New York | 02:30 GMT | BE_VALUATION_NY |
| BE_VESPA_DP_SP | Singapore | 21:30 GMT (T) | BE_VALUATION_SP |

### 5.2 Batch Sequence

```
BE_PAR_CREDIT_CURVES_** (Par credit curve calibration)
    ↓
BE_VALUATION_** (Valuation batch)
    ↓
FD_VESPA_SENS / FD_VESPA_SENSCI (Feeder execution)
    ↓
BE_VESPA_DP_** (CR Delta Par extraction batch)
    ↓
**_MR_VESPA_DP_RPT (Processing script)
    ↓
process_reports.sh (Package to zip)
    ↓
File delivery to VESPA
```

### 5.3 Batch Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| BUSINESS_DATE | :SYSDATE-1 | Previous business day |
| MDS_SET | {REGION}CLOSE | Regional market data set |
| LEGAL_ENTITY | MGB | Meridian Global Bank |
| TIMEOUT | 120 mins | Maximum batch runtime |
| RETRY_COUNT | 3 | Number of retry attempts |

---

## 6. Environment Configuration

### 6.1 Environment Details

| Environment | Purpose | Database | Schedule |
|-------------|---------|----------|----------|
| DEV | Development testing | MXDEV | On-demand |
| UAT | User acceptance testing | MXUAT | Daily (delayed) |
| PROD | Production | MXPROD | Daily (live) |

### 6.2 File System Paths

| Environment | Path |
|-------------|------|
| DEV | /data/dev/feeds/vespa/cr_delta_par/ |
| UAT | /data/uat/feeds/vespa/cr_delta_par/ |
| PROD | /data/prod/feeds/vespa/cr_delta_par/ |

### 6.3 Connection Details

| System | Connection | Protocol |
|--------|------------|----------|
| Murex → Datamart | JDBC | TNS |
| Datamart → File System | Direct | Local FS |
| File System → VESPA | SFTP | SSH |

---

## 7. Monitoring and Alerting

### 7.1 Monitoring Points

| Monitor | Threshold | Alert |
|---------|-----------|-------|
| Batch completion | >06:00 GMT | L2 Support |
| Record count variance | >10% vs T-1 | L2 Support |
| CR01 Par vs CR01 Zero variance | >20% | RAV Team |
| CR01 Par outliers | >10 std dev | RAV Team |
| Missing issuers | Any | Credit Data Team |
| File delivery | >06:30 GMT | L2 Support |

### 7.2 Alert Configuration

| Alert Type | Recipient | Channel |
|------------|-----------|---------|
| Batch failure | Risk Technology | Email, SMS |
| SLA breach | Risk Technology, RAV | Email, SMS |
| Data quality issue | RAV Team | Email |
| Downstream delay | VESPA Support | Email |

---

## 8. Recovery Procedures

### 8.1 Batch Failure Recovery

| Failure Type | Recovery Action |
|--------------|-----------------|
| Par credit curve failure | Use T-1 curves, flag positions |
| Feeder failure | Rerun feeder, check source data |
| Extraction failure | Rerun extraction, check SQL |
| File transfer failure | Retry SFTP, check connectivity |
| Valuation failure | Escalate to L2, use T-1 values |

### 8.2 Data Recovery

| Scenario | Recovery Steps |
|----------|----------------|
| Missing positions | 1. Check feeder logs 2. Verify source view 3. Rerun feeder |
| Incorrect CR01 Par | 1. Verify M_CR01__PA2/PA1 source 2. Check par curves 3. Rerun calculation |
| Duplicate records | 1. Check UNION logic 2. Apply deduplication 3. Regenerate file |

---

## 9. Change Control

### 9.1 Configuration Changes

| Change Type | Approval Required | Lead Time |
|-------------|-------------------|-----------|
| Field addition | Risk Technology + RAV | 2 weeks |
| Filter change | Risk Technology | 1 week |
| Schedule change | Risk Technology | 3 days |
| New region | Risk Technology + MLRC | 4 weeks |

### 9.2 Version Control

| Component | Repository | Branch Strategy |
|-----------|------------|-----------------|
| SQL scripts | GitLab | Feature branches |
| Shell scripts | GitLab | Feature branches |
| Batch config | Murex Workflow | Change tickets |
| Documentation | Confluence | Version history |

---

## 10. Related Documentation

| Document | ID | Relationship |
|----------|-----|--------------|
| [CR Delta Par BRD](./cr-delta-par-brd.md) | CR-DP-BRD-001 | Business requirements |
| [CR Delta Par IDD](./cr-delta-par-idd.md) | CR-DP-IDD-001 | Interface specification |
| [CR Delta Zero Config](../cr-delta-zero/cr-delta-zero-config.md) | CR-DZ-CFG-001 | Related Zero config |
| [Murex GOM Guide](../../murex-gom-guide.md) | MR-L7-GOM | GOM reference |
| [Batch Operations Guide](../../batch-operations.md) | MR-L7-BATCH | Batch procedures |

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
| Performance review | Quarterly | April 2025 |
| Security review | Annual | January 2026 |

---

*End of Document*
