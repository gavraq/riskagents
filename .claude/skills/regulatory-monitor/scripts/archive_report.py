#!/usr/bin/env python3
"""Archive a regulatory scan report to the output directory.

Reads report markdown from stdin.
Writes to output/regulatory-scans/{date}-{job-name}.md.

Output: JSON with status and file path.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("output/regulatory-scans")


def main():
    parser = argparse.ArgumentParser(
        description="Archive a regulatory scan report"
    )
    parser.add_argument("--job-name", required=True,
                        help="Job name for the filename (e.g., 'weekly-scan')")
    args = parser.parse_args()

    report = sys.stdin.read()
    if not report.strip():
        print(json.dumps({
            "status": "skipped",
            "reason": "empty report"
        }))
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    # Sanitise job name for filename
    safe_name = args.job_name.replace(" ", "-").lower()
    filename = f"{date_str}-{safe_name}.md"
    filepath = OUTPUT_DIR / filename

    # If file already exists (multiple runs same day), add a counter
    if filepath.exists():
        counter = 1
        while filepath.exists():
            filename = f"{date_str}-{safe_name}-{counter}.md"
            filepath = OUTPUT_DIR / filename
            counter += 1

    filepath.write_text(report)

    print(json.dumps({
        "status": "ok",
        "path": str(filepath),
        "size_bytes": len(report.encode()),
    }))


if __name__ == "__main__":
    main()
