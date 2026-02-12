---
description: "Multi-perspective code review with configurable depth"
argument-hint: "[mode]"
allowed-tools: ["Bash", "Read", "Task", "AskUserQuestion"]
---

# Custom Code Review

Run a comprehensive, multi-perspective code review using specialized review agents.

**Mode**: "$ARGUMENTS" (optional: light, standard, standard-fast, thorough, thorough-fast)

## Workflow Overview

This command orchestrates a multi-phase review process:
1. **PR Information Collection** - Gather context
2. **Mode Selection** - Choose review depth (interactive)
3. **Parallel Review** - Multiple perspectives in parallel
4. **Consolidation** - Deduplicate findings
5. **Verification** - Check for false positives
6. **User Confirmation** - Interactive review of results

---

## Phase 1: Setup and PR Analysis

### Step 1.1: Generate Session ID

Create a unique session ID for this review:

```bash
SESSION_ID=$(date +%Y%m%d_%H%M%S)_$$
```

### Step 1.2: Create Temporary Directory

```bash
mkdir -p /tmp/claude-code-review-${SESSION_ID}/reviews
```

### Step 1.3: Read Configuration (if exists)

Check for `.claude/custom-code-review.local.md`:

```bash
if [ -f .claude/custom-code-review.local.md ]; then
  # Configuration exists
  echo "Found project configuration"
else
  echo "Using default configuration"
fi
```

If file exists, read it using Read tool to extract:
- YAML frontmatter: mode, excluded_perspectives, max_parallel_agents, language
- Markdown body: additional_instructions

**Default values if not specified**:
- mode: "standard"
- language: "ja" (Japanese)
- max_parallel_agents: 7

### Step 1.4: Launch PR Analyzer

Use Task tool to launch `pr-analyzer` agent:

**Prompt**:
```
Collect PR information for code review.

Session ID: {SESSION_ID}
Language: {language} (default: ja)

Please:
1. Create /tmp/claude-code-review-{SESSION_ID}/ directory
2. Identify changed files (git diff)
3. Get commit messages and PR info
4. Read changed files
5. Find related files
6. Check for .claude/custom-code-review.local.md configuration
7. Write comprehensive summary to /tmp/claude-code-review-{SESSION_ID}/pr-summary.md

Return the path to pr-summary.md when done.
```

---

## Phase 2: Mode Selection

### Step 2.1: Determine Default Mode

Priority order:
1. Command argument ($ARGUMENTS)
2. Configuration file (.local.md mode field)
3. Default: "standard"

### Step 2.2: Read PR Summary

Read `/tmp/claude-code-review-{SESSION_ID}/pr-summary.md` to understand scope.

### Step 2.2a: Present Perspective Coverage for Each Mode

Display to user which perspectives each mode will review:

**Light Mode** (3 perspectives, ~5-10 min):
- P01: AI Agent Instructions
- C01: Bug Detection
- S01: Basic Vulnerabilities

**Standard Mode** (7 perspectives, ~15-20 min):
- P01: AI Agent Instructions
- C01: Bug Detection
- C03: Edge Cases
- S01: Basic Vulnerabilities
- S03: False Positive Filter
- T01: Test Coverage
- Q01: Readability

**Thorough Mode** (15 perspectives, ~25-30 min):
All from Standard, plus:
- P02: Pattern Alignment
- C02: Functional Compliance
- C04: Silent Failures
- C05: Exception Safety
- S02: Common Security Patterns
- S04: Precedent-Based Security
- S05: Adaptive Review Depth
- T02: Test Quality
- T03: Error Handling Quality
- Q02: Complexity
- Q03: Code Smells
- Q04: Antipatterns
- D01: Type Design
- D03: API Design
- DOC01: Comment Quality

**Fast Modes**: Same perspectives as their non-Fast counterparts, but with multiple perspectives per agent for faster execution.

Note to user: "If you want details on any perspective, just ask."

### Step 2.2b: Analyze PR and Recommend Mode

Based on PR summary, analyze:
1. **Change scope**: Number of files, lines changed
2. **Change type**: Bug fix, new feature, refactoring, security fix
3. **Risk level**: Critical path changes, security-sensitive areas

Recommend mode:
- **Light**: Minor changes (< 100 lines), typo fixes, simple bug fixes, documentation updates
- **Standard**: Normal PRs, feature development (100-500 lines), typical bug fixes
- **Thorough**: Critical features, security changes, large refactors (> 500 lines), authentication/authorization changes

Display recommendation to user in this format:

```
Based on this PR:
- Changed files: {count}
- Total changes: ~{lines} lines added/modified
- Type: {Bug fix/Feature/Refactoring/Security fix/Documentation}

**Recommended mode**: {Light/Standard/Thorough} ({brief reason why})

Would you like to proceed with the recommended mode or choose a different one?
```

