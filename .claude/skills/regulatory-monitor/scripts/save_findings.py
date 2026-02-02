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

Outputs summary JSON to stdout.
"""
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

STORE_PATH = Path("data/regulatory_monitor/known_regulations.json")


def atomic_write(path: Path, data: str):
    """Write atomically: temp file in same dir → rename → backup.

    This ensures the store file is never in a partially-written state.
    If the process crashes mid-write, the original file is untouched.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        os.write(fd, data.encode())
        os.close(fd)
        # Atomic rename on same filesystem
        os.rename(tmp_path, path)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        # Clean up temp file on failure
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    # Best-effort backup copy
    try:
        shutil.copy2(path, f"{path}.bak")
    except Exception:
        pass


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"status": "error", "error": "No input provided"}))
        sys.exit(1)

    try:
        classification = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    now = datetime.now(timezone.utc).isoformat()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Load existing store or create new
    if STORE_PATH.exists():
        try:
            store = json.loads(STORE_PATH.read_text())
        except json.JSONDecodeError:
            store = {"version": 1, "items": {}, "last_updated": None, "last_scan_date": None}
    else:
        store = {"version": 1, "items": {}, "last_updated": None, "last_scan_date": None}

    added = 0
    updated = 0

    # Process NEW findings
    for finding in classification.get("new", []):
        finding_id = finding.get("id")
        if not finding_id:
            continue
        finding["first_seen"] = now
        finding["last_seen"] = now
        store["items"][finding_id] = finding
        added += 1

    # Process UPDATED findings
    for finding in classification.get("updated", []):
        finding_id = finding.get("id")
        if not finding_id:
            continue
        existing = store["items"].get(finding_id, {})
        finding["first_seen"] = existing.get("first_seen", now)
        finding["last_seen"] = now
        store["items"][finding_id] = finding
        updated += 1

    # Touch UNCHANGED findings (update last_seen only)
    for finding in classification.get("unchanged", []):
        finding_id = finding.get("id")
        if finding_id and finding_id in store["items"]:
            store["items"][finding_id]["last_seen"] = now

    store["last_updated"] = now
    store["last_scan_date"] = today

    # Atomic write
    atomic_write(STORE_PATH, json.dumps(store, indent=2))

    print(json.dumps({
        "status": "ok",
        "added": added,
        "updated": updated,
        "total_known": len(store["items"]),
        "store_path": str(STORE_PATH),
    }, indent=2))


if __name__ == "__main__":
    main()
