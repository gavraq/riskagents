# Proactive Regulatory Monitoring Service

**Date**: 2026-02-02 (Updated: 2026-02-02)
**Status**: Phase 1-2 Implemented, Phase 3 (Deployment) Pending
**Author**: Risk Agent Team
**Version**: 2.2

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Design Goals](#3-design-goals)
4. [Architecture Overview](#4-architecture-overview)
5. [Skill-Centric Design: Deterministic vs Non-Deterministic Split](#5-skill-centric-design-deterministic-vs-non-deterministic-split)
6. [SKILL.md Specification](#6-skillmd-specification)
7. [Python Scripts (Deterministic Code)](#7-python-scripts-deterministic-code)
8. [Baseline & Diff Strategy](#8-baseline--diff-strategy)
9. [Scheduler (Cron Trigger Layer)](#9-scheduler-cron-trigger-layer)
10. [Reference Architecture: OpenClaw Cron Analysis](#10-reference-architecture-openclaw-cron-analysis)
11. [Configuration](#11-configuration)
12. [Notification & Delivery](#12-notification--delivery)
13. [Deployment Architecture](#13-deployment-architecture)
14. [Integration with Existing System](#14-integration-with-existing-system)
15. [Security Considerations](#15-security-considerations)
16. [Operational Concerns](#16-operational-concerns)
17. [Implementation Plan](#17-implementation-plan)
18. [Appendix A: OpenClaw Source Analysis](#appendix-a-openclaw-source-analysis)
19. [Appendix B: Alternative Approaches Evaluated](#appendix-b-alternative-approaches-evaluated)
20. [Appendix C: Anthropic Skills Best Practices Applied](#appendix-c-anthropic-skills-best-practices-applied)

---

## 1. Executive Summary

This document specifies a **Proactive Regulatory Monitoring Service** for the Risk Agents platform. The service combines three layers:

1. **A SKILL.md file** (`.claude/skills/regulatory-monitor/SKILL.md`) that orchestrates the entire regulatory monitoring workflow — invoking the existing `regulatory-risk-researcher` agent, comparing findings against known state, and deciding what to notify. **✅ Implemented.**
2. **A standalone cron-scheduler service** (`/Volumes/DockSSD/projects/scheduler/`) running in Docker on the Raspberry Pi — a generic scheduling engine that can trigger any project's skills via HTTP.
3. **The existing telegram-agent service** (`~/projects/telegram/agent/`) on the Mac, extended with a `POST /scheduled-job` endpoint to accept scheduled job payloads and execute them via the Claude Agent SDK.

This follows the same proven architecture as the existing Telegram bot: **Pi (always-on, Docker) → HTTPS → Mac (Claude + Max subscription)**. The scheduler is intentionally generic — it knows nothing about regulatory monitoring, only about timing and HTTP delivery.

Following [Anthropic's Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), the design splits responsibilities between **deterministic Python scripts** (JSON I/O, file operations, ID generation, notification delivery) and **LLM reasoning** (web research, semantic comparison, materiality assessment, report synthesis). Scripts handle what code does best; Claude handles what requires judgment.

The design is further informed by a deep analysis of [OpenClaw's](https://github.com/openclaw/openclaw) cron scheduling architecture, extracting their best patterns (isolated sessions, smart timers, atomic persistence, run logs) while avoiding their pitfalls.

---

## 2. Problem Statement

### Current State

The `regulatory-risk-researcher` agent (`.claude/agents/regulatory-risk-researcher.md`) is fully defined and capable of:

- Monitoring PRA, FCA, BoE, EBA, BCBS, IOSCO, and FSB announcements
- Identifying new consultation papers, policy statements, supervisory statements, dear CEO letters
- Assessing materiality and mapping findings to the Risk Taxonomy (L1-L7)
- Generating structured markdown reports with recommended actions

However, it is **purely reactive** — it only runs when explicitly invoked by a user. The agent definition even anticipates scheduled execution (line 195: "Scheduled periodic scan (weekly/monthly)") but no scheduling infrastructure exists.

### The Gap

| Capability | Current | Required |
|---|---|---|
| Regulatory research | On-demand only | Scheduled + on-demand |
| Notification | User reads output | Push to Telegram/email |
| Deduplication | None | Only alert on new findings |
| Run history | None | Auditable execution log |
| Failure handling | Manual retry | Auto-retry with alerting |
| State persistence | Stateless | Track known regulations |

### Business Impact

Without proactive monitoring:
- New PRA/FCA announcements may go unnoticed for weeks
- Consultation paper deadlines could be missed
- The regulatory change pipeline (`researcher → assessor → planner → change-agent`) never starts until someone remembers to check
- No audit trail of when regulatory changes were first identified

---

## 3. Design Goals

### Must Have (P0)

1. **Scheduled execution** — Run regulatory scans on configurable cron schedules
2. **Isolated sessions** — Each scan runs in a fresh context (no stale carry-over)
3. **Telegram notification** — Push findings to the existing Telegram gateway
4. **Deduplication** — Only notify on genuinely new regulatory developments
5. **Run logging** — Auditable JSONL log of every execution with status, duration, findings count
6. **Crash safety** — Atomic persistence, graceful restart, no data loss

### Should Have (P1)

7. **Multiple scan profiles** — Different schedules for different scopes (daily quick check vs weekly deep scan)
8. **Model selection per job** — Use Haiku for quick daily checks, Sonnet/Opus for deep weekly analysis
9. **Output archival** — Full scan reports saved to `output/regulatory-scans/` with timestamps
10. **Health monitoring** — Self-report on execution success/failure trends

### Nice to Have (P2)

11. **Email delivery** — Alternative notification channel
12. **Downstream triggering** — Auto-invoke `regulatory-change-assessor` on critical findings
13. **Web dashboard** — Simple status page showing recent scans and findings
14. **Multi-jurisdiction parallel scans** — Run UK, EU, and International scans in parallel (following the stress-scenario-suggester pattern)

---

## 4. Architecture Overview

### Three-Layer Architecture (Standalone Scheduler)

The system has three distinct layers deployed across two machines, following the same proven pattern as the existing Telegram bot infrastructure:

```
┌─────────────────────────────────────────────────────────────────────┐
│  RASPBERRY PI (Docker, always-on)                                    │
│                                                                      │
│  LAYER 1: Generic Cron Scheduler                                     │
│  Responsibility: WHEN to run                                         │
│                                                                      │
│  /Volumes/DockSSD/projects/scheduler/                                      │
│  ├── src/cron_scheduler/                                             │
│  │   ├── main.py        # Service entrypoint                        │
│  │   ├── scheduler.py   # Smart timer engine (event-driven)         │
│  │   ├── config.py      # Load YAML job definitions                 │
│  │   ├── store.py       # Job state persistence (atomic writes)     │
│  │   ├── run_log.py     # JSONL execution log with auto-prune       │
│  │   └── client.py      # HTTP client to Mac agent service          │
│  ├── config/jobs.yaml   # Job definitions                           │
│  ├── Dockerfile                                                      │
│  └── docker-compose.yml                                              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTPS POST /scheduled-job
                               │ via Nginx Proxy Manager
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  MAC (Claude Agent SDK + Max subscription)                           │
│                                                                      │
│  LAYER 2: Telegram-Agent Service (Extended)                          │
│  Responsibility: HOW to invoke Claude                                │
│                                                                      │
│  ~/projects/telegram/agent/                                          │
│  ├── POST /query            ← Telegram messages (existing)           │
│  ├── POST /scheduled-job    ← Scheduler payloads (NEW endpoint)      │
│  ├── POST /health           ← Health check (existing)                │
│  └── Uses Claude Agent SDK with project autodiscovery                │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ Claude Agent SDK executes in cwd
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 3: SKILL.md + Scripts (in riskagents project)                 │
│  Responsibility: WHAT to do                                          │
│  Status: ✅ IMPLEMENTED                                              │
│                                                                      │
│  .claude/skills/regulatory-monitor/                                  │
│  ├── SKILL.md              # 9-step orchestration workflow           │
│  ├── scripts/              # 7 deterministic Python scripts          │
│  └── reference/            # Taxonomy baseline for semantic matching │
└─────────────────────────────────────────────────────────────────────┘
```

### Why This Architecture?

| Layer | Location | Technology | Responsibility | Changes When |
|-------|----------|-----------|----------------|-------------|
| Scheduler | Pi (Docker) | Python + asyncio | WHEN to run | Schedule/frequency changes |
| Agent Service | Mac (launchd) | FastAPI + Claude SDK | HOW to invoke Claude | Execution logic changes |
| Skill + Scripts | riskagents repo | SKILL.md + Python | WHAT to do | Workflow/logic changes |

**Key design decisions**:

1. **Scheduler is generic** — It knows nothing about regulatory monitoring. It just knows: "At this cron time, POST this payload to this URL." Other projects can register jobs without scheduler code changes.

2. **Reuses existing telegram-agent** — The `POST /scheduled-job` endpoint sits alongside the existing `POST /query` endpoint. Same SDK, same project autodiscovery, same authentication.

3. **Pi runs 24/7** — The Mac may sleep. The Pi scheduler handles timing reliably. If the Mac is asleep, the scheduler retries or queues.

4. **Follows proven pattern** — Identical to how Telegram bot works:

```
TELEGRAM:   Pi gateway  → POST /query         → Mac agent → Claude SDK
SCHEDULER:  Pi scheduler → POST /scheduled-job → Mac agent → Claude SDK
```

### Agent Invocation: Via Telegram-Agent Service

The telegram-agent at `~/projects/telegram/agent/` already wraps the Claude Agent SDK with project autodiscovery, model configuration, session management, and metadata tracking. The new `POST /scheduled-job` endpoint accepts a structured job payload:

```
Pi: Scheduler timer fires
    │
    ▼
HTTPS POST /scheduled-job
{
    "project": "/Volumes/DockSSD/projects/riskagents",
    "prompt": "Run a regulatory monitoring scan. Use the regulatory-monitor skill.",
    "model": "sonnet",
    "max_turns": 15,
    "timeout_seconds": 600,
    "job_name": "weekly-regulatory-scan"
}
    │
    ▼ Mac: telegram-agent receives request
    │ → Sets cwd to payload.project
    │ → Autodiscovers .claude/agents/ and .claude/skills/
    │ → Executes via Claude Agent SDK (fresh session, no resume)
    │ → Returns structured response with duration, cost, skills used
    │
    ▼
Pi: Scheduler captures response → logs result → updates job state
```

---

## 5. Skill-Centric Design: Deterministic vs Non-Deterministic Split

### Design Principle

Following [Anthropic's Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

> *"Prefer scripts for deterministic operations"* — Write `validate_form.py` rather than asking Claude to generate validation code.
>
> *"Scripts provide deterministic operations without consuming context"* — Only script output enters the context window.

Every step in the workflow is classified as either:

- **Deterministic (Script)**: The operation has one correct answer, involves structured data I/O, or requires exact reproducibility. Use Python scripts.
- **Non-Deterministic (LLM)**: The operation requires judgment, semantic understanding, web research, or synthesis. Use Claude's reasoning.

### Step-by-Step Classification

| Step | Operation | Type | Rationale |
|------|-----------|------|-----------|
| **1** | Load known regulations from JSON | **Script** | Pure file I/O. Exact, reproducible. No judgment needed. |
| **2** | Conduct regulatory web research | **LLM** | Requires WebSearch, reading regulatory sites, understanding context, judging relevance. This IS the regulatory-risk-researcher agent's core competency. |
| **3** | Parse researcher output into structured findings | **LLM** | The researcher's output is markdown prose. Claude understands its own output format better than regex. Needs semantic extraction of regulator, reference, dates, materiality. |
| **4** | Generate stable finding IDs | **Script** | Deterministic hash: `sha256(regulator + reference)`. Must be identical across runs for the same regulation. Code guarantees this; LLM might vary. |
| **5** | Compare findings against known state | **LLM** | This is the key insight. Regulatory changes are messy — same regulation described differently across scans, references change format, titles get updated. Claude's semantic understanding catches matches that hash comparison misses. E.g., recognising "PRA PS2/26 on Basel 3.1 output floors" maps to known entry "CRR/CRR III - Output floor implementation". |
| **6** | Decide what is NEW vs UPDATED vs UNCHANGED | **LLM** | Requires judgment: Is a status change from "Consultation" to "Final" an update worth alerting? Has the effective date shifted materially? Is this a genuinely new initiative or a minor amendment to something known? |
| **7** | Assess materiality of new findings | **LLM** | Subjective judgment based on bank context, risk domains affected, timeline urgency. Core CRO-level reasoning. |
| **8** | Update known regulations store | **Script** | Pure JSON merge + write. Deterministic. Atomic file write (OpenClaw pattern). |
| **9** | Write full report to output/ | **Script** | File write with timestamp-based filename. Deterministic. |
| **10** | Format Telegram notification | **Script** | Template-based formatting with emoji indicators. Deterministic output from structured input. |
| **11** | Send Telegram notification | **Script** | HTTP POST. Must not vary. Deterministic. |
| **12** | Log execution result | **Script** | JSONL append with status, duration, counts. Deterministic. |

### Visual Split

```
SKILL.md Workflow
═══════════════════════════════════════════════════════════════

  ┌─────────────────────┐     ┌──────────────────────────────┐
  │   SCRIPT (Python)   │     │   LLM (Claude Reasoning)     │
  │   Deterministic     │     │   Non-Deterministic          │
  │   Low freedom       │     │   High freedom               │
  └─────────┬───────────┘     └──────────────┬───────────────┘
            │                                │
   Step 1:  │ load_known.py                  │
   Load     │ → JSON read                    │
   known    │ → stdout: findings list        │
            │                                │
            │                  Step 2:       │ regulatory-risk-
            │                  Research      │ researcher agent
            │                  (WebSearch)   │ via Task tool
            │                                │
            │                  Step 3:       │ Parse markdown
            │                  Extract       │ output into
            │                  findings      │ structured JSON
            │                                │
   Step 4:  │ generate_ids.py                │
   Generate │ → hash(regulator+ref)          │
   IDs      │ → deterministic IDs            │
            │                                │
            │                  Step 5-7:     │ Semantic diff
            │                  Compare &     │ + materiality
            │                  classify      │ assessment
            │                                │
   Step 8:  │ save_findings.py               │
   Update   │ → atomic JSON write            │
   known    │ → backup copy                  │
            │                                │
   Step 9:  │ archive_report.py              │
   Archive  │ → write to output/             │
            │                                │
   Step 10: │ format_notify.py               │
   Format   │ → template + emoji             │
   message  │                                │
            │                                │
   Step 11: │ send_telegram.py               │
   Notify   │ → HTTP POST                    │
            │                                │
   Step 12: │ log_run.py                     │
   Log      │ → JSONL append                 │
            ▼                                ▼
```

### Why Claude Does the Diff (Not Code)

The original v1.0 design proposed a Python `DiffEngine` class with hash-based matching and `_has_meaningful_changes()` logic. After analysis, this is better handled by Claude for several reasons:

1. **Fuzzy matching**: The same regulation appears differently across scans. A hash of "FCA CP25/3" won't match "FCA Consultation Paper 25/3" — but Claude recognises these as the same document instantly.

2. **Status change significance**: Code can detect that `status` changed from `"Consultation"` to `"Final"`, but Claude can assess *whether this matters* in context. A minor technical standard going final is less urgent than a major capital requirement.

3. **Novel regulation detection**: When something genuinely new appears (like a new AI governance framework), Claude can assess whether it maps to an existing taxonomy family or represents a new regulatory initiative. Code would require pre-programmed rules for every possible mapping.

4. **The taxonomy baseline is prose**: The existing `regulatory-inventory.md` has 23 entries described in natural language with varying levels of detail. Claude reads and understands this directly. A Python diff engine would need a separate structured extraction step.

5. **Cost is negligible**: Reading `known_regulations.json` (even with 100+ entries) adds ~2,000 tokens per run. At Sonnet pricing, this is ~$0.006 per scan.

### What Code Does Better

The scripts handle operations where:
- **Exact reproducibility matters** — Finding IDs must be identical across runs
- **Atomicity matters** — File writes must be crash-safe
- **No judgment is needed** — HTTP POST, JSON serialization, file paths
- **Token efficiency matters** — Scripts execute without entering the context window (only their output does)

---

## 6. SKILL.md Specification

### Skill Directory Structure

```
.claude/skills/regulatory-monitor/
├── SKILL.md                    # Main orchestration instructions
├── reference/
│   └── TAXONOMY_BASELINE.md    # Known regulation families (from L1)
└── scripts/
    ├── load_known.py           # Read known_regulations.json
    ├── save_findings.py        # Atomic write of updated findings
    ├── generate_ids.py         # Deterministic ID generation
    ├── format_notify.py        # Format Telegram notification
    ├── send_telegram.py        # HTTP POST to Telegram gateway
    ├── archive_report.py       # Save report to output/ directory
    └── log_run.py              # Append JSONL run log entry
```

### SKILL.md Content

```markdown
---
name: regulatory-monitor
description: Proactive regulatory monitoring workflow. Scans for new regulatory announcements from PRA, FCA, BoE, EBA, BCBS. Compares against known regulations to identify genuinely new developments. Use when asked to run a regulatory scan, check for new regulations, or monitor regulatory changes. Keywords: regulatory scan, monitor regulations, new announcements, PRA updates, FCA updates, regulatory horizon scan.
---

# Regulatory Monitor

You are a **Regulatory Monitoring Coordinator** who identifies new and changed
regulatory announcements and assesses their impact on the bank's risk framework.

## Your Role

You orchestrate the full monitoring workflow: load known state, invoke the
regulatory researcher, compare findings, update state, and notify. You combine
Python scripts (for deterministic I/O) with your own reasoning (for research
and semantic comparison).

## Workflow

Copy this checklist and track your progress:

```
Regulatory Monitor Progress:
- [ ] Step 1: Load known regulatory state (script)
- [ ] Step 2: Conduct regulatory research (Task → researcher agent)
- [ ] Step 3: Parse findings into structured format (reasoning)
- [ ] Step 4: Generate finding IDs (script)
- [ ] Step 5: Compare against known state (reasoning)
- [ ] Step 6: Update known regulations store (script)
- [ ] Step 7: Archive full report (script)
- [ ] Step 8: Notify if new findings (script)
- [ ] Step 9: Log execution result (script)
```

### Step 1: Load Known State (Script)

Run the loader script to get the current known regulations:

```bash
python .claude/skills/regulatory-monitor/scripts/load_known.py
```

This outputs a JSON summary of known regulatory items to stdout.
If no known state exists yet, the script outputs an empty baseline.
The script does NOT load into context — only its output does.

### Step 2: Conduct Regulatory Research (LLM → Agent)

Launch the `regulatory-risk-researcher` agent using the Task tool:

```
You MUST use the Task tool with subagent_type="regulatory-risk-researcher"
to conduct the actual web research.

The agent should:
- Search PRA, FCA, BoE, EBA, BCBS for recent announcements
- Focus on the time period since the last scan (from Step 1 output)
- Identify consultation papers, policy statements, supervisory statements,
  Dear CEO letters, and other regulatory communications
- Return findings in the standard Regulatory Research Report format
```

Wait for the researcher agent to complete and return its findings.

### Step 3: Parse Findings (LLM Reasoning)

From the researcher's markdown output, extract each finding into this
JSON structure:

```json
[
  {
    "source_regulator": "PRA",
    "document_type": "PS",
    "title": "PS2/26 - Capital Requirements for Market Risk",
    "reference": "PS2/26",
    "publication_date": "2026-01-15",
    "effective_date": "2027-01-01",
    "status": "Final",
    "materiality": "Critical",
    "risk_domains": ["Market Risk", "Capital"],
    "summary": "Updated capital requirements...",
    "key_requirements": ["Requirement 1", "Requirement 2"],
    "source_url": "https://..."
  }
]
```

Use your judgment for materiality and risk domain classification.
If the researcher found nothing new, set findings to an empty list.

### Step 4: Generate Finding IDs (Script)

Pass the parsed findings to the ID generator:

```bash
echo '<findings_json>' | python .claude/skills/regulatory-monitor/scripts/generate_ids.py
```

This adds a deterministic `id` field to each finding based on
`sha256(regulator + ":" + reference)` or `sha256(regulator + ":" + title)`
if no formal reference exists.

IDs MUST be identical across runs for the same regulation.

### Step 5: Compare Against Known State (LLM Reasoning)

This is the critical reasoning step. Using:
- The known state from Step 1
- The current findings with IDs from Step 4
- The taxonomy baseline in [reference/TAXONOMY_BASELINE.md](reference/TAXONOMY_BASELINE.md)

Classify each finding:

**NEW**: Not in known state AND not a variant of an existing entry.
Genuinely novel regulatory development.

**UPDATED**: Matches a known entry but with meaningful changes:
- Status changed (e.g., Consultation → Final)
- Effective date shifted
- Materiality upgraded
- Scope expanded significantly

**UNCHANGED**: Matches a known entry with no material changes.
Same regulation, same status, same timeline.

Use semantic understanding, not just ID matching. The same regulation
may appear with different wording across scans. Consider:
- "FCA CP25/3" and "FCA Consultation Paper 25/3" are the SAME item
- A known REQ-L1-001 (CRR/CRR III) entry covers individual PRA
  policy statements about Basel 3.1 capital requirements

Output your classification as JSON:

```json
{
  "new": [...],
  "updated": [...],
  "unchanged": [...],
  "summary": "Found 2 new items and 1 update out of 7 total findings"
}
```

### Step 6: Update Known State (Script)

Pass the classified findings to the updater:

```bash
echo '<classified_json>' | python .claude/skills/regulatory-monitor/scripts/save_findings.py
```

This atomically updates `data/regulatory_monitor/known_regulations.json`
with new and updated items, setting `first_seen` and `last_seen` timestamps.
Uses atomic write pattern (temp file → rename → backup).

### Step 7: Archive Full Report (Script)

Save the researcher's full report:

```bash
echo '<full_report_text>' | python .claude/skills/regulatory-monitor/scripts/archive_report.py --job-name "weekly-scan"
```

Writes to `output/regulatory-scans/{date}-{job-name}.md`.

### Step 8: Notify If New Findings (Script)

If there are NEW or UPDATED findings, format and send notification:

```bash
echo '<classification_json>' | python .claude/skills/regulatory-monitor/scripts/format_notify.py --job-name "Weekly Scan"
```

Then send the formatted message:

```bash
echo '<formatted_message>' | python .claude/skills/regulatory-monitor/scripts/send_telegram.py
```

If no new or updated findings exist, skip notification.

### Step 9: Log Execution (Script)

Log the run result:

```bash
python .claude/skills/regulatory-monitor/scripts/log_run.py \
  --job-name "weekly-scan" \
  --status "ok" \
  --findings-total 7 \
  --findings-new 2 \
  --findings-updated 1 \
  --duration-seconds 154
```

## Output Format

Present your final summary to the user:

```markdown
# Regulatory Monitor — [Date]

## Summary
- **Total findings**: [N]
- **New**: [N] (notified)
- **Updated**: [N] (notified)
- **Unchanged**: [N]

## New Findings
[List each new finding with regulator, reference, title, materiality]

## Updated Findings
[List each updated finding with what changed]

## Full Report
Archived to: output/regulatory-scans/{date}-{job-name}.md

## Next Steps
- [Recommendations for human review]
- [Any findings requiring regulatory-change-assessor skill]
```

## Governance & Limitations

### What This Skill Does
✅ Orchestrates automated regulatory scanning
✅ Identifies genuinely new regulatory developments
✅ Compares against known state with semantic understanding
✅ Sends proactive Telegram notifications
✅ Archives full reports for audit trail

### What This Skill Does NOT Do
❌ Make compliance decisions
❌ Update the Risk Taxonomy directly
❌ Commit to implementation timelines
❌ Replace human review of regulatory changes

### Human Review Required
All findings flagged as NEW or UPDATED require human review before:
- Updating the regulatory inventory (L1)
- Triggering the regulatory-change-assessor skill
- Modifying policies or controls
- Reporting to Risk Committee
```

---

## 7. Python Scripts (Deterministic Code)

### 7.1 Script Design Principles

Following [Anthropic's guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

> *"Scripts provide deterministic operations without consuming context. When Claude runs `validate_form.py`, the script's code never loads into the context window. Only the script's output consumes tokens."*

Each script:
- **Reads from stdin** or command-line arguments
- **Writes to stdout** (for Claude to capture)
- **Handles errors explicitly** (returns clear error messages, doesn't punt to Claude)
- **Is self-contained** (no cross-script imports)
- **Documents its interface** (argparse with help text)

### 7.2 `load_known.py`

```python
#!/usr/bin/env python3
"""Load known regulatory state from JSON store.

Reads data/regulatory_monitor/known_regulations.json and outputs
a summary to stdout for Claude to consume.

Output format:
{
  "count": 23,
  "last_updated": "2026-01-27T09:00:00Z",
  "items": [
    {
      "id": "abc123",
      "regulator": "PRA",
      "reference": "SS5/25",
      "title": "Climate Risk",
      "status": "Final",
      "first_seen": "2025-12-11",
      "last_seen": "2026-01-27"
    },
    ...
  ]
}
"""
import json
import sys
from pathlib import Path

STORE_PATH = Path("data/regulatory_monitor/known_regulations.json")

def main():
    if not STORE_PATH.exists():
        print(json.dumps({
            "count": 0,
            "last_updated": None,
            "last_scan_date": None,
            "items": [],
            "message": "No known state exists. This is the first scan."
        }, indent=2))
        return

    try:
        data = json.loads(STORE_PATH.read_text())
        items = data.get("items", {})

        # Output summary (not full details — save context tokens)
        summary_items = []
        for item_id, item in items.items():
            summary_items.append({
                "id": item_id,
                "regulator": item.get("source_regulator", ""),
                "reference": item.get("reference", ""),
                "title": item.get("title", ""),
                "status": item.get("status", ""),
                "materiality": item.get("materiality", ""),
                "first_seen": item.get("first_seen", ""),
                "last_seen": item.get("last_seen", ""),
            })

        print(json.dumps({
            "count": len(summary_items),
            "last_updated": data.get("last_updated"),
            "items": summary_items,
        }, indent=2))

    except (json.JSONDecodeError, KeyError) as e:
        print(json.dumps({
            "count": 0,
            "last_updated": None,
            "items": [],
            "error": f"Failed to parse known state: {e}",
            "message": "Treating as empty baseline."
        }, indent=2))

if __name__ == "__main__":
    main()
```

### 7.3 `generate_ids.py`

```python
#!/usr/bin/env python3
"""Generate deterministic IDs for regulatory findings.

Reads JSON findings array from stdin, adds 'id' field to each.
ID = sha256(regulator + ":" + reference)[:16]
Falls back to sha256(regulator + ":" + normalised_title)[:16] if no reference.

Outputs augmented JSON to stdout.
"""
import hashlib
import json
import sys

def generate_id(finding: dict) -> str:
    regulator = finding.get("source_regulator", "UNKNOWN")
    reference = finding.get("reference", "").strip()

    if reference:
        key = f"{regulator}:{reference}"
    else:
        title = finding.get("title", "").lower().strip()
        key = f"{regulator}:{title}"

    return hashlib.sha256(key.encode()).hexdigest()[:16]

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print("[]")
        return

    try:
        findings = json.loads(raw)
        for finding in findings:
            finding["id"] = generate_id(finding)
        print(json.dumps(findings, indent=2))
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {e}"}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 7.4 `save_findings.py`

```python
#!/usr/bin/env python3
"""Update known regulations store with classified findings.

Reads classification JSON from stdin:
{
  "new": [...],
  "updated": [...],
  "unchanged": [...]
}

Atomically updates data/regulatory_monitor/known_regulations.json.
Uses OpenClaw atomic write pattern: temp file → rename → backup.
"""
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

STORE_PATH = Path("data/regulatory_monitor/known_regulations.json")

def atomic_write(path: Path, data: str):
    """Write atomically: temp file → rename → backup."""
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
        raise
    # Best-effort backup
    try:
        import shutil
        shutil.copy2(path, f"{path}.bak")
    except Exception:
        pass

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print("No input provided", file=sys.stderr)
        sys.exit(1)

    classification = json.loads(raw)
    now = datetime.now(timezone.utc).isoformat()

    # Load existing store
    if STORE_PATH.exists():
        store = json.loads(STORE_PATH.read_text())
    else:
        store = {"version": 1, "items": {}, "last_updated": None}

    # Add/update items
    added = 0
    updated = 0

    for finding in classification.get("new", []):
        finding["first_seen"] = now
        finding["last_seen"] = now
        store["items"][finding["id"]] = finding
        added += 1

    for finding in classification.get("updated", []):
        existing = store["items"].get(finding["id"], {})
        finding["first_seen"] = existing.get("first_seen", now)
        finding["last_seen"] = now
        store["items"][finding["id"]] = finding
        updated += 1

    for finding in classification.get("unchanged", []):
        if finding.get("id") and finding["id"] in store["items"]:
            store["items"][finding["id"]]["last_seen"] = now

    store["last_updated"] = now

    # Atomic write
    atomic_write(STORE_PATH, json.dumps(store, indent=2))

    print(json.dumps({
        "status": "ok",
        "added": added,
        "updated": updated,
        "total_known": len(store["items"]),
    }, indent=2))

if __name__ == "__main__":
    main()
```

### 7.5 `format_notify.py`

```python
#!/usr/bin/env python3
"""Format classified findings into a Telegram notification message.

Reads classification JSON from stdin. Outputs formatted text to stdout.
"""
import json
import sys
import argparse

MATERIALITY_EMOJI = {
    "Critical": "🔴",
    "High": "🟡",
    "Medium": "🟢",
    "Low": "⚪",
}

def format_finding(finding: dict) -> str:
    emoji = MATERIALITY_EMOJI.get(finding.get("materiality", ""), "⚪")
    ref = finding.get("reference", "")
    reg = finding.get("source_regulator", "")
    title = finding.get("title", "")
    summary = finding.get("summary", "")[:120]
    effective = finding.get("effective_date", "")

    header = f"{emoji} {finding.get('materiality', 'UNKNOWN')}: {reg} {ref}"
    body = f"   {title}"
    if effective:
        body += f"\n   Effective: {effective}"
    if summary:
        body += f"\n   {summary}"
    return f"{header}\n{body}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-name", default="Regulatory Scan")
    args = parser.parse_args()

    raw = sys.stdin.read().strip()
    classification = json.loads(raw)

    new_items = classification.get("new", [])
    updated_items = classification.get("updated", [])
    total = len(new_items) + len(updated_items) + len(classification.get("unchanged", []))

    lines = [
        f"🔔 Regulatory Monitor: {args.job_name}",
        "━" * 32,
        "",
        f"📊 {len(new_items)} new, {len(updated_items)} updated ({total} total scanned)",
        "",
    ]

    if new_items:
        lines.append("**New Findings:**")
        for f in new_items:
            lines.append(format_finding(f))
            lines.append("")

    if updated_items:
        lines.append("**Updated:**")
        for f in updated_items:
            lines.append(format_finding(f))
            lines.append("")

    lines.append("━" * 32)
    print("\n".join(lines))

if __name__ == "__main__":
    main()
```

### 7.6 `send_telegram.py`

```python
#!/usr/bin/env python3
"""Send a message via the Telegram gateway.

Reads message text from stdin.
Sends HTTP POST to the configured Telegram gateway URL.
"""
import json
import sys
import urllib.request
import urllib.error

GATEWAY_URL = "https://telegram.gavinslater.co.uk/query"

def main():
    message = sys.stdin.read().strip()
    if not message:
        print(json.dumps({"status": "skipped", "reason": "empty message"}))
        return

    payload = json.dumps({"message": message}).encode()
    req = urllib.request.Request(
        GATEWAY_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(json.dumps({
                "status": "ok",
                "http_status": resp.status,
            }))
    except urllib.error.URLError as e:
        print(json.dumps({
            "status": "error",
            "error": str(e),
            "message": "Telegram delivery failed. Report still archived."
        }))

if __name__ == "__main__":
    main()
```

### 7.7 `archive_report.py`

```python
#!/usr/bin/env python3
"""Archive a regulatory scan report to the output directory.

Reads report markdown from stdin. Writes to output/regulatory-scans/{date}-{job}.md.
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("output/regulatory-scans")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-name", required=True)
    args = parser.parse_args()

    report = sys.stdin.read()
    if not report.strip():
        print(f'{{"status": "skipped", "reason": "empty report"}}')
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-{args.job_name}.md"
    filepath = OUTPUT_DIR / filename
    filepath.write_text(report)
    print(f'{{"status": "ok", "path": "{filepath}"}}')

if __name__ == "__main__":
    main()
```

### 7.8 `log_run.py`

```python
#!/usr/bin/env python3
"""Append a run log entry to the JSONL execution log.

Design from OpenClaw: append-only JSONL, one file per job,
auto-prune at 2MB / 2000 lines.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path("data/regulatory_monitor/runs")
MAX_BYTES = 2_000_000
MAX_LINES = 2000

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-name", required=True)
    parser.add_argument("--status", required=True, choices=["ok", "error", "skipped"])
    parser.add_argument("--findings-total", type=int, default=0)
    parser.add_argument("--findings-new", type=int, default=0)
    parser.add_argument("--findings-updated", type=int, default=0)
    parser.add_argument("--duration-seconds", type=float, default=0)
    parser.add_argument("--error", default=None)
    args = parser.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{args.job_name}.jsonl"

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "job_name": args.job_name,
        "status": args.status,
        "findings_total": args.findings_total,
        "findings_new": args.findings_new,
        "findings_updated": args.findings_updated,
        "duration_seconds": args.duration_seconds,
    }
    if args.error:
        entry["error"] = args.error

    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Auto-prune if too large
    try:
        if log_path.stat().st_size > MAX_BYTES:
            lines = log_path.read_text().strip().split("\n")
            kept = lines[-MAX_LINES:]
            log_path.write_text("\n".join(kept) + "\n")
    except Exception:
        pass

    print(json.dumps({"status": "ok", "log_path": str(log_path)}))

if __name__ == "__main__":
    main()
```

---

## 8. Baseline & Diff Strategy

### 8.1 Two Layers of Regulatory State

The diff operates at two conceptual levels:

```
Layer 1: REGULATION FAMILIES (Taxonomy)         Layer 2: INDIVIDUAL DOCUMENTS (Findings)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REQ-L1-001: CRR/CRR III (Basel 3.1)           PRA PS2/26 - Output floor clarification
REQ-L1-002: CRD VI                             EBA RTS 2026/01 - SA-CCR amendments
REQ-L1-015: SS5/25 (Climate Risk)              FCA CP25/3 - AI model governance
...23 entries total                             ...individual announcements

Source: regulatory-inventory.md                 Source: regulatory-risk-researcher scans
Updated: Quarterly (manual)                     Updated: Every scan (automated)
Purpose: Strategic oversight                    Purpose: Operational alerting
```

### 8.2 Seeding the Known State

The initial `known_regulations.json` is seeded from the existing regulatory inventory in `docs/risk-taxonomy/L1-Requirements/regulatory-inventory.md`. This contains **23 structured regulation entries** with:

- Node IDs (`REQ-L1-001` through `REQ-L1-023`)
- Regulator, effective dates, materiality, status
- Document references (SS5/25, CRR III, FRTB, etc.)
- Implementation status

A one-time bootstrap script extracts these into the JSON format. This gives the diff engine:
- Known regulation families to match against
- Known document references (so "SS5/25" isn't flagged as "new" on the first scan)
- A materiality baseline

### 8.3 Taxonomy Baseline Reference File

The skill includes a `reference/TAXONOMY_BASELINE.md` file — a condensed version of the regulatory inventory that Claude can read during the comparison step. This provides the semantic context for matching findings to known regulation families.

```markdown
# Known Regulation Families

| ID | Regulation | Regulator | Key Refs | Status |
|----|-----------|-----------|----------|--------|
| REQ-L1-001 | CRR/CRR III | PRA/EBA | CRR, CRR III, 575/2013 | In progress |
| REQ-L1-002 | CRD VI | PRA | CRD VI | In progress |
| REQ-L1-003 | FRTB | PRA/EBA | FRTB, SS13/13 | In progress |
| REQ-L1-015 | SS5/25 Climate Risk | PRA | SS5/25, PS25/25, CP16/24 | New |
| ... | ... | ... | ... | ... |
```

This is a Level 3 resource (loaded only when referenced in Step 5) — it doesn't consume context until needed.

### 8.4 Known-State Lifecycle

```
Initial state: Bootstrap from regulatory-inventory.md
  → 23 regulation families with known references

First automated scan:
  → Researcher finds 12 current regulatory announcements
  → Claude compares against 23 known families
  → 9 match existing families (UNCHANGED)
  → 3 are genuinely new announcements (NEW)
  → Notify: "3 new findings"
  → All 12 added to known_regulations.json (total: 35)

Second scan (1 week later):
  → Researcher finds 14 announcements
  → 11 match known state (UNCHANGED)
  → 1 status changed: Consultation → Final (UPDATED)
  → 2 genuinely new (NEW)
  → Notify: "2 new, 1 updated"
  → Known state updated (total: 37)

Ongoing:
  → Known state grows incrementally
  → Each scan is efficient — Claude only needs to reason about
    genuinely ambiguous matches, not re-evaluate everything
  → Items not seen for 6+ months flagged as potentially stale
```

---

## 9. Scheduler (Standalone Service on Pi)

### 9.1 Purpose

The cron scheduler is a **standalone, generic service** that runs in Docker on the Raspberry Pi. Its only job is:
1. Load job definitions from YAML config
2. Compute next due times using `croniter`
3. When due, send an HTTP POST to the Mac's telegram-agent service
4. Capture the response and update job state

It knows nothing about regulatory monitoring, Claude skills, or the Risk Agents platform. It is a pure timing + HTTP delivery engine.

### 9.2 Architecture

**Location**: `/Volumes/DockSSD/projects/scheduler/` (standalone project, github.com/gavraq/scheduler)

```
/Volumes/DockSSD/projects/scheduler/
├── pyproject.toml                # Dependencies: croniter, httpx, pyyaml
├── Dockerfile                    # Lightweight Python image
├── docker-compose.yml            # Docker deployment config
├── config/
│   └── jobs.yaml                 # Job definitions (see Section 11)
├── data/                         # Runtime state (Docker volume)
│   ├── job_state.json            # Atomic job state persistence
│   └── runs/                     # JSONL execution logs per job
└── src/cron_scheduler/
    ├── __init__.py
    ├── main.py                   # Service entrypoint + health endpoint
    ├── scheduler.py              # Smart timer loop (asyncio, event-driven)
    ├── config.py                 # YAML config loading + validation
    ├── store.py                  # Atomic JSON state persistence
    ├── run_log.py                # JSONL execution log (append, auto-prune)
    └── client.py                 # httpx async client to Mac agent service
```

### 9.3 Scheduler Core

Adopts the OpenClaw smart-timer pattern (see [Section 10.5](#105-smart-timer-pattern-from-servicetimerts)) but delivers via HTTP instead of subprocess:

```python
class Scheduler:
    """
    Generic cron scheduler: sends HTTP POST on cron schedules.
    Knows nothing about what the jobs do — only about timing and delivery.
    """

    async def _execute_job(self, job: JobConfig, state: JobState):
        """Send job payload to the Mac agent service."""
        start = time.time()
        state.running_since = datetime.now(timezone.utc).isoformat()

        payload = {
            "project": job.project,
            "prompt": job.prompt,
            "model": job.model,
            "max_turns": job.max_turns,
            "timeout_seconds": job.timeout_seconds,
            "job_name": job.name,
        }

        try:
            async with httpx.AsyncClient(timeout=job.timeout_seconds) as client:
                response = await client.post(
                    job.target_url,  # e.g., https://telegram.gavinslater.co.uk/scheduled-job
                    json=payload,
                    headers={"x-api-key": self.api_key},
                )

            duration = time.time() - start
            state.running_since = None
            state.last_run_at = datetime.now(timezone.utc).isoformat()
            state.last_duration_seconds = duration

            if response.status_code == 200:
                result = response.json()
                state.last_status = "ok"
                state.last_response_summary = result.get("summary", "")[:500]
                state.total_runs += 1
            else:
                state.last_status = "error"
                state.last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                state.total_errors += 1

        except httpx.TimeoutException:
            state.running_since = None
            state.last_status = "error"
            state.last_error = f"Timeout after {job.timeout_seconds}s"
            state.total_errors += 1

        except httpx.ConnectError as e:
            state.running_since = None
            state.last_status = "error"
            state.last_error = f"Connection failed: {e}"
            state.total_errors += 1

        # Compute next run
        state.next_run_at = self._compute_next_run(job.schedule)
```

### 9.4 Telegram-Agent Extension: `/scheduled-job` Endpoint

The existing telegram-agent service at `~/projects/telegram/agent/` is extended with a single new endpoint:

```python
# Added to ~/projects/telegram/agent/src/telegram_agent/main.py

class ScheduledJobRequest(BaseModel):
    project: str           # Working directory (e.g., /Volumes/DockSSD/projects/riskagents)
    prompt: str            # Message to send to Claude Agent SDK
    model: str = "sonnet"  # Model to use
    max_turns: int = 15    # Maximum agent turns
    timeout_seconds: int = 600  # Execution timeout
    job_name: str = ""     # For logging/tracking

class ScheduledJobResponse(BaseModel):
    status: str            # "ok" or "error"
    response: str          # Agent response text (truncated)
    duration_ms: int       # Execution time
    cost_usd: float | None # API cost if available
    tools_used: list[str]  # Tools invoked
    skills_used: list[str] # Skills invoked
    summary: str           # Brief summary for scheduler log
    error: str | None = None

@app.post("/scheduled-job")
async def scheduled_job(request: ScheduledJobRequest):
    """Execute a scheduled job via Claude Agent SDK.

    This endpoint is called by the cron-scheduler on Pi.
    It runs the agent in a fresh session (no resume) with the
    specified project directory and prompt.
    """
    # Uses the same run_agent_query() as /query
    # but with explicit model/timeout and no session resume
    result = await run_agent_query(
        message=request.prompt,
        cwd=request.project,
        session_id=None,  # Always fresh session
        model=request.model,
        max_turns=request.max_turns,
    )
    return ScheduledJobResponse(
        status="ok",
        response=result.response[:2000],
        duration_ms=result.duration_ms,
        cost_usd=result.cost_usd,
        tools_used=result.tools_used,
        skills_used=result.skills_used,
        summary=f"Completed in {result.duration_ms/1000:.1f}s, "
                f"used {len(result.skills_used)} skills",
    )
```

This is intentionally minimal. The telegram-agent already handles:
- Project autodiscovery (agents, skills)
- Claude Agent SDK lifecycle
- Error handling and timeout
- Metadata tracking (tools, skills, cost, duration)

---

## 10. Reference Architecture: OpenClaw Cron Analysis

### 10.1 Overview

[OpenClaw](https://github.com/openclaw/openclaw) is a self-hosted personal AI assistant with built-in cron scheduling. Its `src/cron/` module provides a mature, production-tested scheduling engine for AI agent execution. We conducted a deep source-code analysis of every file in this module to extract design patterns.

### 10.2 OpenClaw Cron Module Structure

```
src/cron/                            # OpenClaw's scheduling module
├── types.ts                         # Core data models
├── schedule.ts                      # Next-run time computation
├── store.ts                         # JSON file persistence (atomic writes)
├── run-log.ts                       # JSONL append-only execution log
├── normalize.ts                     # Input validation and coercion
├── parse.ts                         # Time expression parsing
├── payload-migration.ts             # Schema migration for old configs
├── service.ts                       # Public API facade (CronService class)
├── isolated-agent.ts                # Re-exports from isolated-agent/
├── isolated-agent/
│   ├── run.ts                       # Full isolated agent execution
│   ├── session.ts                   # Session management for isolated runs
│   ├── delivery-target.ts           # Channel/recipient resolution
│   └── helpers.ts                   # Output parsing + summary extraction
└── service/
    ├── state.ts                     # Service state + dependency injection
    ├── timer.ts                     # Smart timer arm/disarm + execution
    ├── ops.ts                       # CRUD operations (add/update/remove/run)
    ├── jobs.ts                      # Job lifecycle (create, patch, due-check)
    ├── locked.ts                    # Concurrency mutex (promise chaining)
    ├── store.ts                     # Store loading with migration + caching
    └── normalize.ts                 # Job field normalization
```

### 10.3 Core Data Models (from `types.ts`)

#### Schedule Types

```typescript
type CronSchedule =
  | { kind: "at"; atMs: number }                              // One-shot
  | { kind: "every"; everyMs: number; anchorMs?: number }     // Fixed interval
  | { kind: "cron"; expr: string; tz?: string }               // Cron expression
```

#### Session Targets

```typescript
type CronSessionTarget = "main" | "isolated";
```

**Critical design choice**: Regulatory scans use `isolated` mode — fresh context per run, no history pollution. This prevents the "context buildup" problem documented in [OpenClaw Issue #1594](https://github.com/openclaw/openclaw/issues/1594).

#### Payload Types

```typescript
type CronPayload =
  | { kind: "systemEvent"; text: string }
  | {
      kind: "agentTurn";
      message: string;
      model?: string;
      timeoutSeconds?: number;
      deliver?: boolean;
      channel?: string;
      to?: string;
      bestEffortDeliver?: boolean;
    };
```

#### Job State

```typescript
type CronJobState = {
  nextRunAtMs?: number;
  runningAtMs?: number;        // Acts as execution lock
  lastRunAtMs?: number;
  lastStatus?: "ok" | "error" | "skipped";
  lastError?: string;
  lastDurationMs?: number;
};
```

Auto-clears stuck jobs after 2 hours (`STUCK_RUN_MS = 2 * 60 * 60 * 1000`).

#### Isolation Configuration

```typescript
type CronIsolation = {
  postToMainPrefix?: string;                    // e.g., "RegScan"
  postToMainMode?: "summary" | "full";
  postToMainMaxChars?: number;                  // Default: 8000
};
```

### 10.4 Scheduling Engine (from `schedule.ts`)

Next-run computation using the [`croner`](https://github.com/Hexagon/croner) library. **Python equivalent**: `croniter`.

### 10.5 Smart Timer Pattern (from `service/timer.ts`)

Event-driven scheduling rather than fixed polling:

```typescript
function armTimer(state) {
  clearTimeout(state.timer);
  const nextAt = nextWakeAtMs(state);       // Soonest due job
  if (!nextAt) return;
  const delay = Math.max(nextAt - nowMs(), 0);
  state.timer = setTimeout(() => onTimer(state), delay);
}
```

**Advantages**: Zero CPU when idle, precise timing, self-adjusting.

### 10.6 Persistence Patterns

**Atomic writes**: `temp file → rename → backup`. Crash-safe.
**JSONL run logs**: Append-only, auto-prune at 2MB/2000 lines.
**Concurrency**: Promise-chain mutex per store path. Python equivalent: `asyncio.Lock()`.

### 10.7 What OpenClaw Gets Right (Adopted)

| Pattern | Adopted As |
|---------|-----------|
| Isolated sessions | Fresh Claude SDK session per `/scheduled-job` call |
| Smart timers | `asyncio.sleep()` to next due time |
| Atomic persistence | `save_findings.py` temp→rename pattern |
| JSONL run logs | `log_run.py` with auto-pruning |
| Structured output | Summary for Telegram, full for archive |
| Job state tracking | `store.py` with JobState model |
| Stuck job detection | 2-hour auto-clear in scheduler |
| Model override per job | Config YAML `model` field per job |

### 10.8 What OpenClaw Gets Wrong (Avoided)

| Issue | Problem | Our Approach |
|-------|---------|-------------|
| **Heartbeat coupling** | [Issue #3589](https://github.com/openclaw/openclaw/issues/3589): Cron jobs hijacked by heartbeat prompts | Standalone scheduler. No heartbeat concept. |
| **Over-abstracted delivery** | 4+ layers for message delivery | Single `send_telegram.py` script. |
| **Missing schema docs** | [Issue #4862](https://github.com/openclaw/openclaw/issues/4862): AI couldn't figure out the schema | Clear YAML config + SKILL.md with step-by-step instructions. |
| **No deduplication** | Repeated notifications for same regulation | LLM-powered semantic diff in SKILL.md Step 5. |
| **Gateway dependency** | Deeply coupled to WebSocket control plane | Self-contained skill + standalone generic scheduler on Pi. |

---

## 11. Configuration

### 11.1 Schedule Configuration (Standalone Scheduler on Pi)

```yaml
# /Volumes/DockSSD/projects/scheduler/config/jobs.yaml
# Generic job definitions — scheduler knows nothing about the jobs' content
# It only knows: WHEN to fire, WHERE to send, and WHAT payload to deliver

# Default target for all jobs (can be overridden per job)
defaults:
  target_url: "https://telegram.gavinslater.co.uk/scheduled-job"
  timezone: "Europe/London"

jobs:
  # ─── REGULATORY MONITORING (riskagents project) ───────────────────

  - name: "weekly-regulatory-scan"
    description: "Comprehensive scan of all major regulators"
    enabled: true
    schedule: "0 9 * * 1"              # Every Monday at 09:00
    project: "/Volumes/DockSSD/projects/riskagents"
    prompt: "Run a regulatory monitoring scan for job 'weekly-regulatory-scan'. Use the regulatory-monitor skill."
    model: "sonnet"
    max_turns: 15
    timeout_seconds: 600

  - name: "daily-pra-fca-check"
    description: "Quick daily check for critical PRA/FCA announcements"
    enabled: true
    schedule: "0 8 * * 1-5"            # Weekdays at 08:00
    project: "/Volumes/DockSSD/projects/riskagents"
    prompt: "Run a quick regulatory check focusing on PRA and FCA announcements only. Use the regulatory-monitor skill."
    model: "haiku"
    max_turns: 10
    timeout_seconds: 300

  - name: "monthly-basel-frtb-review"
    description: "Deep analysis of Basel 3.1 and FRTB developments"
    enabled: true
    schedule: "0 10 1 * *"             # 1st of each month at 10:00
    project: "/Volumes/DockSSD/projects/riskagents"
    prompt: "Run a deep regulatory scan focused on Basel 3.1/CRR III and FRTB developments. Use the regulatory-monitor skill."
    model: "sonnet"
    max_turns: 20
    timeout_seconds: 900

  # ─── FUTURE: OTHER PROJECT JOBS ───────────────────────────────────
  # The scheduler is generic. Add jobs for any project:

  # - name: "life-weekly-review"
  #   description: "Weekly life admin review"
  #   enabled: false
  #   schedule: "0 18 * * 5"            # Friday at 18:00
  #   project: "/Users/gavinslater/projects/life"
  #   prompt: "Review this week's tasks and prepare weekend summary."
  #   model: "haiku"
  #   max_turns: 5
  #   timeout_seconds: 120
```

Note: Each job carries its own `project`, `prompt`, and `model`. The scheduler is a generic delivery engine — add any project's jobs to this YAML file without touching scheduler code.

### 11.2 Configuration Comparison with OpenClaw

| Aspect | OpenClaw | Our Design | Rationale |
|--------|----------|-----------|-----------|
| Format | JSON at runtime | YAML in config file | Human-readable, comments, version-controlled |
| Job definition | `cron.add` RPC | Declared in YAML | Config-as-code |
| Workflow logic | Embedded in TypeScript | In SKILL.md | Transparent, modifiable, consistent with platform |
| Mutable state | Mixed with definitions | Separated: YAML (config) + JSON (state) | Clean separation |
| Schema docs | Missing ([Issue #4862](https://github.com/openclaw/openclaw/issues/4862)) | YAML comments + design doc + SKILL.md | Learned from their mistake |

---

## 12. Notification & Delivery

### 12.1 Telegram Delivery

Leverages the existing infrastructure documented in [docs/11-telegram-standalone-architecture.md](11-telegram-standalone-architecture.md):

```
.claude/skills/regulatory-monitor/scripts/send_telegram.py
    │ HTTP POST (urllib, no dependencies)
    ▼
~/projects/telegram/agent (Mac, FastAPI port 8095)
    │ HTTPS via Nginx Proxy Manager
    ▼
telegram-gateway (Pi, Docker)
    │
    ▼
Gavin's Telegram
```

### 12.2 Notification Format

**Summary notification** (daily/weekly):

```
🔔 Regulatory Monitor: Weekly Scan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 3 new, 1 updated (7 total scanned)

**New Findings:**
🔴 CRITICAL: PRA PS2/26
   Capital Requirements for Market Risk under Basel 3.1
   Effective: Jan 2027

🟡 HIGH: FCA CP25/3
   Consultation on AI Governance for Financial Firms
   Response deadline: Apr 2026

🟢 MEDIUM: EBA GL/2026/01
   Guidelines on ESG Risk Integration in ICAAP
   Effective: Jul 2026

**Updated:**
🟡 HIGH: PRA SS5/25
   Climate Risk — Status changed: Consultation → Final

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Full report archived to output/
```

---

## 13. Deployment Architecture

### 13.1 Overview: Two Machines, Three Services

```
┌─────────────────────────────────────────────────────────────────────┐
│  Raspberry Pi (192.168.x.x, Docker, always-on)                      │
│                                                                      │
│  ┌────────────────────────┐  ┌────────────────────────────────┐     │
│  │ telegram-gateway       │  │ cron-scheduler (NEW)           │     │
│  │ Container: running     │  │ Container: running             │     │
│  │ Network: personal-ai   │  │ Network: personal-ai           │     │
│  │ Ports: 3000            │  │ Ports: 8092 (API + dashboard)  │     │
│  └───────────┬────────────┘  └───────────┬────────────────────┘     │
│              │                            │                          │
└──────────────┼────────────────────────────┼──────────────────────────┘
               │ HTTPS via Nginx            │ HTTPS via Nginx
               │ Proxy Manager              │ Proxy Manager
               ▼                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Mac (launchd, always running telegram-agent)                        │
│                                                                      │
│  ~/projects/telegram/agent                                           │
│  Service: com.gavinslater.telegram-agent                             │
│  Port: 8095                                                          │
│  Endpoints:                                                          │
│    POST /query          ← telegram-gateway                           │
│    POST /scheduled-job  ← cron-scheduler (NEW)                       │
│    GET  /health         ← both                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### 13.2 Scheduler: Docker on Pi

```yaml
# /Volumes/DockSSD/projects/scheduler/docker-compose.yml
services:
  cron-scheduler:
    build: .
    container_name: cron-scheduler
    restart: unless-stopped
    ports:
      - "8092:8092"
    volumes:
      - ./config:/app/config:ro
      - scheduler-data:/app/data
    environment:
      - AGENT_API_KEY=${AGENT_API_KEY}
      - TARGET_URL=https://telegram.gavinslater.co.uk/scheduled-job
      - TZ=Europe/London
    networks:
      - personal-ai

volumes:
  scheduler-data:

networks:
  personal-ai:
    external: true
```

### 13.3 Agent Service: Mac (Existing, Extended)

The telegram-agent service already runs via launchd (`com.gavinslater.telegram-agent`). The `/scheduled-job` endpoint is added to the existing service — no new deployment needed. Just update the code and restart:

```bash
cd ~/projects/telegram/agent
git pull
uv sync
launchctl kickstart -k gui/$(id -u)/com.gavinslater.telegram-agent
```

### 13.4 Nginx Proxy Manager Routes

Add a new route for the scheduler health endpoint:

| Subdomain | Target | Purpose |
|-----------|--------|---------|
| `telegram.gavinslater.co.uk` | Mac:8095 | Existing: Telegram + scheduled jobs |
| `scheduler.gavinslater.co.uk` | Pi:8092 | Scheduler API + web dashboard |

---

## 14. Integration with Existing System

### 14.1 Agent Integration

The SKILL.md invokes the existing `regulatory-risk-researcher` agent via the Task tool. No changes to the agent definition are needed — the skill provides the trigger mechanism that the agent already anticipates (`.claude/agents/regulatory-risk-researcher.md` line 195).

### 14.2 Downstream Pipeline

```
regulatory-monitor (SKILL.md, automated)
    │
    ▼ Findings flagged as NEW or UPDATED
Human review via Telegram notification
    │
    ▼ Human decides to investigate further
regulatory-change-assessor (skill, manual invocation)
    │ Maps to taxonomy L1-L7
    ▼
project-planner (skill)
    │ Creates implementation plan
    ▼
change-agent (orchestrates implementation)
```

### 14.3 Parallel Research Pattern

Future enhancement: jurisdiction-specific parallel scans following the stress-scenario-suggester pattern (launches 5 agents simultaneously via Task tool).

### 14.4 Existing Skill Consistency

This skill follows the same patterns as the existing 9 skills:

| Aspect | stress-scenario-suggester | regulatory-monitor |
|--------|--------------------------|-------------------|
| SKILL.md location | `.claude/skills/stress-scenario-suggester/SKILL.md` | `.claude/skills/regulatory-monitor/SKILL.md` |
| Agent invocation | Task tool → 5 research agents | Task tool → regulatory-risk-researcher |
| Output format | Structured markdown report | Structured markdown report |
| Scripts | None (LLM-only) | 7 Python scripts for deterministic I/O |
| Human review | Required for all suggestions | Required for NEW/UPDATED findings |

---

## 15. Security Considerations

### 15.1 Authentication

- **Pi → Mac**: The scheduler authenticates to the telegram-agent via `x-api-key` header (same key used by the Telegram gateway). Stored in scheduler's `.env` file, not in YAML config.
- **Mac → Claude**: The telegram-agent uses the existing Max subscription via the Claude Agent SDK. No separate API key needed.
- **HTTPS**: All Pi → Mac traffic goes through Nginx Proxy Manager with TLS.

### 15.2 Prompt Integrity

Prompts are entirely internal (defined in SKILL.md in the repo). No external prompt injection risk.

### 15.3 Data Sensitivity

- `data/regulatory_monitor/` is not committed to git (add to `.gitignore`)
- `output/regulatory-scans/` stored locally only
- Telegram notifications use summary format only

---

## 16. Operational Concerns

### 16.1 Cost Management

| Job | Model | Frequency | Est. Cost/Run | Monthly Cost |
|-----|-------|-----------|---------------|-------------|
| Daily PRA/FCA check | Haiku | 5x/week | ~$0.005 | ~$0.10 |
| Weekly full scan | Sonnet | 1x/week | ~$0.20 | ~$0.80 |
| Monthly Basel deep dive | Sonnet | 1x/month | ~$0.40 | ~$0.40 |
| **Total estimated** | | | | **~$1.30/month** |

Using Max subscription means these runs consume subscription capacity rather than per-token API charges.

### 16.2 Failure Handling

| Failure | Handling |
|---------|----------|
| Mac agent unreachable | Scheduler logs HTTP error, retries on next schedule |
| Telegram gateway down | Skill archives report anyway, notification skipped |
| Scan timeout | Scheduler HTTP timeout, logs `status=error` |
| Stuck job (>2 hours) | Auto-clear `running_since` flag |
| Skill script failure | Skill logs error in step checklist, continues to next step |

### 16.3 Monitoring

```bash
# Scheduler health (from anywhere)
curl https://scheduler.gavinslater.co.uk/health

# Job status and recent runs
curl https://scheduler.gavinslater.co.uk/jobs
curl https://scheduler.gavinslater.co.uk/jobs/weekly-regulatory-scan/logs?limit=10

# Manual trigger (run job now)
curl -X POST https://scheduler.gavinslater.co.uk/jobs/weekly-regulatory-scan/run-now \
  -H "x-api-key: $SCHEDULER_API_KEY"

# Check local run logs (on Mac, from riskagents project)
cat data/regulatory_monitor/runs/weekly-regulatory-scan.jsonl | tail -5
```

---

## 17. Implementation Plan

### Phase 1: Skill + Scripts ✅ COMPLETE

**Deliverables** (all implemented):
1. ✅ `.claude/skills/regulatory-monitor/SKILL.md` — 9-step orchestration workflow
2. ✅ 7 Python scripts in `scripts/` + 1 bootstrap script
3. ✅ `reference/TAXONOMY_BASELINE.md` — 23 known regulation families
4. ✅ `data/regulatory_monitor/known_regulations.json` — Bootstrapped with 23 entries
5. ✅ `.gitignore` updated for runtime data directories

**Outcome**: Full regulatory monitoring workflow, invokable on-demand via Claude.

### Phase 2a: Extend Telegram-Agent (Mac Side) ✅ COMPLETE

**Location**: `~/projects/telegram/agent/`

**Deliverables** (all implemented):
1. ✅ `POST /scheduled-job` endpoint in `main.py` — Accept structured job payloads
2. ✅ `ScheduledJobRequest` / `ScheduledJobResponse` Pydantic models
3. ✅ `run_agent_query()` extension — Support explicit model and max_turns parameters
4. Restart launchd service to pick up changes

**Outcome**: Mac agent service can accept and execute scheduled job requests.

### Phase 2b: Standalone Cron Scheduler (Pi Side) ✅ COMPLETE

**Location**: `/Volumes/DockSSD/projects/scheduler/` (standalone project, [github.com/gavraq/scheduler](https://github.com/gavraq/scheduler))
**Port**: 8092, subdomain: `scheduler.gavinslater.co.uk`

**Deliverables** (all implemented):
1. ✅ `src/cron_scheduler/scheduler.py` — Smart timer engine (asyncio, event-driven)
2. ✅ `src/cron_scheduler/config.py` — YAML config loading/saving with validation
3. ✅ `src/cron_scheduler/store.py` — Atomic JSON job state persistence
4. ✅ `src/cron_scheduler/run_log.py` — JSONL execution log with auto-prune
5. ✅ `src/cron_scheduler/client.py` — httpx async client for Mac delivery
6. ✅ `src/cron_scheduler/main.py` — FastAPI API (CRUD + health/status) + scheduler startup
7. ✅ `config/jobs.yaml` — Initial job definitions (3 regulatory monitoring jobs)
8. ✅ `Dockerfile` + `docker-compose.yml` — Pi deployment (port 8092)
9. ✅ `pyproject.toml` — Dependencies: croniter, httpx, pyyaml, fastapi, uvicorn
10. ✅ CRUD API endpoints — Create, update, delete, toggle jobs via REST API
11. ✅ Web dashboard — Single-page app at `src/cron_scheduler/static/index.html`

**API Endpoints**:
- `GET /` — Web dashboard (job list, create/edit/delete, logs, run-now)
- `GET /health` — Health check
- `GET /api/jobs` — List all jobs with status
- `GET /api/jobs/{name}` — Get job config + status
- `GET /api/jobs/{name}/logs` — Recent execution logs
- `POST /api/jobs` — Create new job
- `PUT /api/jobs/{name}` — Update job config
- `DELETE /api/jobs/{name}` — Delete job
- `POST /api/jobs/{name}/toggle` — Enable/disable job
- `POST /api/jobs/{name}/run-now` — Manual trigger

**Outcome**: Generic, always-on scheduler with web management UI running in Docker on Pi.

### Phase 3: Deployment & Testing

**Deliverables**:
1. Nginx Proxy Manager route for scheduler (`scheduler.gavinslater.co.uk` → Pi:8092)
2. End-to-end test: scheduler → agent → skill → notification
3. Docker volume setup for persistent state on Pi
4. Monitoring: health checks from both services
5. Push code to GitHub repos

**Outcome**: Production deployment with full observability.

### Phase 4: Enhancements (P2)

**Deliverables**:
1. Email notification channel
2. Parallel jurisdiction scans (UK, EU, International)
3. Auto-trigger regulatory-change-assessor for critical findings
4. Retry logic with exponential backoff on Mac connectivity failures

---

## Appendix A: OpenClaw Source Analysis

### Files Analysed

| File | Lines | Purpose | Key Patterns Extracted |
|------|-------|---------|----------------------|
| `src/cron/types.ts` | ~90 | Data models | Schedule types, payload types, job state, isolation config |
| `src/cron/schedule.ts` | ~35 | Next-run computation | Cron expression parsing, interval calculation |
| `src/cron/store.ts` | ~45 | File persistence | Atomic write (temp → rename → backup) |
| `src/cron/run-log.ts` | ~95 | Execution log | JSONL append, auto-prune, reverse-chronological read |
| `src/cron/normalize.ts` | ~130 | Input validation | Schedule kind inference, payload coercion |
| `src/cron/service.ts` | ~45 | Public API | Facade pattern over ops module |
| `src/cron/service/state.ts` | ~70 | Service state | Dependency injection, state initialisation |
| `src/cron/service/timer.ts` | ~200 | Timer engine | Smart timer arm/disarm, job execution, delivery |
| `src/cron/service/ops.ts` | ~100 | CRUD operations | Start, stop, status, list, add, update, remove, run |
| `src/cron/service/jobs.ts` | ~200 | Job lifecycle | Create, patch, due-check, next-run, stuck detection |
| `src/cron/service/locked.ts` | ~20 | Concurrency | Promise-chain mutex per store path |
| `src/cron/service/store.ts` | ~60 | Store management | Lazy loading, caching, migration, persist |
| `src/cron/isolated-agent/run.ts` | ~300 | Agent execution | Session isolation, model resolution, delivery, security |
| **Total** | **~1390** | | |

### OpenClaw Dependencies (Not Adopted)

- `src/infra/heartbeat-runner.ts` — Heartbeat system ([Issue #3589](https://github.com/openclaw/openclaw/issues/3589))
- `src/agents/` — Full agent runtime (model catalogs, fallbacks, providers)
- `src/routing/` — Session routing and key management
- `src/security/` — External content wrapping
- `src/infra/outbound/` — Multi-channel outbound delivery pipeline
- `src/daemon/` — Cross-platform service management (launchd, systemd, schtasks)

---

## Appendix B: Alternative Approaches Evaluated

### B.1 claude-code-scheduler

**Source**: [github.com/jshchnz/claude-code-scheduler](https://github.com/jshchnz/claude-code-scheduler)

Plugin using OS-native scheduling to invoke `claude -p`. **Verdict**: Good trigger mechanism, but no dedup, no skill workflow, no notification push.

### B.2 claude-mcp-scheduler

**Source**: [github.com/tonybentley/claude-mcp-scheduler](https://github.com/tonybentley/claude-mcp-scheduler)

Node.js + Claude API + MCP. **Verdict**: Wrong tech stack (Node.js), requires API key.

### B.3 OpenClaw Gateway (Full)

**Source**: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)

Full AI assistant with cron. **Verdict**: Overkill. Extracted scheduling patterns only (Section 10).

### B.4 SKILL.md + Thin Scheduler (Selected)

**Verdict**: Best fit. Consistent with platform patterns, transparent workflow, deterministic/non-deterministic split follows Anthropic best practices, uses Max subscription, integrates with existing agents and skills.

---

## Appendix C: Anthropic Skills Best Practices Applied

Reference: [Anthropic Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

| Best Practice | How Applied |
|--------------|-------------|
| **"Concise is key"** | SKILL.md focuses on workflow steps. Domain knowledge lives in the researcher agent, not repeated here. |
| **"Set appropriate degrees of freedom"** | Scripts = low freedom (exact operations). LLM comparison = high freedom (context-dependent reasoning). |
| **"Use workflows for complex tasks"** | 9-step checklist with progress tracking. |
| **"Provide utility scripts"** | 7 scripts for deterministic operations. Executed, not loaded into context. |
| **"Implement feedback loops"** | Step 5 (diff) acts as validation: Claude must justify why each finding is NEW vs UNCHANGED. |
| **"Progressive disclosure"** | TAXONOMY_BASELINE.md is a Level 3 resource — loaded only during Step 5 comparison. |
| **"Keep references one level deep"** | All reference files linked directly from SKILL.md. |
| **"Solve, don't punt"** | Scripts handle errors explicitly (return JSON error messages, don't crash). |
| **"Create verifiable intermediate outputs"** | Step 3 produces JSON findings; Step 4 adds IDs; Step 5 classifies. Each step's output can be verified. |
| **"Prefer scripts for deterministic operations"** | JSON I/O, file writes, HTTP POST, ID generation — all scripts. Semantic analysis — all LLM. |
| **"Test with all models"** | Config supports model override per job: Haiku for quick, Sonnet for deep. |

---

*This document is part of the Risk Agents platform documentation. See also:*
- *[docs/02-agents.md](02-agents.md) — Agent architecture*
- *[docs/06e-stress-scenario-suggester.md](06e-stress-scenario-suggester.md) — Parallel research pattern*
- *[docs/11-telegram-standalone-architecture.md](11-telegram-standalone-architecture.md) — Telegram infrastructure*
- *[.claude/agents/regulatory-risk-researcher.md](../.claude/agents/regulatory-risk-researcher.md) — Regulatory researcher agent*
- *[Anthropic Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)*
