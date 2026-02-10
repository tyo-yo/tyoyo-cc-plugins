# Bartolli: Claude Code TypeScript Hooks

**Source:** https://github.com/bartolli/claude-code-typescript-hooks
**Stars:** 167
**Type:** Hooks

## Overview

Quality check hooks for Claude Code that validate and auto-fix TypeScript, ESLint, and Prettier issues on file edits.

## Hook System

- Triggered after Write/Edit/MultiEdit operations
- Project-specific implementations (react-app, vscode-extension, node-typescript)
- Exit code 0 = success (silent)
- Exit code 2 = quality issues (blocking)

## Core Components

### 1. settings.local.json
Configures which hooks run and when

### 2. quality-check.js
Main validation logic for each project type

### 3. hook-config.json
Defines rules, severity levels, allowed patterns

### 4. tsconfig-cache.json
Auto-generated cache mapping project paths to TypeScript configs

## Quality Checks Performed

1. **TypeScript compilation** (using project's tsconfig.json)
2. **ESLint** with auto-fix capability
3. **Prettier** formatting with auto-fix
4. **Custom rules**:
   - Console usage detection
   - 'as any' usage
   - Debugger statements
   - TODO comments

## Configuration

Edit `hook-config.json` to:
- Change rule severity (info/warning/error)
- Add allowed patterns for specific rules
- Adjust TypeScript/ESLint/Prettier behavior

## Cache Management

Uses SHA256 checksums to detect TypeScript config changes. Cache invalidated when:
- tsconfig.json files modified
- New TypeScript projects added
- Cache files deleted

## Writing Style Guidelines

From CLAUDE.md:

**Banned:**
- Emojis
- Marketing language or praise
- "Thank you" pleasantries
- Explanatory preambles
- Non-informative adjectives

**Banned words:**
- powerful, seamless, comprehensive, robust, elegant
- enhanced, amazing, great, awesome, wonderful, excellent
- sophisticated, advanced, intuitive, user-friendly
- cutting-edge, state-of-the-art, innovative, revolutionary

**Write:**
- Facts only
- Direct statements
- Concrete specifics
- Technical accuracy

## Review Aspects

- TypeScript type safety
- ESLint compliance
- Prettier formatting
- Custom rule violations
- Real-time feedback on file edits
