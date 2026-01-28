#!/usr/bin/env bun

/**
 * Copy Last Message Hook
 *
 * Stop フックとして動作し、最後のアシスタントメッセージをクリップボードにコピーする。
 * macOS (pbcopy), Linux (xclip/xsel), WSL (clip.exe) に対応。
 */

interface StopHookInput {
  session_id: string;
  transcript_path: string;
  hook_event_name: string;
}

interface TranscriptEntry {
  type: string;
  message: {
    content: Array<{ type: string; text?: string }>;
  };
}

async function extractLastAssistantMessage(
  transcriptPath: string,
): Promise<string | null> {
  try {
    const content = await Bun.file(transcriptPath).text();
    const lines = content.trim().split('\n');

    for (let i = lines.length - 1; i >= 0; i--) {
      try {
        const entry = JSON.parse(lines[i]) as TranscriptEntry;
        if (entry.type !== 'assistant') continue;

        const textContent = entry.message.content.find(
          (c) => c.type === 'text',
        );
        if (textContent?.text) return textContent.text;
      } catch {
        continue;
      }
    }

    return null;
  } catch (error) {
    console.error('Failed to read transcript:', error);
    return null;
  }
}

function getClipboardCommand(): string[] {
  const platform = process.platform;

  if (platform === 'darwin') {
    return ['pbcopy'];
  }

  if (platform === 'linux') {
    // WSL の場合
    if (process.env.WSL_DISTRO_NAME) {
      return ['clip.exe'];
    }
    // xclip が使えればそれを、なければ xsel を試す
    if (Bun.spawnSync(['which', 'xclip']).exitCode === 0) {
      return ['xclip', '-selection', 'clipboard'];
    }
    return ['xsel', '--clipboard', '--input'];
  }

  // フォールバック
  return ['pbcopy'];
}

async function main() {
  try {
    const input = JSON.parse(await Bun.stdin.text()) as StopHookInput;
    const message = await extractLastAssistantMessage(input.transcript_path);

    if (!message) {
      console.log('No assistant message with text found');
      return;
    }

    const clipboardCmd = getClipboardCommand();
    const proc = Bun.spawn(clipboardCmd, { stdin: 'pipe' });
    proc.stdin.write(message);
    proc.stdin.end();
    await proc.exited;

    console.log('Last message copied to clipboard');
  } catch (error) {
    console.error('Error:', error);
  }
}

main();
