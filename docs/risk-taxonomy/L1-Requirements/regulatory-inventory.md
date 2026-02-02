# L1: Regulatory Requirements Inventory

**Reference Bank**: Meridian Global Bank
**Version**: 1.1
**Last Updated**: 2025-12-11
**Review Date**: 2026-06-11
**Change Summary**: Added SS5/25 (climate), FCA SDR; SS5/25 replaces SS3/19

---

## 1. Overview

### 1.1 Purpose

This document provides a comprehensive inventory of regulatory requirements that drive risk management activities at Meridian Global Bank. As a UK-headquartered, PRA-regulated institution with global operations, the Bank must comply with multiple regulatory frameworks across jurisdictions.

The regulatory inventory serves as:
- **L1 of the Risk Taxonomy**: The apex of the pyramid - the "why" that cascades to all other layers
- **Change Driver**: New or amended regulations trigger updates throughout the taxonomy
- **Completeness Check**: Ensures all regulatory requirements are mapped to risk activities
- **Skills Context**: Enables AI agents to understand regulatory context for queries

### 1.2 Regulatory Landscape

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        REGULATORY HIERARCHY                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐     │
│  │  INTERNATIONAL   │   │    EUROPEAN      │   │    UK PRIMARY    │     │
│  │    STANDARDS     │   │   LEGISLATION    │   │   LEGISLATION    │     │
│  │                  │   │                  │   │                  │     │
│  │  Basel III/IV    │   │  CRR/CRR III     │   │  FSMA 2000       │     │
│  │  BCBS Standards  │   │  CRD VI          │   │  Banking Act     │     │
│  │  IOSCO           │   │  BRRD II         │   │  2009            │     │
│  │  FSB Guidelines  │   │  MiFID II/MiFIR  │   │                  │     │
│  └────────┬─────────┘   └────────┬─────────┘   └────────┬─────────┘     │
│           │                      │                      │               │
│           └──────────────────────┼──────────────────────┘               │
│                                  ▼                                      │
│                    ┌──────────────────────────┐                         │
│                    │   PRA/FCA RULES &        │                         │
│                    │   SUPERVISORY STATEMENTS │                         │
│                    │                          │                         │
│                    │   PRA Rulebook           │                         │
│                    │   Supervisory Statements │                         │
│                    │   Policy Statements      │                         │
│                    │   Dear CEO Letters       │                         │
│                    └──────────────────────────┘                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Scope

| In Scope | Out of Scope |
|----------|--------------|
| Prudential regulation (PRA) | Tax legislation |
| Conduct regulation (FCA) | Employment law |
| Market conduct rules | Environmental permits |
| Financial crime prevention | Corporate law |
| Resolution and recovery | Health & safety |

---

## 2. Regulatory Framework Categories

### 2.1 Category Overview

| Category | Primary Regulator | Key Frameworks | Risk Domains Impacted |
|----------|------------------|----------------|----------------------|
| **Capital Requirements** | PRA | CRR/CRD, Basel III/IV | Market, Credit, Operational |
| **Liquidity Requirements** | PRA | CRR, LCR/NSFR | Liquidity |
| **Market Risk** | PRA | FRTB, IMA | Market |
| **Credit Risk** | PRA | SA-CR, IRB, ECL | Credit |
| **Operational Risk** | PRA | SMA, Operational Resilience | Operational |
| **Model Risk** | PRA/Fed | SS1/23, SR 11-7 | Model |
| **Conduct & Markets** | FCA | MiFID II, MAR | Operational, Market |
| **Financial Crime** | FCA/NCA | MLR, Sanctions | Operational |
| **Climate & ESG** | PRA/FCA | TCFD, SDR | Sustainability |
| **Recovery & Resolution** | PRA/BoE | BRRD II, MREL | All |
| **Data & Reporting** | PRA/FCA | BCBS 239, RegData | All |

---

## 3. Detailed Regulatory Inventory

### 3.1 Capital Requirements Framework

