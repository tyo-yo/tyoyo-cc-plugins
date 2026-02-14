---
name: unity-mcp-assistant
description: |
  Unity game development with MCP integration.
  Use when user wants to:
  - "create Unity scenes"
  - "modify GameObjects"
  - "generate Unity scripts"
  - "debug Unity projects"
  - "manage Unity assets"
  - "automate Unity tasks"
  - "Unity MCP操作"
  - "Unityシーン作成"
  - "Unityスクリプト生成"
allowed-tools: Bash(command:*), Read, Write, Glob, Grep
---

# Unity MCP Assistant

Unity MCPを使ったUnity Editor操作の専門スキル。Claude CodeからUnityプロジェクトを直接操作する。

## Prerequisites Check

Before starting Unity operations, verify:

1. **Unity MCP Server Status**
   - Run `claude mcp list` to check if Unity-MCP is connected
   - Ensure Unity Editor is running with the MCP plugin installed
   - Verify MCP connection is active (HTTP or Stdio transport)

2. **Unity Project State**
   - Confirm current Unity project path
   - Check if project is open in Unity Editor
   - Verify no ongoing Play mode or build process

3. **MCP Tools Availability**
   - Confirm access to core tools: manage_scene, manage_gameobject, create_script, manage_asset
   - Check batch_execute availability for performance optimization

## Core Workflows

### 1. Scene Manipulation (シーン操作)

**基本フロー**:
1. Read current scene state with `manage_scene: get_scene_info`
2. Create or modify scene elements with `manage_gameobject`
3. Verify changes with screenshot or hierarchy query
4. Ask user for confirmation before destructive operations

**Example Operations**:
- Create new scene: `manage_scene: create`
- Add GameObject: `manage_gameobject: create`
- Modify transforms: `manage_gameobject: modify`
- Apply materials: `manage_material: apply`

### 2. Script Generation (スクリプト生成)

**段階的アプローチ**:
1. Understand user requirements clearly
2. Generate minimal working script first
3. Review script structure (class name matches file name)
4. Create script with proper Unity namespaces
5. Verify no BOM in UTF-8 encoding

**Script Template Pattern**:
```csharp
using UnityEngine;

public class ClassName : MonoBehaviour
{
    // Public fields for Inspector

    void Start()
    {
        // Initialization
    }

    void Update()
    {
        // Per-frame logic
    }
}
```

### 3. Asset Management (アセット管理)

**Best Practices**:
- Use `manage_asset: import` for external assets
- Organize by feature (Assets/Features/Player/, Assets/Features/Enemy/)
- Never delete Assets folder directly
- Use batch_execute for multiple asset operations

### 4. Batch Operations (バッチ処理)

**Performance Optimization**:
- Use `batch_execute` tool for 10-100x speedup
- Group related operations together
- Maximum efficiency for bulk GameObject creation, material application, hierarchy modifications

**Example Batch Request**:
```json
[
  {"tool": "manage_gameobject", "action": "create", "name": "Cube1"},
  {"tool": "manage_gameobject", "action": "create", "name": "Cube2"},
  {"tool": "manage_material", "action": "apply", "target": "Cube1"}
]
```

## Best Practices

### Stepwise Approach (段階的アプローチ)

Follow Josh English's recommended workflow:

1. **Start with Read-Only Tools**: Query scene state, hierarchy, assets before making changes
2. **Train Agent to Ask Before Acting**: Always explain what will change and wait for user approval
3. **Demand Evidence as Habit**: Verify changes with screenshots, console output, hierarchy queries
4. **Default to Playmode and Console Inspection**: Test changes in Play mode, check for errors
5. **Gate Sophisticated Changes Behind Confirmation**: Complex refactoring requires explicit approval
6. **Maintain Small, Reviewable Edits**: Keep changes focused and understandable
7. **Expand Autonomy Only When Verification Surface Supports**: Increase automation only when validation is robust

### Safety Guards

**Critical Constraints**:
- **DO NOT** delete Assets folder or critical project files
- **DO NOT** perform major refactoring without user confirmation
- **DO NOT** modify multiple scripts simultaneously without review
- **ALWAYS** create backup-worthy changes in small increments
- **ALWAYS** verify script syntax before applying (class name = file name, proper namespaces)

**Confirmation Required Before**:
- Deleting any assets or GameObjects
- Modifying existing scripts (unless explicitly requested)
- Changing scene hierarchy significantly
- Applying materials that may override existing settings

### Performance Considerations

**Use batch_execute when**:
- Creating 3+ GameObjects
- Applying materials to multiple objects
- Modifying transforms in bulk
- Importing multiple assets

**Paging Settings** (default):
- page_size: 50
- max_nodes: 1000
- Use summary-first approach (get overview, then details as needed)

### Japanese Environment (日本語環境)

**文字コード**:
- All scripts: UTF-8 without BOM
- JSON files: UTF-8 without BOM
- Unity Editor: UTF-8 default
- Python MCP Server: Set `PYTHONUTF8=1` environment variable

**Path Constraints**:
- Avoid spaces in paths (use `MyProjects` not `My Projects`)
- Windows: Use recommended uv.exe path `%LOCALAPPDATA%\Microsoft\WinGet\Links\uv.exe`
- macOS/Linux: Standard uv installation paths work

**Error Messages**:
- Unity console errors may be in Japanese
- Translate error messages if needed for debugging
- Common errors: BOM detection, path encoding issues, null reference exceptions

## Troubleshooting

### MCP Connection Issues

**Symptoms**: Tools not available, timeout errors

**Solutions**:
1. Check Unity Editor is running and MCP plugin is installed
2. Verify `claude mcp list` shows Unity-MCP as connected
3. Restart MCP server: `claude mcp restart Unity-MCP`
4. Check HTTP endpoint (http://localhost:8080/mcp) or Stdio transport
5. Review MCP timeout setting (default: 720000ms)

### Script Generation Errors

**Symptoms**: Compile errors, null references, class name mismatches

**Solutions**:
1. Verify class name matches file name exactly (case-sensitive)
2. Check UTF-8 encoding without BOM
3. Ensure proper Unity namespaces (using UnityEngine;)
4. Review MonoBehaviour inheritance for component scripts
5. Validate field types and Unity API usage

### Performance Slowdowns

**Symptoms**: Slow operations, individual tool calls taking too long

**Solutions**:
1. Switch to batch_execute for bulk operations
2. Reduce page_size for hierarchy queries
3. Use summary-first approach (overview before details)
4. Limit max_nodes for large scenes
5. Close unnecessary Unity windows/tabs

### Asset Import Failures

**Symptoms**: Assets not appearing, import errors

**Solutions**:
1. Verify asset path is within Assets/ folder
2. Check file format is supported (PNG, JPG for sprites; FBX, OBJ for 3D)
3. Ensure no path encoding issues (UTF-8, no special characters)
4. Use AssetDatabase.Refresh after import
5. Check Unity console for import warnings/errors

## Reference Links

- [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp) - Primary MCP implementation
- [Unity MCP Documentation](https://github.com/CoplayDev/unity-mcp/blob/main/README.md)
- [Unity Scripting API](https://docs.unity3d.com/ScriptReference/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## Summary

This skill enables Claude Code to operate Unity Editor through MCP. Follow stepwise approach, prioritize safety, use batch operations for performance, and always verify changes before committing. Support both English and Japanese workflows, with special attention to encoding and path issues.
