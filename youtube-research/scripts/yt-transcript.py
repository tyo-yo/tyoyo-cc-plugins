#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "youtube-transcript-api>=1.0.0",
# ]
# ///

"""YouTube 字幕取得スクリプト - タイムスタンプ付きマークダウンで出力"""

import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    patterns = [
        r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def format_timestamp(seconds: float) -> str:
    s = int(seconds)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = {a for a in sys.argv[1:] if a.startswith("-")}
    timestamps = "--timestamps" in flags or "-t" in flags

    if not args:
        print("Usage: yt-transcript.py <youtube-url-or-id> [language] [--timestamps]", file=sys.stderr)
        sys.exit(1)

    url = args[0]
    preferred_langs = args[1].split(",") if len(args) > 1 else ["ja", "en"]

    video_id = extract_video_id(url)
    ytt = YouTubeTranscriptApi()

    transcript = ytt.fetch(video_id, languages=preferred_langs)
    entries = list(transcript)

    total_duration = max(e.start + e.duration for e in entries) if entries else 0

    output_path = f"/tmp/yt-transcript-{video_id}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Transcript: {video_id}\n\n")
        f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
        f.write(f"Entries: {len(entries)} | Duration: {format_timestamp(total_duration)}\n\n")
        f.write("---\n\n")
        for e in entries:
            ts = format_timestamp(e.start)
            if timestamps:
                t = int(e.start)
                f.write(f"[{ts}](https://www.youtube.com/watch?v={video_id}&t={t}) {e.text}\n\n")
            else:
                f.write(f"{ts} {e.text}\n\n")

    print(f"video_id: {video_id}")
    print(f"entries: {len(entries)}")
    print(f"duration: {format_timestamp(total_duration)}")
    print(f"saved: {output_path}")


if __name__ == "__main__":
    main()
