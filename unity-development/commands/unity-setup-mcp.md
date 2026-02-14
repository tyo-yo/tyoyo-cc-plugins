---
name: unity-setup-mcp
description: Setup Unity MCP server and connect to Claude Code
argument-hint: "[project-path]"
allowed-tools: Bash, Read, Write
---

# Unity MCP Setup Command

Setup Unity MCP server and configure Claude Code integration.

## Instructions

Execute the following steps to set up Unity MCP:

### 1. Detect Operating System

Determine the user's OS (macOS, Linux, or Windows) to provide appropriate installation commands.

### 2. Install Prerequisites

**macOS/Linux**:
- Check if `uv` package manager is installed: `uv --version`
- If not installed, install via: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Verify Unity 6.2+ is installed: Check `/Applications/Unity/Hub/Editor/` or ask user

**Windows**:
- Check if `uv.exe` is installed: `uv --version`
- If not installed, install via WinGet: `winget install --id=astral-sh.uv -e`
- Recommended path: `%LOCALAPPDATA%\Microsoft\WinGet\Links\uv.exe`
- Verify Unity 6.2+ is installed: Check `C:\Program Files\Unity\Hub\Editor\` or ask user

### 3. Install Unity MCP Package

Explain to user they need to add Unity MCP package to their Unity project via one of:

**Option A: OpenUPM (Recommended)**:
```bash
# Add via Package Manager > Add package by name
# Package name: com.coplaydev.unity-mcp
```

**Option B: Git URL**:
```bash
# Add via Package Manager > Add package from git URL
# URL: https://github.com/CoplayDev/unity-mcp.git?path=/Packages/com.coplaydev.unity-mcp
```

Provide clear instructions for Unity Editor's Package Manager UI.

### 4. Configure MCP Server in Claude Code

**For macOS/Linux (HTTP transport - recommended)**:

Ask user to confirm Unity Editor is running, then configure MCP:

```bash
# Check if Unity MCP HTTP endpoint is accessible
curl -s http://localhost:8080/mcp > /dev/null 2>&1 && echo "Unity MCP HTTP server is running" || echo "Unity MCP HTTP server is not accessible. Please ensure Unity Editor is running with MCP plugin installed."

# Add Unity MCP to Claude Code configuration
# User needs to manually edit ~/.claude.json or use Claude Desktop settings
```

Provide the JSON configuration for user to add:

```json
{
  "mcpServers": {
    "unity-mcp": {
      "url": "http://localhost:8080/mcp",
      "timeout": 720000
    }
  }
}
```

**For macOS/Linux (Stdio transport - legacy)**:

```json
{
  "mcpServers": {
    "unity-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "mcpforunityserver",
        "mcp-for-unity",
        "--transport",
        "stdio"
      ],
      "env": {
        "MCP_TOOL_TIMEOUT": "720000"
      }
    }
  }
}
```

**For Windows (Stdio transport)**:

```json
{
  "mcpServers": {
    "unity-mcp": {
      "command": "C:\\Users\\YourName\\AppData\\Local\\Microsoft\\WinGet\\Links\\uv.exe",
      "args": [
        "--from",
        "mcpforunityserver",
        "mcp-for-unity",
        "--transport",
        "stdio"
      ],
      "env": {
        "MCP_TOOL_TIMEOUT": "720000",
        "PYTHONUTF8": "1"
      }
    }
  }
}
```

Note: Replace `YourName` with actual Windows username.

### 5. Verify Connection

After configuration, verify MCP connection:

```bash
# List configured MCP servers
claude mcp list

# Check Unity-MCP is in the list and connected
# If not connected, restart Claude Code or check Unity Editor status
```

Test basic MCP operation:

```bash
# This should work if MCP is properly configured
# User can try: "Get current Unity scene information"
# This will use manage_scene tool internally
```

### 6. Provide Setup Completion Summary

Display a completion message with:

1. Confirmation of installed components
2. MCP server status (connected/not connected)
3. Next steps: "Try creating a GameObject with: 'Create a Cube in the current Unity scene'"
4. Troubleshooting link if connection failed

## Error Handling

**If uv installation fails**:
- Provide alternative installation methods (Homebrew, manual download)
- Link to official uv documentation

**If Unity MCP package installation fails**:
- Verify Unity 6.2+ is installed
- Check Unity Package Manager logs
- Suggest manual installation via .unitypackage file

**If MCP connection fails**:
- Verify Unity Editor is running
- Check if MCP HTTP endpoint is accessible (http://localhost:8080/mcp)
- Review Unity console for MCP plugin errors
- Suggest restarting Unity Editor

**If path/encoding issues on Windows**:
- Ensure PYTHONUTF8=1 is set
- Verify uv.exe path is correct
- Check for spaces in project path (recommend moving project if needed)

## Success Criteria

Setup is successful when:

1. `uv` is installed and accessible
2. Unity MCP package is added to Unity project
3. Unity Editor is running with MCP plugin active
4. `claude mcp list` shows Unity-MCP as connected
5. Basic MCP operation (e.g., get_scene_info) works

## Important Notes

- HTTP transport is recommended over Stdio for better performance and reliability
- Stdio transport may be deprecated in future versions
- Timeout of 720000ms (12 minutes) is recommended for large projects
- Windows users must set PYTHONUTF8=1 for proper encoding
- Project paths with spaces may cause issues on some platforms
