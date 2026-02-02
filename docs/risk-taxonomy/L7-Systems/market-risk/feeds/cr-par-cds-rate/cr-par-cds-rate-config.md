---
# Document Metadata
document_id: CR-PAR-CFG-001
document_name: CR Par CDS Rate Feed - IT Configuration Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Steering Committee

# Parent Reference
parent_document: CR-PAR-BRD-001
feed_id: CR-PAR-001
---

# CR Par CDS Rate Feed - IT Configuration Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-PAR-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Related BRD** | CR-PAR-BRD-001 |

---

## 1. Configuration Overview

This document specifies the technical configuration for the CR Par CDS Rate feed within the Murex Global Operating Model (GOM). The feed extracts **par CDS conventional spread** (market data) by joining position data with credit curve data from TBL_AC_CRDCURVES_REP.

### 1.1 Component Summary

| Component Type | Name | Purpose |
|---------------|------|---------|
| Simulation Views | VW_Vespa_Sensitivities, VW_Vespa_Sensitivities_CRDI | Source position data |
| Datamart Tables | TBL_VESPA_SENS_REP, TBL_VESPA_SENSCI_REP | Position staging |
| Credit Curve Table | TBL_AC_CRDCURVES_REP | Par CDS spread source |
| Reference Tables | SB_CP_REP, TBL_CRD_RECOVERY_REP, SB_TP_REP | Static data |
| Data Extractors | DE_VESPA_CR_PARCDS | Extract to CSV |
| Extraction Requests | ER_VESPA_CR_Par_CDS_Rate | Execute extraction |
| Processing Scripts | **_MR_VESPA_PAR_RPT | Post-processing |
| Batch Events | BE_VESPA_PAR_** | Scheduled execution |

---

## 2. Murex GOM Configuration

### 2.1 Credit Curve Source

#### 2.1.1 TBL_AC_CRDCURVES_REP

| Property | Value |
|----------|-------|
| **Table Name** | TBL_AC_CRDCURVES_REP |
| **Schema** | DATAMART |
| **Purpose** | Credit curve market data for non-bonds |
| **Key Field** | M_CONVENTIO (Conventional spread) |
| **Market Data Viewer** | MKTP_CRED_CURVES |

**Key Columns**:
| Column | Description | Usage |
|--------|-------------|-------|
| M_LABEL | Curve label/name | Join to CURVE_NAME |
| M_TENOR | Tenor pillar | Join to DATE |
| M_CONVENTIO | Conventional spread (bps) | PAR_CDS = M_CONVENTIO/100 |
| M_RESTRUCT | Restructuring clause | Reference |
| M_REF_DATA | Market data set reference | Filter |

### 2.2 Simulation Views

#### 2.2.1 Non-CRDI: VW_Vespa_Sensitivities

| Property | Value |
|----------|-------|
| **View Name** | VW_Vespa_Sensitivities |
| **Purpose** | Credit positions for single-name products |
| **Key Join Field** | M_CURVE_NA1 (curve name) |
| **Tenor Field** | M_DATE__ZER |

**Filter Criteria**:
```sql
STP_STATUS IN ('RELE', 'VERI', 'STTL')
AND LEGAL_ENTITY = 'MGB'
AND CREDIT_DELTA_DATE IS NOT NULL
AND ISSUER IS NOT NULL
AND M_GROUP <> 'CRDI'
```

#### 2.2.2 CRDI: VW_Vespa_Sensitivities_CRDI

| Property | Value |
|----------|-------|
| **View Name** | VW_Vespa_Sensitivities_CRDI |
| **Purpose** | Credit index positions |
| **Key Join Field** | M_PL_INSTRU (index label) |
| **Tenor Field** | M_DATE |

**Filter Criteria**:
```sql
STP_STATUS IN ('RELE', 'VERI', 'STTL')
AND LEGAL_ENTITY = 'MGB'
AND M_GROUP = 'CRDI'
```

### 2.3 PAR_CDS Calculation

