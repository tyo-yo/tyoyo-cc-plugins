# 構造スメルリファクタルール

REFACTOR フェーズで「修正」ではなく「検知」に全振りするためのルール。
誤検知を許容して見逃しを減らす。

## 目的

- 違和感を最大量で掘り起こす
- 「そもそも不要実装」の仮説を必ず出す
- 既存パターンとのズレを特定する
- 標準ライブラリや既存フレームワーク機能への置換可能性を検知する

## 実行ルール

- 修正案の提示は後回しにして、まず検知のみを行う
- 精度より再現率を優先し、迷った指摘も出す
- すべての指摘に根拠のコード位置を付ける
- すべての指摘に「将来壊れるシナリオ」を1行で付ける
- すべてのモジュールで「削除可能性」の仮説を最低1件出す
- 代替案がなくても課題の指摘だけで良い

## 検知タスク

- 削除可能性検知: この関数、分岐、層は消しても責務が成立するか
- 境界違反検知: バリデーション、例外、型変換、状態管理がレイヤー越境していないか
- 一貫性破綻検知: 同一リポジトリの類似実装と命名、責務分割、エラーパターンがズレていないか
- 再実装検知: 標準ライブラリ、既存フレームワーク、定番ライブラリの機能を手作りしていないか
- 将来脆弱性検知: 仕様追加で壊れやすい形になっていないか

## スメルタイプ

- speculative-generality: 将来のためだけの先回り抽象化
- fake-abstraction: 実装が1つしかない抽象
- single-use-helper: 呼び出しが1箇所のヘルパー
- redundant-validation: 境界外での再バリデーション
- optional-inflation: 不要な Optional
- boolean-flag-api: 真偽値引数で責務が分岐
- parameter-clump: 同じ引数群の繰り返し
- control-flow-labyrinth: if/elif の迷路化
- deep-nesting: 深すぎるネスト
- exception-erasure: 例外情報の欠落
- log-and-swallow: ログのみで握りつぶし
- silent-fallback: 無言デフォルトフォールバック
- non-idempotent-retry: 危険なリトライ
- state-leak: 隠れ状態への依存
- naming-drift: 命名と実態の乖離
- comment-lie: コメントと実装の不一致
- framework-bypass: 既存フレームワーク機能の迂回
- stdlib-reimplementation: 標準機能の再実装
- transport-type-leak: 境界の型が内部へ侵食
- dead-compat-branch: 死んだ後方互換分岐
- copy-rule-divergence: 同一ルールの重複実装
- pseudo-domain-layer: 層はあるが責務が空
- over-normalization: 分割しすぎによる理解コスト増
- premature-async: 不要な非同期化
- temporal-coupling: 呼び順依存
- wrong-cuts: ドメイン境界ではなく技術都合で分割されている
- shared-persistency: 複数サービスが同一DBを直接共有している
- synchronous-chains: 同期呼び出しが数珠つなぎで遅延と障害を伝播する
- circular-imports: モジュールやレイヤーの依存が循環している
- divergent-change: 1つのモジュールが多種類の理由で頻繁に変更される
- shotgun-surgery: 1つの変更のために多数の箇所を同時修正する必要がある
- anemic-domain-model: ドメインオブジェクトがデータ入れ物化しロジックが外部へ流出している
- singletonitis: シングルトンやグローバル状態に依存し変更とテストが硬直している
- source-of-truth-split: 同じ業務事実を複数箇所で更新し整合性が割れている
- transaction-boundary-leak: 整合性が必要な境界とトランザクション境界が一致していない
- contract-drift: APIやイベント契約が利用側と乖離している
- orchestrator-god-service: 1サービスが複数コンテキストの制御を抱え込み肥大化している
- shared-type-across-contexts: 境界をまたいで型やDTOを共有し独立進化できない
- observability-blind-spot: 障害時に因果関係を追跡できる観測点が不足している
- pipeline-jungle: パイプラインが継ぎ足しで複雑化し依存関係が読めない
- cace-entanglement: 一部変更が全体挙動に波及する強い絡み合いがある
- large-class: 責務過多でクラスが肥大化している
- long-method: 関数が長すぎて意図の追跡が難しい
- long-parameter-list: 引数が多すぎて呼び出しと責務が不明瞭になっている
- data-clumps: 同じ引数群やデータ群が繰り返し登場する
- primitive-obsession: ドメイン概念を基本型の組み合わせで無理に表現している
- feature-envy: 他オブジェクトのデータに過剰依存したロジック配置になっている
- message-chains: 連鎖呼び出しが深く構造変更に極端に弱い
- inappropriate-intimacy: モジュール間で実装詳細に過剰依存している
- duplicate-code: 同一ロジックが複数箇所に重複している
- middle-man: 実質委譲のみの層が増えインダイレクションが過剰
- lazy-class: 役割の薄いクラスが増え構造だけ複雑化している
- broad-exceptions: 例外捕捉が広すぎて障害原因を隠している
- dead-code: 到達しないコードや使われないAPIが残置されている
- magic-literals: 意味の説明がない数値や文字列リテラルに依存している
- print-debugging-leftovers: 本番経路にprintデバッグの痕跡が残っている
- assertion-roulette: テスト失敗時にどの検証が壊れたか判別しづらい

## どんでん返しの問い

- これは本当に存在に値するか
- これを全部消しても要件を満たせない理由は何か
- この責務は1つ上か1つ下のレイヤーに寄せるべきではないか
- フレームワーク既存機能に戻したら何行消えるか
- 状態を減らして値を返す形に倒せないか

## LLM への指示文

- あなたの仕事は修正ではなく検知。誤検知を許容して見逃しを最小化せよ。
- 各ファイルで不要実装、境界違反、一貫性破綻、再実装を優先して探せ。
- すべての指摘に根拠位置と将来破綻シナリオを付けよ。
- 修正案はまだ書くな。違和感を最大数列挙せよ。
