# Risk Taxonomy Schema

**Version**: 1.0
**Last Updated**: 2025-12-11

---

## Overview

This document defines the schema structure for the Risk Taxonomy Framework. The schema enables:
- Consistent node definitions across all taxonomy layers
- Machine-readable structure for AI agent context loading
- Human-navigable documentation hierarchy
- Full audit trail through parent-child relationships

---

## 1. Taxonomy Node Schema

### 1.1 YAML Schema Definition

```yaml
# Taxonomy Node Schema v1.0

node:
  # Required Fields
  id: string                    # Unique identifier (format: {DOMAIN}-L{LAYER}-{SEQ})
  layer: integer                # 1-7 (see Layer Definitions)
  name: string                  # Human-readable name
  domain: string                # Primary risk domain (see Domain List)
  description: string           # Purpose/definition of this node

  # Hierarchy Fields
  parent: string | null         # Parent node ID (null for L1 nodes)
  children: list[string]        # Child node IDs (empty for L7 nodes)

  # Cross-Reference Fields
  cross_refs: list[object]      # Related nodes in other domains
    - node_id: string           # Target node ID
      relationship: string      # Type: "input_to", "output_from", "shares_data", "governs"
      description: string       # Nature of relationship

  # Skills Integration
  skills: list[string]          # Applicable skill names
  skill_coverage: string        # "full", "partial", "none"

  # Artefact Links
  artefacts: list[object]       # Supporting documents/systems
    - type: string              # See Artefact Types
      name: string              # Artefact name
      path: string              # File path or URL
      format: string            # File format

  # Metadata
  metadata:
    owner: string               # Responsible team/person
    owner_email: string         # Contact email
    created_date: date          # Node creation date
    review_date: date           # Next review date
    status: string              # "draft", "active", "deprecated"
    version: string             # Document version
    confidentiality: string     # "public", "internal", "confidential"

  # AI Context Hints
  context:
    summary: string             # 1-2 sentence summary for agent context
    keywords: list[string]      # Search/trigger keywords
    related_queries: list[string]  # Example questions this node answers
```

### 1.2 Example Node

```yaml
node:
  id: "MR-L4-001"
  layer: 4
  name: "Market Risk Process Orchestration Process"
  domain: "Market Risk"
  description: |
    End-to-end process for calculating and reporting daily Value at Risk (VaR)
    across all trading book portfolios. Covers data sourcing, calculation,
    validation, and dissemination to stakeholders.

  parent: "MR-L3-001"  # Market Risk Policy
  children:
    - "MR-L5-001"      # VaR Limits
    - "MR-L5-002"      # Backtesting Controls
    - "MR-L5-003"      # Data Quality Controls

  cross_refs:
    - node_id: "CR-L7-003"
      relationship: "input_to"
      description: "Trade feed provides positions for VaR calculation"
    - node_id: "FIN-L4-002"
      relationship: "output_to"
      description: "VaR results feed into capital calculation"

  skills:
    - "pillar-stress-generator"
    - "process-documenter"
  skill_coverage: "partial"

  artefacts:
    - type: "process_map"
      name: "Market Risk Process Orchestration BPMN"
      path: "/docs/risk-taxonomy/L4-Processes/processes/daily-var-production/process.bpmn"
      format: "bpmn"
    - type: "procedure"
      name: "VaR Production Runbook"
      path: "/docs/risk-taxonomy/L4-Processes/processes/daily-var-production/runbook.md"
      format: "markdown"
    - type: "system"
      name: "VESPA VaR Engine"
      path: "/docs/risk-taxonomy/L7-Data-Systems/systems/vespa.md"
      format: "markdown"

  metadata:
    owner: "Market Risk Analytics"
    owner_email: "mra@meridianbank.com"
    created_date: "2025-12-11"
    review_date: "2026-06-11"
    status: "active"
    version: "1.0"
    confidentiality: "internal"

  context:
    summary: "Daily process to calculate VaR across trading portfolios using historical simulation, validate results, and distribute to stakeholders."
    keywords:
      - "VaR"
      - "value at risk"
      - "daily production"
      - "market risk measurement"
      - "historical simulation"
    related_queries:
      - "How is VaR calculated?"
      - "What is the VaR production timeline?"
      - "Who receives the daily VaR report?"
```

---

## 2. Layer Definitions

