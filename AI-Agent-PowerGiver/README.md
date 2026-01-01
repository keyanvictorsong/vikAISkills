# AI Agent PowerGiver

This repository contains enhanced permission configurations for popular AI coding assistants, giving them more autonomy while maintaining essential safety guardrails.

## Overview

Modern AI coding assistants can be significantly more productive when given appropriate permissions to execute common development commands automatically. This repository provides battle-tested configurations that balance autonomy with safety.

## Included Configurations

### 1. GitHub Copilot (`copilot-ai-agent/`)
Enhanced VS Code settings for GitHub Copilot with:
- Auto-approval for most terminal commands
- Smart blocking of destructive operations
- Network security controls

### 2. Claude Code (`claude-ai-agent/`)
Permission settings for Claude Code with auto-approval for:
- Version control (git)
- Package managers (npm, pip, etc.)
- Build tools and testing frameworks
- Container and cloud tools
- Common file operations

## Quick Start

Choose your AI assistant and follow the setup instructions in the respective folder:
- [Copilot Setup](./copilot-ai-agent/README.md)
- [Claude Code Setup](./claude-ai-agent/README.md)

## Safety Philosophy

Both configurations follow these principles:
1. **Auto-approve common dev tasks** - git, package managers, builds, tests
2. **Block destructive operations** - file deletion, system shutdown, format operations
3. **Control network access** - prevent arbitrary code download/execution
4. **No privilege escalation** - sudo, chmod, chown require approval

## Benefits

- **Faster iteration**: AI can run tests, build, and commit without constant approval prompts
- **Better flow**: Stay in the coding mindset instead of approving every command
- **Maintained safety**: Critical operations still require your explicit approval
- **Consistent across projects**: Use the same settings everywhere

## Additional Resources

- [AI Skills Documentation](./Skills_README.md)
- [Workspace Organization Principles](./code_workspace_organization_principles.md)
- [Browser Automation Tools](./browser_tools/)

## Contributing

Feel free to submit PRs with:
- Additional AI assistant configurations
- Improved safety rules
- Documentation enhancements

## License

MIT License - Use freely in your projects

---

**Note**: These configurations are opinionated and designed for experienced developers who understand the commands they're auto-approving. Review and adjust based on your security requirements.
