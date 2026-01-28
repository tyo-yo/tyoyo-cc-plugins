#!/usr/bin/env bun
/**
 * CCBUT Auto-Commit Hook
 *
 * Claude Code の Stop フック。セッション終了時に変更を自動コミット。
 * - GitButler (but コマンド) でブランチ管理・コミット
 * - Claude Haiku でコミットタイトルを自動生成
 *
 * 環境変数:
 *   CCBUT_BRANCH             - コミット先ブランチ名（未設定の場合はスキップ）
 *   CCBUT_MESSAGE_MAX_LENGTH - タイトル生成に使うメッセージ最大長（デフォルト: 2000）
 *   CCBUT_TITLE_PROMPT       - コミットタイトル生成プロンプト
 *   CCBUT_COMMIT_FOOTER      - コミットメッセージのフッター
 *   CCBUT_LOG_FILE           - ログファイルパス（デフォルト: /tmp/ccbut-auto-commit.log）
 */
import { appendFileSync } from 'fs';

// ========================================
// 定数
// ========================================

const LOG_FILE = process.env.CCBUT_LOG_FILE || '/tmp/ccbut-auto-commit.log';
const MESSAGE_MAX_LENGTH = parseInt(
  process.env.CCBUT_MESSAGE_MAX_LENGTH || '2000',
  10,
);

const COMMIT_TITLE_PROMPT =
  process.env.CCBUT_TITLE_PROMPT ||
  `以下のメッセージを50文字以内の日本語で要約してください。形式は「feat: 〜」「fix: 〜」「refactor: 〜」などのConventional Commits形式を使用してください。タイトルのみを出力し、説明や追加情報は含めないでください。必ず1行で出力してください。余計なコードブロックは不要です。`;

const COMMIT_FOOTER =
  process.env.CCBUT_COMMIT_FOOTER ||
  `\n\n---\n\n*Auto-committed by Claude Code Stop hook*\nCo-Authored-By: Claude <noreply@anthropic.com>`;

// ========================================
// 型定義
// ========================================

interface StopHookInput {
  session_id: string;
  transcript_path: string;
  hook_event_name: string;
}

interface TranscriptEntry {
  type: string;
  message: {
    content: Array<{
      type: string;
      text?: string;
      name?: string;
      input?: {
        file_path?: string;
      };
    }>;
  };
}

interface TranscriptData {
  lastMessage: string | null;
  editedFiles: Set<string>;
}

// ========================================
// ユーティリティ
// ========================================

function log(message: string): void {
  const timestamp = new Date().toISOString();
  appendFileSync(LOG_FILE, `[${timestamp}] ${message}\n`);
}

// ========================================
// トランスクリプト処理
// ========================================

/**
 * トランスクリプトファイルから必要な情報を一度に抽出
 */
async function parseTranscript(
  transcriptPath: string,
): Promise<TranscriptData> {
  try {
    const content = await Bun.file(transcriptPath).text();
    const lines = content.trim().split('\n');

    let lastMessage: string | null = null;
    const editedFiles = new Set<string>();

    for (let i = lines.length - 1; i >= 0; i--) {
      try {
        const entry = JSON.parse(lines[i]) as TranscriptEntry;

        if (!lastMessage && entry.type === 'assistant') {
          const textContent = entry.message.content.find(
            (c) => c.type === 'text',
          );
          if (textContent?.text) {
            lastMessage = textContent.text;
          }
        }

        if (entry.type === 'assistant' && entry.message.content) {
          for (const content of entry.message.content) {
            if (
              content.type === 'tool_use' &&
              (content.name === 'Edit' || content.name === 'Write') &&
              content.input?.file_path
            ) {
              editedFiles.add(content.input.file_path);
            }
          }
        }

      } catch (error) {
        log(`Failed to parse line ${i}: ${error}`);
        continue;
      }
    }

    log(`Edited files in this session: ${editedFiles.size}`);
    return { lastMessage, editedFiles };
  } catch (error) {
    log(`Failed to read transcript: ${error}`);
    return { lastMessage: null, editedFiles: new Set() };
  }
}

// ========================================
// Git / GitButler 操作
// ========================================

function getChangedFiles(): string[] {
  const result = Bun.spawnSync(['git', 'status', '--porcelain'], {
    stdout: 'pipe',
  });
  if (result.exitCode !== 0) {
    log('Git status failed');
    return [];
  }

  return result.stdout
    .toString()
    .trim()
    .split('\n')
    .filter((line) => line.trim())
    .map((line) => line.slice(3).trim())
    .filter(Boolean);
}

function ensureBranch(stackName: string): boolean {
  const result = Bun.spawnSync(['but', 'branch', 'new', stackName], {
    stderr: 'ignore',
  });
  return result.exitCode === 0 || result.exitCode === 1;
}

