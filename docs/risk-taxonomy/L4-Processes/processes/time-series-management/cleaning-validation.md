---
# Process Metadata
process_id: MR-L4-005d
process_name: Cleaning & Validation
version: 1.0
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Reporting, Analysis & Validation (RAV)
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-005  # Time Series Management
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-022  # BCBS 239
l2_risk_types:
  - MR-L2-001   # Market Risk
l7_systems:
  - SYS-MR-010  # Time Series Service
---

# Cleaning & Validation Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-005d |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Time Series Management (MR-L4-005) |
| **Owner** | Head of Reporting, Analysis & Validation (RAV) |

---

## 1. Purpose

The Cleaning & Validation process ensures that collected price observations meet quality standards before being used in VaR and other risk calculations. This process applies automated validation rules, flags exceptions for review, and ensures data integrity throughout the time series.

---

## 2. Scope

### 2.1 Validation Checks Applied

| Check Category | Description |
|----------------|-------------|
| **Completeness** | All required observations present |
| **Staleness** | Observations not older than threshold |
| **Reasonableness** | Values within expected ranges |
| **Consistency** | Cross-source agreement |
| **Continuity** | No unexplained discontinuities |

### 2.2 Out of Scope

- Source selection (handled in Risk Factor Setup)
- Gap filling (handled in Proxying Process)
- Curve construction (handled in Curve Stripping)

---

## 3. Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        CLEANING & VALIDATION PROCESS                                    │
│                        (Daily - London Time)                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [From Price Collection]
              │
              ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         1. AUTOMATED VALIDATION RULES                                   │
│                                                                                         │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│   │ STALE CHECK     │  │ SPIKE DETECTION │  │ ZERO/NEGATIVE   │  │ CROSS-SOURCE    │    │
│   │                 │  │                 │  │ CHECK           │  │ VALIDATION      │    │
│   │ Age > threshold │  │ |Return| > 3σ   │  │ Value ≤ 0       │  │ |Diff| > 5%     │    │
│   │ → Exception     │  │ → Exception     │  │ → Exception     │  │ → Exception     │    │
│   └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘    │
│            │                    │                    │                    │             │
│            └────────────────────┴────────────────────┴────────────────────┘             │
│                                           │                                             │
└───────────────────────────────────────────┼─────────────────────────────────────────────┘
                                            │
                         ┌──────────────────┴──────────────────┐
                         │                                     │
                         ▼                                     ▼
              ┌─────────────────────┐             ┌─────────────────────┐
              │   PASS              │             │   EXCEPTION         │
              │                     │             │                     │
              │   Observation       │             │   Flagged for       │
              │   accepted          │             │   review            │
              └──────────┬──────────┘             └──────────┬──────────┘
                         │                                   │
                         │                                   ▼
                         │                        ┌─────────────────────┐
                         │                        │ 2. EXCEPTION QUEUE  │
                         │                        │                     │
                         │                        │ • Stale observations│
                         │                        │ • Spike alerts      │
                         │                        │ • Zero values       │
                         │                        │ • Source conflicts  │
                         │                        └──────────┬──────────┘
                         │                                   │
                         │                                   ▼
                         │                        ┌─────────────────────┐
                         │                        │ 3. MANUAL REVIEW    │
                         │                        │    (RAV Team)       │
                         │                        │                     │
                         │                        │ For each exception: │
                         │                        │ • Check alt sources │
                         │                        │ • Validate against  │
                         │                        │   market events     │
                         │                        │ • Determine action  │
                         │                        └──────────┬──────────┘
                         │                                   │
                         │           ┌───────────────────────┼───────────────────────┐
                         │           │                       │                       │
                         │           ▼                       ▼                       ▼
                         │  ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
                         │  │ CONFIRM       │      │ CORRECT       │      │ ESCALATE      │
                         │  │               │      │               │      │               │
                         │  │ Observation   │      │ Use alternate │      │ To Market     │
                         │  │ is valid      │      │ value/source  │      │ Risk/RMA      │
                         │  │ (e.g., real   │      │               │      │               │
                         │  │ market move)  │      │               │      │               │
                         │  └───────┬───────┘      └───────┬───────┘      └───────┬───────┘
                         │          │                      │                      │
                         └──────────┴──────────────────────┴──────────────────────┘
                                                  │
                                                  ▼
                                    ┌─────────────────────────┐
                                    │ 4. VALIDATED STAGING    │
                                    │                         │
                                    │ Clean observations      │
                                    │ ready for curve         │
                                    │ stripping and           │
                                    │ time series construction│
                                    └─────────────────────────┘
                                                  │
                                                  ▼
                                    [To Curve Stripping / Time Series Construction]
```

---

## 4. Validation Rules

### 4.1 Staleness Check (TS-C03)

**Purpose**: Ensure observations are current and reflect recent market conditions.

| Parameter | Setting | Governance |
|-----------|---------|------------|
| **Default threshold** | 2 business days | Model Forum approval |
| **FX spot** | 1 business day | More liquid, tighter threshold |
| **Illiquid credit** | 5 business days | Less frequent observations acceptable |

**Exception Handling**:
- Stale observations flagged but not automatically rejected
- Reviewer determines if stale value should be used or proxy applied
- Recurring staleness triggers source review

### 4.2 Spike Detection (TS-C04)

**Purpose**: Identify potentially erroneous observations caused by data errors.

**Calculation**:
```
Daily Return = (Value_t - Value_{t-1}) / Value_{t-1}
Z-Score = |Return - Mean_Return| / StdDev_Return