### Step 2.3: Present Mode Options to User

Use AskUserQuestion to let user select mode:

**Question**: "Which review mode would you like to use?"

**Options**:

1. **Light**
   - Label: "Light"
   - Description: "Quick review (3 perspectives, ~5-10 min). Best for minor changes."

2. **Standard**
   - Label: "Standard (Recommended)"
   - Description: "Balanced review (7 perspectives, ~15-20 min). Best for most PRs."

3. **Standard Fast**
   - Label: "Standard Fast"
   - Description: "Same as Standard but faster (7 perspectives, 3-4 agents, ~10-15 min)."

4. **Thorough**
   - Label: "Thorough"
   - Description: "Deep review (15 perspectives, ~25-30 min). Best for critical features."

5. **Thorough Fast**
   - Label: "Thorough Fast"
   - Description: "Same as Thorough but faster (15 perspectives, 5-7 agents, ~15-20 min)."

### Step 2.4: Process Mode Selection

Based on selected mode, determine:
- **Perspectives to review** (list of IDs)
- **Agent parallelization** (deep: 1 perspective per agent, fast: multiple per agent)
- **Expected time**

---

## Phase 3: Perspective Selection Logic

### Mode Definitions

#### Light Mode
**Perspectives** (3-5):
- P01: AI Agent Instructions
- C01: Bug Detection
- S01: Basic Vulnerabilities

**Agents**: 3 agents (1 perspective each)

#### Standard Mode
**Perspectives** (7-10):
- P01: AI Agent Instructions
- C01: Bug Detection
- C03: Edge Cases
- S01: Basic Vulnerabilities
- S03: False Positive Filter
- T01: Test Coverage
- Q01: Readability

**Agents**: 7 agents (1 perspective each)

#### Standard Fast Mode
**Perspectives** (same as Standard: 7-10)

**Agents**: 3-4 agents (2-3 perspectives each):
- Agent 1: P01, C01
- Agent 2: C03, S01
- Agent 3: S03, T01
- Agent 4: Q01

#### Thorough Mode
**Perspectives** (15-20):
- All from Standard +
- P02, C02, C04, C05
- S02, S04, S05
- T02, T03
- Q02, Q03, Q04
- D01, D03
- DOC01

**Agents**: 15-20 agents (1 perspective each)

#### Thorough Fast Mode
**Perspectives** (same as Thorough: 15-20)

**Agents**: 5-7 agents (3-4 perspectives each):
- Agent 1: P01, P02, C01
- Agent 2: C02, C03, C04
- Agent 3: C05, S01, S02
- Agent 4: S03, S04, S05
- Agent 5: T01, T02, T03
- Agent 6: Q01, Q02, Q03
- Agent 7: Q04, D01, D03, DOC01

### Apply Exclusions

If configuration has `excluded_perspectives`:
- Remove those IDs from the selected list
- Adjust agent grouping if needed

---

## Phase 4: Parallel Perspective Review

### Step 4.1: Prepare Agent Launches

For each agent (based on mode):
- Determine assigned perspective ID(s)
- Build perspective file paths
- Prepare prompt

### Step 4.2: Launch Perspective Reviewers in Parallel

**Important**: Launch ALL agents in a SINGLE message (parallel execution).

For each agent, use Task tool:

**Prompt Template** (Deep Mode - 1 perspective):
```
Review code against perspective {PERSPECTIVE_ID}.

Session ID: {SESSION_ID}
Language: {language} (default: ja)

Inputs:
1. PR Summary: /tmp/claude-code-review-{SESSION_ID}/pr-summary.md
2. Perspective: ${CLAUDE_PLUGIN_ROOT}/references/perspectives/{category}/{ID}-{name}.md

Please:
1. Read PR summary
2. Read perspective guideline
3. Review changed files against perspective checklist
4. Assign confidence scores (0-100)
5. Report only issues with confidence ≥ 80
6. Write to /tmp/claude-code-review-{SESSION_ID}/reviews/perspective-{ID}.md

Agent type: perspective-reviewer
```

**Prompt Template** (Fast Mode - multiple perspectives):
```
Review code against perspectives {ID1}, {ID2}, {ID3}.

Session ID: {SESSION_ID}
Language: {language} (default: ja)

Inputs:
1. PR Summary: /tmp/claude-code-review-{SESSION_ID}/pr-summary.md
2. Perspectives:
   - ${CLAUDE_PLUGIN_ROOT}/references/perspectives/{category1}/{ID1}-{name1}.md
   - ${CLAUDE_PLUGIN_ROOT}/references/perspectives/{category2}/{ID2}-{name2}.md
   - ${CLAUDE_PLUGIN_ROOT}/references/perspectives/{category3}/{ID3}-{name3}.md

Please:
1. Read PR summary
2. Read all assigned perspectives
3. Review changed files against all perspective checklists
4. Assign confidence scores (0-100)
5. Report only issues with confidence ≥ 80
6. Write to /tmp/claude-code-review-{SESSION_ID}/reviews/perspective-{ID1}-{ID2}-{ID3}.md

Agent type: perspective-reviewer
```