#### REQ-L1-001: Capital Requirements Regulation (CRR/CRR III)

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-001 |
| **Regulation** | Capital Requirements Regulation (EU) 2019/876 as retained in UK law |
| **Regulator** | PRA |
| **Effective Date** | June 2021 (CRR II), Jan 2025 (CRR III - Basel 3.1) |
| **Review Cycle** | Ongoing - significant amendments 2025 |
| **Risk Domains** | Market Risk, Credit Risk, Operational Risk |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Part | Requirement | L2 Risk Type | L3 Policy |
|------|-------------|--------------|-----------|
| Part 2 | Own Funds | All | Capital Policy |
| Part 3, Title I | Credit Risk - SA | CR-L2-001 | Credit Risk Policy |
| Part 3, Title I | Credit Risk - IRB | CR-L2-001 | Credit Risk Policy |
| Part 3, Title II | Counterparty Credit Risk | CR-L2-002 | Credit Risk Policy |
| Part 3, Title III | Market Risk - SA | MR-L2-001 | Market Risk Policy |
| Part 3, Title III | Market Risk - IMA | MR-L2-001 | Market Risk Policy |
| Part 3, Title IV | Operational Risk - SMA | OR-L2-001 | Operational Risk Policy |
| Part 3, Title V | CVA Risk | CR-L2-002/MR-L2-001 | Credit/Market Policy |
| Part 6 | Liquidity | LR-L2-001 | Liquidity Policy |
| Part 7 | Leverage | STR-L2-002 | Capital Policy |
| Part 8 | Disclosure | All | Disclosure Policy |

**Implementation Status**:
- CRR II: ✅ Fully implemented
- CRR III (Basel 3.1): 🔄 Implementation in progress (Jan 2025 go-live)

**Skills Mapping**:
- `pillar-stress-generator` - Stress capital calculations
- `regulatory-research-agent` (new) - Track CRR amendments

---

#### REQ-L1-002: Capital Requirements Directive VI (CRD VI)

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-002 |
| **Regulation** | Capital Requirements Directive (transposed into PRA rules) |
| **Regulator** | PRA |
| **Effective Date** | Various - ongoing implementation |
| **Risk Domains** | All |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Article | Requirement | L2 Risk Type |
|---------|-------------|--------------|
| Art 73-96 | Supervisory Review (Pillar 2) | All |
| Art 74 | Internal Governance | OR-L2-001 |
| Art 76 | Internal Capital (ICAAP) | All |
| Art 77 | Credit and Counterparty Risk | CR-L2-001 |
| Art 78 | Residual Risk | CR-L2-001 |
| Art 79 | Concentration Risk | CR-L2-006 |
| Art 80 | Securitisation Risk | CR-L2-001 |
| Art 81 | Market Risk | MR-L2-001 |
| Art 82 | Interest Rate Risk (Banking Book) | MR-L2-002 |
| Art 83 | Operational Risk | OR-L2-001 |
| Art 84 | Liquidity Risk | LR-L2-001 |

---

### 3.2 Market Risk Framework

#### REQ-L1-003: Fundamental Review of the Trading Book (FRTB)

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-003 |
| **Regulation** | CRR Art 325-361 (FRTB Standardised & IMA) |
| **Regulator** | PRA |
| **Effective Date** | January 2025 (reporting), July 2025 (capital) |
| **Risk Domains** | Market Risk |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Component | CRR Article | Requirement | L5 Control |
|-----------|-------------|-------------|------------|
| Boundary | Art 325 | Trading book boundary | Trading Book Policy |
| SA-TB | Art 325a-325h | Standardised Approach | SA capital calculation |
| SbM | Art 325i-325p | Sensitivities-based Method | Delta, Vega, Curvature |
| DRC | Art 325q-325w | Default Risk Charge | Jump-to-default |
| RRAO | Art 325x | Residual Risk Add-on | Exotic optionality |
| IMA | Art 325az-325bp | Internal Models Approach | ES, DRC, SES |
| P&L Attribution | Art 325bg | PLA test | Daily PLA monitoring |
| Backtesting | Art 325bf | VaR backtesting | Exception tracking |

**Implementation Status**: 🔄 In progress
- SA reporting: Ready for Jan 2025
- IMA application: Submitted to PRA
- P&L Attribution: Parallel running

**Skills Mapping**:
- `pillar-stress-generator` - Stress scenario impacts on FRTB
- `process-documenter` - FRTB implementation process documentation

---

#### REQ-L1-004: PRA SS13/13 - Market Risk

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-004 |
| **Regulation** | Supervisory Statement 13/13 - Market Risk |
| **Regulator** | PRA |
| **Effective Date** | Updated November 2024 |
| **Risk Domains** | Market Risk |
| **Materiality** | HIGH |

