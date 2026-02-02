#!/usr/bin/env python3
"""Send a notification via the Telegram Bot API.

Reads message text from stdin.
Sends directly to Telegram using the Bot API (no gateway needed).

Requires environment variables:
  TELEGRAM_BOT_TOKEN  - Bot token from @BotFather
  TELEGRAM_CHAT_ID    - Target chat/user ID

Output: JSON with status and any error details.
"""
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def _load_env():
    """Load .env file from project root (walk up from script location)."""
    # Try cwd first, then walk up from script dir
    for start in [Path.cwd(), Path(__file__).resolve().parent]:
        d = start
        for _ in range(10):
            env_file = d / ".env"
            if env_file.exists():
                for line in env_file.read_text().splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        key = key.strip()
                        value = value.strip()
                        if key and key not in os.environ:
                            os.environ[key] = value
                return
            if d.parent == d:
                break
            d = d.parent


def main():
    _load_env()
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    message = sys.stdin.read().strip()
    if not message:
        print(json.dumps({
            "status": "skipped",
            "reason": "empty message"
        }))
        return

    if not token or not chat_id:
        print(json.dumps({
            "status": "skipped",
            "reason": "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set"
        }))
        return

    # Telegram max message length is 4096 chars
    if len(message) > 4096:
        message = message[:4090] + "\n[...]"

    payload = json.dumps({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }).encode()

    url = TELEGRAM_API.format(token=token)
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            print(json.dumps({
                "status": "ok",
                "http_status": resp.status,
                "message_id": result.get("result", {}).get("message_id"),
            }))
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200] if hasattr(e, 'read') else str(e)
        print(json.dumps({
            "status": "error",
            "error": f"HTTP {e.code}: {body}",
            "message": "Telegram delivery failed. Report still archived."
        }))
    except urllib.error.URLError as e:
        print(json.dumps({
            "status": "error",
            "error": str(e),
            "message": "Telegram delivery failed. Report still archived."
        }))
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": str(e),
            "message": "Unexpected error sending Telegram notification."
        }))


if __name__ == "__main__":
    main()
