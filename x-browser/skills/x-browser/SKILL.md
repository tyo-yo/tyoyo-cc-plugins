---
name: x-browser
description: X/Twitter の情報取得。"X を検索", "Twitter 検索", "Grok でリサーチ", "タイムラインを見て", "X の最新情報", "ツイートを検索", "search X", "X timeline", "Grok research" のような指示で使用。
allowed-tools: Bash(command:ab *)
---

# X/Twitter ブラウザスキル

agent-browser (`ab`) 経由で X/Twitter の情報を取得する。

**前提**: Chrome CDP 接続済み + X/Twitter にログイン済み。

---

## 1. X 検索（ツイート一括取得）

### 基本フロー

```bash
# 1. 検索URLを開く（演算子でフィルタ）
ab open "https://x.com/search?q=QUERY&src=typed_query&f=top"

# 2. スクロール＋蓄積（10回スクロール、約7秒で完了）
SCROLL_JS="${CLAUDE_PLUGIN_ROOT}/scripts/scroll-harvest.js"
ab eval "$(cat "$SCROLL_JS")"

# 3. もっと取りたい場合は同じコマンドを繰り返す（スクロール位置が引き継がれる）
ab eval "$(cat "$SCROLL_JS")"
```

**ポイント**:
- スクリプトは `scripts/scroll-harvest.js` に配置済み。毎回書く必要なし
- 1回の実行で 10 スクロール（約7秒）→ CDP タイムアウトを回避
- X は仮想スクロール（画面外 DOM を削除）するため、Map で蓄積しながらスクロールする
- 広告ツイート（`time` 要素なし）は自動スキップ
- `f=top`（話題）の代わりに `f=live`（最新）も使える
- 繰り返し実行するとスクロール位置が引き継がれ、新しいツイートを追加取得できる

### 高度な検索演算子

URLの `q=` パラメータに以下を組み合わせる（URLエンコード必要）:

| 演算子 | 用途 | 例 |
|--------|------|-----|
| `since:YYYY-MM-DD` | 指定日以降 | `since:2026-02-01` |
| `until:YYYY-MM-DD` | 指定日以前 | `until:2026-02-09` |
| `min_faves:N` | いいね N 件以上 | `min_faves:100` |
| `min_retweets:N` | RT N 件以上 | `min_retweets:50` |
| `min_replies:N` | リプライ N 件以上 | `min_replies:10` |
| `-min_faves:N` | いいね N 件以下 | `-min_faves:1000` |
| `lang:xx` | 言語指定 | `lang:ja`, `lang:en` |
| `from:user` | 特定ユーザーの投稿 | `from:AnthropicAI` |
| `to:user` | 特定ユーザーへのリプライ | `to:AnthropicAI` |
| `filter:media` | メディア付きのみ | |
| `filter:links` | リンク付きのみ | |
| `filter:replies` | リプライのみ | |
| `OR` | OR 検索 | `Claude Code OR "claude code"` |
| `-keyword` | 除外 | `-RT -filter:replies` |

**実用例**:
```
# 日本語で今週のClaude Code関連、いいね100以上
Claude Code lang:ja min_faves:100 since:2026-02-03

# 公式アカウントの投稿
from:AnthropicAI Claude Code since:2026-02-01

# 英語の話題ツイート（RT除外）
"Claude Code" lang:en min_faves:500 -filter:replies
```

---

## 2. Grok リサーチ（x.com/i/grok）

X 上の投稿を検索・要約してくれる AI。X のポストへの直接リンク付きで結果を返す。

### 基本フロー

```bash
# 1. Grok を開く
ab open "https://x.com/i/grok"

# 2. テキスト入力
ab snapshot -i -c -s "main"   # textbox の ref を取得
ab fill @eN "質問内容"         # textbox に入力

# 3. 送信
ab snapshot -i -c -s "main"   # "Grokに聞く" ボタンの ref を取得
ab click @eM                   # 送信

# 4. 完了ポーリング（「キャンセル」ボタンが消えたら完了）
# 5秒間隔、最大120秒待機
for i in $(seq 1 24); do
  result=$(ab snapshot -i -c -s "main" 2>/dev/null | grep -c "キャンセル")
  if [ "$result" -eq 0 ]; then
    echo "Complete after ~$((i*5))s"
    break
  fi
  ab wait 5000 2>/dev/null
done

# 5. 結果取得
ab snapshot -c -s "main" -d 3
```

**ポイント**:
- Grok の応答は通常 5〜60 秒（長い質問やX検索を伴う場合は 40〜90 秒程度）
- 「キャンセル」ボタンの有無で生成完了を判定する
- 結果には X ポストの `@ユーザー名` リンクやウェブページリンクが含まれる
- `ab snapshot -c -s "main" -d 3` で左サイドバー等を除外してメインコンテンツだけ取得

### モデル選択

Grok ページの「自動」ボタンでモデルを切り替え可能。デフォルトの「自動」で十分。

---

## 3. タイムライン読み取り

自分のタイムラインをスクロールしてツイートを一括抽出する。

### 基本フロー

```bash
# おすすめ + フォロー中のタイムライン
ab open "https://x.com/home"

# フォロー中のみ（時系列順）
ab open "https://x.com/home?tab=following"
```

タイムラインを開いた後は **X 検索と同じスクロールスクリプト** でツイートを抽出する（セクション1のステップ2〜3をそのまま使う）。

**`x.com/home` vs `x.com/home?tab=following`**:
- `home`: おすすめアルゴリズム（話題のポストが上位に来る）
- `home?tab=following`: フォロー中のみ、純粋な時系列順

---

## 4. grok.com フォールバック

x.com/i/grok が使えない場合、grok.com でも同様のことが可能。ただし操作が複雑なため、x.com/i/grok を優先する。

### grok.com の操作手順

```bash
# 1. 開く
ab open "https://grok.com/"

# 2. 入力（contenteditable のため ab eval で直接操作）
# 注意: テキスト内のクォートはエスケープすること
ab eval 'const el = document.querySelector("[contenteditable]"); el.focus(); el.textContent = "質問内容"; el.dispatchEvent(new Event("input", {bubbles: true}));'

# 3. DeepSearch を有効化（オプション）
ab snapshot -i -c
ab click @eN   # "DeepSearch" ボタン

# 4. 送信
ab snapshot -i -c
ab click @eM   # "送信" ボタン

# 5. 完了待ち + 結果取得
ab wait 60000
ab snapshot -c
```

**grok.com の特徴**:
- DeepSearch ボタンで深い検索が可能
- 入力は `contenteditable` な `div.tiptap.ProseMirror` → `ab fill` が使えないため `ab eval` で直接操作
- 結果は X ポストへの直接リンクを含まない（一般的な情報のみ）
- x.com/i/grok の方が操作が簡単で、X ポストリンクも取れるため推奨

---

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| CDP 接続失敗 | Chrome で `chrome://inspect/#remote-debugging` を開いてリモートデバッグ有効化 |
| X にログインしていない | Chrome で x.com にログインしてから再実行 |
| 検索結果が少ない | `min_faves` を下げる、日付範囲を広げる、`f=live` に切り替え |
| Grok が応答しない | 120 秒待っても完了しない場合はページリロードして再送信 |
| スクロールでツイートが増えない | 検索結果がそもそも少ない可能性。条件を緩くする |
| `ab eval` で Resource temporarily unavailable | eval の実行時間が長すぎる。スクロール回数を5回以下に分割し、`window.__tweets` で状態を保持する |
| grok.com の入力が効かない | `ab eval` の引用符のエスケープを確認。シングルクォート内にダブルクォートを使う |
