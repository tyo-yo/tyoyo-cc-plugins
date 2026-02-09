# superwhisper-transcribe

SuperWhisper を使って音声ファイルを CLI から文字起こしするスキル。

## 仕組み

macOS の `open -a superwhisper` コマンドで音声ファイルを SuperWhisper に渡すと、アプリがバックグラウンドで文字起こしを実行する。結果は SQLite データベースに保存されるので、`sqlite3` コマンドで取得できる。

## 前提条件

- [SuperWhisper](https://superwhisper.com/) がインストール済み
- **Pro プラン**が必要（ファイルからの文字起こしは Pro 限定機能）
- SuperWhisper が起動中であること
