---
name: youtube-research
description: YouTube動画のリサーチ・要約。"YouTube動画を要約", "動画の内容を教えて", "YouTubeで検索", "YouTube research", "summarize video" のような指示で使用。
allowed-tools: Bash(yt-dlp:*), Bash(uv:*)
---

# YouTube Research

YouTube 動画の検索・字幕取得・要約を行うプラグイン。

## 動画の要約

YouTube URL が渡されたら **youtube-fetch エージェント**に処理を委譲する。
エージェントが字幕を取得し要約を返す。

複数 URL を一度に渡すことも可能。エージェントが全て処理する。

## 動画の検索

yt-dlp を使って YouTube を検索できる。

### キーワード検索

```bash
yt-dlp "ytsearch10:検索キーワード" \
  --print "%(title)s | %(channel)s | %(duration_string)s | %(view_count)s views | https://youtu.be/%(id)s" \
  --skip-download
```

- `ytsearch10:` の数字で結果数を指定（5, 10, 20 など）
- 日本語キーワードも使用可能

### チャンネルの動画一覧

```bash
yt-dlp "https://www.youtube.com/@チャンネルハンドル/videos" \
  --print "%(title)s | %(upload_date)s | https://youtu.be/%(id)s" \
  --flat-playlist --skip-download --playlist-end 10
```

### チャンネル内検索（一覧取得 → フィルタ）

```bash
yt-dlp "https://www.youtube.com/@チャンネルハンドル/videos" \
  --print "%(title)s | https://youtu.be/%(id)s" \
  --flat-playlist --skip-download | grep -i "キーワード"
```

## 前提条件

- `yt-dlp`: `brew install yt-dlp`
- `uv`: Python スクリプト実行に使用（PEP 723 インラインメタデータ）
