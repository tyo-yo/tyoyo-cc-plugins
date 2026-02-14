#!/usr/bin/env -S deno run --allow-read --allow-env

/**
 * Pre-Destructive Check Hook
 *
 * Warns before potentially destructive Write/Edit operations on Unity files.
 * Checks for:
 * - Critical Unity files (ProjectSettings, Packages/manifest.json)
 * - Scene files (.unity)
 * - Prefab files (.prefab)
 * - Large-scale modifications
 */

interface ToolUseEvent {
  tool: string;
  parameters: {
    file_path?: string;
    content?: string;
    old_string?: string;
    new_string?: string;
    replace_all?: boolean;
  };
}

function isDestructiveOperation(event: ToolUseEvent): {
  isDestructive: boolean;
  reason: string;
} {
  const filePath = event.parameters.file_path || '';

  // Critical Unity project files
  const criticalPaths = [
    'ProjectSettings/',
    'Packages/manifest.json',
    'Packages/packages-lock.json',
    'Assets/csc.rsp',
    'Assets/mcs.rsp',
  ];

  for (const criticalPath of criticalPaths) {
    if (filePath.includes(criticalPath)) {
      return {
        isDestructive: true,
        reason: `Modifying critical Unity file: ${criticalPath}`,
      };
    }
  }

  // Scene and Prefab files (binary or complex YAML)
  if (filePath.endsWith('.unity')) {
    return {
      isDestructive: true,
      reason: 'Modifying Unity scene file (.unity) - use Unity MCP tools instead',
    };
  }

  if (filePath.endsWith('.prefab')) {
    return {
      isDestructive: true,
      reason: 'Modifying Unity prefab file (.prefab) - use Unity MCP tools instead',
    };
  }

  // Assets folder deletion check
  if (filePath.includes('/Assets/') && event.tool === 'Write' && !event.parameters.content) {
    return {
      isDestructive: true,
      reason: 'Potential deletion of Assets folder contents',
    };
  }

  // Replace all flag (may affect many occurrences)
  if (event.parameters.replace_all === true) {
    return {
      isDestructive: true,
      reason: 'Using replace_all flag - may modify many occurrences',
    };
  }

  return { isDestructive: false, reason: '' };
}

async function main() {
  try {
    // Read tool use event from stdin (provided by Claude Code)
    const eventJson = Deno.env.get('TOOL_USE_EVENT');

    if (!eventJson) {
      console.log('No tool use event provided');
      Deno.exit(0);
    }

    const event: ToolUseEvent = JSON.parse(eventJson);

    // Check if operation is destructive
    const check = isDestructiveOperation(event);

    if (check.isDestructive) {
      console.log('\n⚠️  Destructive Operation Detected\n');
      console.log(`Reason: ${check.reason}\n`);
      console.log('This operation may have significant impact on your Unity project.');
      console.log('Please ensure you have:\n');
      console.log('  1. Committed recent changes to version control');
      console.log('  2. Reviewed the intended changes carefully');
      console.log('  3. Confirmed this operation is necessary\n');
      console.log('Recommendation: Use Unity MCP tools for Unity-specific files.\n');

      // Don't block the operation, just warn
      // User can proceed if they understand the risks
      Deno.exit(0);
    } else {
      // Not destructive, proceed silently
      Deno.exit(0);
    }
  } catch (error) {
    console.error(`Pre-check error: ${error.message}`);
    Deno.exit(0); // Don't block on errors
  }
}

main();
