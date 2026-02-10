# Veraticus: CC-Tools

**Source:** https://github.com/Veraticus/cc-tools
**Stars:** 46
**Type:** Hooks + Go Tool

## Overview

Claude Code tools written in Go. Provides hooks and utilities for Claude Code workflows.

## Architecture

Built in Go with:
- Command-line interface
- Hook support
- Configuration management (TOML/YAML)
- golangci-lint integration

## Components

### Configuration
- `example-config.toml`
- `example-config.yaml`
- Flexible configuration options

### Reference Documentation
- `reference/statusline.md` - Status line documentation
- `reference/hooks.md` - Hook system documentation

### Development
- Makefile for build automation
- Flake.nix for Nix support
- golangci-lint for code quality

## Features

Based on directory structure:
- Hook integration
- Status line customization
- Go-based tooling
- Configuration flexibility

## Review Aspects

- Go-based implementation
- Hook system
- Configuration management
- Command-line interface
- Linting integration

Note: Limited documentation in README. Main features inferred from code structure.
