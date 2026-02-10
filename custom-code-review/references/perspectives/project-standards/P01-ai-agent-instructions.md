# AIエージェント向け指示の遵守

**ID**: P01
**カテゴリ**: プロジェクト標準
**優先度**: Tier 1（必須）
**信頼度基準**: 91-100点（明示的違反）、80-90点（暗黙的違反）

---

## 参照元

- [PR Review Toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit)
- [Feature Dev](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)
- [matsengrp/plugins](https://github.com/matsengrp/plugins)

---

## 概要

この観点は、プロジェクト固有のAIエージェント向けガイドラインへの準拠を確認します。CLAUDE.md（Claude Code）や.cursorrules（Cursor）などのファイルに記載されたコーディング規約、命名規則、フレームワーク固有のルールが正しく適用されているかをチェックします。

AIエージェントに対する明示的な指示は、プロジェクトの一貫性を保つために最も重要な基準であり、すべてのコード変更で適用されるべきです。

---

## チェック内容

- CLAUDE.mdやREADME内のAI向けセクションに記載されたルールの遵守
- インポートパターンの統一
  - 相対インポートvs絶対インポート
  - インポート順序の規約
- フレームワーク規約の適用
  - React Hooksの使用ルール
  - Djangoのクラスベースビューvs関数ベースビュー
- 命名規則の一貫性
  - camelCase、snake_case、PascalCaseの使い分け
  - ファイル名規約
  - 変数名・関数名の接頭辞/接尾辞ルール
- ロギング規約の適用
  - ログレベルの使い分け
  - ログフォーマットの統一
- エラーハンドリング規約の適用
  - カスタム例外クラスの使用
  - エラーメッセージのフォーマット
- コメントスタイルの統一
  - JSDoc、docstring等のフォーマット
  - TODOコメントの記法
- ディレクトリ構造とファイル配置の慣習

---

## 適用基準

### 使用する場合

- ✅ 常に適用（すべてのコード変更）
- ✅ 新規ファイル追加
- ✅ 既存コードの修正
- ✅ リファクタリング

### 使用しない場合

- ❌ 該当なし（必須観点）

---

## 具体例

### ❌ 悪い例

```python
# CLAUDE.md: "Use absolute imports from project root"
# 違反: 相対インポートを使用
from ..utils import helper
from ...models import User

# CLAUDE.md: "Use snake_case for function names"
# 違反: camelCaseを使用
def calculateTotalPrice(items):
    return sum(item.price for item in items)

# CLAUDE.md: "Use structured logging with context"
# 違反: print文を使用
print(f"User {user_id} logged in")
```

**問題点**: CLAUDE.mdに明示的に記載されたルールに直接違反しており、コードベース全体の一貫性が損なわれます。

### ✅ 良い例

```python
# CLAUDE.md: "Use absolute imports from project root"
from myproject.utils import helper
from myproject.models import User

# CLAUDE.md: "Use snake_case for function names"
def calculate_total_price(items):
    return sum(item.price for item in items)

# CLAUDE.md: "Use structured logging with context"
logger.info("user_login", extra={"user_id": user_id})
```

**理由**: すべてのコードがCLAUDE.mdのガイドラインに準拠しており、プロジェクトの一貫性が保たれています。

---

## 関連観点

- [P02] 既存パターンとの整合性
- [Q01] 読みやすさ
