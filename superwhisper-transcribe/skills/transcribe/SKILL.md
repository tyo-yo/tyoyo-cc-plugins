---
name: transcribe
description: 音声ファイルの文字起こし。"音声を文字起こし", "transcribe audio", "音声認識", "文字起こしして", "wavを文字に", "音声ファイルをテキストに" のような指示で使用。
allowed-tools: Bash(open:*), Bash(sqlite3:*)
---

# 音声ファイル文字起こし（SuperWhisper）

SuperWhisper に音声ファイルを渡して文字起こしし、結果をテキストとして取得する。

## 手順

### 1. 文字起こし開始

```bash
open -a superwhisper /path/to/audio.wav
```

対応形式: wav, m4a, mp3, aiff など（`public.audio` / `public.movie` 全般）

### 2. 結果取得（ポーリング）

```bash
while true; do
  RESULT=$(sqlite3 ~/Library/Application\ Support/superwhisper/database/superwhisper.sqlite \
    "SELECT f.rawResult FROM recording r JOIN recording_fts f ON r.id = f.recordingId WHERE r.fromFile = 1 ORDER BY r.datetime DESC LIMIT 1;")
  [ -n "$RESULT" ] && echo "$RESULT" && break
  sleep 1
done
```

- `rawResult`: 生の文字起こしテキスト
- LLM処理後のテキストが必要なら `f.llmResult` を使う

### 3. メタデータ取得（必要に応じて）

最新録音の `meta.json` から詳細情報を取得できる:

```bash
LATEST=$(ls ~/Documents/superwhisper/recordings/ | sort -n | tail -1)
cat ~/Documents/superwhisper/recordings/$LATEST/meta.json
```

`meta.json` に含まれる情報: `rawResult`, `result`, `segments`（タイムスタンプ付き）, `duration`, `modelName` 等。
