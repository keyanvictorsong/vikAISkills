# GitHub Copilot AI Agent Power Settings

This folder contains enhanced permission settings for GitHub Copilot to give it more autonomy while maintaining safety guardrails.

## Settings Overview

### Auto-Approval Features
- **Global tool auto-approve**: Enabled
- **Terminal command auto-approve**: Enabled with intelligent filtering
- **Smart commit**: Enabled for git operations

### Safety Guardrails

The configuration blocks destructive commands while allowing most development operations:

**Blocked Commands:**
- File deletion: `rm`, `rmdir`, `del`, `rd`
- Process control: `kill`, `killall`
- System operations: `shutdown`, `reboot`, `format`, `mkfs`, `diskpart`
- Network downloads: `curl`, `wget`, `Invoke-WebRequest`, `Invoke-RestMethod`
- Code execution: `eval`, `Invoke-Expression`
- Privilege escalation: `sudo`
- Permission changes: `chmod`, `chown`, `Remove-Item`

### How to Use

1. Copy the contents of `copilot-settings.json`
2. Add to your VS Code settings (User or Workspace level)
3. Copilot will now have enhanced autonomy for development tasks

### Security Note

This configuration is designed to balance productivity with security. All destructive operations require manual approval.
