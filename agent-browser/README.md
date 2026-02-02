# agent-browser Plugin

Claude Code plugin for browser automation using [agent-browser](https://github.com/vercel-labs/agent-browser).

## Features

- AI-first browser automation with accessibility tree snapshots
- CDP mode for connecting to existing Chrome sessions (with authentication)
- 50+ commands for navigation, forms, screenshots, network, storage

## Prerequisites

- [agent-browser](https://github.com/vercel-labs/agent-browser) installed
- Chrome with CDP enabled (via `chrome-debug` command)

## Quick Start

1. Start Chrome in CDP mode (separate terminal):
   ```bash
   chrome-debug
   ```

2. Use agent-browser:
   ```bash
   agent-browser --cdp 9222 open https://example.com
   agent-browser --cdp 9222 snapshot -i -c
   ```

## Files

- `skills/agent-browser/SKILL.md` - Main skill with command reference
- `skills/agent-browser/SETUP.md` - Installation and setup guide

## Setup

See `skills/agent-browser/SETUP.md` for detailed setup instructions.
