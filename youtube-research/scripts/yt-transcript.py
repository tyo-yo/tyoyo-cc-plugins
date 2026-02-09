#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "youtube-transcript-api>=1.0.0",
# ]
# ///

"""YouTube 字幕取得スクリプト - 動画の字幕をJSON形式で出力"""

import sys
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """YouTube URL から video ID を抽出"""
    patterns = [
        r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def main():
    if len(sys.argv) < 2:
        print("Usage: yt-transcript.py <youtube-url-or-id> [language]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    preferred_langs = sys.argv[2].split(",") if len(sys.argv) > 2 else ["ja", "en"]

    video_id = extract_video_id(url)
    ytt = YouTubeTranscriptApi()

    # 字幕取得
    transcript = ytt.fetch(video_id, languages=preferred_langs)
    entries = list(transcript)

    total_duration = max(e.start + e.duration for e in entries) if entries else 0
    total_chars = sum(len(e.text) for e in entries)

    result = {
        "video_id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "entry_count": len(entries),
        "total_duration_sec": round(total_duration),
        "total_chars": total_chars,
        "entries": [
            {"text": e.text, "start": e.start, "duration": e.duration}
            for e in entries
        ],
    }

    output_path = f"/tmp/yt-transcript-{video_id}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"video_id: {video_id}")
    print(f"entries: {len(entries)}")
    print(f"duration: {round(total_duration)}s")
    print(f"chars: {total_chars}")
    print(f"saved: {output_path}")


if __name__ == "__main__":
    main()
