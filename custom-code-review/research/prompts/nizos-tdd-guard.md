# Nizos: TDD Guard

**Source:** https://github.com/nizos/tdd-guard
**Stars:** 1747
**Type:** Hooks + CLI Tool

## Overview

Automated Test-Driven Development enforcement for Claude Code. Blocks implementation without failing tests and prevents over-implementation.

## Features

- **Test-First Enforcement** - Blocks implementation without failing tests
- **Minimal Implementation** - Prevents code beyond current test requirements
- **Lint Integration** - Enforces refactoring using linting rules
- **Multi-Language Support** - TypeScript, JavaScript, Python, PHP, Go, Rust, Storybook
- **Customizable Rules** - Adjust validation rules to match TDD style
- **Flexible Validation** - Choose faster or more capable models
- **Session Control** - Toggle on/off mid-session

## Supported Test Frameworks

### JavaScript/TypeScript
- Vitest (via tdd-guard-vitest reporter)
- Jest (via tdd-guard-jest reporter)
- Storybook (via tdd-guard-storybook reporter)

### Python
- pytest (via tdd-guard-pytest reporter)

### PHP
- PHPUnit (via tdd-guard/phpunit reporter)

### Go
- go test (via tdd-guard-go reporter)

### Rust
- cargo test / cargo nextest (via tdd-guard-rust reporter)

## Architecture

### Test Reporters
Language-specific reporters capture test results and save to `.claude/tdd-guard/data/test.json`

### Claude Code Hooks
Three hooks validate operations:

1. **PreToolUse Hook** (Write|Edit|MultiEdit|TodoWrite)
   - Validates file modifications
   - Blocks if tests not failing or over-implementing

2. **UserPromptSubmit Hook**
   - Provides quick toggle commands
   - Handles session commands

3. **SessionStart Hook** (startup|resume|clear)
   - Automatic session management
   - Initializes TDD Guard state

## TDD Enforcement Rules

1. **Red Phase** - Must have failing test before implementation
2. **Green Phase** - Only implement enough to make test pass
3. **Refactor Phase** - Must pass linting rules

## Configuration

### Custom Instructions
Customize TDD validation rules in configuration

### Lint Integration
Automated refactoring support using linting tools

### Strengthening Enforcement
Prevent agents from bypassing validation

### Ignore Patterns
Control which files are validated

### Validation Model
Choose between faster or more capable model for validation

## Workflow

```
User writes test → Test fails (Red) → Agent writes minimal code → Test passes (Green) → Refactor with linting
```

If agent tries to:
- Write code without failing test → BLOCKED
- Implement more than needed → BLOCKED
- Skip refactoring → BLOCKED (if lint failures)

## Security Notice

Hooks execute with user permissions. TDD Guard follows security best practices:
- Automated security scanning
- Dependency audits
- Test-driven development

## Roadmap

- Support more testing frameworks (Mocha, unittest)
- Support more languages (Ruby, Java, C#)
- Validate MCP and shell command modifications
- OpenCode integration
- Encourage meaningful refactoring when tests green
- Multiple concurrent sessions per project

## Review Aspects

- Test-first discipline
- Minimal implementation
- Refactoring enforcement
- Multi-language support
- Session management
