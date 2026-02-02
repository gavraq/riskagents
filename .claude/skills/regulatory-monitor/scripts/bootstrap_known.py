#!/usr/bin/env python3
"""Bootstrap the known_regulations.json from the existing regulatory inventory.

One-time script to seed the known state from the 23 entries in:
  docs/risk-taxonomy/L1-Requirements/regulatory-inventory.md

This gives the regulatory monitor a baseline to diff against on its first
automated scan, preventing the first run from flagging all 23 existing
regulations as "NEW".

Usage:
    python .claude/skills/regulatory-monitor/scripts/bootstrap_known.py

The script is idempotent — running it again will overwrite the existing
known_regulations.json with a fresh seed from the inventory.
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

STORE_PATH = Path("data/regulatory_monitor/known_regulations.json")

# The 23 regulatory entries from regulatory-inventory.md
# Each entry captures the essential attributes for diff matching
SEED_REGULATIONS = [
    {
        "source_regulator": "PRA",
        "document_type": "Regulation",
        "title": "Capital Requirements Regulation (CRR/CRR III)",
        "reference": "CRR/CRR III",
        "effective_date": "2025-01-01",
        "status": "In progress",
        "materiality": "Critical",
        "risk_domains": ["Market Risk", "Credit Risk", "Operational Risk"],
        "summary": "Basel 3.1 implementation via CRR III. Covers own funds, credit risk (SA/IRB), market risk (SA/IMA), operational risk (SMA), CVA, liquidity, leverage, and disclosure.",
        "taxonomy_node": "REQ-L1-001",
    },
    {
        "source_regulator": "PRA",
        "document_type": "Directive",
        "title": "Capital Requirements Directive VI (CRD VI)",
        "reference": "CRD VI",
        "effective_date": "Various",
        "status": "Active",
        "materiality": "Critical",
        "risk_domains": ["All"],
        "summary": "Supervisory review (Pillar 2), internal governance, ICAAP, concentration risk, market risk, operational risk, liquidity risk.",
        "taxonomy_node": "REQ-L1-002",
    },
    {
        "source_regulator": "PRA",
        "document_type": "Regulation",
        "title": "Fundamental Review of the Trading Book (FRTB)",
        "reference": "FRTB",
        "effective_date": "2025-07-01",
        "status": "In progress",
        "materiality": "Critical",
        "risk_domains": ["Market Risk"],
        "summary": "CRR Art 325-361. Standardised (SbM, DRC, RRAO) and IMA (ES, DRC, SES) approaches. P&L attribution test and backtesting requirements.",
        "taxonomy_node": "REQ-L1-003",
    },
    {
        "source_regulator": "PRA",
        "document_type": "SS",
        "title": "PRA SS13/13 - Market Risk",
        "reference": "SS13/13",
        "effective_date": "2024-11-01",
        "status": "Active",
        "materiality": "High",
        "risk_domains": ["Market Risk"],
        "summary": "IMA scope, VaR model requirements, stressed VaR, IRC, CRM, model validation, stress testing, backtesting.",
        "taxonomy_node": "REQ-L1-004",
    },
    {
        "source_regulator": "PRA",
        "document_type": "Regulation",
        "title": "CRR Part 3 - Credit Risk",
        "reference": "CRR Part 3 Title II",
        "effective_date": "Current",
        "status": "Active",
        "materiality": "Critical",
        "risk_domains": ["Credit Risk"],
        "summary": "Standardised Approach (SA-CR), Internal Ratings Based (IRB), Counterparty Credit Risk (CCR via SA-CCR/IMM), Credit Risk Mitigation.",
        "taxonomy_node": "REQ-L1-005",
    },
    {
        "source_regulator": "FRC",
        "document_type": "Standard",
        "title": "IFRS 9 - Expected Credit Loss",
        "reference": "IFRS 9",
        "effective_date": "2018-01-01",
        "status": "Active",
        "materiality": "Critical",
        "risk_domains": ["Credit Risk"],
        "summary": "SPPI test, business model classification, Stage 1/2/3 ECL, SICR triggers, PD/LGD/EAD models.",
        "taxonomy_node": "REQ-L1-006",
    },
    {
        "source_regulator": "PRA",
        "document_type": "Regulation",
        "title": "Large Exposures Regime",
        "reference": "CRR Part 4",
        "effective_date": "Current",
        "status": "Active",
        "materiality": "High",
        "risk_domains": ["Credit Risk"],
        "summary": "Single counterparty limits (25% Tier 1), G-SIB limits (15% Tier 1), exemptions for covered bonds and sovereigns.",
        "taxonomy_node": "REQ-L1-007",
    },
    {
        "source_regulator": "PRA",
        "document_type": "Regulation",
        "title": "Operational Risk - Standardised Measurement Approach (SMA)",
        "reference": "SMA",
        "effective_date": "2025-01-01",
        "status": "In progress",
        "materiality": "Critical",
        "risk_domains": ["Operational Risk"],
        "summary": "Business Indicator Component (BIC), Internal Loss Multiplier (ILM), 10-year loss history, €20k threshold.",
        "taxonomy_node": "REQ-L1-008",
    },
    {
        "source_regulator": "PRA",
        "document_type": "SS",
        "title": "Operational Resilience (SS1/21)",
        "reference": "SS1/21",
        "effective_date": "2025-03-01",
        "status": "In progress",
        "materiality": "Critical",
        "risk_domains": ["Operational Risk"],
        "summary": "Important Business Services identification, impact tolerances, resource mapping, scenario testing, board attestation by March 2025.",
        "taxonomy_node": "REQ-L1-009",
    },
    {
        "source_regulator": "PRA",
        "document_type": "SS",
        "title": "Outsourcing and Third Party Risk Management (SS2/21)",
        "reference": "SS2/21",
        "effective_date": "2022-03-01",
        "status": "Active",
        "materiality": "High",
        "risk_domains": ["Operational Risk"],
        "summary": "Materiality assessment, outsourcing register, exit plans, concentration risk monitoring, PRA notification.",
        "taxonomy_node": "REQ-L1-010",
    },
    {
        "source_regulator": "PRA",
        "document_type": "Regulation",
        "title": "Liquidity Coverage Ratio (LCR)",
        "reference": "CRR Part 6 LCR",
        "effective_date": "Current",
        "status": "Active",
        "materiality": "Critical",
        "risk_domains": ["Liquidity Risk"],
        "summary": "HQLA / Net outflows ≥100% over 30 days. Level 1/2A/2B composition rules, stressed outflow assumptions, inflow caps.",
        "taxonomy_node": "REQ-L1-011",
    },
    {
        "source_regulator": "PRA",
        "document_type": "Regulation",
        "title": "Net Stable Funding Ratio (NSFR)",
        "reference": "CRR Art 428a-428az",
        "effective_date": "2021-06-01",
        "status": "Active",
        "materiality": "Critical",
        "risk_domains": ["Liquidity Risk"],
        "summary": "Available Stable Funding / Required Stable Funding ≥100%. Liability and asset weighting factors.",
        "taxonomy_node": "REQ-L1-012",
    },
    {
        "source_regulator": "PRA",
        "document_type": "SS",
        "title": "Model Risk Management (SS1/23)",
        "reference": "SS1/23",
        "effective_date": "2025-05-01",
        "status": "In progress",
        "materiality": "Critical",
        "risk_domains": ["Model Risk"],
        "summary": "Comprehensive MRM framework, model inventory, development standards, independent validation, data quality, board governance.",
        "taxonomy_node": "REQ-L1-013",
    },
    {
        "source_regulator": "Federal Reserve",
        "document_type": "SR Letter",
        "title": "SR 11-7 - Model Risk Management (US)",
        "reference": "SR 11-7",
        "effective_date": "2011-04-01",
        "status": "Active",
        "materiality": "High",
        "risk_domains": ["Model Risk"],
        "summary": "US model risk management guidance. Influential globally, principles reflected in PRA SS1/23.",
        "taxonomy_node": "REQ-L1-014",
    },
    {
        "source_regulator": "PRA",
        "document_type": "SS",
        "title": "PRA SS5/25 - Climate Risk",
        "reference": "SS5/25",
        "effective_date": "2025-12-03",
        "status": "New",
        "materiality": "Critical",
        "risk_domains": ["Sustainability Risk", "Credit Risk", "Market Risk", "Operational Risk"],
        "summary": "Supersedes SS3/19. Board oversight, climate integration into all risk types, quantitative scenario analysis, data quality framework, TCFD/ISSB disclosure. Action plan due June 2026.",
        "taxonomy_node": "REQ-L1-015",
    },
    {
        "source_regulator": "FCA",
        "document_type": "Standard",
        "title": "TCFD Recommendations",
        "reference": "TCFD",
        "effective_date": "2022-01-01",
        "status": "Active",
        "materiality": "High",
        "risk_domains": ["Sustainability Risk"],
        "summary": "Governance, strategy, risk management, metrics & targets for climate-related financial disclosures. Being superseded by ISSB S2.",
        "taxonomy_node": "REQ-L1-016",
    },
    {
        "source_regulator": "FCA",
        "document_type": "Regulation",
        "title": "MiFID II / MiFIR",
        "reference": "MiFID II",
        "effective_date": "2018-01-03",
        "status": "Active",
        "materiality": "High",
        "risk_domains": ["Operational Risk", "Market Risk"],
        "summary": "Best execution, transaction reporting, record keeping, product governance, inducements restrictions.",
        "taxonomy_node": "REQ-L1-017",
    },
    {
        "source_regulator": "FCA",
        "document_type": "Regulation",
        "title": "Market Abuse Regulation (MAR)",
        "reference": "UK MAR",
        "effective_date": "Current",
        "status": "Active",
        "materiality": "High",
        "risk_domains": ["Operational Risk", "Market Risk"],
        "summary": "Insider lists, PDMR dealing notifications, suspicious order reporting, market manipulation surveillance.",
        "taxonomy_node": "REQ-L1-018",
    },
    {
        "source_regulator": "FCA",
        "document_type": "Regulation",
        "title": "Money Laundering Regulations 2017",
        "reference": "MLR 2017",
        "effective_date": "Current",
        "status": "Active",
        "materiality": "Critical",
        "risk_domains": ["Operational Risk"],
        "summary": "Business-wide risk assessment, CDD/EDD, ongoing monitoring, SAR reporting, staff training.",
        "taxonomy_node": "REQ-L1-019",
    },
    {
        "source_regulator": "HM Treasury",
        "document_type": "Regulation",
        "title": "Sanctions Regulations (SAMLA 2018)",
        "reference": "SAMLA 2018",
        "effective_date": "Current",
        "status": "Active",
        "materiality": "Critical",
        "risk_domains": ["Operational Risk"],
        "summary": "Customer and transaction screening, asset freezing obligations, OFSI reporting, licence applications.",
        "taxonomy_node": "REQ-L1-020",
    },
    {
        "source_regulator": "Bank of England",
        "document_type": "Directive",
        "title": "BRRD II / UK Resolution Regime",
        "reference": "BRRD II",
        "effective_date": "Current",
        "status": "Active",
        "materiality": "Critical",
        "risk_domains": ["All"],
        "summary": "Annual recovery plan, resolution pack, MREL, bail-in mechanism, operational continuity in resolution.",
        "taxonomy_node": "REQ-L1-021",
    },
    {
        "source_regulator": "PRA",
        "document_type": "Standard",
        "title": "BCBS 239 - Risk Data Aggregation",
        "reference": "BCBS 239",
        "effective_date": "2016-01-01",
        "status": "Active",
        "materiality": "Critical",
        "risk_domains": ["All"],
        "summary": "Data governance, architecture, accuracy, completeness, timeliness, adaptability, reporting comprehensiveness.",
        "taxonomy_node": "REQ-L1-022",
    },
    {
        "source_regulator": "FCA",
        "document_type": "PS",
        "title": "FCA Sustainability Disclosure Requirements (SDR)",
        "reference": "PS23/16 SDR",
        "effective_date": "2024-12-02",
        "status": "In progress",
        "materiality": "High",
        "risk_domains": ["Sustainability Risk", "Operational Risk"],
        "summary": "Anti-greenwashing rule, investment labels, consumer-facing disclosures, product/entity-level disclosures, naming/marketing rules.",
        "taxonomy_node": "REQ-L1-023",
    },
]


def generate_id(finding: dict) -> str:
    """Generate deterministic ID matching generate_ids.py logic."""
    regulator = finding.get("source_regulator", "UNKNOWN").upper().strip()
    reference = finding.get("reference", "").strip()
    if reference:
        key = f"{regulator}:{reference}"
    else:
        title = " ".join(finding.get("title", "").lower().split())
        key = f"{regulator}:{title}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def atomic_write(path: Path, data: str):
    """Atomic write: temp → rename → backup."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        os.write(fd, data.encode())
        os.close(fd)
        os.rename(tmp_path, path)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    try:
        shutil.copy2(path, f"{path}.bak")
    except Exception:
        pass


def main():
    now = datetime.now(timezone.utc).isoformat()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    items = {}
    for reg in SEED_REGULATIONS:
        reg_id = generate_id(reg)
        reg["id"] = reg_id
        reg["first_seen"] = now
        reg["last_seen"] = now
        reg["source"] = "bootstrap"
        items[reg_id] = reg

    store = {
        "version": 1,
        "last_updated": now,
        "last_scan_date": today,
        "bootstrap_date": today,
        "items": items,
    }

    atomic_write(STORE_PATH, json.dumps(store, indent=2))

    print(f"Bootstrapped known_regulations.json with {len(items)} entries.")
    print(f"Store path: {STORE_PATH}")
    print()
    print("Entries:")
    for reg_id, reg in items.items():
        print(f"  {reg_id[:8]}  {reg['taxonomy_node']}: {reg['title']}")


if __name__ == "__main__":
    main()