**Key Requirements**:

| Section | Topic | Implementation |
|---------|-------|----------------|
| Chapter 2 | Scope of IMA permission | Model perimeter |
| Chapter 3 | VaR model requirements | VaR methodology |
| Chapter 4 | Stressed VaR | SVaR calibration |
| Chapter 5 | IRC requirements | IRC methodology |
| Chapter 6 | CRM requirements | Correlation trading |
| Chapter 7 | Model validation | Independent validation |
| Chapter 8 | Stress testing | Stress framework |
| Chapter 9 | Backtesting | Backtesting framework |

---

### 3.3 Credit Risk Framework

#### REQ-L1-005: CRR Part 3 - Credit Risk

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-005 |
| **Regulation** | CRR Part 3, Title II - Credit Risk |
| **Regulator** | PRA |
| **Effective Date** | Current |
| **Risk Domains** | Credit Risk |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Chapter | Approach | Requirement | L6 Model |
|---------|----------|-------------|----------|
| Ch 2 | SA-CR | Standardised Approach | Exposure mapping |
| Ch 3 | IRB | Internal Ratings Based | PD, LGD, EAD models |
| Ch 4 | CCR | Counterparty Credit Risk | SA-CCR, IMM |
| Ch 5 | CRM | Credit Risk Mitigation | Collateral models |

---

#### REQ-L1-006: IFRS 9 - Expected Credit Loss

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-006 |
| **Regulation** | IFRS 9 Financial Instruments |
| **Regulator** | FRC / PRA (prudential overlay) |
| **Effective Date** | January 2018 |
| **Risk Domains** | Credit Risk |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Phase | Requirement | L6 Model |
|-------|-------------|----------|
| Classification | SPPI test, Business model | Asset classification |
| Stage 1 | 12-month ECL | PD/LGD/EAD |
| Stage 2 | Lifetime ECL | Staging criteria |
| Stage 3 | Lifetime ECL (impaired) | Impairment models |
| SICR | Significant increase in credit risk | Transfer triggers |

**Skills Mapping**:
- `climate-scorecard-filler` - ESG overlay to ECL

---

#### REQ-L1-007: Large Exposures Regime

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-007 |
| **Regulation** | CRR Part 4 - Large Exposures |
| **Regulator** | PRA |
| **Effective Date** | Current |
| **Risk Domains** | Credit Risk - Concentration |
| **Materiality** | HIGH |

**Key Requirements**:

| Article | Requirement | Limit |
|---------|-------------|-------|
| Art 392 | Definition | >10% Tier 1 |
| Art 395 | Limit to single counterparty | 25% Tier 1 |
| Art 395 | Limit to G-SIB | 15% Tier 1 |
| Art 400 | Exemptions | Covered bonds, sovereigns |

---

### 3.4 Operational Risk Framework

#### REQ-L1-008: Operational Risk - SMA

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-008 |
| **Regulation** | CRR Part 3, Title III - Operational Risk |
| **Regulator** | PRA |
| **Effective Date** | January 2025 (SMA go-live) |
| **Risk Domains** | Operational Risk |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Component | Requirement | Data Required |
|-----------|-------------|---------------|
| BIC | Business Indicator Component | 3-year financials |
| ILM | Internal Loss Multiplier | 10-year loss history |
| Loss Data | Loss event collection | Above €20k threshold |

---

#### REQ-L1-009: Operational Resilience

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-009 |
| **Regulation** | PRA SS1/21 - Operational Resilience |
| **Regulator** | PRA/FCA |
| **Effective Date** | March 2022 (initial), March 2025 (full) |
| **Risk Domains** | Operational Risk |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Requirement | Description | Deadline |
|-------------|-------------|----------|
| Important Business Services | Identify and map | Complete |
| Impact Tolerances | Set maximum tolerable disruption | Complete |
| Mapping | Map resources to IBS | Complete |
| Testing | Severe but plausible scenarios | Ongoing |
| Self-Assessment | Annual board attestation | March 2025 |

**Skills Mapping**:
- `process-documenter` - IBS process mapping
- `stakeholder-analysis` - IBS ownership mapping

---

