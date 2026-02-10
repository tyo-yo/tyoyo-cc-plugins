# Trail of Bits: Differential Review Skill

**Source:** https://github.com/trailofbits/skills
**Stars:** 2498
**Type:** Skill + Commands

## Overview

Security-focused differential review for PRs, commits, and diffs. Adapts analysis depth to codebase size and uses git history for context.

## Core Principles

1. **Risk-First**: Focus on auth, crypto, value transfer, external calls
2. **Evidence-Based**: Every finding backed by git history, line numbers, attack scenarios
3. **Adaptive**: Scale to codebase size (SMALL/MEDIUM/LARGE)
4. **Honest**: Explicitly state coverage limits and confidence
5. **Output-Driven**: Always generate markdown report

## Codebase Size Strategy

| Size | Files | Strategy | Approach |
|------|-------|----------|----------|
| SMALL | <20 | DEEP | Read all deps, full git blame |
| MEDIUM | 20-200 | FOCUSED | 1-hop deps, priority files |
| LARGE | 200+ | SURGICAL | Critical paths only |

## Risk Level Triggers

| Level | Triggers |
|-------|----------|
| HIGH | Auth, crypto, external calls, value transfer, validation removal |
| MEDIUM | Business logic, state changes, new public APIs |
| LOW | Comments, tests, UI, logging |

## Workflow Phases

### Pre-Analysis: Baseline Context Building

Uses `audit-context-building` skill if available to understand:
- System-wide invariants
- Trust boundaries and privilege levels
- Validation patterns (defense-in-depth)
- Complete call graphs
- State flow diagrams
- External dependencies

### Phase 0: Intake & Triage

- Extract changes (git diff, gh pr view)
- Assess codebase size
- Classify complexity
- Risk score each file

### Phase 1: Changed Code Analysis

For each changed file:
1. Read both versions (baseline + changed)
2. Analyze each diff region
3. Git blame removed code (check for security commits)
4. Check for regressions (re-added code)
5. Micro-adversarial analysis
6. Generate concrete attack scenarios

### Phase 2: Test Coverage Analysis

- Identify coverage gaps
- Risk elevation rules:
  - NEW function + NO tests → MEDIUM→HIGH
  - MODIFIED validation + UNCHANGED tests → HIGH
  - Complex logic (>20 lines) + NO tests → HIGH

### Phase 3: Blast Radius Analysis

Calculate impact by caller count:
- 1-5 calls: LOW
- 6-20 calls: MEDIUM
- 21-50 calls: HIGH
- 50+ calls: CRITICAL

Priority matrix based on change risk × blast radius.

### Phase 4: Deep Context Analysis

Uses `audit-context-building` for HIGH RISK changes:
- Map complete function flow
- Trace internal calls
- Trace external calls
- Identify invariants
- Five Whys root cause analysis
- Cross-cutting pattern detection

### Phase 5: Adversarial Analysis (for HIGH RISK)

See [adversarial.md](trailofbits-adversarial-analysis.md)

### Phase 6: Report Generation

See [reporting.md](methodology document)

## Common Vulnerability Patterns

See [patterns.md](trailofbits-vulnerability-patterns.md)

## Rationalizations to Avoid

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "Small PR, quick review" | Heartbleed was 2 lines | Classify by RISK, not size |
| "I know this codebase" | Familiarity breeds blind spots | Build explicit baseline context |
| "Git history takes too long" | History reveals regressions | Never skip Phase 1 |
| "Blast radius is obvious" | You'll miss transitive callers | Calculate quantitatively |
| "No tests = not my problem" | Missing tests = elevated risk | Flag in report, elevate severity |
| "Just a refactor" | Refactors break invariants | Analyze as HIGH until proven LOW |
| "I'll explain verbally" | No artifact = findings lost | Always write report |

## Red Flags (Immediate Escalation)

- Removed code from "security", "CVE", or "fix" commits
- Access control modifiers removed
- Validation removed without replacement
- External calls added without checks
- High blast radius (50+) + HIGH risk change

## Quality Checklist

Before delivering:
- [ ] All changed files analyzed
- [ ] Git blame on removed security code
- [ ] Blast radius calculated for HIGH risk
- [ ] Attack scenarios are concrete
- [ ] Findings reference line numbers + commits
- [ ] Report file generated
- [ ] User notified with summary

## Review Aspects

- Security regressions
- Blast radius quantification
- Test coverage gaps
- Invariant violations
- Concrete exploit scenarios
- Git history analysis
