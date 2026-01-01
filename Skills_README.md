# Global Skills Reference

This folder contains reusable automation tools for GitHub Copilot.

## 📁 Folder Structure

```
C:\WorkFolder\effeciency\skillsFolder\
├── browser_tools\
│   ├── browser_tool.py                  # Web browsing automation
│   ├── browser_automation_capabilities.md  # Documentation
│   └── azure_tools\
│       └── azure_automation.py          # Azure resource management
├── code_workspace_organization_principles.md
└── Skills_README.md                     # This file
```

## 🛠️ How to Use in Any Workspace

### Method 1: Copy `.github/copilot-instructions.md`
Copy the instructions file to any workspace's `.github/` folder.

### Method 2: Reference in Chat
Just tell Copilot:
> "Use the browser tool at C:\WorkFolder\effeciency\skillsFolder\browser_tools\browser_tool.py"

### Method 3: Add to VS Code Settings
Add to your User Settings (Ctrl+Shift+P → "Open User Settings JSON"):

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "text": "You have access to automation tools at C:\\WorkFolder\\effeciency\\skillsFolder\\"
    }
  ]
}
```

## 🔧 Tool Quick Reference

### Browser Tool
```powershell
cd C:\WorkFolder\effeciency\skillsFolder\browser_tools
python browser_tool.py search "query"
python browser_tool.py get_text "url"
python browser_tool.py screenshot "url"
```

### Azure Tool
```powershell
cd C:\WorkFolder\effeciency\skillsFolder\browser_tools\azure_tools
python azure_automation.py account
python azure_automation.py get_keys cognitive <name> <rg>

# Or use Azure CLI directly:
az cognitiveservices account keys list --name <name> --resource-group <rg>
az storage account keys list --account-name <name> --resource-group <rg>
```

## ➕ Adding New Skills

1. Create a new folder: `skillsFolder\new_tool\`
2. Add Python script with CLI interface
3. Update `.github\copilot-instructions.md` with usage examples
4. Copilot will automatically learn to use it!
