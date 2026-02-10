# アクセシビリティ

**ID**: PERF02
**カテゴリ**: パフォーマンス
**優先度**: Tier 3（オプション）
**信頼度基準**: 85-100点

---

## 参照元

- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)
- [The Complete Code Review Process for 2026](https://www.codeant.ai/blogs/good-code-review-practices-guide)

---

## 概要

WCAG（Web Content Accessibility Guidelines）準拠とアクセシビリティ標準への適合性を確認する観点。この観点は**UI/Web開発に限定**され、バックエンドやCLIツールには適用されない。

2026年のトレンドとして、ネイティブHTML要素（`<button>`、`<dialog>`等）の活用が推奨され、カスタム実装よりも標準要素を優先する傾向が強い。AIツールはアクセシビリティを考慮せずにUIを生成することが多いため、人間のレビューが重要となる。

---

## チェック内容

- **セマンティックHTMLの使用**: 適切なHTML要素の選択（`<button>`、`<nav>`、`<main>`等）
- **ARIA属性の適切な使用**: 必要な場合のみ使用（`aria-label`、`aria-describedby`等）
- **キーボードナビゲーション対応**: Tab、Enter、Escapeキーでの操作
- **スクリーンリーダー対応**: 読み上げ順序と内容の適切性
- **色コントラスト**: WCAG AA基準（4.5:1以上）
- **フォーカス管理**: フォーカスの可視化と論理的な順序
- **ネイティブHTML要素の活用**: カスタム実装よりも標準要素を優先
- **代替テキスト**: 画像、アイコンへの適切な説明

---

## 適用基準

### 使用する場合

- ✅ フロントエンドUIコンポーネント追加・変更
- ✅ Webアプリケーションのインタラクティブ要素
- ✅ フォーム要素の追加・変更
- ✅ モーダル、ダイアログの実装
- ✅ ナビゲーションメニューの変更

### 使用しない場合

- ❌ バックエンドAPI実装
- ❌ データベーススキーマ変更
- ❌ CLIツール
- ❌ 内部管理画面（ただし推奨はされる）
- ❌ ドキュメントのみの変更

---

## 具体例

### ❌ 悪い例1: divをボタンとして使用

```tsx
// アクセシビリティ問題あり
<div onClick={() => handleSubmit()}>
  Submit
</div>
```

**問題点**:
- キーボードでフォーカスできない
- スクリーンリーダーがボタンと認識しない
- Enterキーで実行できない

### ❌ 悪い例2: ARIA属性の誤用

```tsx
// 不要なARIA属性
<button aria-label="Submit button">Submit</button>
```

**問題点**: ボタンのテキストが明確な場合、`aria-label`は不要。かえってスクリーンリーダーの読み上げが冗長になる。

### ❌ 悪い例3: 色のみで情報を伝達

```tsx
// 色だけで成功/エラーを表現
<div style={{ color: isError ? 'red' : 'green' }}>
  {message}
</div>
```

**問題点**: 色覚異常のユーザーや、モノクロ表示では判別できない。

### ✅ 良い例1: ネイティブボタン要素を使用

```tsx
// アクセシビリティ対応
<button onClick={() => handleSubmit()}>
  Submit
</button>
```

**理由**: ネイティブ`<button>`要素は自動的にキーボードフォーカス、スクリーンリーダー対応、Enterキー実行をサポート。

### ✅ 良い例2: 適切なARIA属性

```tsx
// アイコンボタンにのみaria-labelを使用
<button aria-label="閉じる">
  <IconClose />
</button>
```

**理由**: アイコンのみのボタンは視覚的にのみ意味を持つため、`aria-label`でスクリーンリーダーに説明を提供。

### ✅ 良い例3: 色とテキストで情報を伝達

```tsx
// 色と明示的なテキストを併用
<div className={isError ? 'error' : 'success'}>
  {isError ? '❌ エラー: ' : '✅ 成功: '}
  {message}
</div>
```

**理由**: 色だけでなく、絵文字とテキストで状態を明示的に伝達。色覚異常のユーザーにも対応。

### ✅ 良い例4: ネイティブdialog要素を使用

```tsx
// 2026年推奨: ネイティブdialog要素
function Modal({ isOpen, onClose, children }) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    if (isOpen) {
      dialogRef.current?.showModal();
    } else {
      dialogRef.current?.close();
    }
  }, [isOpen]);

  return (
    <dialog ref={dialogRef} onClose={onClose}>
      {children}
      <button onClick={onClose}>閉じる</button>
    </dialog>
  );
}
```

**理由**:
- ネイティブ`<dialog>`要素はフォーカストラップ、Escapeキーでの閉じる、背景のスクロール防止を自動対応
- カスタム実装よりもアクセシビリティが保証されている

### ✅ 良い例5: セマンティックHTMLの活用

```tsx
// セマンティックな構造
<nav aria-label="メインナビゲーション">
  <ul>
    <li><a href="/">ホーム</a></li>
    <li><a href="/about">概要</a></li>
    <li><a href="/contact">お問い合わせ</a></li>
  </ul>
</nav>

<main>
  <h1>ページタイトル</h1>
  <article>
    <h2>記事タイトル</h2>
    <p>本文</p>
  </article>
</main>

<footer>
  <p>&copy; 2026 会社名</p>
</footer>
```

**理由**: `<nav>`、`<main>`、`<article>`、`<footer>`を使うことで、スクリーンリーダーがページ構造を理解しやすくなる。

---

## 2026年トレンド

ネイティブHTML要素の活用が強く推奨される。特に`<dialog>`、`<details>`、`<button>`等の標準要素は、カスタム実装よりもアクセシビリティが保証されており、保守性も高い。

AIツールはアクセシビリティを考慮せずに`<div>`ベースのUIを生成する傾向があるため、人間のレビューでネイティブ要素への置き換えを推奨する。

---

## 関連観点

- [Q01] 読みやすさ
- [D03] API設計
- [P01] AIエージェント向け指示の遵守
