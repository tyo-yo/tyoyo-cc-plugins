# Piebald-AI: Security Review Command

**Source:** https://github.com/Piebald-AI/claude-code-system-prompts
**Stars:** 4310
**Type:** Agent Prompt

## Overview

Comprehensive security-focused review with sub-task workflow for vulnerability detection and false positive filtering.

## Key Features

- **Two-phase validation**: Initial detection + per-finding false positive filtering
- **High confidence threshold**: Only reports findings with confidence ≥8/10
- **Extensive exclusion rules**: 17+ hard exclusions to minimize false positives
- **Sub-task parallelization**: Uses parallel sub-tasks for efficient validation

## Security Categories

### Input Validation
- SQL injection
- Command injection
- XXE injection
- Template injection
- NoSQL injection
- Path traversal

### Authentication & Authorization
- Authentication bypass
- Privilege escalation
- Session management flaws
- JWT vulnerabilities
- Authorization bypasses

### Crypto & Secrets
- Hardcoded credentials
- Weak cryptographic algorithms
- Improper key management
- Randomness issues
- Certificate validation bypasses

### Injection & Code Execution
- Remote code execution via deserialization
- Pickle injection
- YAML deserialization
- Eval injection
- XSS (reflected, stored, DOM-based)

### Data Exposure
- Sensitive data logging
- PII handling violations
- API data leakage
- Debug information exposure

## Methodology

### Phase 1: Repository Context Research
- Identify security frameworks in use
- Examine secure coding patterns
- Find sanitization patterns
- Understand threat model

### Phase 2: Comparative Analysis
- Compare against established patterns
- Identify deviations
- Flag inconsistent security
- Note new attack surfaces

### Phase 3: Vulnerability Assessment
- Examine modified files
- Trace data flows
- Check privilege boundaries
- Identify injection points

## False Positive Filtering

### Hard Exclusions (17 patterns)

1. Denial of Service vulnerabilities
2. Secrets stored on disk (if otherwise secured)
3. Rate limiting concerns
4. Memory/CPU exhaustion
5. Input validation without proven impact
6. GitHub Action workflow sanitization (unless clearly exploitable)
7. Lack of hardening measures
8. Theoretical race conditions
9. Outdated third-party libraries
10. Memory safety in memory-safe languages (Rust, etc.)
11. Unit test files
12. Log spoofing
13. SSRF with path-only control
14. User content in AI prompts
15. Regex injection
16. Regex DOS
17. Documentation issues

### Precedents

- Logging high-value secrets = vulnerability
- UUIDs assumed unguessable
- Environment variables/CLI flags = trusted
- Resource leaks = not valid
- Subtle web vulnerabilities (tabnabbing, XS-Leaks) = only if high confidence
- React/Angular = generally XSS-safe (unless using unsafe methods)
- GitHub Actions = mostly not exploitable
- Client-side auth checks = not required (server-side responsibility)
- Medium findings = only if obvious and concrete
- Notebook vulnerabilities = only if concrete attack path
- Logging non-PII = not a vulnerability
- Shell command injection = only if concrete untrusted input path

## Severity Guidelines

- **HIGH**: Directly exploitable → RCE, data breach, auth bypass
- **MEDIUM**: Requires conditions but significant impact
- **LOW**: Defense-in-depth or lower impact

## Confidence Scoring

- 0.9-1.0: Certain exploit path
- 0.8-0.9: Clear vulnerability with known exploitation
- 0.7-0.8: Suspicious pattern needing conditions
- <0.7: Don't report (too speculative)

## Workflow

1. Create sub-task to identify vulnerabilities
2. For each finding, create parallel sub-tasks for false positive filtering
3. Filter out findings with confidence <8
4. Output markdown report only

## Output Format

```markdown
# Vuln 1: XSS: `foo.py:42`

* Severity: High
* Description: User input from `username` parameter is directly interpolated into HTML without escaping
* Exploit Scenario: Attacker crafts URL like /bar?q=<script>alert(document.cookie)</script> to execute JavaScript
* Recommendation: Use Flask's escape() function or Jinja2 templates with auto-escaping
```

## Review Aspects

- Exploitable vulnerabilities only
- Concrete attack paths
- High-confidence findings
- No theoretical issues
- No false positives