### Step 4.3: Wait for All Agents

All perspective-reviewer agents run in parallel. Wait for all to complete.

---

## Phase 5: Consolidation

### Step 5.1: Launch Consolidator

Use Task tool to launch `consolidator` agent:

**Prompt**:
```
Consolidate review findings from multiple perspectives.

Session ID: {SESSION_ID}
Language: {language} (default: ja)

Please:
1. Read all files in /tmp/claude-code-review-{SESSION_ID}/reviews/perspective-*.md
2. Identify duplicate issues (same file, same line, similar description)
3. Merge duplicates (keep most detailed, combine perspective IDs)
4. Sort by severity (Critical 91-100, Important 80-90)
5. Write to /tmp/claude-code-review-{SESSION_ID}/consolidated.md

Do NOT filter or remove issues - only deduplicate.

Agent type: consolidator
```

---

## Phase 6: False Positive Verification

### Step 6.1: Read Consolidated Report and Analyze

Read `/tmp/claude-code-review-{SESSION_ID}/consolidated.md` to:
1. Count total issues
2. Extract issues with confidence 80-90 (need verification)
3. Extract Critical issues 91-100 (auto-verified)

### Step 6.2: Partition Issues for Parallel Verification

If there are confidence 80-90 issues:

**Determine parallelization**:
- 1-3 issues: 1 verifier
- 4-7 issues: 2-3 verifiers
- 8-14 issues: 4-5 verifiers
- 15+ issues: 7 verifiers (max)

**Partition strategy**:
Divide issues evenly among verifiers. Example with 20 issues and 7 verifiers:
- Verifier 1: Issues 1-3
- Verifier 2: Issues 4-6
- Verifier 3: Issues 7-9
- Verifier 4: Issues 10-12
- Verifier 5: Issues 13-15
- Verifier 6: Issues 16-18
- Verifier 7: Issues 19-20

### Step 6.3: Launch Verifiers in Parallel

**Important**: Launch ALL verifiers in a SINGLE message (parallel execution).

For each verifier, use Task tool:

**Prompt Template**:
```
Verify review findings to reduce false positives.

Session ID: {SESSION_ID}
Language: {language} (default: ja)
Assigned Issues: {ISSUE_NUMBERS} (e.g., "1-3" or "4, 7, 9")

Please:
1. Read /tmp/claude-code-review-{SESSION_ID}/consolidated.md
2. Extract your assigned issues (by number/title)
3. For each assigned issue with confidence 80-90:
   - Deep analysis of code context
   - Check if handled elsewhere
   - Use WebSearch/WebFetch for external validation when needed
   - Consult documentation and best practices
   - Test code if possible
   - Verify it's a real issue
4. Classify each as:
   - ✅ Verified (real issue)
   - ⚠️ Needs User Verification (uncertain)
   - ❌ False Positive (not an issue)
5. Write results to /tmp/claude-code-review-{SESSION_ID}/verifier-{N}.md

Use all available tools for thorough verification:
- WebSearch for known issues, best practices
- WebFetch for official documentation
- Bash for testing code snippets
- Skills for domain-specific knowledge

Agent type: verifier
```

### Step 6.4: Consolidate Verification Results

After all verifiers complete:

1. Read all `/tmp/claude-code-review-{SESSION_ID}/verifier-*.md` files
2. Combine verification results
3. Add Critical issues (91-100) as auto-verified
4. Sort by category:
   - Critical Issues (91-100) - all verified
   - Verified Issues (80-90) - confirmed real
   - Needs User Verification (80-90) - uncertain
   - False Positives (80-90) - confirmed not issues
5. Write final report to `/tmp/claude-code-review-{SESSION_ID}/verified.md`

---

## Phase 7: Results Presentation

### Step 7.1: Read Verified Report

Read `/tmp/claude-code-review-{SESSION_ID}/verified.md`

### Step 7.2: Present Results to User

Show summary:

```markdown
✅ **Code Review Complete**

**Session ID**: {SESSION_ID}
**Mode**: {Selected Mode}
**Perspectives Reviewed**: {Count}
**Review Files**: `/tmp/claude-code-review-{SESSION_ID}/`

## Results Summary

- 🔴 **Critical Issues**: {count} (Must fix)
- 🟡 **Important Issues**: {count} verified, {count} need your review
- ⚪ **False Positives**: {count} (can ignore)

## Files

- **Full Report**: `/tmp/claude-code-review-{SESSION_ID}/verified.md`
- **Consolidated Findings**: `/tmp/claude-code-review-{SESSION_ID}/consolidated.md`
- **PR Summary**: `/tmp/claude-code-review-{SESSION_ID}/pr-summary.md`
- **Individual Reviews**: `/tmp/claude-code-review-{SESSION_ID}/reviews/`

You can:
1. Read the verified report for detailed findings
2. Review the "Needs User Verification" items
3. Fix the verified issues
4. Re-run review after fixes
```

