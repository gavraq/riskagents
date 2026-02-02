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
    """Generate a deterministic ID for a regulatory finding.

    Uses regulator + reference as the primary key.
    Falls back to regulator + normalised title if no reference.
    """
    regulator = finding.get("source_regulator", "UNKNOWN").upper().strip()
    reference = finding.get("reference", "").strip()

    if reference:
        key = f"{regulator}:{reference}"
    else:
        # Normalise title: lowercase, strip whitespace, collapse spaces
        title = " ".join(finding.get("title", "").lower().split())
        key = f"{regulator}:{title}"

    return hashlib.sha256(key.encode()).hexdigest()[:16]


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print("[]")
        return

    try:
        findings = json.loads(raw)
        if not isinstance(findings, list):
            print(json.dumps({"error": "Expected JSON array of findings"}),
                  file=sys.stderr)
            sys.exit(1)

        for finding in findings:
            finding["id"] = generate_id(finding)

        print(json.dumps(findings, indent=2))

    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {e}"}),
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
