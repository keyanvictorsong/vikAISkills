# Claude AI Agent Power Settings

This folder contains enhanced permission settings for Claude Code to give it more autonomy for development tasks.

## Settings Overview

### Auto-Approved Commands

Claude can execute these commands without asking for permission:

**Version Control:**
- All git commands (`git:*`)

**Package Managers:**
- npm, yarn, pnpm
- pip, pip3

**Programming Languages:**
- node, python, python3
- go, cargo, rustc
- dotnet

**Build Tools:**
- make, cmake
- maven (mvn), gradle

**Container & Cloud:**
- docker, docker-compose, kubectl
- Azure CLI (az), AWS CLI (aws), Google Cloud (gcloud)
- terraform, ansible

**Testing Frameworks:**
- pytest, jest, mocha, vitest

**File Operations:**
- ls, cd, pwd, cat, echo
- mkdir, touch, cp, mv
- grep, find

**Development Tools:**
- GitHub CLI (gh)
- VS Code (code)
- npx, ng (Angular), vue

## How to Use

### For this repository:
Copy `claude-settings.json` to `.claude/settings.local.json` in your project root.

### For all repositories (user-level):
Copy `claude-settings.json` to `~/.claude/settings.json`

**Windows:** `%USERPROFILE%\.claude\settings.json`
**Mac/Linux:** `~/.claude/settings.json`

## Safety Notes

This configuration does NOT include auto-approval for:
- Destructive commands (`rm`, `del`, `shutdown`, etc.)
- Network downloads that could execute arbitrary code
- Privilege escalation commands

These commands will still require manual approval, maintaining safety while improving productivity.