#### REQ-L1-010: PRA SS2/21 - Outsourcing and Third Party Risk

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-010 |
| **Regulation** | SS2/21 Outsourcing and Third Party Risk Management |
| **Regulator** | PRA |
| **Effective Date** | March 2022 |
| **Risk Domains** | Operational Risk |
| **Materiality** | HIGH |

**Key Requirements**:

| Requirement | Description |
|-------------|-------------|
| Materiality Assessment | Assess all outsourcing arrangements |
| Register | Maintain outsourcing register |
| Exit Plans | Document exit strategies |
| Concentration Risk | Monitor provider concentration |
| Notification | Notify PRA of material outsourcing |

---

### 3.5 Liquidity Framework

#### REQ-L1-011: Liquidity Coverage Ratio (LCR)

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-011 |
| **Regulation** | CRR Part 6 - Liquidity |
| **Regulator** | PRA |
| **Effective Date** | Current |
| **Risk Domains** | Liquidity Risk |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Metric | Requirement | Minimum |
|--------|-------------|---------|
| LCR | HQLA / Net outflows (30 days) | ≥100% |
| HQLA | Level 1 / Level 2A / Level 2B | Composition rules |
| Outflows | Stressed outflow assumptions | Regulatory rates |
| Inflows | Capped at 75% of outflows | Cap rules |

---

#### REQ-L1-012: Net Stable Funding Ratio (NSFR)

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-012 |
| **Regulation** | CRR Art 428a-428az |
| **Regulator** | PRA |
| **Effective Date** | June 2021 |
| **Risk Domains** | Liquidity Risk |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Metric | Requirement | Minimum |
|--------|-------------|---------|
| NSFR | ASF / RSF | ≥100% |
| ASF | Available Stable Funding | Liability weighting |
| RSF | Required Stable Funding | Asset weighting |

---

### 3.6 Model Risk Framework

#### REQ-L1-013: PRA SS1/23 - Model Risk Management

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-013 |
| **Regulation** | Supervisory Statement 1/23 - Model Risk Management |
| **Regulator** | PRA |
| **Effective Date** | May 2024 (initial), May 2025 (full) |
| **Risk Domains** | Model Risk |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Principle | Requirement | Implementation |
|-----------|-------------|----------------|
| MRM Framework | Comprehensive MRM policy | Model Risk Policy |
| Model Inventory | Complete model inventory | Model Registry |
| Model Development | Development standards | Methodology docs |
| Model Validation | Independent validation | Validation function |
| Model Use | Appropriate model use | User attestations |
| Data Quality | Data standards | Data quality framework |
| Governance | Board oversight | MRM Committee |

**Skills Mapping**:
- `process-documenter` - MRM process documentation

---

#### REQ-L1-014: SR 11-7 - Model Risk Management (US)

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-014 |
| **Regulation** | Federal Reserve SR Letter 11-7 |
| **Regulator** | Federal Reserve / OCC |
| **Effective Date** | April 2011 |
| **Risk Domains** | Model Risk |
| **Materiality** | HIGH (for US operations) |

**Note**: While a US regulation, SR 11-7 has been influential globally and many of its principles are reflected in PRA SS1/23.

---

### 3.7 Climate & ESG Framework

#### REQ-L1-015: PRA SS5/25 - Climate Risk (Supersedes SS3/19)

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-015 |
| **Regulation** | SS5/25 - Solvent exit planning for non-systemic banks and building societies |
| **Supersedes** | SS3/19 (April 2019) |
| **Regulator** | PRA |
| **Publication Date** | 3 December 2025 (PS25/25) |
| **Effective Date** | 3 December 2025 (immediate) |
| **Key Deadline** | **3 June 2026** - Gap analysis + board-approved action plan required |
| **Risk Domains** | Sustainability Risk, Credit Risk, Market Risk, Operational Risk |
| **Materiality** | **CRITICAL** |

**Key Changes from SS3/19**:

| Area | SS3/19 (Old) | SS5/25 (New) |
|------|--------------|--------------|
| Approach | High-level expectations | Significantly more granular implementation guidance |
| Data | Quantify data limitations | Understand and manage data uncertainty |
| Scenario Analysis | General expectation | Quantitative analysis only where risks are material |
| Proportionality | Limited guidance | Enhanced proportionality for smaller firms |
| Implementation | Principle-based only | Detailed "how to" guidance |

**Key Requirements (SS5/25)**:

