# Trail of Bits: Fix Review Skill

**Source:** https://github.com/trailofbits/skills
**Stars:** 2498
**Type:** Skill + Commands

## Overview

Verifies that git commits address security audit findings without introducing bugs. Cross-references code changes with audit reports.

## When to Use

- Reviewing fix branches against security audit reports
- Validating remediation commits
- Checking if specific findings (TOB-XXX) were fixed
- Analyzing commit ranges for bug introduction
- Cross-referencing with audit recommendations

## When NOT to Use

- Initial security audits (use audit-context-building or differential-review)
- Code review without specific baseline
- Greenfield development
- Documentation-only changes

## Input Requirements

| Input | Required | Format |
|-------|----------|--------|
| Source commit | Yes | Git commit hash or ref (baseline before fixes) |
| Target commit(s) | Yes | One or more commit hashes |
| Security report | No | Local path, URL, or Google Drive link |

## Finding Status Values

| Status | Meaning |
|--------|---------|
| FIXED | Code change directly addresses the finding |
| PARTIALLY_FIXED | Some aspects addressed, others remain |
| NOT_ADDRESSED | No relevant changes found |
| CANNOT_DETERMINE | Insufficient context to verify |

## Workflow Phases

### Phase 1: Input Gathering

Collect required inputs:
- Source commit (baseline)
- Target commit(s)
- Security report (optional)

### Phase 2: Report Retrieval

When report provided, retrieve based on format:

**Local file (PDF, MD, JSON, HTML):**
- Read directly using Read tool
- Claude processes PDFs natively

**URL:**
- Fetch using WebFetch tool

**Google Drive:**
- See `references/report-parsing.md` for fallback logic using `gdrive` CLI

### Phase 3: Finding Extraction

Parse report to extract findings:

**Trail of Bits format:**
- Look for "Detailed Findings" section
- Pattern: `TOB-[A-Z]+-[0-9]+`
- Capture: ID, title, severity, description, affected files

**Other formats:**
- Numbered findings (Finding 1, Finding 2)
- Severity-based sections
- JSON with `findings` array

### Phase 4: Commit Analysis

For each target commit:
```bash
# Get commit list
git log <source>..<target> --oneline

# Get full diff
git diff <source>..<target>

# Get changed files
git diff <source>..<target> --name-only
```

For each commit:
1. Examine diff for bug introduction patterns
2. Check for security anti-patterns
3. Map changes to relevant findings

### Phase 5: Finding Verification

For each finding:

1. **Identify relevant commits** - Match by:
   - File paths in finding
   - Function/variable names
   - Commit messages referencing finding ID

2. **Verify the fix**:
   - Root cause addressed (not just symptoms)
   - Fix follows report's recommendation
   - No new vulnerabilities introduced

3. **Assign status** based on evidence

4. **Document evidence**:
   - Commit hash(es)
   - Specific file/line changes
   - How fix addresses root cause

### Phase 6: Output Generation

**1. Report file (`FIX_REVIEW_REPORT.md`):**

```markdown
# Fix Review Report

**Source:** <commit>
**Target:** <commit>
**Report:** <path or "none">
**Date:** <date>

## Executive Summary

[X findings reviewed, Y fixed, Z concerns]

## Finding Status

| ID | Title | Severity | Status | Evidence |
|----|-------|----------|--------|----------|
| TOB-XXX-1 | Finding title | High | FIXED | abc123 |
| TOB-XXX-2 | Another finding | Medium | NOT_ADDRESSED | - |

## Bug Introduction Concerns

[Potential bugs or regressions]

## Per-Commit Analysis

### Commit abc123: "Fix reentrancy in withdraw()"

**Files changed:** contracts/Vault.sol
**Findings addressed:** TOB-XXX-1
**Concerns:** None

[Detailed analysis]

## Recommendations

[Follow-up actions]
```

**2. Conversation summary:**
- Total findings: X
- Fixed: Y
- Not addressed: Z
- Concerns: [bug introduction risks]

## Bug Detection Patterns

Key anti-patterns to watch:
- Access control weakening (modifiers removed)
- Validation removal (require/assert deleted)
- Error handling reduction (try/catch removed)
- External call reordering (state after call)
- Integer operation changes (SafeMath removed)
- Cryptographic weakening

See `references/bug-detection.md` for comprehensive patterns.

## Rationalizations to Avoid

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "Commit message says it fixes TOB-XXX" | Messages lie; code tells truth | Verify actual code change |
| "Small fix, no new bugs" | Small changes cause big bugs | Analyze all changes |
| "I'll check important findings" | All findings matter | Systematically check every finding |
| "Tests pass" | Tests may not cover the fix | Verify fix logic |
| "Same developer" | Familiarity breeds blind spots | Fresh analysis of every change |

## Tips

**Do:**
- Verify actual code, not commit messages
- Check fixes address root causes
- Look for unintended side effects
- Cross-reference interacting findings
- Document evidence for every status

**Don't:**
- Trust commit messages as proof
- Skip minor-seeming findings
- Assume passing tests = correct fixes
- Ignore out-of-scope changes
- Mark FIXED without clear evidence

## Review Aspects

- Root cause verification
- Bug introduction detection
- Finding-to-commit mapping
- Comprehensive coverage
- Evidence-based status
