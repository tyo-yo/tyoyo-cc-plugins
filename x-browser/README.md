# x-browser

agent-browser (`ab`) 経由で X/Twitter の情報を取得する Claude Code プラグイン。

## 機能

- **X 検索**: 高度な検索演算子 + JS蓄積スクロールで上位50〜70件のツイートを構造化データとして一括取得
- **Grok リサーチ**: x.com/i/grok 経由で X 上の情報をAIが検索・要約（ポストリンク付き）
- **タイムライン読み取り**: ホーム/フォロー中タイムラインをスクロールして注目ツイートを抽出
- **grok.com フォールバック**: grok.com DeepSearch の操作手順（x.com/i/grok が使えない場合）

## 前提条件

- [agent-browser](https://github.com/vercel-labs/agent-browser) がインストール済み（`ab` コマンド）
- Chrome でリモートデバッグが有効（`chrome://inspect/#remote-debugging`）
- X/Twitter にログイン済み