If Z-Score > Threshold → Flag as spike
```

| Parameter | Setting | Notes |
|-----------|---------|-------|
| **Default threshold** | 3σ | Flags ~0.3% of normal observations |
| **Lookback for σ calculation** | 252 business days | Rolling annual window |
| **Override for volatility regime** | 5σ | Applied during known high-vol periods |

**Exception Handling**:
- Cross-reference against news/market events
- Check alternative sources
- If genuine market move, confirm and document
- If data error, use alternative source or previous day

### 4.3 Zero/Negative Value Check (TS-C05)

**Purpose**: Reject clearly invalid observations.

| Risk Factor Type | Zero Allowed? | Negative Allowed? |
|------------------|:-------------:|:-----------------:|
| Interest rates | Yes (near-zero rates) | Yes (negative rates) |
| FX rates | No | No |
| Equity prices | No | No |
| Credit spreads | No | No |
| Volatility | No | No |

**Exception Handling**:
- Zero/negative where not permitted → automatic rejection
- Use backup source or previous day value

### 4.4 Cross-Source Validation (TS-C06)

**Purpose**: Ensure primary and backup sources agree within tolerance.

**Calculation**:
```
Variance = |Primary_Value - Backup_Value| / Primary_Value

If Variance > Threshold → Flag for review
```

| Risk Factor Type | Variance Threshold |
|------------------|:-----------------:|
| FX spot | 0.5% |
| Interest rates | 5 bps |
| Credit spreads | 10% |
| Equity prices | 1% |
| Volatility | 5% (relative) |

**Exception Handling**:
- Determine which source is correct
- Document source preference rationale
- If persistent disagreement, escalate to RMA for source review

---

## 5. Exception Queue Management

### 5.1 Exception Workflow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           EXCEPTION QUEUE STATUSES                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐            │
│  │ NEW     │────▶│ ASSIGNED│────▶│ REVIEWED│────▶│ RESOLVED│────▶│ CLOSED  │            │
│  │         │     │         │     │         │     │         │     │         │            │
│  │Auto-    │     │Analyst  │     │Decision │     │Action   │     │Audit    │            │
│  │generated│     │assigned │     │made     │     │applied  │     │trail    │            │
│  └─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘            │
│                                                                                         │
│  Target: All exceptions resolved by 21:00 GMT                                           │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Exception Priority

| Severity | Criteria | Target Resolution | Escalation |
|----------|----------|-------------------|------------|
| **Critical** | >10 risk factors affected; or major asset class | 30 minutes | RAV Manager immediately |
| **High** | 5-10 risk factors; or key trading curve | 1 hour | RAV Team Lead |
| **Medium** | 1-4 risk factors; spike or staleness | 2 hours | RAV Analyst |
| **Low** | Minor variance; single observation | EOD | RAV Analyst |

### 5.3 Resolution Actions

| Action | Description | Audit Requirement |
|--------|-------------|-------------------|
| **Confirm** | Accept observation as valid | Document market rationale |
| **Correct** | Use alternative value | Document source and reason |
| **Reject** | Exclude observation | Document reason; may trigger proxy |
| **Escalate** | Refer to Market Risk/RMA | Document rationale |

---

## 6. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| CV-C01 | All observations pass validation rules before use | Preventive | RAV |
| CV-C02 | Exceptions assigned within 15 minutes | Detective | RAV |
| CV-C03 | 4-eyes review for material exceptions | Preventive | RAV + MR |
| CV-C04 | Exception resolution documented | Detective | RAV |
| CV-C05 | Exception queue cleared before T+1 cutoff | Preventive | RAV |
| CV-C06 | Recurring exceptions trigger root cause analysis | Detective | RAV |

---

## 7. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| Validation batch complete | 19:45 GMT | 20:00 GMT | RAV Manager |
| Exception queue assignment | 15 minutes | 30 minutes | RAV Team Lead |
| Critical exceptions resolved | 30 minutes | 1 hour | RAV Manager |
| All exceptions resolved | 21:00 GMT | 21:30 GMT | Market Risk |
| Exception rate | <2% | <5% | RAV Manager |

---

## 8. Monitoring and Reporting

### 8.1 Real-Time Monitoring

- **Exception Dashboard**: Live count by severity and type
- **Resolution Timer**: Time-in-queue per exception
- **Coverage Status**: Pass/fail rates by risk factor type

### 8.2 Daily Reports

| Report | Recipients | Content |
|--------|------------|---------|
| **Validation Summary** | RAV, Market Risk | Pass/fail counts, exception breakdown |
| **Exception Log** | RAV, Audit | All exceptions with resolution |
| **Recurring Issues** | RMA, Market Risk | Patterns requiring structural fix |

### 8.3 Monthly Analysis

- **Exception trend analysis**: Identifying systemic issues
- **Source quality scoring**: Which sources generate most exceptions
- **Threshold review**: Are thresholds appropriately calibrated?

---

## 9. Integration Points

### 9.1 Upstream Dependencies

| Process | Dependency |
|---------|------------|
| **Price Collection** | Provides raw observations |
| **Risk Factor Setup** | Defines validation parameters |

### 9.2 Downstream Consumers

| Process | Data Provided |
|---------|---------------|
| **Curve Stripping** | Validated par rates |
| **Time Series Construction** | Clean observations |
| **Proxying Process** | Gap list (rejected observations) |

---

## 10. Related Documents

| Document | Relationship |
|----------|--------------|
| [Time Series Management](./time-series-overview.md) | Parent process |
| [Price Collection](./price-collection.md) | Upstream - provides raw data |
| [Curve Stripping](./curve-stripping.md) | Downstream - uses validated rates |
| [Proxying Process](./proxying-process.md) | Related - fills rejected/missing data |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |

---

*End of Document*
