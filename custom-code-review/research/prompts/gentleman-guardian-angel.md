# Gentleman Guardian Angel (gga)

**Source:** https://github.com/Gentleman-Programming/gentleman-guardian-angel
**Stars:** 560
**Type:** Git Hook + CLI Tool

## Overview

Provider-agnostic code review using AI. Runs on every commit, validating staged files against project's coding standards file (AGENTS.md or custom).

## Key Features

- **Provider agnostic** - Works with Claude, Gemini, Codex, OpenCode, Ollama, or any AI CLI
- **Zero dependencies** - Pure Bash, no Node/Python/Go required
- **Git native** - Standard pre-commit hook
- **Highly configurable** - File patterns, exclusions, custom rules
- **Strict mode** - Fail CI on ambiguous responses
- **Smart caching** - Skip unchanged files for faster reviews
- **Homebrew ready** - One command install

## Supported AI Providers

| Provider | Config Value | CLI Command |
|----------|--------------|-------------|
| Claude | `claude` | `echo "prompt" \| claude --print` |
| Gemini | `gemini` | `echo "prompt" \| gemini` |
| Codex | `codex` | `codex exec "prompt"` |
| OpenCode | `opencode` | `echo "prompt" \| opencode run` |
| Ollama | `ollama:<model>` | `ollama run <model> "prompt"` |

## Configuration (.gga)

```bash
# AI Provider (required)
PROVIDER="claude"

# File patterns to review (comma-separated globs)
FILE_PATTERNS="*.ts,*.tsx,*.js,*.jsx"

# Patterns to exclude
EXCLUDE_PATTERNS="*.test.ts,*.spec.ts,*.d.ts"

# File containing coding standards
RULES_FILE="AGENTS.md"

# Fail if AI response is ambiguous (recommended for CI)
STRICT_MODE="true"
```

## Rules File Best Practices (AGENTS.md)

### 1. Keep it Concise (~100-200 lines)
Large files dilute AI focus. Focused file = better reviews.

### 2. Use Clear Action Keywords

| Keyword | Meaning | AI Action |
|---------|---------|-----------|
| `REJECT if` | Hard rule, must fail | Returns `STATUS: FAILED` |
| `REQUIRE` | Mandatory pattern | Returns `STATUS: FAILED` if missing |
| `PREFER` | Soft recommendation | May note but won't fail |

### 3. Use References for Complex Projects

```markdown
## References

- UI guidelines: `ui/AGENTS.md`
- API guidelines: `api/AGENTS.md`
- Shared rules: `docs/CODE-STYLE.md`
```

Claude, Gemini, and Codex have built-in tools to read referenced files.

**Note:** Ollama is pure LLM without file-reading tools. Need to consolidate manually.

### 4. Structure for Scanning

Use bullet points, not paragraphs. AI scans faster.

```markdown
## TypeScript/React

REJECT if:
- `import * as React` → use `import { useState }`
- Union types `type X = "a" | "b"` → use `const X = {...} as const`
- `any` type without `// @ts-expect-error` justification

PREFER:
- Named exports over default exports
- Composition over inheritance
```

### 5. Response Format Specification

```markdown
## Response Format

FIRST LINE must be exactly:
STATUS: PASSED
or
STATUS: FAILED

If FAILED, list: `file:line - rule violated - issue`
```

## Smart Caching System

### How It Works

```
1. Hash AGENTS.md + .gga config
   └─► If changed → Invalidate ALL cache

2. For each staged file:
   └─► Hash file content
       └─► If hash exists in cache with PASSED → Skip
       └─► If not cached → Send to AI for review

3. After PASSED review:
   └─► Store file hash in cache
```

### Cache Invalidation

| Change | Effect |
|--------|--------|
| File content changes | Only that file re-reviewed |
| AGENTS.md changes | **All files** re-reviewed |
| .gga config changes | **All files** re-reviewed |

### Cache Commands

```bash
gga cache status       # Check cache status
gga cache clear        # Clear project cache
gga cache clear-all    # Clear all cache (all projects)
gga run --no-cache     # Bypass cache
```

## Commands

```bash
gga init                      # Create sample .gga config
gga install                   # Install pre-commit hook
gga install --commit-msg      # Install commit-msg hook (validates commit message)
gga uninstall                 # Remove hooks
gga run                       # Run review on staged files
gga run --ci                  # Run review on last commit (for CI/CD)
gga run --no-cache            # Force review all files
gga config                    # Display configuration
gga cache status              # Show cache status
gga cache clear               # Clear project cache
gga cache clear-all           # Clear all cache
gga help                      # Show help
gga version                   # Show version
```

## Workflow

```
git commit
    │
    ▼
┌───────────────────┐
│  Pre-commit Hook  │
└───────────────────┘
    │
    ├──▶ 1. Load config from .gga
    ├──▶ 2. Validate provider installed
    ├──▶ 3. Check AGENTS.md exists
    ├──▶ 4. Get staged files matching FILE_PATTERNS
    ├──▶ 5. Read coding rules from AGENTS.md
    ├──▶ 6. Build prompt: rules + file contents
    ├──▶ 7. Send to AI provider
    └──▶ 8. Parse response
            │
            ├── "STATUS: PASSED" ──▶ ✅ Commit proceeds
            └── "STATUS: FAILED" ──▶ ❌ Commit blocked
```

## Integration Examples

### Husky (Node.js)

```bash
# .husky/pre-commit
#!/usr/bin/env bash
gga run || exit 1
```

### pre-commit (Python)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: gga
        name: Gentleman Guardian Angel
        entry: gga run
        language: system
        pass_filenames: false
        stages: [pre-commit]
```

### Lefthook (Go)

```yaml
# lefthook.yml
pre-commit:
  commands:
    ai-review:
      run: gga run
```

### GitHub Actions

```yaml
# .github/workflows/ai-review.yml
- name: Run AI Review
  run: |
    git diff --name-only origin/${{ github.base_ref }}...HEAD | xargs git add
    gga run
```

## Bypass Review

```bash
# Skip pre-commit hook
git commit --no-verify -m "wip: work in progress"

# Short form
git commit -n -m "hotfix: urgent fix"
```

## Test Suite

**Total: 161 tests**

| Module | Tests | Coverage |
|--------|-------|----------|
| cache.sh | 27 | Hash functions, cache validation |
| providers.sh | 49 | All providers, routing, security |
| CLI commands | 34 | init, install, run, config |
| Ollama integration | 12 | Real Ollama tests |
| OpenCode | 8 | OpenCode provider tests |
| STATUS parsing | 14 | Edge cases, preamble handling |

## Changelog Highlights

### v2.6.1 (Latest)
- Relaxed STATUS parsing (handles AI preamble text)
- Accepts markdown formatting
- 161 tests total

### v2.6.0
- Commit message validation support
- Read from staging area (fixes race conditions)
- Signal handling for cleanup
- 147 tests

### v2.5.0
- OpenCode provider support
- 130 tests

### v2.4.0
- CI mode (`--ci` flag)
- 118 tests

### v2.3.0
- Fixed Ollama ANSI escape codes
- Worktree support
- 104 tests

### v2.1.0
- Smart caching system
- Auto-invalidation

## Review Aspects

- Provider-agnostic AI integration
- Git-native workflow
- Smart caching
- Configurable rules
- Pre-commit enforcement
- Commit message validation
- Pure Bash implementation
- Comprehensive test coverage