| Chapter | Requirement | Implementation |
|---------|-------------|----------------|
| Governance | Board oversight with defined accountability | Climate Risk Committee / Board Risk Committee oversight |
| Risk Management | Integrate climate into all risk types (credit, market, liquidity, op) | Update risk policies, limits, appetite statements |
| Scenario Analysis | Quantitative climate scenario analysis where risks are **significant** | Short, medium, long-term horizons; physical & transition risks |
| Data & Metrics | Understand data limitations; don't let gaps prevent action | Data quality framework, proxy methodologies, uncertainty disclosure |
| Disclosures | TCFD-aligned, expanding to ISSB S2 | Annual climate report, Pillar 3 ESG template |
| Capital | Consider climate in ICAAP/ILAAP | Climate stress capital add-ons where material |

**Critical Deadlines**:

| Milestone | Date | Requirement |
|-----------|------|-------------|
| SS5/25 Effective | 3 December 2025 | Regulation in force |
| Internal Review | By June 2026 | Complete gap analysis vs SS5/25 |
| Action Plan | 3 June 2026 | Board-approved remediation plan submitted |
| Full Compliance | 2026-2027 | Phased implementation per action plan |

**Implementation Status**: 🔴 New - Gap analysis required

**Skills Mapping**:
- `climate-scorecard-filler` - Counterparty climate assessment (physical/transition risks)
- `stress-scenario-suggester` - Climate scenario identification
- `pillar-stress-generator` - Climate stress parameterization
- `regulatory-risk-researcher` - Monitor SS5/25 Q&A and guidance
- `regulatory-change-assessor` - Impact assessment on taxonomy artefacts

**Related Documents**:
- PS25/25 (Policy Statement)
- CP16/24 (Consultation Paper - superseded)
- Climate Financial Risk Forum (CFRF) guidance

---

#### REQ-L1-016: TCFD Recommendations

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-016 |
| **Regulation** | Task Force on Climate-related Financial Disclosures |
| **Regulator** | FCA (mandatory disclosure) |
| **Effective Date** | 2022 (premium listed), expanding |
| **Risk Domains** | Sustainability Risk |
| **Materiality** | HIGH |
| **Note** | Being superseded by ISSB S2 (IFRS S2) globally |

**Key Requirements**:

| Pillar | Requirement |
|--------|-------------|
| Governance | Board and management oversight |
| Strategy | Climate risks and opportunities |
| Risk Management | Integration into risk framework |
| Metrics & Targets | GHG emissions, climate metrics |

---

#### REQ-L1-023: FCA Sustainability Disclosure Requirements (SDR)

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-023 |
| **Regulation** | FCA Sustainability Disclosure Requirements and Investment Labels |
| **Regulator** | FCA |
| **Publication Date** | November 2023 (PS23/16), updated 2024-2025 |
| **Effective Dates** | Phased: Dec 2024 (labels), 2025-2026 (disclosures) |
| **Risk Domains** | Sustainability Risk, Operational Risk |
| **Materiality** | HIGH |

**Scope**: Asset managers, investment firms, wealth managers. Banks impacted through:
- Investment product distribution
- Own asset management activities
- Wealth management businesses

**Key Requirements**:

| Requirement | Description | Deadline |
|-------------|-------------|----------|
| Anti-Greenwashing Rule | Sustainability claims must be fair, clear, not misleading | Immediate |
| Investment Labels | Four voluntary labels (Sustainability Focus, Improvers, Impact, Mixed Goals) | 2 December 2024 |
| Consumer-Facing Disclosures | Pre-contractual, ongoing, and periodic disclosures | H1 2025 |
| Product-Level Disclosures | Detailed sustainability disclosures for labelled products | 2025 |
| Entity-Level Disclosures | Firm-level sustainability reporting | 2026 |
| Naming & Marketing Rules | Restrictions on use of sustainability-related terms | 2 December 2024 |

**Banking Relevance**:

| Business Area | SDR Impact |
|---------------|------------|
| Asset Management | Full scope - labels, disclosures required |
| Wealth Management | Distributor rules, anti-greenwashing |
| Corporate Banking | Advisory on client ESG financing |
| Treasury/Investments | Own book sustainability claims |

**Implementation Status**: 🔄 In progress

