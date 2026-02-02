#!/usr/bin/env python3
"""Format classified findings into a Telegram notification message.

Reads classification JSON from stdin. Outputs formatted text to stdout.

Input format:
{
  "new": [...findings...],
  "updated": [...findings...],
  "unchanged": [...findings...],
  "summary": "..."
}

Output: Formatted Telegram-friendly text with emoji indicators.
"""
import argparse
import json
import sys

MATERIALITY_EMOJI = {
    "Critical": "\U0001f534",   # 🔴
    "High": "\U0001f7e1",       # 🟡
    "Medium": "\U0001f7e2",     # 🟢
    "Low": "\u26aa",            # ⚪
}


def format_finding(finding: dict) -> str:
    """Format a single finding for Telegram display."""
    emoji = MATERIALITY_EMOJI.get(finding.get("materiality", ""), "\u26aa")
    ref = finding.get("reference", "")
    reg = finding.get("source_regulator", "")
    title = finding.get("title", "")
    summary = finding.get("summary", "")[:120]
    effective = finding.get("effective_date", "")
    change_desc = finding.get("change_description", "")

    header = f"{emoji} {finding.get('materiality', 'UNKNOWN')}: {reg} {ref}"
    body = f"   {title}"
    if effective:
        body += f"\n   Effective: {effective}"
    if change_desc:
        body += f"\n   Change: {change_desc}"
    elif summary:
        body += f"\n   {summary}"
    return f"{header}\n{body}"


def main():
    parser = argparse.ArgumentParser(
        description="Format regulatory findings for Telegram notification"
    )
    parser.add_argument("--job-name", default="Regulatory Scan",
                        help="Name of the scan job for the header")
    args = parser.parse_args()

    raw = sys.stdin.read().strip()
    if not raw:
        print("")
        return

    try:
        classification = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error parsing input: {e}", file=sys.stderr)
        sys.exit(1)

    new_items = classification.get("new", [])
    updated_items = classification.get("updated", [])
    total = (len(new_items)
             + len(updated_items)
             + len(classification.get("unchanged", [])))

    lines = [
        f"\U0001f514 Regulatory Monitor: {args.job_name}",  # 🔔
        "\u2501" * 32,  # ━
        "",
        f"\U0001f4ca {len(new_items)} new, {len(updated_items)} updated ({total} total scanned)",  # 📊
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

    if not new_items and not updated_items:
        lines.append("\u2705 No new or updated regulatory findings.")  # ✅
        lines.append("")

    lines.append("\u2501" * 32)  # ━
    lines.append("\U0001f4c4 Full report archived to output/regulatory-scans/")  # 📄

    print("\n".join(lines))


if __name__ == "__main__":
    main()
