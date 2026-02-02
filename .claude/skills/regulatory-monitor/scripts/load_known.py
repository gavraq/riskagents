#!/usr/bin/env python3
"""Load known regulatory state from JSON store.

Reads data/regulatory_monitor/known_regulations.json and outputs
a summary to stdout for Claude to consume.

Output format:
{
  "count": 23,
  "last_updated": "2026-01-27T09:00:00Z",
  "last_scan_date": "2026-01-27",
  "items": [
    {
      "id": "abc123",
      "regulator": "PRA",
      "reference": "SS5/25",
      "title": "Climate Risk",
      "status": "Final",
      "materiality": "Critical",
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
            "last_scan_date": data.get("last_scan_date"),
            "items": summary_items,
        }, indent=2))

    except (json.JSONDecodeError, KeyError) as e:
        print(json.dumps({
            "count": 0,
            "last_updated": None,
            "last_scan_date": None,
            "items": [],
            "error": f"Failed to parse known state: {e}",
            "message": "Treating as empty baseline."
        }, indent=2))


if __name__ == "__main__":
    main()