### Step 7.3: Ask for Next Action

Use AskUserQuestion to ask user what to do next:

**Question**: "What would you like to do with the review results?"

**Options**:

1. **View Critical Issues**
   - Label: "View Critical Issues"
   - Description: "See only the must-fix critical issues (confidence 91-100)"

2. **View All Issues**
   - Label: "View All Verified Issues"
   - Description: "See all verified issues (Critical + Important)"

3. **Review Uncertain Items**
   - Label: "Review Uncertain Items"
   - Description: "See items flagged as 'Needs User Verification' to decide if they're real"

4. **View Full Report**
   - Label: "View Full Report"
   - Description: "Read the complete verified.md file"

5. **Done**
   - Label: "Done"
   - Description: "I'll review the files myself"

### Step 7.4: Handle User Choice

Based on selection:

**View Critical Issues**: Read and display only Critical section from verified.md

**View All Issues**: Read and display Critical + Important sections

**Review Uncertain Items**: Read and display "Needs User Verification" section, ask user to verify each

**View Full Report**: Read and display full verified.md

**Done**: Provide final message with file paths

---

## Error Handling

### If PR Analyzer Fails

- Check if in git repository
- Check if any changes exist
- Provide helpful error message

### If No Issues Found

```markdown
✅ **No Issues Found**

The code review found no high-confidence issues (threshold: 80+).

This means:
- No critical bugs detected
- No security vulnerabilities found
- Code follows project standards
- All checked perspectives passed

**Note**: This doesn't guarantee perfection, but the {count} perspectives reviewed found no significant concerns.

Review files available at: `/tmp/claude-code-review-{SESSION_ID}/`
```

### If Configuration File Invalid

- Warn user about invalid YAML
- Fall back to defaults
- Continue with review

---

## Configuration Reference

Users can create `.claude/custom-code-review.local.md`:

```markdown
---
mode: standard  # light, standard, standard-fast, thorough, thorough-fast
language: ja    # ja (Japanese), en (English), pt (Portuguese), etc.
excluded_perspectives:
  - DOC01  # Example: Skip comment quality checks
  - PERF02 # Example: Skip accessibility checks
max_parallel_agents: 7
---

# Additional Instructions

{Any custom instructions for reviewers}
```

---

## Perspective ID Reference (Quick Lookup)

**Tier 1 (Must-have)**:
- P01: AI Agent Instructions
- C01: Bug Detection
- S01: Basic Vulnerabilities
- T01: Test Coverage
- Q01: Readability

**Tier 2 (Important)**:
- P02: Pattern Alignment
- C02: Functional Compliance
- C03: Edge Cases
- C04: Silent Failures
- C05: Exception Safety
- S02: Common Security Patterns
- S03: False Positive Filter
- S04: Precedent-Based Security
- S05: Adaptive Review Depth
- S06: Attacker Modeling
- S07: Security Regression
- S08: Blast Radius
- S09: Baseline Context
- S10: Red Flag Escalation
- T02: Test Quality
- T03: Error Handling Quality
- T04: Regression Tests
- T05: E2E Test Plan
- Q02: Complexity
- Q03: Code Smells
- Q04: Antipatterns
- Q05: YAGNI Check
- D01: Type Design
- D02: Architecture Patterns
- D03: API Design
- D04: Dependency Management
- D05: Data Flow
- D06: Fix Review
- DOC01: Comment Quality
- DOC02: Documentation Consistency
- PERF01: Performance
- PERF02: Accessibility
- PERF03: Resource Management
- CTX01: Git History Analysis
- CTX02: Codebase Understanding

---

## Usage Examples

**Quick review**:
```
/custom-code-review:review light
```

**Standard review (recommended)**:
```
/custom-code-review:review
# or
/custom-code-review:review standard
```

**Fast comprehensive review**:
```
/custom-code-review:review standard-fast
```

**Deep review**:
```
/custom-code-review:review thorough
```

**Very comprehensive review**:
```
/custom-code-review:review thorough-fast
```

---

## Notes

- **Parallel Execution**: Agents run in parallel for speed
- **Session Isolation**: Each review has unique session ID
- **Temporary Files**: All output in `/tmp/claude-code-review-{session-id}/`
- **Configurable**: Use `.local.md` for project-specific settings
- **False Positive Reduction**: Verifier checks borderline issues
- **Interactive**: User can explore results at their pace
