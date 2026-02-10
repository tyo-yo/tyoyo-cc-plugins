# New Code Review Repositories Research Summary

**Date:** 2026-02-10
**Research Focus:** Code review prompts, commands, agents, and methodologies

## Repository Overview

| Repository | Stars | Type | Key Focus |
|------------|-------|------|-----------|
| [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | 4,310 | System Prompts | PR review, security review |
| [trailofbits/skills](https://github.com/trailofbits/skills) | 2,498 | Skills | Security-focused differential review |
| [obra/superpowers](https://github.com/obra/superpowers) | 48,935 | Skills + Agents | Code reviewer agent, review workflow |
| [Gentleman-Programming/gentleman-guardian-angel](https://github.com/Gentleman-Programming/gentleman-guardian-angel) | 560 | Git Hook + CLI | Pre-commit AI review tool |
| [nizos/tdd-guard](https://github.com/nizos/tdd-guard) | 1,747 | Hooks + CLI | TDD enforcement |
| [bartolli/claude-code-typescript-hooks](https://github.com/bartolli/claude-code-typescript-hooks) | 167 | Hooks | TypeScript quality checks |
| [Veraticus/cc-tools](https://github.com/Veraticus/cc-tools) | 46 | Go Tool | Claude Code utilities |

## 1. Piebald-AI: Claude Code System Prompts

**Stars:** 4,310

### Key Features
- Complete collection of Claude Code system prompts
- 18 builtin tool descriptions
- Sub-agent prompts (Plan/Explore/Task)
- Utility prompts

### Code Review Components

#### /review-pr Command
- Simple PR review workflow
- Uses `gh` CLI for PR details
- Focuses on:
  - Code correctness
  - Project conventions
  - Performance implications
  - Test coverage
  - Security considerations

#### /security-review Command
- Comprehensive security-focused review
- **Two-phase workflow:**
  1. Initial vulnerability detection (sub-task)
  2. Parallel false positive filtering (per-finding sub-tasks)
- **High confidence threshold:** Only reports findings ≥8/10 confidence
- **17+ hard exclusions** to minimize false positives
- **Security categories:**
  - Input validation (SQL, command, XXE, template, NoSQL, path traversal)
  - Authentication & authorization
  - Crypto & secrets management
  - Injection & code execution
  - Data exposure

### Review Aspects Extracted

**General Code Review:**
- Code correctness
- Project conventions
- Performance implications
- Test coverage
- Security considerations

**Security Review:**
- Exploitable vulnerabilities only
- Concrete attack paths
- High-confidence findings
- No theoretical issues
- Evidence-based reporting

### Unique Methodology
- **Sub-task parallelization** for efficient validation
- **False positive filtering** with 17+ exclusion patterns
- **Precedent-based evaluation** (e.g., React/Angular XSS safety, environment variables as trusted)

---

## 2. Trail of Bits: Security Skills

**Stars:** 2,498

### Key Features
- Security research and vulnerability detection focus
- Multiple specialized plugins (25+ plugins)
- Audit workflow skills
- Domain-specific patterns

### Code Review Components

#### differential-review Skill
**Most comprehensive security-focused review methodology found**

**Core Principles:**
1. Risk-First (auth, crypto, value transfer, external calls)
2. Evidence-Based (git history, line numbers, attack scenarios)
3. Adaptive (scales to codebase size)
4. Honest (explicit coverage limits)
5. Output-Driven (always generates markdown report)

**Codebase Size Strategy:**
| Size | Strategy | Approach |
|------|----------|----------|
| SMALL (<20 files) | DEEP | Read all deps, full git blame |
| MEDIUM (20-200) | FOCUSED | 1-hop deps, priority files |
| LARGE (200+) | SURGICAL | Critical paths only |

**Six-Phase Workflow:**

**Pre-Analysis:** Baseline Context Building
- Uses `audit-context-building` skill if available
- System-wide invariants
- Trust boundaries
- Validation patterns
- Call graphs
- State flows

**Phase 0:** Intake & Triage
- Extract changes
- Assess codebase size
- Risk score each file

**Phase 1:** Changed Code Analysis
- Read both versions
- Git blame removed code
- Check for regressions
- Micro-adversarial analysis
- Generate attack scenarios

**Phase 2:** Test Coverage Analysis
- Identify gaps
- Risk elevation rules (e.g., NEW function + NO tests → HIGH)

**Phase 3:** Blast Radius Analysis
- Calculate caller count
- Priority matrix (risk × blast radius)

**Phase 4:** Deep Context Analysis
- Map function flows
- Trace calls
- Identify invariants
- Five Whys root cause

**Phase 5:** Adversarial Analysis (for HIGH RISK)
- Define specific attacker model
- Identify concrete attack vectors
- Rate exploitability (EASY/MEDIUM/HARD)
- Build complete exploit scenario
- Cross-reference with baseline

**Phase 6:** Report Generation
- Markdown report with findings
- File/line references
- Attack scenarios
- Recommendations

#### fix-review Skill
Verifies git commits address security audit findings without introducing bugs.

**Input Requirements:**
- Source commit (baseline)
- Target commit(s)
- Security report (optional)

**Finding Status:**
- FIXED
- PARTIALLY_FIXED
- NOT_ADDRESSED
- CANNOT_DETERMINE

**Six-Phase Workflow:**
1. Input gathering
2. Report retrieval (local/URL/Google Drive)
3. Finding extraction (TOB-XXX pattern, other formats)
4. Commit analysis
5. Finding verification
6. Output generation

**Bug Detection Patterns:**
- Access control weakening
- Validation removal
- Error handling reduction
- External call reordering
- Integer operation changes
- Cryptographic weakening

#### Common Vulnerability Patterns

**10 Key Patterns:**
1. Security regressions
2. Double decrease/increase bugs
3. Missing validation
4. Underflow/overflow
5. Reentrancy (CEI violations)
6. Access control bypass
7. Race conditions / front-running
8. Timestamp manipulation
9. Unchecked return values
10. Denial of service

**Quick Detection Commands:**
```bash
# Find removed security checks
git diff <range> | grep "^-" | grep -E "require|assert|revert"

# Find new external calls
git diff <range> | grep "^+" | grep -E "\.call|\.delegatecall|\.staticcall"

# Find changed access modifiers
git diff <range> | grep -E "onlyOwner|onlyAdmin|internal|private|public|external"
```

### Review Aspects Extracted

**Differential Review:**
- Risk-first prioritization
- Git history analysis
- Blast radius quantification
- Test coverage gaps
- Invariant violations
- Concrete exploit scenarios
- Adaptive depth based on codebase size
- Evidence-based findings

**Fix Review:**
- Root cause verification
- Bug introduction detection
- Finding-to-commit mapping
- Comprehensive coverage
- Evidence-based status

**Vulnerability Patterns:**
- Security regressions
- Accounting bugs
- Validation removal
- Reentrancy
- Access control
- Race conditions
- Timestamp manipulation

### Unique Methodology

**Rationalizations to Avoid:**
| Rationalization | Why Wrong | Action |
|-----------------|-----------|--------|
| "Small PR, quick review" | Heartbleed was 2 lines | Classify by RISK, not size |
| "I know this codebase" | Familiarity → blind spots | Build explicit baseline |
| "Git history takes long" | History reveals regressions | Never skip |
| "Just a refactor" | Refactors break invariants | Analyze as HIGH until proven LOW |

**Red Flags (Immediate Escalation):**
- Removed code from "security", "CVE", "fix" commits
- Access control modifiers removed
- Validation removed without replacement
- External calls added without checks
- High blast radius (50+) + HIGH risk

---

## 3. Obra: Superpowers

**Stars:** 48,935 (most starred)

### Key Features
- Agentic skills framework
- Software development methodology
- Multiple workflow skills
- Agent-based architecture

### Code Review Components

#### code-reviewer Agent
Senior code reviewer agent for production readiness validation.

**When to Use:**
- After major project step completion
- When need to validate against plan

**Six Responsibilities:**

1. **Plan Alignment Analysis**
   - Compare implementation vs plan
   - Identify deviations
   - Assess justification
   - Verify functionality

2. **Code Quality Assessment**
   - Patterns/conventions
   - Error handling
   - Type safety
   - Maintainability
   - Test coverage
   - Security/performance

3. **Architecture and Design Review**
   - SOLID principles
   - Separation of concerns
   - Integration
   - Scalability

4. **Documentation and Standards**
   - Comments
   - File headers
   - Coding standards

5. **Issue Identification**
   - Critical (must fix)
   - Important (should fix)
   - Suggestions (nice to have)
   - Actionable recommendations

6. **Communication Protocol**
   - Ask coding agent to confirm deviations
   - Recommend plan updates
   - Clear guidance

**Output Structure:**
```
### Strengths
[Specific accomplishments]

### Issues
#### Critical (Must Fix)
[Bugs, security, data loss, broken functionality]

#### Important (Should Fix)
[Architecture, missing features, error handling, test gaps]

#### Minor (Nice to Have)
[Code style, optimization, documentation]

### Recommendations
[Improvements]

### Assessment
Ready to merge? [Yes/No/With fixes]
Reasoning: [1-2 sentences]
```

**Review Checklist:**
- Code Quality (separation, error handling, type safety, DRY, edge cases)
- Architecture (design, scalability, performance, security)
- Testing (real tests, edge cases, integration, passing)
- Requirements (plan met, matches spec, no scope creep, breaking changes)
- Production Readiness (migration, compatibility, documentation, no bugs)

#### requesting-code-review Skill
Workflow for requesting code review.

**Core Principle:** Review early, review often.

**Mandatory Review Points:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but Valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

**Three-Step Process:**
1. Get git SHAs (BASE_SHA, HEAD_SHA)
2. Dispatch code-reviewer subagent with template
3. Act on feedback:
   - Fix Critical immediately
   - Fix Important before proceeding
   - Note Minor for later
   - Push back if wrong (with reasoning)

**Integration with Workflows:**
- Subagent-Driven Development: Review after EACH task
- Executing Plans: Review after each batch (3 tasks)
- Ad-Hoc Development: Review before merge

**Red Flags (Never):**
- Skip because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

#### receiving-code-review Skill
Guidance on receiving feedback with technical rigor.

**Core Principle:** Verify before implementing. Technical correctness over social comfort.

**Response Pattern:**
1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One at a time, test each

**Forbidden Responses:**
- "You're absolutely right!"
- "Great point!"
- "Let me implement that now" (before verification)

**Handling Unclear Feedback:**
```
IF any item unclear:
  STOP - do not implement anything
  ASK for clarification

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Source-Specific Handling:**

**From Partner:**
- Trusted - implement after understanding
- Still ask if unclear
- No performative agreement
- Skip to action

**From External Reviewers:**
- Check: Technically correct?
- Check: Breaks functionality?
- Check: Reviewer understands context?
- If wrong: Push back with technical reasoning
- If can't verify: Say so
- If conflicts with partner: Discuss first

**YAGNI Check:**
```
IF reviewer suggests "implementing properly":
  grep codebase for actual usage
  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

**When to Push Back:**
- Breaks existing functionality
- Reviewer lacks context
- Violates YAGNI
- Technically incorrect
- Legacy/compatibility reasons
- Conflicts with architectural decisions

**Acknowledging Correct Feedback:**
```
✅ "Fixed. [Brief description]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix and show in code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ ANY gratitude expression
```

**Why no thanks:** Actions speak. Code shows you heard feedback.

### Review Aspects Extracted

**Code Reviewer Agent:**
- Plan alignment
- Code quality
- Architecture
- Testing
- Documentation
- Production readiness
- Issue categorization (Critical/Important/Minor)
- Clear verdict (Yes/No/With fixes)

**Receiving Review:**
- Technical rigor
- No performative agreement
- Verification before implementation
- YAGNI checks
- Context-aware pushback
- One-at-a-time implementation
- Action over words

### Unique Methodology

**Review Workflow Integration:**
- Review after EACH task (subagent-driven development)
- Review after batch (executing plans)
- Review before merge (ad-hoc)

**Communication Protocol:**
- No performative language
- Technical acknowledgment only
- Actions > words
- Push back when technically wrong
- Signal if uncomfortable: "Strange things afoot at the Circle K"

**YAGNI Enforcement:**
- Grep codebase for actual usage
- Remove unused features
- Don't implement "properly" if unused

---

## 4. Gentleman Guardian Angel (gga)

**Stars:** 560

### Key Features
- Provider-agnostic AI code review
- Pure Bash implementation
- Git-native pre-commit hook
- Smart caching system
- Zero dependencies

### Code Review Components

#### Pre-commit Hook System
Runs AI code review on every commit.

**Supported AI Providers:**
- Claude (`claude`)
- Gemini (`gemini`)
- Codex (`codex`)
- OpenCode (`opencode` or `opencode:model`)
- Ollama (`ollama:model`)

**Configuration (.gga):**
```bash
PROVIDER="claude"
FILE_PATTERNS="*.ts,*.tsx,*.js,*.jsx"
EXCLUDE_PATTERNS="*.test.ts,*.spec.ts,*.d.ts"
RULES_FILE="AGENTS.md"
STRICT_MODE="true"
```

#### Rules File Best Practices (AGENTS.md)

**Five Key Principles:**

1. **Keep Concise (~100-200 lines)**
   - Large files dilute AI focus
   - Focused file = better reviews

2. **Use Clear Action Keywords**
   | Keyword | Meaning | AI Action |
   |---------|---------|-----------|
   | `REJECT if` | Hard rule | Returns `STATUS: FAILED` |
   | `REQUIRE` | Mandatory | Returns `STATUS: FAILED` if missing |
   | `PREFER` | Soft recommendation | May note but won't fail |

3. **Use References for Complex Projects**
   ```markdown
   ## References
   - UI guidelines: `ui/AGENTS.md`
   - API guidelines: `api/AGENTS.md`
   ```
   Claude/Gemini/Codex can read referenced files.
   Note: Ollama cannot (pure LLM, no tools).

4. **Structure for Scanning**
   - Use bullet points, not paragraphs
   - AI scans faster

5. **Specify Response Format**
   ```markdown
   ## Response Format
   FIRST LINE must be exactly:
   STATUS: PASSED
   or
   STATUS: FAILED

   If FAILED, list: `file:line - rule violated - issue`
   ```

**Example Rules File:**
```markdown
# Code Review Rules

## References
- UI details: `ui/AGENTS.md`
- SDK details: `sdk/AGENTS.md`

---

## ALL FILES

REJECT if:
- Hardcoded secrets/credentials
- `any` type (TypeScript) or missing type hints (Python)
- Code duplication (violates DRY)
- Silent error handling (empty catch blocks)

---

## TypeScript/React

REJECT if:
- `import React` → use `import { useState }`
- `var()` or hex colors → use Tailwind
- Missing `"use client"` in client components

PREFER:
- `cn()` for conditional classes
- Semantic HTML over divs

---

## Response Format

FIRST LINE: STATUS: PASSED or STATUS: FAILED
If FAILED: `file:line - rule - issue`
```

#### Smart Caching System

**How It Works:**
1. Hash AGENTS.md + .gga config
   - If changed → Invalidate ALL cache
2. For each staged file:
   - Hash file content
   - If cached with PASSED → Skip
   - If not cached → Send to AI
3. After PASSED review:
   - Store file hash in cache

**Cache Invalidation:**
| Change | Effect |
|--------|--------|
| File content | Only that file re-reviewed |
| AGENTS.md | **All files** re-reviewed |
| .gga config | **All files** re-reviewed |

**Cache Commands:**
```bash
gga cache status       # Check status
gga cache clear        # Clear project
gga cache clear-all    # Clear all
gga run --no-cache     # Bypass cache
```

**Cache Location:**
```
~/.cache/gga/
├── <project-hash>/
│   ├── metadata          # Hash of AGENTS.md + .gga
│   └── files/
│       ├── <file-hash>   # "PASSED"
```

#### Workflow

```
git commit
    │
    ▼
┌───────────────────┐
│  Pre-commit Hook  │
└───────────────────┘
    │
    ├──▶ 1. Load .gga config
    ├──▶ 2. Validate provider
    ├──▶ 3. Check AGENTS.md
    ├──▶ 4. Get staged files (matching patterns)
    ├──▶ 5. Read rules from AGENTS.md
    ├──▶ 6. Build prompt: rules + files
    ├──▶ 7. Send to AI provider
    └──▶ 8. Parse response
            │
            ├── STATUS: PASSED ──▶ ✅ Commit
            └── STATUS: FAILED ──▶ ❌ Block
```

#### Commands

```bash
gga init                   # Create .gga config
gga install                # Install pre-commit hook
gga install --commit-msg   # Install commit-msg hook (validates message)
gga uninstall              # Remove hooks
gga run                    # Review staged files
gga run --ci               # Review last commit (CI/CD)
gga run --no-cache         # Force review all
gga config                 # Display config
gga cache status           # Cache status
gga version                # Version
```

#### Integration Examples

**Husky (Node.js):**
```bash
# .husky/pre-commit
gga run || exit 1
```

**pre-commit (Python):**
```yaml
repos:
  - repo: local
    hooks:
      - id: gga
        entry: gga run
        language: system
```

**GitHub Actions:**
```yaml
- name: Run AI Review
  run: |
    git diff --name-only origin/${{ github.base_ref }}...HEAD | xargs git add
    gga run
```

**Lefthook (Go):**
```yaml
pre-commit:
  commands:
    ai-review:
      run: gga run
```

#### Test Suite

**Total: 161 tests**

| Module | Tests | Coverage |
|--------|-------|----------|
| cache.sh | 27 | Hash functions, validation |
| providers.sh | 49 | All providers, routing, security |
| CLI commands | 34 | All commands |
| Ollama | 12 | Real tests |
| OpenCode | 8 | Provider tests |
| STATUS parsing | 14 | Edge cases, preamble |

**Recent Improvements (v2.6.1):**
- Relaxed STATUS parsing (handles AI preamble)
- Accepts markdown formatting (`**STATUS: PASSED**`)
- Works with system-wide instruction files

### Review Aspects Extracted

**Pre-commit Enforcement:**
- Automatic review on every commit
- Configurable file patterns
- Rule-based validation
- Provider flexibility
- Smart caching

**Rules File Design:**
- Concise (100-200 lines)
- Action keywords (REJECT/REQUIRE/PREFER)
- References for complex projects
- Scannable structure
- Response format specification

**Caching Strategy:**
- Content-based hashing
- Config-aware invalidation
- File-level granularity
- Performance optimization

### Unique Methodology

**Provider Agnostic:**
- Works with any AI CLI
- Bash-based (no dependencies)
- Git-native hook
- Cross-platform

**Smart Caching:**
- Hash-based cache keys
- Automatic invalidation
- Config-aware
- Performance optimization

**Rules File Optimization:**
- LLM parsing optimized
- Reference system (Claude/Gemini/Codex can read)
- Keyword-based directives
- Response format enforcement

**Bypass Options:**
```bash
git commit --no-verify     # Skip hook
git commit -n              # Short form
```

---

## 5. Nizos: TDD Guard

**Stars:** 1,747

### Key Features
- Automated TDD enforcement
- Multi-language support (TypeScript, JavaScript, Python, PHP, Go, Rust, Storybook)
- Pre-tool-use hooks
- Test reporter system
- Session management

### Code Review Components

#### TDD Enforcement System

**Three Hooks:**

1. **PreToolUse Hook** (`Write|Edit|MultiEdit|TodoWrite`)
   - Validates file modifications
   - Blocks if tests not failing
   - Prevents over-implementation

2. **UserPromptSubmit Hook**
   - Quick toggle commands
   - Session commands

3. **SessionStart Hook** (`startup|resume|clear`)
   - Automatic session management
   - Initializes state

#### Test Reporters

Language-specific reporters capture test results:

**JavaScript/TypeScript:**
- Vitest (tdd-guard-vitest)
- Jest (tdd-guard-jest)
- Storybook (tdd-guard-storybook)

**Python:**
- pytest (tdd-guard-pytest)

**PHP:**
- PHPUnit (tdd-guard/phpunit)

**Go:**
- go test (tdd-guard-go)

**Rust:**
- cargo test / cargo nextest (tdd-guard-rust)

All save to: `.claude/tdd-guard/data/test.json`

#### TDD Workflow Enforcement

```
User writes test → Test fails (Red)
    → Agent writes minimal code
    → Test passes (Green)
    → Refactor with linting
```

**Blocks:**
- Write code without failing test
- Implement more than needed
- Skip refactoring (if lint failures)

#### Configuration Options

1. **Custom Instructions** - Customize TDD validation rules
2. **Lint Integration** - Automated refactoring support
3. **Strengthening Enforcement** - Prevent bypass attempts
4. **Ignore Patterns** - Control validated files
5. **Validation Model** - Choose model (faster/capable)

### Review Aspects Extracted

**TDD Discipline:**
- Test-first enforcement
- Minimal implementation
- Refactoring enforcement
- Multi-language support
- Session management

**Workflow Integration:**
- Pre-tool-use validation
- Session-based state
- Test result monitoring
- Lint integration

### Unique Methodology

**Three-Phase Enforcement:**
1. **Red Phase** - Must have failing test
2. **Green Phase** - Only implement enough to pass
3. **Refactor Phase** - Must pass linting

**Multi-Language Support:**
- Language-specific reporters
- Unified validation model
- Cross-framework compatibility

**Session Management:**
- Toggle on/off mid-session
- Automatic state initialization
- Session-based validation

---

## 6. Bartolli: Claude Code TypeScript Hooks

**Stars:** 167

### Key Features
- Quality check hooks for Claude Code
- Real-time validation on file edits
- Auto-fix capability
- Project-specific implementations

### Code Review Components

#### Hook System

**Trigger:** After Write/Edit/MultiEdit operations on TypeScript/JavaScript files

**Exit Codes:**
- 0 = success (silent)
- 2 = quality issues (blocking)

**Project Types:**
- react-app
- vscode-extension
- node-typescript

#### Quality Checks

**Four Check Types:**

1. **TypeScript Compilation**
   - Uses project's tsconfig.json
   - Type checking
   - Compilation errors

2. **ESLint**
   - Auto-fix capability
   - Configurable rules
   - Project-specific config

3. **Prettier**
   - Formatting validation
   - Auto-fix capability
   - Consistent style

4. **Custom Rules**
   - Console usage detection
   - 'as any' usage
   - Debugger statements
   - TODO comments

#### Core Components

**1. settings.local.json**
- Configures which hooks run
- When they trigger

**2. quality-check.js**
- Main validation logic
- Per-project implementation

**3. hook-config.json**
- Rule definitions
- Severity levels (info/warning/error)
- Allowed patterns
- TypeScript/ESLint/Prettier behavior

**4. tsconfig-cache.json**
- Auto-generated cache
- Maps project paths to TypeScript configs
- SHA256 checksums for invalidation

#### Cache Management

**Invalidation Triggers:**
- tsconfig.json files modified
- New TypeScript projects added
- Cache files deleted

**Cache Strategy:**
- SHA256 checksums
- Automatic invalidation
- Project-path mapping

#### Configuration

Edit `hook-config.json`:
```json
{
  "rules": {
    "console-usage": {
      "severity": "error",
      "allowedPatterns": ["console.error", "console.warn"]
    },
    "any-type": {
      "severity": "warning",
      "allowedPatterns": []
    }
  }
}
```

### Review Aspects Extracted

**Real-Time Validation:**
- TypeScript type safety
- ESLint compliance
- Prettier formatting
- Custom rule violations
- Immediate feedback

**Auto-Fix Capability:**
- ESLint auto-fix
- Prettier formatting
- Reduces manual work

**Project-Specific:**
- Per-project configurations
- Shared patterns
- Customizable rules

### Unique Methodology

**Post-Edit Validation:**
- Runs after file edits
- Blocks on errors (exit 2)
- Silent on success (exit 0)

**Writing Style (from CLAUDE.md):**

**Banned:**
- Emojis
- Marketing language
- "Thank you" pleasantries
- Explanatory preambles
- Non-informative adjectives

**Banned Words:**
- powerful, seamless, comprehensive, robust, elegant
- enhanced, amazing, great, awesome, wonderful, excellent
- sophisticated, advanced, intuitive, user-friendly
- cutting-edge, state-of-the-art, innovative, revolutionary

**Write:**
- Facts only
- Direct statements
- Concrete specifics
- Technical accuracy

**Secret:** Write like code comments for yourself. Facts only. No adjectives.

---

## 7. Veraticus: CC-Tools

**Stars:** 46

### Key Features
- Go-based Claude Code tools
- Command-line interface
- Hook support
- Configuration management

### Code Review Components

#### Architecture

**Built in Go with:**
- CLI interface
- Hook integration
- TOML/YAML configuration
- golangci-lint integration

#### Components

**Configuration:**
- `example-config.toml`
- `example-config.yaml`
- Flexible options

**Reference Documentation:**
- `reference/statusline.md` - Status line docs
- `reference/hooks.md` - Hook system docs

**Development:**
- Makefile for automation
- Flake.nix for Nix support
- golangci-lint for quality

#### Features

Based on directory structure:
- Hook integration
- Status line customization
- Go-based tooling
- Configuration flexibility

### Review Aspects Extracted

**Go Implementation:**
- Compiled tool (performance)
- Native hook support
- Cross-platform

**Configuration:**
- TOML/YAML support
- Flexible options
- Example configs

**Linting:**
- golangci-lint integration
- Code quality enforcement

### Note

Limited documentation in README. Features inferred from code structure. Appears to be utility tool rather than comprehensive review system.

---

## Comparative Analysis

### By Type

| Type | Repositories | Focus |
|------|--------------|-------|
| System Prompts | Piebald-AI | PR review, security review |
| Skills | Trail of Bits, Obra | Security audit, code quality |
| Hooks | TDD Guard, Bartolli, CC-Tools | TDD enforcement, quality checks |
| Git Hook + CLI | Gentleman Guardian Angel | Pre-commit AI review |

### By Review Focus

| Focus | Repositories |
|-------|--------------|
| Security | Piebald-AI (security-review), Trail of Bits (differential-review, fix-review) |
| General Code Quality | Piebald-AI (review-pr), Obra (code-reviewer), Bartolli |
| TDD Enforcement | TDD Guard |
| Pre-commit AI Review | Gentleman Guardian Angel |
| Workflow/Process | Obra (requesting/receiving review) |

### By Methodology Uniqueness

**Trail of Bits:**
- Adaptive depth (SMALL/MEDIUM/LARGE codebase strategies)
- Six-phase workflow
- Blast radius quantification
- Git history analysis
- Adversarial analysis with attacker modeling

**Piebald-AI:**
- Two-phase validation (detection + false positive filtering)
- 17+ hard exclusions
- Sub-task parallelization
- Precedent-based evaluation

**Obra:**
- Review workflow integration
- YAGNI enforcement
- No performative agreement
- Technical rigor over social comfort

**Gentleman Guardian Angel:**
- Provider-agnostic (works with any AI CLI)
- Smart caching (content-based with config-aware invalidation)
- Rules file optimization (LLM parsing focused)
- Pure Bash (zero dependencies)

**TDD Guard:**
- Three-phase enforcement (Red/Green/Refactor)
- Multi-language support with unified model
- Session-based validation
- Test reporter system

**Bartolli:**
- Real-time post-edit validation
- Auto-fix capability
- Project-specific configurations
- Strict writing style guidelines

---

## Key Review Aspects by Category

### 1. Security Review Aspects

**From Piebald-AI (security-review):**
- Input validation (SQL, command, XXE, template, NoSQL, path traversal)
- Authentication & authorization bypass
- Crypto & secrets management
- Injection & code execution
- Data exposure
- High confidence threshold (≥8/10)
- Concrete attack paths only
- 17+ hard exclusions

**From Trail of Bits (differential-review):**
- Risk-first prioritization
- Git history analysis (security commits)
- Blast radius quantification
- Invariant violations
- Attacker modeling (WHO/WHAT/WHERE)
- Exploitability rating (EASY/MEDIUM/HARD)
- Complete exploit scenarios
- Baseline context comparison

**From Trail of Bits (vulnerability patterns):**
- Security regressions (re-added vulnerable code)
- Double decrease/increase bugs
- Missing validation
- Underflow/overflow
- Reentrancy (CEI violations)
- Access control bypass
- Race conditions / front-running
- Timestamp manipulation
- Unchecked return values
- Denial of service

### 2. General Code Quality Aspects

**From Piebald-AI (review-pr):**
- Code correctness
- Project conventions
- Performance implications
- Test coverage
- Security considerations

**From Obra (code-reviewer):**
- Plan alignment
- Code quality (patterns, error handling, type safety, maintainability)
- Architecture (SOLID, separation of concerns, integration, scalability)
- Documentation (comments, headers, standards)
- Issue categorization (Critical/Important/Minor)
- Production readiness (migration, compatibility, documentation)

**From Bartolli (TypeScript hooks):**
- TypeScript type safety
- ESLint compliance
- Prettier formatting
- Custom rule violations (console, 'as any', debugger, TODO)
- Real-time feedback

### 3. Workflow/Process Aspects

**From Obra (requesting/receiving review):**
- Review early, review often
- Mandatory review points (after task, after feature, before merge)
- Three-step process (get SHAs, dispatch, act on feedback)
- Technical rigor over performative agreement
- YAGNI checks
- Context-aware pushback
- One-at-a-time implementation

**From Trail of Bits (differential-review):**
- Adaptive depth based on codebase size
- Six-phase workflow
- Evidence-based findings
- Always generate report
- Rationalizations to avoid
- Red flags for immediate escalation

**From Gentleman Guardian Angel:**
- Pre-commit enforcement
- Provider-agnostic
- Smart caching
- Rules file optimization
- Response format specification

**From TDD Guard:**
- Test-first enforcement
- Minimal implementation
- Refactoring enforcement
- Session-based validation

### 4. Validation Techniques

**Git-Based:**
- Git blame for removed code (Trail of Bits)
- Git history analysis for regressions (Trail of Bits)
- Commit range analysis (Trail of Bits fix-review)
- Staged files review (Gentleman Guardian Angel)

**Static Analysis:**
- TypeScript compilation (Bartolli)
- ESLint rules (Bartolli)
- Prettier formatting (Bartolli)
- Custom pattern matching (Bartolli)

**AI-Based:**
- LLM code review (Gentleman Guardian Angel)
- Sub-task parallelization (Piebald-AI)
- Provider-agnostic validation (Gentleman Guardian Angel)

**Test-Based:**
- Test result monitoring (TDD Guard)
- Test reporter system (TDD Guard)
- Coverage gap detection (Trail of Bits)

### 5. Caching & Performance

**From Gentleman Guardian Angel:**
- Content-based hashing (SHA256)
- Config-aware invalidation (AGENTS.md + .gga)
- File-level granularity
- Cache commands (status/clear/clear-all)

**From Bartolli:**
- TypeScript config caching (tsconfig-cache.json)
- SHA256 checksums
- Automatic invalidation

**From Trail of Bits:**
- Adaptive depth (SMALL/MEDIUM/LARGE)
- Priority matrix (risk × blast radius)
- Focused vs surgical analysis

### 6. Reporting & Communication

**From Trail of Bits (differential-review):**
- Always generate markdown report
- File/line references
- Attack scenarios
- Recommendations
- Explicit coverage limits

**From Obra (code-reviewer):**
- Structured output (Strengths/Issues/Recommendations/Assessment)
- Issue categorization (Critical/Important/Minor)
- Clear verdict (Yes/No/With fixes)
- Actionable recommendations

**From Piebald-AI (security-review):**
- Markdown format with severity
- Description + exploit scenario + recommendation
- Confidence scoring
- Evidence-based findings

**From Gentleman Guardian Angel:**
- Response format specification
- STATUS: PASSED/FAILED
- file:line - rule - issue format

---

## Unique Contributions by Repository

### Piebald-AI
- **Sub-task parallelization** for false positive filtering
- **17+ hard exclusions** to minimize noise
- **Precedent-based evaluation** (React/Angular XSS, env vars trusted)

### Trail of Bits
- **Adaptive depth** based on codebase size
- **Blast radius quantification** (caller count)
- **Adversarial analysis** with attacker modeling
- **Baseline context building** with invariants
- **Vulnerability pattern library** (10+ common patterns)
- **Fix review** methodology (cross-reference commits with audit findings)

### Obra
- **Review workflow integration** (when to review)
- **No performative agreement** guideline
- **YAGNI enforcement** (grep codebase before implementing)
- **Technical rigor** over social comfort
- **Communication protocol** (when to push back)

### Gentleman Guardian Angel
- **Provider-agnostic** AI integration (works with any CLI)
- **Pure Bash** implementation (zero dependencies)
- **Smart caching** with config-aware invalidation
- **Rules file optimization** for LLM parsing
- **Action keywords** (REJECT/REQUIRE/PREFER)
- **Reference system** for complex projects
- **161 comprehensive tests**

### TDD Guard
- **Three-phase enforcement** (Red/Green/Refactor)
- **Multi-language** unified model (7 languages)
- **Test reporter system** (language-specific)
- **Session-based validation**
- **Pre-tool-use hooks** for blocking

### Bartolli
- **Real-time post-edit validation**
- **Auto-fix capability** (ESLint + Prettier)
- **Project-specific configurations**
- **Strict writing style guidelines** (no emojis, marketing language)
- **Writing like code comments** philosophy

---

## Implementation Recommendations

Based on this research, a comprehensive code review plugin should consider:

### Core Features (Must Have)

1. **Adaptive Review Depth** (from Trail of Bits)
   - Classify codebase size (SMALL/MEDIUM/LARGE)
   - Adjust analysis depth accordingly

2. **Risk-Based Prioritization** (from Trail of Bits)
   - Categorize changes by risk (HIGH/MEDIUM/LOW)
   - Focus on auth, crypto, validation, external calls

3. **Git History Analysis** (from Trail of Bits)
   - Git blame removed code
   - Check for security commit regressions
   - Track code that was previously fixed

4. **Evidence-Based Findings** (from Trail of Bits, Piebald-AI)
   - File/line references
   - Concrete examples
   - Attack scenarios (for security)
   - Recommendations

5. **Issue Categorization** (from Obra)
   - Critical (must fix)
   - Important (should fix)
   - Minor (nice to have)

6. **Smart Caching** (from Gentleman Guardian Angel)
   - Content-based hashing
   - Config-aware invalidation
   - File-level granularity

7. **Response Format Specification** (from Gentleman Guardian Angel)
   - Clear output format
   - Machine-parseable
   - STATUS indication

### Advanced Features (Should Have)

8. **Blast Radius Quantification** (from Trail of Bits)
   - Count callers
   - Priority matrix (risk × blast radius)

9. **Test Coverage Analysis** (from Trail of Bits)
   - Identify gaps
   - Risk elevation rules

10. **Vulnerability Patterns** (from Trail of Bits)
    - Pre-defined common patterns
    - Quick detection commands

11. **False Positive Filtering** (from Piebald-AI)
    - Hard exclusions
    - Confidence scoring
    - Precedent-based evaluation

12. **Review Workflow** (from Obra)
    - When to review guidance
    - Integration points
    - Feedback protocol

13. **YAGNI Checks** (from Obra)
    - Grep codebase for usage
    - Remove unused features

### Optional Features (Nice to Have)

14. **TDD Enforcement** (from TDD Guard)
    - Test-first validation
    - Minimal implementation
    - Refactoring checks

15. **Real-Time Validation** (from Bartolli)
    - Post-edit checks
    - Auto-fix capability
    - Lint integration

16. **Provider Flexibility** (from Gentleman Guardian Angel)
    - Multiple AI providers
    - Easy switching
    - Model selection

17. **Rules File System** (from Gentleman Guardian Angel)
    - Action keywords (REJECT/REQUIRE/PREFER)
    - Reference system
    - LLM-optimized format

---

## Files Saved

All prompts and analyses saved to `/tmp/code-review-research/prompts/`:

1. `piebald-ai-review-pr.md` - Simple PR review
2. `piebald-ai-security-review.md` - Comprehensive security review
3. `trailofbits-differential-review.md` - Adaptive security-focused review
4. `trailofbits-adversarial-analysis.md` - Attacker modeling methodology
5. `trailofbits-vulnerability-patterns.md` - Common vulnerability patterns
6. `trailofbits-fix-review.md` - Fix verification methodology
7. `obra-code-reviewer-agent.md` - Code reviewer agent
8. `obra-receiving-code-review.md` - Review reception guidelines
9. `bartolli-typescript-hooks.md` - TypeScript quality hooks
10. `nizos-tdd-guard.md` - TDD enforcement
11. `veraticus-cc-tools.md` - Go-based utilities
12. `gentleman-guardian-angel.md` - Pre-commit AI review tool

Summary saved to: `/tmp/code-review-research/repositories/new-repositories-summary.md`
