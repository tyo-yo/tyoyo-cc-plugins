# Unity Development Plugin

Unity開発をClaude Codeで効率化するプラグイン。Unity MCP統合、AI機能活用、スクリプト生成を支援します。

## 概要

このプラグインは、Unity MCP (Model Context Protocol) を通じてUnity EditorをClaude Codeから直接操作し、"Vibe Coding"ワークフローを実現します。自然言語でUnityプロジェクトを操作し、ゲーム開発を高速化できます。

### 主な機能

- **Unity MCP統合**: Unity Editorをターミナルから操作
- **スクリプト自動生成**: C#スクリプトをAIが生成・検証
- **シーン操作**: GameObjectの作成、配置、設定を自動化
- **安全ガード**: 破壊的操作前の確認、スクリプト検証
- **バッチ処理**: 複数操作を一括実行（10-100倍高速化）
- **日本語対応**: UTF-8エンコーディング、日本語パス対応

## インストール

### 前提条件

- Unity 6.2+ (推奨) または Unity 2023.2+
- Claude Code CLI
- [uv](https://github.com/astral-sh/uv) パッケージマネージャー

### クイックスタート

**ステップ1: uvのインストール**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
winget install --id=astral-sh.uv -e
```

**ステップ2: プラグインのインストール**

```bash
# プラグインをインストール
claude plugin add tyoyo-cc-plugins/unity-development

# または、ローカルパスから
claude plugin add /path/to/tyoyo-cc-plugins/unity-development
```

**ステップ3: 環境変数の設定**

Unity MCPにプロジェクトパスを教えるため、環境変数を設定:

```bash
# macOS/Linux (bash/zsh)
echo 'export UNITY_PROJECT_PATH="/path/to/your/unity/project"' >> ~/.zshrc
source ~/.zshrc

# Windows (PowerShell)
[Environment]::SetEnvironmentVariable("UNITY_PROJECT_PATH", "C:\path\to\your\unity\project", "User")
```

**ステップ4: 確認**

Claude Codeを再起動して、Unity MCPが自動的に設定されていることを確認:

```bash
/mcp
```

`unity-mcp` がリストに表示されればOK！

**ステップ5: 動作確認**

Unity Editorを起動した状態で、Claude Codeから試してみましょう:

```
Unityで新しいシーンを作成して、Cubeを配置してください
```

### 重要な注意点

- **Unity MCPは自動設定**: プラグインの `.mcp.json` により、MCP サーバーは自動的に設定されます
- **環境変数は必須**: `UNITY_PROJECT_PATH` を設定後、Claude Codeを再起動してください
- **Windowsユーザー**: UTF-8エンコーディングは自動的に有効化されます (`PYTHONUTF8=1`)

### セットアップヘルプ

セットアップで困ったときは:

```bash
/unity-development:unity-setup-mcp [your-unity-project-path]
```

このコマンドで前提条件の確認と環境変数設定をサポートします。

## 使い方

### 基本的なワークフロー

#### 1. シーン作成とオブジェクト配置

```
水族館のシーンを作って。水槽、魚のオブジェクト、ライティングを設定してください。
```

Claude Codeが以下を実行:
- 新しいシーンを作成
- GameObjectを配置
- マテリアルを適用
- ライティングを設定
- 結果をスクリーンショットで確認

#### 2. C#スクリプト生成

```
プレイヤーがWASDで移動できるスクリプトを作成してください。
```

Claude Codeが以下を実行:
- スクリプトファイルを生成
- Unity命名規則に従う (クラス名 = ファイル名)
- UTF-8エンコーディング検証
- 基本的な構文チェック

#### 3. アセット管理

```
Assets/Sprites/フォルダ内のすべてのスプライトにPixelPerfectマテリアルを適用してください。
```

Claude Codeが以下を実行:
- batch_executeで一括処理
- 各スプライトにマテリアル適用
- Unity Editorで結果を確認

### コマンド

#### `/unity-development:unity-setup-mcp`

Unity MCPサーバーをセットアップします。初回セットアップ時に使用。

```bash
/unity-development:unity-setup-mcp
```

### スキル

#### `unity-mcp-assistant`

Unity MCP経由でUnity Editorを操作する専門スキル。以下のようなフレーズで自動的にロードされます:

- "create Unity scenes"
- "modify GameObjects"
- "generate Unity scripts"
- "debug Unity projects"
- "manage Unity assets"
- "automate Unity tasks"
- "Unity MCP操作"
- "Unityシーン作成"
- "Unityスクリプト生成"

手動でロード:
```bash
/unity-mcp-assistant
```

## ベストプラクティス

### 段階的アプローチ

1. **読み取り操作から始める**: まずシーン状態を確認
2. **小さな変更を積み重ねる**: 一度に大きな変更をしない
3. **確認を求める**: 破壊的操作前に必ず確認
4. **Play modeでテスト**: 変更後は必ず動作確認
5. **エビデンスを要求**: スクリーンショット、コンソール出力で検証

### パフォーマンス最適化

- **batch_executeを活用**: 3個以上のオブジェクト操作時は必須
- **サマリーファースト**: 概要取得 → 必要時に詳細取得
- **ページング設定**: 大規模シーンでは page_size を調整

### 安全性

- **バージョン管理**: 重要な変更前は必ずコミット
- **Assets フォルダ削除禁止**: プラグインが自動的に警告
- **スクリプト検証**: クラス名とファイル名の一致を自動チェック
- **UTF-8エンコーディング**: BOM検出を自動チェック

## トラブルシューティング

### MCP接続できない

**症状**: ツールが利用できない、タイムアウトエラー

**解決策**:
1. Unity Editorが起動しているか確認
2. Unity MCPプラグインがインストールされているか確認
3. `claude mcp list` でUnity-MCPが表示されるか確認
4. MCP サーバーを再起動: `claude mcp restart Unity-MCP`
5. HTTPエンドポイントが稼働しているか確認: `curl http://localhost:8080/mcp`

### スクリプトのコンパイルエラー

**症状**: Unityコンソールにエラーが表示される

**解決策**:
1. クラス名とファイル名が一致しているか確認 (大文字小文字も含む)
2. UTF-8エンコーディング (BOMなし) になっているか確認
3. `using UnityEngine;` が含まれているか確認
4. MonoBehaviour継承が正しいか確認

### パフォーマンスが遅い

**症状**: 操作に時間がかかる、個別ツール呼び出しが遅い

**解決策**:
1. batch_executeに切り替える
2. page_size を減らす (デフォルト: 50)
3. 不要なUnityウィンドウを閉じる
4. HTTPトランスポートを使用 (Stdioより高速)

### 日本語パスの問題 (Windows)

**症状**: パスが正しく認識されない、エンコーディングエラー

**解決策**:
1. `PYTHONUTF8=1` 環境変数を設定
2. プロジェクトパスにスペースがないか確認
3. uv.exeのパスが正しいか確認
4. Unity Editorを再起動

## 技術仕様

### 対応Unity MCPツール

- `manage_scene`: シーン作成、読み込み、保存、スクリーンショット
- `manage_gameobject`: GameObject作成、変更、削除
- `create_script`: C#スクリプト生成
- `manage_asset`: アセットインポート、移動、削除
- `manage_material`: マテリアル作成、適用
- `batch_execute`: 複数操作の一括実行 (10-100倍高速化)

### フック

- **PreToolUse**: 破壊的操作前の警告 (Edit/Write時)
- **PostToolUse**: スクリプト検証 (Write/Edit後)

### 検証項目

- BOM検出 (UTF-8 without BOM推奨)
- Unity namespace確認 (`using UnityEngine;`)
- クラス名とファイル名の一致
- MonoBehaviour継承の確認
- 破壊的操作の警告 (ProjectSettings, .unity, .prefab等)

## 参考リンク

- [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp) - Unity MCP公式リポジトリ
- [Unity MCP Documentation](https://github.com/CoplayDev/unity-mcp/blob/main/README.md)
- [Unity Scripting API](https://docs.unity3d.com/ScriptReference/)
- [MCP Protocol](https://modelcontextprotocol.io/)

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照

## 作者

tyo-yo

## 貢献

Issue、Pull Requestは歓迎します。Unity開発のベストプラクティスやバグ修正があれば、ぜひお知らせください。

## 今後の予定

**Phase 2 (AI機能統合)**:
- Unity AI Generators統合
- 画像生成MCP連携
- アセット自動生成ワークフロー

**Phase 3 (高度な機能)**:
- Unity Sentis統合ガイド
- ML-Agents訓練支援
- シーン自動構築エージェント

---

**始めましょう**: `/unity-development:unity-setup-mcp` でセットアップを開始してください!
