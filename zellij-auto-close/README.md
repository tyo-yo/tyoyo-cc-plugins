# zellij-auto-close

Claude Code のセッション終了時に、Zellij のパネルを自動的に閉じるプラグイン。

## 仕組み

- `SessionEnd` フックを使用
- Zellij セッション内で実行されている場合のみ動作（`ZELLIJ_SESSION_NAME` 環境変数で検出）
- `zellij action close-pane` でカレントパネルを閉じる

## 参考

- [thoo/claude-code-zellij-status](https://github.com/thoo/claude-code-zellij-status) - Claude Code + Zellij 連携の参考実装
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) - SessionEnd フックの仕様