| Scenario | Calculation | Source |
|----------|-------------|--------|
| **CDS Products** | M_CONVENTIO / 100 | TBL_AC_CRDCURVES_REP |
| **Bond Products** | 0 (hardcoded) | N/A - bonds use z-spread |
| **CRDI Products** | M_CONVENTIO / 100 | TBL_AC_CRDCURVES_REP (via index label) |

### 2.4 Datamart Tables

#### 2.4.1 TBL_VESPA_SENS_REP (Non-CRDI)

| Property | Value |
|----------|-------|
| **Table Name** | TBL_VESPA_SENS_REP |
| **Schema** | DATAMART |
| **Refresh Mode** | Truncate and Load |
| **Partition** | By ASOF_DATE |

#### 2.4.2 TBL_VESPA_SENSCI_REP (CRDI)

| Property | Value |
|----------|-------|
| **Table Name** | TBL_VESPA_SENSCI_REP |
| **Schema** | DATAMART |
| **Refresh Mode** | Truncate and Load |
| **Partition** | By ASOF_DATE |

---

## 3. Data Extraction Configuration

### 3.1 Data Extractor: DE_VESPA_CR_PARCDS

| Property | Value |
|----------|-------|
| **Extractor Name** | DE_VESPA_CR_PARCDS |
| **Type** | SQL-based Extraction |
| **Output Format** | CSV |
| **Delimiter** | Semicolon (;) |
| **Header** | Yes |
| **Encoding** | UTF-8 |

### 3.2 Extraction SQL Structure

```sql
-- ========================================
-- PART 1: Non-CRDI Positions
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
    VSP.M_DATE__ZER AS DTE,
    VSP.M_RATE AS RECOVERY_RATE,
    -- PAR_CDS: Set to 0 for bonds, otherwise get from credit curve
    CASE WHEN VSP.M_GROUP = 'BOND'
         THEN 0
         ELSE CUR.M_CONVENTIO / 100
    END AS PAR_CDS,
    VSP.M_CURRENCY2 AS CURRENCY,
    CP.M_U_CIF_ID AS CIF,
    CP.M_U_GLOBID AS GLOBUS_ID,
    NVL(CP.M_U_RSK_CTRY, ' ') AS COUNTRY,
    NVL(OBL.M_REF_OBLI1, ' ') AS ISIN,
    TP.M_TP_DTEEXP AS MATURITY,
    NVL(OBL.M_REF_OBLIG, ' ') AS UNDERLYING
FROM DM.TBL_VESPA_SENS_REP VSP
LEFT JOIN DM.SB_CP_REP CP
    ON VSP.M_ISSUER = CP.M_DSP_LABEL
    AND CP.M_REF_DATA = @MxDataSetKey:N
LEFT JOIN DM.TBL_CRD_RECOVERY_REP OBL
    ON VSP.M_TRADE_NUM = OBL.M_NB
    AND VSP.M_REF_DATA = OBL.M_REF_DATA
    AND VSP.M_GROUP = 'CDS'
JOIN DM.SB_TP_REP TP
    ON TP.M_REF_DATA = VSP.M_REF_DATA
    AND VSP.M_TRADE_NUM = TP.M_NB
    AND TP.M_TP_LENTDSP = @LegalEntity:C
    AND TP.M_STP_STATUS IN ('RELE', 'VERI', 'STTL')
-- Join to credit curve table for PAR_CDS
LEFT JOIN (
    SELECT DISTINCT
        CURVE.M_RESTRUCT,
        CURVE.M_LABEL,
        CURVE.M_TENOR,
        CURVE.M_CONVENTIO
    FROM TBL_AC_CRDCURVES_REP CURVE
    WHERE CURVE.M_REF_DATA = @MxHistoricalData1:N
) CUR ON CUR.M_LABEL = VSP.M_CURVE_NA1
    AND CUR.M_TENOR = VSP.M_DATE__ZER
WHERE VSP.M_REF_DATA = @MxDataSetKey:N
    AND VSP.M_DATE__ZER IS NOT NULL
    AND VSP.M_ISSUER IS NOT NULL
    AND VSP.M_GROUP <> 'CRDI'

UNION ALL

-- ========================================
-- PART 2: CRDI (Credit Index) Positions
-- ========================================
SELECT
    VSP.M_TRADE_NUM AS TRADE_NUM,
    VSP.M_FAMILY AS FAMILY,
    VSP.M_GROUP AS GRO,
    VSP.M_TYPE AS TYP,
    VSP.M_TYPOLOGY AS TYPOLOGY,
    VSP.M_PORTFOLIO AS PORTFOLIO,
    VSP.M_PL_INSTRU AS INSTRUMENT,
    VSP.M_PL_INSTRU AS ISSUER,           -- Index label
    VSP.M_PL_INSTRU AS CURVE_NAME,       -- Index label
    VSP.M_DATE AS DTE,
    0 AS RECOVERY_RATE,                   -- Set to 0 for indices
    CUR.M_CONVENTIO / 100 AS PAR_CDS,    -- From index curve
    VSP.M_CURRENCY AS CURRENCY,
    0 AS CIF,                             -- Not applicable
    '' AS GLOBUS_ID,                      -- Not applicable
    ' ' AS COUNTRY,                       -- Multi-country
    ' ' AS ISIN,                          -- Not applicable
    TP.M_TP_DTEEXP AS MATURITY,
    ' ' AS UNDERLYING                     -- Not applicable
FROM DM.TBL_VESPA_SENSCI_REP VSP
JOIN DM.SB_TP_REP TP
    ON TP.M_REF_DATA = VSP.M_REF_DATA
    AND VSP.M_TRADE_NUM = TP.M_NB
    AND TP.M_TP_LENTDSP = @LegalEntity:C
    AND TP.M_STP_STATUS IN ('RELE', 'VERI', 'STTL')
-- Join to credit curve table using PL Instrument (index label)
LEFT JOIN (
    SELECT DISTINCT
        CURVE.M_RESTRUCT,
        CURVE.M_LABEL,
        CURVE.M_CONVENTIO
    FROM TBL_AC_CRDCURVES_REP CURVE
    WHERE CURVE.M_REF_DATA = @MxHistoricalData1:N
) CUR ON CUR.M_LABEL = VSP.M_PL_INSTRU
WHERE VSP.M_REF_DATA = @MxDataSetKey:N
    AND VSP.M_GROUP = 'CRDI'
```