**Skills Mapping**:
- `climate-scorecard-filler` - Product sustainability assessment
- `regulatory-risk-researcher` - Monitor FCA SDR updates
- `regulatory-change-assessor` - Impact on product governance

---

### 3.8 Conduct & Markets Framework

#### REQ-L1-017: MiFID II / MiFIR

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-017 |
| **Regulation** | Markets in Financial Instruments (as retained in UK law) |
| **Regulator** | FCA |
| **Effective Date** | January 2018 |
| **Risk Domains** | Operational Risk, Market Risk |
| **Materiality** | HIGH |

**Key Requirements**:

| Area | Requirement |
|------|-------------|
| Best Execution | Best execution policy and monitoring |
| Transaction Reporting | EMIR/MiFIR reporting |
| Record Keeping | Communication recording |
| Product Governance | Product approval process |
| Inducements | Restrictions on inducements |

---

#### REQ-L1-018: Market Abuse Regulation (MAR)

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-018 |
| **Regulation** | UK Market Abuse Regulation |
| **Regulator** | FCA |
| **Effective Date** | Current |
| **Risk Domains** | Operational Risk, Market Risk |
| **Materiality** | HIGH |

**Key Requirements**:

| Area | Requirement |
|------|-------------|
| Insider Lists | Maintain and update |
| PDMR Dealing | Manager transaction notifications |
| Suspicious Orders | Report to FCA |
| Market Manipulation | Surveillance and prevention |

---

### 3.9 Financial Crime Framework

#### REQ-L1-019: Money Laundering Regulations

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-019 |
| **Regulation** | Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017 |
| **Regulator** | FCA / NCA |
| **Effective Date** | Current (amended regularly) |
| **Risk Domains** | Operational Risk |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Requirement | Description |
|-------------|-------------|
| Risk Assessment | Business-wide risk assessment |
| CDD | Customer due diligence |
| EDD | Enhanced due diligence (high risk) |
| Ongoing Monitoring | Transaction monitoring |
| SAR | Suspicious activity reporting |
| Training | Staff training |

---

#### REQ-L1-020: Sanctions Regulations

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-020 |
| **Regulation** | Sanctions and Anti-Money Laundering Act 2018, OFSI regulations |
| **Regulator** | HM Treasury / OFSI |
| **Effective Date** | Ongoing |
| **Risk Domains** | Operational Risk |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Requirement | Description |
|-------------|-------------|
| Screening | Customer and transaction screening |
| Blocking | Asset freezing obligations |
| Reporting | OFSI reporting |
| Licensing | License application process |

---

### 3.10 Recovery & Resolution Framework

#### REQ-L1-021: BRRD II / UK Resolution Regime

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-021 |
| **Regulation** | Bank Recovery and Resolution Directive (UK implementation) |
| **Regulator** | Bank of England |
| **Effective Date** | Current |
| **Risk Domains** | All |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Requirement | Description |
|-------------|-------------|
| Recovery Plan | Annual recovery plan |
| Resolution Pack | Resolution information |
| MREL | Minimum requirement for eligible liabilities |
| Bail-in | Bail-in mechanism preparation |
| Continuity | Operational continuity in resolution |

---

### 3.11 Data & Reporting Framework

#### REQ-L1-022: BCBS 239 - Risk Data Aggregation

| Attribute | Value |
|-----------|-------|
| **Node ID** | REQ-L1-022 |
| **Regulation** | BCBS 239 - Principles for effective risk data aggregation and risk reporting |
| **Regulator** | PRA (via CRD) |
| **Effective Date** | January 2016 |
| **Risk Domains** | All |
| **Materiality** | CRITICAL |

**Key Requirements**:

| Principle | Requirement |
|-----------|-------------|
| Governance | Data governance framework |
| Architecture | Data architecture and IT infrastructure |
| Accuracy | Data accuracy and integrity |
| Completeness | Capture all material risks |
| Timeliness | Timely data for risk management |
| Adaptability | Ability to produce ad-hoc reports |
| Accuracy of Reporting | Report accuracy |
| Comprehensiveness | Reports cover all material risks |
| Clarity | Reports clear and useful |
| Frequency | Appropriate reporting frequency |
| Distribution | Distributed to right people |

**Skills Mapping**:
- `process-documenter` - Data lineage documentation

---

## 4. Regulatory Change Tracking

### 4.1 Current Regulatory Pipeline (2025-2026)

