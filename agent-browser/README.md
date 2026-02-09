# agent-browser Plugin

Claude Code plugin for browser automation using [agent-browser](https://github.com/vercel-labs/agent-browser).

## Features

- AI-first browser automation with accessibility tree snapshots
- Chrome 144+ のリモートデバッグ機能で普段使いの Chrome にそのまま CDP 接続
- 専用プロファイルや Chrome の再起動が不要
- 50+ commands for navigation, forms, screenshots, network, storage

## Prerequisites

- [agent-browser](https://github.com/vercel-labs/agent-browser) v0.9.0+
- Chrome 144+ with remote debugging enabled via `chrome://inspect/#remote-debugging`

## Quick Start

1. Chrome で `chrome://inspect/#remote-debugging` を開いてリモートデバッグを有効化

2. Use agent-browser:
   ```bash
   ab open https://example.com
   ab snapshot -i -c
   ```

## Files

- `skills/agent-browser/SKILL.md` - Main skill with command reference
- `skills/agent-browser/SETUP.md` - Installation and setup guide

## Setup

See `skills/agent-browser/SETUP.md` for detailed setup instructions.