### 3.3 Extraction Request: ER_VESPA_CR_Par_CDS_Rate

| Property | Value |
|----------|-------|
| **Request Name** | ER_VESPA_CR_Par_CDS_Rate |
| **Data Extractor** | DE_VESPA_CR_PARCDS |
| **Output Directory** | /data/feeds/vespa/cr_par_cds/ |
| **File Pattern** | MxMGB_MR_Credit_ParCDS_{REGION}_{YYYYMMDD}.csv |

### 3.4 Output File Configuration

| Property | Value |
|----------|-------|
| **File Name Pattern** | MxMGB_MR_Credit_ParCDS_{REGION}_{YYYYMMDD}.csv |
| **Example** | MxMGB_MR_Credit_ParCDS_LN_20250102.csv |
| **Field Count** | 19 |
| **Delimiter** | Semicolon (;) |
| **Record Terminator** | LF |

---

## 4. Processing Scripts

### 4.1 Regional Processing Scripts

| Region | Script Name | Purpose |
|--------|-------------|---------|
| London | LN_MR_VESPA_PAR_RPT | Process LN par CDS rates |
| Hong Kong | HK_MR_VESPA_PAR_RPT | Process HK par CDS rates |
| New York | NY_MR_VESPA_PAR_RPT | Process NY par CDS rates |
| Singapore | SP_MR_VESPA_PAR_RPT | Process SP par CDS rates |

### 4.2 Script Functionality

```bash
#!/bin/bash
# **_MR_VESPA_PAR_RPT Processing Script Template

# 1. Validate input files
validate_input_files()

# 2. Apply data quality checks
check_mandatory_fields()
validate_par_cds_values()
check_currency_codes()

# 3. Generate output file
generate_output_file()

# 4. Archive source files
archive_processed_files()

# 5. Package with other sensitivities
package_to_zip()  # MxMGB_MR_Credit_Sens_Region_YYYYMMDD.zip

# 6. Trigger downstream notifications
notify_downstream_systems()
```