| Regulation | Change | Effective Date | Impact | Status |
|------------|--------|----------------|--------|--------|
| CRR III (Basel 3.1) | Full implementation | Jan 2025 | CRITICAL | 🔄 In progress |
| FRTB | Capital requirements | Jul 2025 | CRITICAL | 🔄 In progress |
| SS1/23 (MRM) | Full compliance | May 2025 | HIGH | 🔄 In progress |
| Op Resilience | Board attestation | Mar 2025 | HIGH | 🔄 In progress |
| SMA | Operational risk capital | Jan 2025 | HIGH | 🔄 In progress |
| **SS5/25 (Climate)** | **Supersedes SS3/19** | **Dec 2025 (effective), Jun 2026 (action plan)** | **CRITICAL** | **🔴 NEW** |
| **FCA SDR** | **Investment labels, disclosures** | **Dec 2024 - 2026 (phased)** | **HIGH** | **🔄 In progress** |
| Taxonomy Regulation | EU alignment | 2025 | MEDIUM | 📋 Planning |
| Digital Operational Resilience | DORA-equivalent | TBD | HIGH | 📋 Monitoring |

### 4.2 SS5/25 Implementation Timeline (CRITICAL)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SS5/25 CLIMATE RISK IMPLEMENTATION                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Dec 2025          Mar 2026          Jun 2026          Dec 2026            │
│     │                 │                 │                 │                 │
│     ▼                 ▼                 ▼                 ▼                 │
│  ┌──────┐         ┌──────┐         ┌──────┐         ┌──────┐               │
│  │SS5/25│         │ Gap  │         │Action│         │ Full │               │
│  │Effect│────────▶│Assess│────────▶│ Plan │────────▶│Comply│               │
│  │ive   │         │ment  │         │to PRA│         │      │               │
│  └──────┘         └──────┘         └──────┘         └──────┘               │
│     │                 │                 │                 │                 │
│     │                 │                 │                 │                 │
│  Regulation       Complete          Board-           Phased                 │
│  in force         internal          approved         implementation        │
│                   review            plan due         complete               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**SS5/25 Action Items** (by June 2026):
1. ☐ Gap analysis against SS5/25 requirements
2. ☐ Board paper on climate risk materiality
3. ☐ Update Climate Risk Policy
4. ☐ Review scenario analysis methodology
5. ☐ Data quality assessment for climate metrics
6. ☐ Board-approved action plan with timeline

### 4.3 Emerging Regulatory Themes

| Theme | Regulators | Expected Timeline | Risk Domains |
|-------|------------|-------------------|--------------|
| AI Governance | PRA/FCA | 2025-2026 | Model Risk, Op Risk |
| Nature-related Risk (TNFD) | PRA | 2025-2027 | Sustainability |
| Crypto-assets | PRA/FCA | 2025 | Market, Op Risk |
| T+1 Settlement | Industry/FCA | 2027 | Op Risk, Liquidity |
| Basel IV Output Floors | PRA | 2028-2030 | Credit Risk |
| ISSB S1/S2 (Sustainability) | FRC | 2025-2026 | Sustainability |
| Biodiversity/Nature Risk | PRA/International | 2026-2028 | Sustainability |

---

## 5. Regulatory-to-Risk Mapping Matrix

### 5.1 Mapping Overview

```
                      │ MR  │ CR  │ OR  │ LR  │ MDR │ SR  │ RR  │ STR │
──────────────────────────────────────────────────────────────────────
CRR/CRR III           │  ●  │  ●  │  ●  │  ●  │  ◐  │  ○  │  ●  │  ○  │
CRD VI                │  ●  │  ●  │  ●  │  ●  │  ○  │  ○  │  ●  │  ●  │
FRTB                  │  ●  │  ◐  │  ○  │  ○  │  ●  │  ○  │  ●  │  ○  │
IFRS 9                │  ○  │  ●  │  ○  │  ○  │  ●  │  ○  │  ●  │  ○  │
SS1/23 (MRM)          │  ◐  │  ◐  │  ◐  │  ◐  │  ●  │  ○  │  ●  │  ○  │
SS1/21 (Op Res)       │  ○  │  ○  │  ●  │  ○  │  ○  │  ○  │  ●  │  ○  │
SS5/25 (Climate) NEW  │  ◐  │  ●  │  ◐  │  ◐  │  ◐  │  ●  │  ●  │  ●  │
TCFD                  │  ○  │  ◐  │  ○  │  ○  │  ○  │  ●  │  ●  │  ●  │
FCA SDR (NEW)         │  ○  │  ○  │  ◐  │  ○  │  ○  │  ●  │  ●  │  ◐  │
MiFID II              │  ●  │  ○  │  ●  │  ○  │  ○  │  ○  │  ●  │  ○  │
MLR/Sanctions         │  ○  │  ◐  │  ●  │  ○  │  ○  │  ○  │  ●  │  ○  │
BCBS 239              │  ●  │  ●  │  ●  │  ●  │  ○  │  ◐  │  ●  │  ○  │
──────────────────────────────────────────────────────────────────────
Legend: ● Primary │ ◐ Secondary │ ○ Tangential
```

