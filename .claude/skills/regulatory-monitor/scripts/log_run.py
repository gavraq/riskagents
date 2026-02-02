#!/usr/bin/env python3
"""Append a run log entry to the JSONL execution log.

Design inspired by OpenClaw: append-only JSONL, one file per job name,
auto-prune at 2MB / 2000 lines.

Each line is a JSON object with execution metadata:
- timestamp, job name, status, findings counts, duration

Output: JSON with status and log file path.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path("data/regulatory_monitor/runs")
MAX_BYTES = 2_000_000  # 2MB
MAX_LINES = 2000


def main():
    parser = argparse.ArgumentParser(
        description="Log a regulatory monitor execution"
    )
    parser.add_argument("--job-name", required=True,
                        help="Name of the scan job")
    parser.add_argument("--status", required=True,
                        choices=["ok", "error", "skipped"],
                        help="Execution status")
    parser.add_argument("--findings-total", type=int, default=0,
                        help="Total findings from scan")
    parser.add_argument("--findings-new", type=int, default=0,
                        help="New findings count")
    parser.add_argument("--findings-updated", type=int, default=0,
                        help="Updated findings count")
    parser.add_argument("--duration-seconds", type=float, default=0,
                        help="Total execution duration in seconds")
    parser.add_argument("--error", default=None,
                        help="Error description if status=error")
    args = parser.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = args.job_name.replace(" ", "-").lower()
    log_path = LOG_DIR / f"{safe_name}.jsonl"

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

    # Append entry
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Auto-prune if file exceeds size limit
    try:
        if log_path.stat().st_size > MAX_BYTES:
            lines = log_path.read_text().strip().split("\n")
            if len(lines) > MAX_LINES:
                kept = lines[-MAX_LINES:]
                log_path.write_text("\n".join(kept) + "\n")
    except Exception:
        pass  # Pruning failure is non-fatal

    print(json.dumps({
        "status": "ok",
        "log_path": str(log_path),
    }))


if __name__ == "__main__":
    main()
