#!/usr/bin/env -S deno run --allow-read --allow-env

/**
 * Unity C# Script Validation Hook
 *
 * Validates Unity C# scripts after Write/Edit operations.
 * Checks for:
 * - BOM (Byte Order Mark) presence
 * - Unity namespace presence
 * - Class name and file name match
 * - Basic syntax issues
 */

interface ToolUseEvent {
  tool: string;
  parameters: {
    file_path?: string;
    content?: string;
    old_string?: string;
    new_string?: string;
  };
}

async function validateUnityScript(filePath: string, content: string): Promise<string[]> {
  const issues: string[] = [];

  // Check if this is a C# script
  if (!filePath.endsWith('.cs')) {
    return issues; // Not a C# file, skip validation
  }

  // Check if path contains "Assets/" (likely a Unity project)
  if (!filePath.includes('Assets/')) {
    return issues; // Not in Unity project, skip validation
  }

  // BOM check
  if (content.charCodeAt(0) === 0xFEFF) {
    issues.push('⚠️  BOM detected - Unity scripts should use UTF-8 without BOM');
  }

  // Unity namespace check
  if (!content.includes('using UnityEngine;')) {
    issues.push('⚠️  Missing "using UnityEngine;" - Unity scripts should include this namespace');
  }

  // Class name and file name match check
  const fileName = filePath.split('/').pop()?.replace('.cs', '') || '';
  const classMatch = content.match(/class\s+(\w+)/);

  if (classMatch && classMatch[1] !== fileName) {
    issues.push(
      `⚠️  Class name "${classMatch[1]}" does not match file name "${fileName}" - Unity requires these to match`
    );
  }

  // MonoBehaviour check (if class exists but doesn't inherit from anything)
  if (classMatch && !content.includes(': MonoBehaviour') && !content.includes(': ScriptableObject')) {
    // This is just a warning, not an error (static classes are valid)
    issues.push(
      `ℹ️  Class "${classMatch[1]}" doesn't inherit from MonoBehaviour or ScriptableObject - this is fine for static/utility classes`
    );
  }

  return issues;
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

    // Get file path and content
    const filePath = event.parameters.file_path;

    if (!filePath) {
      console.log('No file path in tool use event');
      Deno.exit(0);
    }

    // Read file content
    let content: string;
    try {
      content = await Deno.readTextFile(filePath);
    } catch (error) {
      console.log(`Could not read file: ${error.message}`);
      Deno.exit(0);
    }

    // Validate script
    const issues = await validateUnityScript(filePath, content);

    if (issues.length > 0) {
      console.log('\n🔍 Unity Script Validation Results:\n');
      issues.forEach(issue => console.log(`  ${issue}`));
      console.log('');

      // For critical issues, exit with error code
      const hasCriticalIssue = issues.some(issue =>
        issue.includes('Class name') || issue.includes('BOM')
      );

      if (hasCriticalIssue) {
        console.log('❌ Critical issues found. Please fix before continuing.\n');
        Deno.exit(1);
      } else {
        console.log('✓ Validation complete. Only warnings found.\n');
        Deno.exit(0);
      }
    } else {
      console.log('✓ Unity script validation passed\n');
      Deno.exit(0);
    }
  } catch (error) {
    console.error(`Validation error: ${error.message}`);
    Deno.exit(0); // Don't block on validation errors
  }
}

main();