---

## 6. Skills Integration

### 6.1 Current Skills

| Skill | Regulatory Relevance |
|-------|---------------------|
| `pillar-stress-generator` | CRR stress testing, ICAAP, FRTB |
| `stress-scenario-suggester` | Emerging regulatory themes |
| `climate-scorecard-filler` | SS3/19, TCFD |
| `process-documenter` | All - process documentation |
| `project-planner` | Regulatory change projects |
| `status-reporter` | Regulatory implementation tracking |

### 6.2 Proposed New Skills

| Skill | Purpose | L1 Nodes Served |
|-------|---------|-----------------|
| `regulatory-research-agent` | Monitor regulatory changes, assess impacts | All REQ-L1-xxx |
| `regulatory-change-assessor` | Impact assessment on taxonomy artefacts | All REQ-L1-xxx |
| `capital-calculator` | CRR capital calculations | REQ-L1-001, REQ-L1-003 |
| `compliance-checker` | Compliance status tracking | All |

---

## 7. Document Control

### 7.1 Review Cycle

| Review Type | Frequency | Responsible |
|-------------|-----------|-------------|
| Regulatory Pipeline | Monthly | Regulatory Affairs |
| Full Inventory Review | Quarterly | Risk COO |
| New Regulation Assessment | As needed | Regulatory Affairs |

### 7.2 Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-12-11 | Initial creation | Risk Taxonomy Team |
| 2025-12-11 | **v1.1**: Added SS5/25 (supersedes SS3/19), added FCA SDR (REQ-L1-023), updated regulatory pipeline | regulatory-risk-researcher |

---

## Appendix A: Regulatory Node Index

| Node ID | Regulation | Category | Status |
|---------|------------|----------|--------|
| REQ-L1-001 | CRR/CRR III | Capital | Active |
| REQ-L1-002 | CRD VI | Capital | Active |
| REQ-L1-003 | FRTB | Market Risk | Active |
| REQ-L1-004 | SS13/13 | Market Risk | Active |
| REQ-L1-005 | CRR Part 3 | Credit Risk | Active |
| REQ-L1-006 | IFRS 9 | Credit Risk | Active |
| REQ-L1-007 | Large Exposures | Credit Risk | Active |
| REQ-L1-008 | SMA | Op Risk | Active |
| REQ-L1-009 | SS1/21 Op Res | Op Risk | Active |
| REQ-L1-010 | SS2/21 Outsourcing | Op Risk | Active |
| REQ-L1-011 | LCR | Liquidity | Active |
| REQ-L1-012 | NSFR | Liquidity | Active |
| REQ-L1-013 | SS1/23 MRM | Model Risk | Active |
| REQ-L1-014 | SR 11-7 | Model Risk | Active |
| REQ-L1-015 | **SS5/25 Climate** (replaces SS3/19) | Sustainability | **NEW** |
| REQ-L1-016 | TCFD | Sustainability | Active |
| REQ-L1-017 | MiFID II | Conduct | Active |
| REQ-L1-018 | MAR | Conduct | Active |
| REQ-L1-019 | MLR | Financial Crime | Active |
| REQ-L1-020 | Sanctions | Financial Crime | Active |
| REQ-L1-021 | BRRD II | Resolution | Active |
| REQ-L1-022 | BCBS 239 | Data | Active |
| REQ-L1-023 | **FCA SDR** | Sustainability | **NEW** |

---

*This document is the property of Meridian Global Bank and is intended for internal use only.*