### 4.3 Data Quality Checks

| Check | Rule | Action |
|-------|------|--------|
| Mandatory Fields | All required fields populated | Reject record |
| PAR_CDS Range | PAR_CDS between 0 and 0.50 (typical) | Flag outliers |
| Bond PAR_CDS | GROUP = 'BOND' implies PAR_CDS = 0 | Flag violations |
| Currency Validation | Valid ISO currency code | Reject record |
| Issuer Check | Non-CRDI must have issuer | Use INSTRUMENT |

---

## 5. Batch Configuration

### 5.1 Batch Events

| Batch Event | Region | Schedule | Dependencies |
|-------------|--------|----------|--------------|
| BE_VESPA_PAR_LN | London | 04:30 GMT | BE_CREDIT_CURVES_LN |
| BE_VESPA_PAR_HK | Hong Kong | 20:30 GMT (T) | BE_CREDIT_CURVES_HK |
| BE_VESPA_PAR_NY | New York | 02:30 GMT | BE_CREDIT_CURVES_NY |
| BE_VESPA_PAR_SP | Singapore | 21:30 GMT (T) | BE_CREDIT_CURVES_SP |

### 5.2 Batch Sequence

```
BE_CREDIT_CURVES_** (Credit curve calibration)
    ↓
TBL_AC_CRDCURVES_REP populated
    ↓
BE_VALUATION_** (Valuation batch)
    ↓
FD_VESPA_SENS / FD_VESPA_SENSCI (Feeder execution)
    ↓
BE_VESPA_PAR_** (Par CDS extraction batch)
    ↓
**_MR_VESPA_PAR_RPT (Processing script)
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
| MxHistoricalData1 | {REGION}CLOSE | Historical data for curves |
| LEGAL_ENTITY | MGB | Meridian Global Bank |
| TIMEOUT | 90 mins | Maximum batch runtime |
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
| DEV | /data/dev/feeds/vespa/cr_par_cds/ |
| UAT | /data/uat/feeds/vespa/cr_par_cds/ |
| PROD | /data/prod/feeds/vespa/cr_par_cds/ |

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
| PAR_CDS outliers | >0.30 (3000 bps) | RAV Team |
| Missing curve data | >1% positions | Market Data Control |
| File delivery | >06:30 GMT | L2 Support |

### 7.2 Alert Configuration

| Alert Type | Recipient | Channel |
|------------|-----------|---------|
| Batch failure | Risk Technology | Email, SMS |
| SLA breach | Risk Technology, RAV | Email, SMS |
| Curve data issue | Market Data Control | Email |
| Downstream delay | VESPA Support | Email |

---

## 8. Recovery Procedures

### 8.1 Batch Failure Recovery

| Failure Type | Recovery Action |
|--------------|-----------------|
| Credit curve table empty | Escalate to Market Data Control |
| Curve join failure | Check M_LABEL/M_TENOR join keys |
| Feeder failure | Rerun feeder, check source data |
| Extraction failure | Rerun extraction, check SQL |
| File transfer failure | Retry SFTP, check connectivity |

### 8.2 Data Recovery

| Scenario | Recovery Steps |
|----------|----------------|
| Missing positions | 1. Check feeder logs 2. Verify source view 3. Rerun feeder |
| Incorrect PAR_CDS | 1. Verify TBL_AC_CRDCURVES_REP 2. Check join keys 3. Rerun |
| Missing curve data | 1. Check curve calibration 2. Escalate to Market Data |

---

## 9. Change Control

### 9.1 Configuration Changes

| Change Type | Approval Required | Lead Time |
|-------------|-------------------|-----------|
| Field addition | Risk Technology + RAV | 2 weeks |
| Curve source change | Market Data Control | 1 week |
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
| [CR Par CDS Rate BRD](./cr-par-cds-rate-brd.md) | CR-PAR-BRD-001 | Business requirements |
| [CR Par CDS Rate IDD](./cr-par-cds-rate-idd.md) | CR-PAR-IDD-001 | Interface specification |
| [CR Delta Zero Config](../cr-delta-zero/cr-delta-zero-config.md) | CR-DZ-CFG-001 | Related config |
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
