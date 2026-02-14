---
name: unity-setup-mcp
description: Check prerequisites and configure environment for Unity MCP
argument-hint: "[unity-project-path]"
allowed-tools: Bash, Read, Write
---

# Unity MCP Setup Verification

Verify prerequisites and help configure environment variables for Unity MCP integration.

**Note**: Unity MCP is automatically configured via this plugin's `.mcp.json`. This command helps with environment setup and verification.

## Instructions

### 1. Check Prerequisites

**Check uv installation**:
```bash
uv --version
```

If not installed:
- **macOS/Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows**: `winget install --id=astral-sh.uv -e`

### 2. Set Unity Project Path

Unity MCP requires `UNITY_PROJECT_PATH` environment variable.

**If user provided project-path argument**:
- Use that path
- Validate it's a Unity project (check for `Assets/` and `ProjectSettings/`)

**If no argument**:
- Check if current directory is a Unity project
- Ask user for Unity project path

**Set environment variable**:

**macOS/Linux (bash/zsh)**:
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export UNITY_PROJECT_PATH="/path/to/unity/project"' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell)**:
```powershell
# Set user environment variable
[Environment]::SetEnvironmentVariable("UNITY_PROJECT_PATH", "C:\path\to\unity\project", "User")
```

Inform user they may need to restart terminal/Claude Code for changes to take effect.

### 3. Verify MCP Server Status

Check if Unity MCP is available:

```bash
# This command shows all configured MCP servers
# Unity MCP should appear in the list automatically due to .mcp.json
```

Run `/mcp` slash command to verify Unity MCP server is listed.

### 4. Install Unity MCP Package (Optional)

If user wants to use Unity MCP's advanced features, guide them to install the Unity package:

**Option A: Package Manager UI**:
1. Open Unity Editor
2. Window > Package Manager
3. Click "+" > Add package from git URL
4. Enter: `https://github.com/CoplayDev/unity-mcp.git?path=/Packages/com.coplaydev.unity-mcp`

**Option B: OpenUPM**:
```bash
# If user has OpenUPM CLI installed
openupm add com.coplaydev.unity-mcp
```

Note: Unity package is optional for basic MCP functionality via uvx.

### 5. Verify Setup

Confirm everything is ready:

1. ✅ `uv` is installed
2. ✅ `UNITY_PROJECT_PATH` environment variable is set
3. ✅ Unity MCP appears in `/mcp` output
4. ✅ (Optional) Unity MCP package installed in Unity project

Suggest user try: "Get information about the current Unity scene"

## Troubleshooting

**"unity-mcp not found in /mcp output"**:
- Restart Claude Code to reload plugin configuration
- Check `.mcp.json` exists in plugin directory
- Verify `uv` is installed and in PATH

**"UNITY_PROJECT_PATH not set"**:
- Environment variable must be set before starting Claude Code
- Restart terminal/Claude Code after setting variable
- Verify with: `echo $UNITY_PROJECT_PATH` (bash/zsh) or `$env:UNITY_PROJECT_PATH` (PowerShell)

**Windows UTF-8 encoding issues**:
- Ensure PYTHONUTF8=1 is set (automatically included in .mcp.json)
- Avoid project paths with non-ASCII characters

## Success Criteria

Setup is complete when:
1. `/mcp` command shows `unity-mcp` server
2. `UNITY_PROJECT_PATH` environment variable is set correctly
3. User can interact with Unity via Claude Code
