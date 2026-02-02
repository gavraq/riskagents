# Known Regulation Families — Taxonomy Baseline

This file provides the known regulation families from the Risk Taxonomy L1 layer.
Used during Step 5 of the regulatory-monitor skill to match new findings against
established regulation families.

**Source**: `docs/risk-taxonomy/L1-Requirements/regulatory-inventory.md`
**Last synced**: 2026-02-02
**Total entries**: 23

---

## Regulation Families

| ID | Regulation | Category | Regulator | Key References | Status | Materiality |
|----|-----------|----------|-----------|----------------|--------|-------------|
| REQ-L1-001 | CRR/CRR III (Basel 3.1) | Capital | PRA/EBA | CRR, CRR III, EU 2019/876 | In progress | Critical |
| REQ-L1-002 | CRD VI | Capital | PRA | CRD VI, Art 73-96 | Active | Critical |
| REQ-L1-003 | FRTB | Market Risk | PRA | CRR Art 325-361, SA-TB, IMA | In progress | Critical |
| REQ-L1-004 | SS13/13 Market Risk | Market Risk | PRA | SS13/13, VaR, SVaR, IRC | Active | High |
| REQ-L1-005 | CRR Part 3 Credit Risk | Credit Risk | PRA | SA-CR, IRB, CCR, SA-CCR, IMM | Active | Critical |
| REQ-L1-006 | IFRS 9 ECL | Credit Risk | FRC/PRA | IFRS 9, ECL, SPPI, staging | Active | Critical |
| REQ-L1-007 | Large Exposures | Credit Risk | PRA | CRR Part 4, Art 392-395 | Active | High |
| REQ-L1-008 | Operational Risk SMA | Op Risk | PRA | CRR Part 3 Title III, SMA, BIC, ILM | In progress | Critical |
| REQ-L1-009 | Operational Resilience | Op Risk | PRA/FCA | SS1/21, IBS, impact tolerances | In progress | Critical |
| REQ-L1-010 | Outsourcing & Third Party | Op Risk | PRA | SS2/21, outsourcing register | Active | High |
| REQ-L1-011 | LCR | Liquidity | PRA | CRR Part 6, HQLA, LCR ≥100% | Active | Critical |
| REQ-L1-012 | NSFR | Liquidity | PRA | CRR Art 428a-428az, ASF/RSF | Active | Critical |
| REQ-L1-013 | Model Risk Management | Model Risk | PRA | SS1/23, MRM framework, model inventory | In progress | Critical |
| REQ-L1-014 | SR 11-7 (US MRM) | Model Risk | Fed/OCC | SR 11-7, model validation | Active | High |
| REQ-L1-015 | SS5/25 Climate Risk | Sustainability | PRA | SS5/25, PS25/25, CP16/24 (supersedes SS3/19) | New | Critical |
| REQ-L1-016 | TCFD | Sustainability | FCA | TCFD, governance, strategy, metrics | Active | High |
| REQ-L1-017 | MiFID II/MiFIR | Conduct | FCA | MiFID II, best execution, reporting | Active | High |
| REQ-L1-018 | MAR | Conduct | FCA | UK MAR, insider lists, PDMR, surveillance | Active | High |
| REQ-L1-019 | Money Laundering Regs | Financial Crime | FCA/NCA | MLR 2017, CDD, EDD, SAR | Active | Critical |
| REQ-L1-020 | Sanctions | Financial Crime | HMT/OFSI | SAMLA 2018, screening, blocking | Active | Critical |
| REQ-L1-021 | BRRD II / Resolution | Resolution | BoE | BRRD II, MREL, recovery plan, bail-in | Active | Critical |
| REQ-L1-022 | BCBS 239 Data | Data & Reporting | PRA | BCBS 239, data governance, aggregation | Active | Critical |
| REQ-L1-023 | FCA SDR | Sustainability | FCA | PS23/16, investment labels, anti-greenwashing | In progress | High |

---

## Emerging Regulatory Themes (Not Yet in Inventory)

These themes are being monitored but don't yet have formal L1 entries:

| Theme | Regulators | Expected | Notes |
|-------|-----------|----------|-------|
| AI Governance | PRA/FCA | 2025-2026 | May generate CP/SS |
| Nature-related Risk (TNFD) | PRA | 2025-2027 | Following TCFD pattern |
| Crypto-assets | PRA/FCA | 2025 | Digital asset regulation |
| T+1 Settlement | FCA/Industry | 2027 | Operational impact |
| Basel IV Output Floors | PRA | 2028-2030 | Under CRR III umbrella |
| ISSB S1/S2 | FRC | 2025-2026 | Superseding TCFD |
| Biodiversity/Nature Risk | PRA/International | 2026-2028 | Extension of climate |
| DORA-equivalent (UK) | PRA/FCA | TBD | Digital operational resilience |

---

## Matching Guidance

When comparing scan findings against this baseline:

1. **Exact reference match**: If a finding references "SS1/23", it maps to REQ-L1-013
2. **Regulation family match**: PRA announcements about "Basel 3.1 output floors" relate to REQ-L1-001
3. **Consultation → Final progression**: CP/PS about an existing regulation family is an UPDATE, not NEW
4. **New regulation entirely**: If it doesn't fit any existing family or emerging theme, it is genuinely NEW
5. **Supersession**: SS5/25 superseded SS3/19 — new PRA climate risk announcements map to REQ-L1-015
6. **Cross-jurisdictional**: EBA/BCBS announcements about Basel/CRR relate to REQ-L1-001 even if from different regulator