| Layer | Code | Name | Description | Parent Layer | Child Layer |
|-------|------|------|-------------|--------------|-------------|
| **1** | L1 | Requirements | Regulatory mandates, business requirements, strategic objectives | None | L2 |
| **2** | L2 | Risk Types | Risk classification, definitions, materiality assessment | L1 | L3 |
| **3** | L3 | Governance | Policies, committees, mandates, terms of reference | L2 | L4 |
| **4** | L4 | Processes | Business processes, procedures, workflows | L3 | L5 |
| **5** | L5 | Controls & Metrics | Key controls, KRIs, limits, RCSA | L4 | L6 |
| **6** | L6 | Models | Risk models, methodologies, validation | L5 | L7 |
| **7** | L7 | Data & Systems | Data domains, systems, feeds, architecture | L6 | None |

---

## 3. Domain Codes

| Domain | Code | Full Name | Scope |
|--------|------|-----------|-------|
| **MR** | MR | Market Risk | Trading book, FX, Interest rate, Commodities |
| **CR** | CR | Credit Risk | Counterparty, Concentration, Country, Issuer |
| **OR** | OR | Operational Risk | Process, People, Systems, External events |
| **LR** | LR | Liquidity Risk | Funding, LCR, NSFR, Intraday |
| **MDR** | MDR | Model Risk | Validation, Governance, Inventory |
| **SR** | SR | Sustainability Risk | Climate, Environmental, Social, Governance |
| **RR** | RR | Regulatory Risk | Compliance, Capital, Reporting |
| **STR** | STR | Strategic Risk | Business, M&A, Reputation |
| **CM** | CM | Change Management | Projects, Governance, Benefits |
| **CC** | CC | Cross-Cutting | Shared processes, common controls |

---

## 4. Artefact Types

| Type | Code | Description | Typical Formats |
|------|------|-------------|-----------------|
| **policy** | POL | Policy documents | .md, .pdf, .docx |
| **procedure** | PROC | Operating procedures, runbooks | .md, .pdf |
| **process_map** | BPMN | Process diagrams | .bpmn, .mmd (mermaid) |
| **committee_tor** | TOR | Terms of Reference | .md, .pdf |
| **control** | CTRL | Control descriptions | .md, .xlsx |
| **kri** | KRI | KRI definitions | .md, .xlsx |
| **limit** | LIM | Limit frameworks | .md, .xlsx |
| **model** | MOD | Model documentation | .md, .pdf |
| **methodology** | METH | Methodology documents | .md, .pdf |
| **validation** | VAL | Validation reports | .md, .pdf |
| **data_dictionary** | DATA | Data definitions | .md, .xlsx, .json |
| **feed_spec** | FEED | Interface definitions | .md, .json |
| **system** | SYS | System documentation | .md |
| **architecture** | ARCH | Architecture diagrams | .md, .png, .drawio |
| **report** | RPT | Report templates/specs | .md, .xlsx |
| **test_pack** | TEST | Test documentation | .md, .xlsx |

---

## 5. Relationship Types

| Type | Description | Example |
|------|-------------|---------|
| **input_to** | Provides data/information to target node | Trade feed → VaR calculation |
| **output_from** | Receives data/information from source node | Daily report ← VaR calculation |
| **governs** | Sets rules/policies for target node | Market Risk Policy → VaR process |
| **governed_by** | Is subject to rules from source node | VaR process → Market Risk Policy |
| **shares_data** | Bidirectional data sharing | CVA ↔ Credit exposure |
| **validates** | Provides validation/assurance for target | Model validation → VaR model |
| **depends_on** | Requires target to function | Stress test → VaR infrastructure |
| **triggers** | Initiates target process/action | Limit breach → Escalation process |

---

## 6. Node ID Format

### Format: `{DOMAIN}-L{LAYER}-{SEQUENCE}`

| Component | Description | Example |
|-----------|-------------|---------|
| **DOMAIN** | 2-3 letter domain code | MR, CR, OR |
| **L** | Literal "L" prefix | L |
| **LAYER** | Layer number (1-7) | 4 |
| **SEQUENCE** | 3-digit sequential number | 001 |

### Examples
- `MR-L4-001` - First Market Risk Layer 4 (Process) node
- `CR-L2-003` - Third Credit Risk Layer 2 (Risk Type) node
- `CC-L5-012` - Twelfth Cross-Cutting Layer 5 (Control) node