function assignFilesToBranch(files: string[], stackName: string): void {
  const statusResult = Bun.spawnSync(['but', 'status'], { stdout: 'pipe' });
  if (statusResult.exitCode !== 0) {
    log('Failed to get but status');
    return;
  }

  const statusOutput = statusResult.stdout.toString();

  for (const file of files) {
    const lines = statusOutput.split('\n');
    let fileId: string | null = null;

    for (const line of lines) {
      if (line.includes(file)) {
        const match = line.match(/^[○●]\s+([a-z0-9]+)\s+/);
        if (match) {
          fileId = match[1];
          break;
        }
      }
    }

    if (fileId) {
      const result = Bun.spawnSync(['but', 'rub', fileId, stackName], {
        stderr: 'pipe',
      });
      if (result.exitCode !== 0) {
        log(
          `Failed to assign ${file} (ID: ${fileId}): ${result.stderr.toString()}`,
        );
      }
    } else {
      log(`File ID not found for: ${file}`);
    }
  }
}

// ========================================
// ブランチ名決定
// ========================================

function determineBranchName(): string | null {
  if (process.env.CCBUT_BRANCH) {
    log(`Using CCBUT_BRANCH: ${process.env.CCBUT_BRANCH}`);
    return process.env.CCBUT_BRANCH;
  }

  log('CCBUT_BRANCH not set, skipping auto-commit');
  return null;
}

// ========================================
// コミットタイトル生成
// ========================================

async function generateCommitTitle(message: string): Promise<string> {
  const fallback = message.split('\n')[0].trim();

  const prompt = `${COMMIT_TITLE_PROMPT}

メッセージ:
${message.substring(0, MESSAGE_MAX_LENGTH)}`;

  try {
    const claudePath =
      Bun.which('claude') || `${process.env.HOME}/.claude/local/claude`;
    const result = Bun.spawnSync(
      [claudePath, '--model', 'haiku', '-p', prompt],
      {
        stdout: 'pipe',
        stderr: 'pipe',
        cwd: '/tmp',
      },
    );

    if (result.exitCode === 0) {
      const title = result.stdout
        .toString()
        .trim()
        .split('\n')[0]
        .replace(/^["']|["']$/g, '')
        .trim();

      log(`Generated title: ${title}`);
      return title;
    }

    log(`Title generation failed (exit ${result.exitCode}), using fallback`);
    return fallback;
  } catch (error) {
    log(`Title generation error: ${error}`);
    return fallback;
  }
}

// ========================================
// コミット作成
// ========================================

async function createCommit(
  message: string,
  stackName: string,
): Promise<boolean> {
  const title = await generateCommitTitle(message);

  const commitMessage = `${title}\n\n${message}${COMMIT_FOOTER}`;

  const result = Bun.spawnSync(
    ['but', 'commit', '-m', commitMessage, stackName],
    {
      stdout: 'inherit',
      stderr: 'inherit',
    },
  );

  return result.exitCode === 0;
}

// ========================================
// メインフロー
// ========================================

async function main(): Promise<void> {
  try {
    log('=== Hook started ===');

    const inputText = await Bun.stdin.text();
    const input = JSON.parse(inputText) as StopHookInput;
    log(`Session: ${input.session_id}`);
    log(`Transcript: ${input.transcript_path}`);

    const { lastMessage, editedFiles } = await parseTranscript(
      input.transcript_path,
    );
    if (!lastMessage) {
      log('No message found, skipping');
      return;
    }
    log(`Message: ${lastMessage.substring(0, 100)}...`);

    const allChangedFiles = getChangedFiles();
    const changedFiles = allChangedFiles.filter((file) => {
      const absolutePath = file.startsWith('/')
        ? file
        : `${process.cwd()}/${file}`;
      return editedFiles.has(file) || editedFiles.has(absolutePath);
    });

    log(
      `Total changed files: ${allChangedFiles.length}, Session edited files: ${changedFiles.length}`,
    );
    if (changedFiles.length === 0) {
      log('No changes, skipping');
      return;
    }

    const branchName = determineBranchName();
    if (!branchName) {
      log('Branch name not determined, skipping');
      return;
    }
    if (!ensureBranch(branchName)) {
      log('Failed to ensure branch');
      return;
    }

    assignFilesToBranch(changedFiles, branchName);

    const finalChangedFiles = getChangedFiles();
    if (finalChangedFiles.length === 0) {
      log('No changes after file assignment, skipping commit');
      return;
    }

    const success = await createCommit(lastMessage, branchName);
    if (success) {
      log(`Committed ${finalChangedFiles.length} file(s) to ${branchName}`);
    } else {
      log('Commit failed');
    }
  } catch (error) {
    log(`Error: ${error}`);
  }
}

main();
