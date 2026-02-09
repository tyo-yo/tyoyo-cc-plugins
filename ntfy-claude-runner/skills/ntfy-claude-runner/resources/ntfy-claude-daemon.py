#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "textual>=1.0",
#   "httpx",
#   "sh>=2.0",
# ]
# ///
"""ntfy.sh → Claude Code TUI dashboard.

Usage:
    uv run ntfy-claude-daemon.py                          # default topic
    NTFY_TOPIC=my-secret-topic uv run ntfy-claude-daemon.py

Message format (plain text → interactive):
    curl -d "Fix the auth bug" ntfy.sh/my-claude-tasks

Message format (JSON → auto/interactive):
    curl -d '{"type":"auto","prompt":"Summarize README.md"}' ntfy.sh/my-claude-tasks
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

import httpx
import sh
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    Markdown,
    Static,
)

# ── Config ───────────────────────────────────────────────────────────────────

NTFY_SERVER = os.environ.get("NTFY_SERVER", "https://ntfy.sh")
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "my-claude-tasks")
ZELLIJ_SESSION = os.environ.get("ZELLIJ_SESSION", "main")
CLAUDE_TIMEOUT = int(os.environ.get("CLAUDE_TIMEOUT", "600"))  # 10 min
CLAUDE_SKIP_PERMISSIONS = os.environ.get("CLAUDE_SKIP_PERMISSIONS", "").lower() in (
    "1", "true", "yes"
)
CLAUDE_ALLOWED_TOOLS = os.environ.get(
    "CLAUDE_ALLOWED_TOOLS",
    "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch",
)

DATA_DIR = Path.home() / ".local/share/ntfy-claude"
STATE_FILE = DATA_DIR / "last-timestamp"
JOBS_FILE = DATA_DIR / "jobs.jsonl"


# ── Data Model ───────────────────────────────────────────────────────────────


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Job:
    id: str
    time: int
    prompt: str
    type: str  # "auto" | "interactive"
    status: JobStatus = JobStatus.PENDING
    result: str | None = None
    cost_usd: float | None = None
    duration_ms: int | None = None
    error: str | None = None
    steps: list[dict] | None = None  # [{"type": "text"|"tool_use", "content": "..."}]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> Job:
        d = dict(d)
        d["status"] = JobStatus(d["status"])
        # Drop unknown keys for forward compat
        from dataclasses import fields as _fields
        known = {f.name for f in _fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in known})


# ── Job Store (JSONL) ────────────────────────────────────────────────────────


class JobStore:
    def __init__(self, path: Path = JOBS_FILE):
        self._path = path
        self._jobs: dict[str, Job] = {}
        self._load()

    def _load(self):
        if not self._path.exists():
            return
        for line in self._path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                job = Job.from_dict(json.loads(line))
                self._jobs[job.id] = job
            except (json.JSONDecodeError, TypeError, KeyError):
                continue

    def _save(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        lines = [json.dumps(j.to_dict(), ensure_ascii=False) for j in self._jobs.values()]
        self._path.write_text("\n".join(lines) + "\n" if lines else "")

    def add(self, job: Job):
        self._jobs[job.id] = job
        self._save()

    def update(self, job: Job):
        self._jobs[job.id] = job
        self._save()

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def all_auto(self) -> list[Job]:
        """Return auto jobs sorted by time descending."""
        return sorted(
            (j for j in self._jobs.values() if j.type == "auto"),
            key=lambda j: j.time,
            reverse=True,
        )

    def all_jobs(self) -> list[Job]:
        """Return all jobs sorted by time descending."""
        return sorted(
            self._jobs.values(),
            key=lambda j: j.time,
            reverse=True,
        )


# ── Since-timestamp persistence ──────────────────────────────────────────────


def load_since() -> str:
    try:
        return STATE_FILE.read_text().strip()
    except FileNotFoundError:
        return "all"


def save_since(ts: int):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(str(ts))


# ── stream-json parser ───────────────────────────────────────────────────────


def _format_tool_args(input_data: dict) -> str:
    """Format tool input as compact key=value pairs."""
    parts = []
    for k, v in input_data.items():
        if isinstance(v, str):
            v_disp = v if len(v) <= 50 else v[:47] + "..."
            parts.append(f'{k}="{v_disp}"')
        else:
            v_str = json.dumps(v, ensure_ascii=False)
            if len(v_str) > 50:
                v_str = v_str[:47] + "..."
            parts.append(f"{k}={v_str}")
    return ", ".join(parts)


def parse_stream_json(stdout: str) -> tuple[list[dict], dict | None]:
    """Parse claude --output-format stream-json output.

    Returns (steps, result_event_or_none).
    Each step: {"type": "text"|"tool_use", "content": "..."}.
    """
    steps: list[dict] = []
    result_event: dict | None = None

    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        etype = event.get("type")

        if etype == "assistant":
            for block in event.get("message", {}).get("content", []):
                btype = block.get("type")
                if btype == "text":
                    text = block.get("text", "")
                    if text.strip():
                        steps.append({"type": "text", "content": text})
                elif btype == "tool_use":
                    name = block.get("name", "?")
                    args = _format_tool_args(block.get("input", {}))
                    summary = f"{name}({args})"
                    if len(summary) > 200:
                        summary = summary[:197] + "..."
                    steps.append({"type": "tool_use", "content": summary})

        elif etype == "result":
            result_event = event

    return steps, result_event


# ── Widgets ──────────────────────────────────────────────────────────────────

STATUS_ICONS = {
    JobStatus.PENDING: "⏳",
    JobStatus.RUNNING: ">>",
    JobStatus.COMPLETED: "OK",
    JobStatus.FAILED: "ERR",
}


class ConnectionStatus(Static):
    def update_status(self, connected: bool, job_count: int, running_count: int):
        conn = "Connected" if connected else "Disconnected"
        self.update(f" {conn} | Jobs: {job_count} | Running: {running_count} ")


class JobListItem(ListItem):
    """A single row in the job list."""

    def __init__(self, job: Job, **kwargs):
        super().__init__(**kwargs)
        self.job = job

    def compose(self) -> ComposeResult:
        icon = STATUS_ICONS.get(self.job.status, "??")
        ts = datetime.fromtimestamp(self.job.time).strftime("%m/%d %H:%M")
        prompt_text = self.job.prompt[:60]

        # interactive jobs are displayed muted
        if self.job.type == "interactive":
            yield Label(f" [dim]INT  {prompt_text}  {ts}[/]")
        elif self.job.status == JobStatus.FAILED:
            yield Label(f" [bold red]{icon}[/]  {prompt_text}  [dim]{ts}[/]")
        elif self.job.status == JobStatus.RUNNING:
            yield Label(f" [bold yellow]{icon}[/]  {prompt_text}  [dim]{ts}[/]")
        elif self.job.status == JobStatus.COMPLETED:
            yield Label(f" [bold green]{icon}[/]  {prompt_text}  [dim]{ts}[/]")
        else:
            yield Label(f" [dim]{icon}[/]  {prompt_text}  [dim]{ts}[/]")


# ── Detail Screen ────────────────────────────────────────────────────────────


class JobDetailScreen(Screen):
    BINDINGS = [
        Binding("escape", "pop_screen", "Back"),
        Binding("q", "pop_screen", "Back"),
    ]

    CSS = """
    JobDetailScreen {
        layout: vertical;
    }
    #detail-prompt {
        height: 3;
        padding: 1;
        background: $surface;
    }
    #detail-content {
        height: 1fr;
        padding: 1;
    }
    .step-tool-use {
        color: $text-muted;
        padding: 0 1;
    }
    #detail-meta {
        height: 3;
        padding: 1;
        background: $surface;
        color: $text-muted;
    }
    """

    def __init__(self, job: Job, **kwargs):
        super().__init__(**kwargs)
        self.job = job

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Label(f" Prompt: {self.job.prompt}", id="detail-prompt")
        with VerticalScroll(id="detail-content"):
            if self.job.steps:
                for step in self.job.steps:
                    if step["type"] == "text":
                        yield Markdown(step["content"])
                    elif step["type"] == "tool_use":
                        content = step["content"]
                        if len(content) > 120:
                            content = content[:117] + "..."
                        yield Static(
                            f"[dim]🔧 {content}[/]",
                            classes="step-tool-use",
                        )
            elif self.job.result:
                yield Markdown(self.job.result)
            elif self.job.error:
                yield Static(f"[bold red]Error:[/] {self.job.error}")
            elif self.job.status == JobStatus.RUNNING:
                yield Static("[dim]Running...[/]")
            else:
                yield Static("[dim]No output[/]")
        yield self._meta_bar()
        yield Footer()

    def _meta_bar(self) -> Static:
        parts: list[str] = []
        parts.append(self.job.status.value.capitalize())
        if self.job.duration_ms is not None:
            secs = self.job.duration_ms / 1000
            parts.append(f"Duration: {secs:.1f}s")
        if self.job.cost_usd is not None:
            parts.append(f"Cost: ${self.job.cost_usd:.3f}")
        return Static(" | ".join(parts), id="detail-meta")

    def action_pop_screen(self):
        self.app.pop_screen()


# ── Main App ─────────────────────────────────────────────────────────────────


class NtfyClaudeApp(App):
    TITLE = "ntfy-claude"

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh_list", "Refresh"),
    ]

    CSS = """
    #job-list {
        height: 1fr;
    }
    #status-bar {
        height: 3;
        padding: 1;
        background: $surface;
        dock: bottom;
    }
    """

    def __init__(self):
        super().__init__()
        self.store = JobStore()
        self._connected = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield ListView(id="job-list")
        yield ConnectionStatus(id="status-bar")
        yield Footer()

    def on_mount(self):
        self._refresh_job_list()
        self._update_status_bar()
        self.start_ntfy_subscriber()

    # ── List management ──────────────────────────────────────────────────

    def _refresh_job_list(self):
        list_view: ListView = self.query_one("#job-list", ListView)
        list_view.clear()
        for job in self.store.all_jobs():
            list_view.append(JobListItem(job))

    def _update_status_bar(self):
        bar: ConnectionStatus = self.query_one("#status-bar", ConnectionStatus)
        jobs = self.store.all_auto()
        running = sum(1 for j in jobs if j.status == JobStatus.RUNNING)
        bar.update_status(self._connected, len(jobs), running)

    def action_refresh_list(self):
        self._refresh_job_list()
        self._update_status_bar()

    def on_list_view_selected(self, event: ListView.Selected):
        item = event.item
        if isinstance(item, JobListItem) and item.job.type == "auto":
            self.push_screen(JobDetailScreen(item.job))

    # ── ntfy subscriber Worker ───────────────────────────────────────────

    @work(thread=True, exclusive=True)
    def start_ntfy_subscriber(self):
        attempt = 0
        while not self.app._exit:
            try:
                self._subscribe_loop()
                attempt = 0
            except (httpx.HTTPError, httpx.StreamError, ConnectionError) as e:
                if self.app._exit:
                    break
                self.call_from_thread(self._set_disconnected)
                delay = min(2**attempt, 60)
                self.log.warning(f"Connection lost: {e}. Retry in {delay}s...")
                time.sleep(delay)
                attempt += 1

    def _subscribe_loop(self):
        since = load_since()
        url = f"{NTFY_SERVER}/{NTFY_TOPIC}/json"

        with httpx.stream("GET", url, params={"since": since}, timeout=None) as resp:
            resp.raise_for_status()
            self.call_from_thread(self._set_connected)

            for line in resp.iter_lines():
                if self.app._exit:
                    return
                if not line.strip():
                    continue

                msg = json.loads(line)

                if ts := msg.get("time"):
                    save_since(ts)

                if msg.get("event") == "message":
                    try:
                        self.call_from_thread(self._dispatch, msg)
                    except Exception as e:
                        self.log.error(f"Dispatch failed: {e}")

    def _set_connected(self):
        self._connected = True
        self._update_status_bar()

    def _set_disconnected(self):
        self._connected = False
        self._update_status_bar()

    # ── Dispatch ─────────────────────────────────────────────────────────

    def _dispatch(self, msg: dict):
        body = msg.get("message", "")
        msg_id = msg.get("id", str(msg.get("time", "")))
        msg_time = msg.get("time", int(time.time()))

        # Skip if already processed (dedup on restart)
        if self.store.get(msg_id):
            return

        try:
            payload = json.loads(body)
            task_type = payload.get("type", "interactive")
            prompt = payload.get("prompt", body)
        except (json.JSONDecodeError, TypeError):
            task_type = "interactive"
            prompt = body

        if not prompt:
            return

        job = Job(
            id=msg_id,
            time=msg_time,
            prompt=prompt,
            type=task_type,
        )

        if task_type == "auto":
            job.status = JobStatus.PENDING
            self.store.add(job)
            self._refresh_job_list()
            self._update_status_bar()
            self.run_claude_auto(job)
        else:
            # Save interactive job for history (but don't track status)
            job.status = JobStatus.COMPLETED  # Mark as "sent to Zellij"
            self.store.add(job)
            self._refresh_job_list()
            self._update_status_bar()
            self._run_interactive(job)

    # ── Interactive task (Zellij pane) ───────────────────────────────────

    def _run_interactive(self, job: Job):
        label = job.prompt[:20]
        try:
            zellij = sh.zellij.bake("--session", ZELLIJ_SESSION)
            zellij.run(
                "--close-on-exit",
                "--name", f"task:{label}",
                "--", "claude", job.prompt,
            )
        except Exception as e:
            self.log.error(f"Interactive dispatch failed: {e}")

    # ── Auto task Worker ─────────────────────────────────────────────────

    @work(thread=True, group="claude")
    def run_claude_auto(self, job: Job):
        job.status = JobStatus.RUNNING
        self.call_from_thread(self._on_job_updated, job)

        try:
            # Build command with permission settings
            cmd = [
                "claude", "-p", job.prompt,
                "--output-format", "stream-json",
                "--verbose",
                "--max-turns", "10",
            ]
            if CLAUDE_SKIP_PERMISSIONS:
                # Full auto mode (use in isolated environments only)
                cmd.append("--dangerously-skip-permissions")
            else:
                # Safe auto mode: allow edits + specific tools
                cmd.extend(["--permission-mode", "acceptEdits"])
                cmd.extend(["--allowedTools", CLAUDE_ALLOWED_TOOLS])

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=CLAUDE_TIMEOUT,
            )

            steps, result_event = parse_stream_json(proc.stdout)
            job.steps = steps if steps else None

            if result_event:
                job.result = result_event.get("result")
                job.cost_usd = result_event.get("total_cost_usd")
                job.duration_ms = result_event.get("duration_ms")
                if result_event.get("is_error"):
                    job.error = result_event.get("result", "Unknown error")
                    job.status = JobStatus.FAILED
                else:
                    job.status = JobStatus.COMPLETED
            elif proc.returncode == 0:
                job.result = proc.stdout
                job.status = JobStatus.COMPLETED
            else:
                job.error = proc.stderr or f"Exit code {proc.returncode}"
                job.status = JobStatus.FAILED

        except subprocess.TimeoutExpired:
            job.error = f"Timeout after {CLAUDE_TIMEOUT}s"
            job.status = JobStatus.FAILED
        except FileNotFoundError:
            job.error = "claude command not found"
            job.status = JobStatus.FAILED
        except Exception as e:
            job.error = str(e)
            job.status = JobStatus.FAILED

        self.call_from_thread(self._on_job_updated, job)

    def _on_job_updated(self, job: Job):
        self.store.update(job)
        self._refresh_job_list()
        self._update_status_bar()


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = NtfyClaudeApp()
    app.run()