### Special IDs
- `REQ-L1-xxx` - Regulatory requirements (domain-agnostic)
- `CC-Lx-xxx` - Cross-cutting nodes shared across domains

---

## 7. Status Values

| Status | Description | Valid Actions |
|--------|-------------|---------------|
| **draft** | Under development, not yet reviewed | Edit, Review, Publish |
| **active** | Current, approved version | Review, Deprecate, Archive |
| **deprecated** | Being phased out, superseded | Archive only |
| **archived** | Historical reference only | View only |

---

## 8. Validation Rules

### Mandatory Fields
- `id`, `layer`, `name`, `domain`, `description`
- `metadata.owner`, `metadata.status`

### Hierarchical Rules
- L1 nodes: `parent` must be null
- L2-L7 nodes: `parent` must be valid node in layer above
- L7 nodes: `children` must be empty

### ID Format Rules
- Domain code must be in Domain Codes list
- Layer must be 1-7
- Sequence must be 3-digit padded

### Cross-Reference Rules
- Target node must exist
- Relationship type must be in Relationship Types list

---

## 9. Context Loading for AI Agents

### Context Retrieval Logic

When an agent receives a query:

1. **Keyword Match**: Match query terms to `context.keywords`
2. **Related Query Match**: Match to `context.related_queries`
3. **Load Node Summary**: Return `context.summary`
4. **Expand if Needed**: Load full `description` and `artefacts` if deeper context required
5. **Traverse Links**: Follow `cross_refs` for related context

### Token Efficiency Strategy

| Query Depth | Content Loaded | Estimated Tokens |
|-------------|----------------|------------------|
| **Quick** | Summary only | 50-100 |
| **Standard** | Summary + description | 200-500 |
| **Deep** | Full node + linked artefacts | 1,000-5,000 |
| **Comprehensive** | Node + children + cross-refs | 5,000-20,000 |

---

## Appendix: Schema Validation Script

```python
# taxonomy/schema.py

from dataclasses import dataclass
from typing import List, Optional
from datetime import date
from enum import Enum

class Layer(Enum):
    REQUIREMENTS = 1
    RISK_TYPES = 2
    GOVERNANCE = 3
    PROCESSES = 4
    CONTROLS = 5
    MODELS = 6
    DATA_SYSTEMS = 7

class Domain(Enum):
    MARKET_RISK = "MR"
    CREDIT_RISK = "CR"
    OPERATIONAL_RISK = "OR"
    LIQUIDITY_RISK = "LR"
    MODEL_RISK = "MDR"
    SUSTAINABILITY_RISK = "SR"
    REGULATORY_RISK = "RR"
    STRATEGIC_RISK = "STR"
    CHANGE_MANAGEMENT = "CM"
    CROSS_CUTTING = "CC"

class Status(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

@dataclass
class CrossRef:
    node_id: str
    relationship: str
    description: str

@dataclass
class Artefact:
    type: str
    name: str
    path: str
    format: str

@dataclass
class Metadata:
    owner: str
    owner_email: str
    created_date: date
    review_date: date
    status: Status
    version: str
    confidentiality: str

@dataclass
class Context:
    summary: str
    keywords: List[str]
    related_queries: List[str]

@dataclass
class TaxonomyNode:
    id: str
    layer: Layer
    name: str
    domain: Domain
    description: str
    parent: Optional[str]
    children: List[str]
    cross_refs: List[CrossRef]
    skills: List[str]
    skill_coverage: str
    artefacts: List[Artefact]
    metadata: Metadata
    context: Context

    def validate(self) -> List[str]:
        """Returns list of validation errors, empty if valid"""
        errors = []

        # ID format validation
        parts = self.id.split("-")
        if len(parts) != 3:
            errors.append(f"Invalid ID format: {self.id}")

        # Layer hierarchy validation
        if self.layer == Layer.REQUIREMENTS and self.parent is not None:
            errors.append("L1 nodes must have null parent")
        if self.layer != Layer.REQUIREMENTS and self.parent is None:
            errors.append("L2-L7 nodes must have a parent")
        if self.layer == Layer.DATA_SYSTEMS and len(self.children) > 0:
            errors.append("L7 nodes cannot have children")

        return errors
```

---

*Document Control*
- **Created**: 2025-12-11
- **Author**: Risk Agents Team
- **Classification**: Internal
