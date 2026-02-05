#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
#   "sh>=2.0",
# ]
# ///
"""ntfy.sh → Zellij → Claude Code daemon.

Usage:
    uv run ntfy-claude-daemon.py                          # default topic
    NTFY_TOPIC=my-secret-topic uv run ntfy-claude-daemon.py

Message format (plain text → interactive):
    curl -d "Fix the auth bug" ntfy.sh/my-claude-tasks

Message format (JSON → auto/interactive):
    curl -d '{"type":"auto","prompt":"Summarize README.md"}' ntfy.sh/my-claude-tasks
"""

import json
import logging
import os
import signal
import sys
import time
from pathlib import Path

import httpx
import sh

# ── Config (env vars with defaults) ──────────────────────────────────────────

NTFY_SERVER = os.environ.get("NTFY_SERVER", "https://ntfy.sh")
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "my-claude-tasks")
ZELLIJ_SESSION = os.environ.get("ZELLIJ_SESSION", "main")
STATE_FILE = Path.home() / ".local/share/ntfy-claude/last-timestamp"

log = logging.getLogger("ntfy-claude")

# ── Graceful shutdown ─────────────────────────────────────────────────────────

running = True


def _shutdown(sig, _frame):
    global running
    log.info("Received %s, shutting down...", signal.Signals(sig).name)
    running = False


signal.signal(signal.SIGTERM, _shutdown)
signal.signal(signal.SIGINT, _shutdown)

# ── Since-timestamp persistence (for catch-up after disconnect) ───────────────


def load_since() -> str:
    try:
        return STATE_FILE.read_text().strip()
    except FileNotFoundError:
        return "all"


def save_since(ts: int):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(str(ts))


# ── Task dispatch ─────────────────────────────────────────────────────────────


def dispatch(msg: dict):
    """Parse ntfy message and spawn a Zellij pane with Claude Code."""
    body = msg.get("message", "")

    # Try JSON payload, fall back to plain text
    try:
        payload = json.loads(body)
        task_type = payload.get("type", "interactive")
        prompt = payload.get("prompt", body)
    except (json.JSONDecodeError, TypeError):
        task_type = "interactive"
        prompt = body

    if not prompt:
        log.warning("Empty prompt, skipping")
        return

    label = msg.get("title", prompt[:30])
    log.info("[%s] %s", task_type, label)

    zellij = sh.zellij.bake("--session", ZELLIJ_SESSION)

    if task_type == "auto":
        zellij.run(
            "--name", f"auto:{label[:20]}",
            "--", "claude", "-p", prompt,
            "--output-format", "json", "--max-turns", "10",
        )
    else:
        zellij.run(
            "--name", f"task:{label[:20]}",
            "--", "claude", prompt,
        )


# ── ntfy stream consumer ─────────────────────────────────────────────────────


def subscribe():
    """Connect to ntfy JSON stream and dispatch messages."""
    since = load_since()
    url = f"{NTFY_SERVER}/{NTFY_TOPIC}/json"

    log.info("Connecting to %s (since=%s)", url, since)

    with httpx.stream("GET", url, params={"since": since}, timeout=None) as resp:
        resp.raise_for_status()
        log.info("Connected")

        for line in resp.iter_lines():
            if not running:
                break
            if not line.strip():
                continue

            msg = json.loads(line)

            if ts := msg.get("time"):
                save_since(ts)

            if msg.get("event") == "message":
                try:
                    dispatch(msg)
                except Exception:
                    log.exception("Dispatch failed")


# ── Main ──────────────────────────────────────────────────────────────────────


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        stream=sys.stderr,
    )
    log.info("Topic: %s | Session: %s", NTFY_TOPIC, ZELLIJ_SESSION)

    attempt = 0
    while running:
        try:
            subscribe()
            attempt = 0
        except (httpx.HTTPError, httpx.StreamError, ConnectionError) as e:
            if not running:
                break
            delay = min(2**attempt, 60)
            log.warning("Connection lost: %s. Retry in %ds...", e, delay)
            time.sleep(delay)
            attempt += 1

    log.info("Stopped")


if __name__ == "__main__":
    main()
