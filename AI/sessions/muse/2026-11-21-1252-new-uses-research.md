---
date: 2026-11-21
tags: [session, muse, research]
project: second-brain
related: ["[[AI/新規活用法レポート]]"]
---

# 新規プライベート活用法の収集とレポート化（Muse作業）

## 指示内容
Ryo：「昨日の資料は既存の運用ナレッジのまとめ中心だった。まだ持っていない新しいプライベート活用法を、記事・ブログ・YouTubeからイヴォンヌ自身で収集してレポートにまとめてほしい。作業はClaude Codeに実施させ、HTML経由でデザインのあるレポートを作らせること」

## 処理の流れ
1. 既存ナレッジの棚卸し：wiki調査ページと AI/活用術-資料 の見出しから「もう知っていること」10項目を除外リスト化。
2. MuseがWebリサーチを実施（日英、記事・ブログ・YouTube）：新規活用法29項目＋YouTube 7本を収集。成果はリサーチノート（Claude側）に保存。
3. ソース一式を `00-inbox/source-new-private-uses-2026-11-21.md` としてVaultに配置（Claude CodeはWeb取得不可のため）。
4. Claude Code（ヘッドレス、Sonnet、acceptEdits）にHTMLレポート作成を委任。1回目の実行はランタイム再起動（VM置き換え）で中断され、成果物なしを確認して再実行し完了。レポート本体の作成とセッションレポート・ダッシュボード・log更新は [[AI/sessions/claude-code/2026-11-21-1245-new-uses-report]]。
5. Muse側で検証：HTMLのラベル・出典・YouTube／未確認セクションを確認。Claude Codeが残した一時フォルダ `AI/_gen/` を削除。WeasyPrintでPDF版（A4・15ページ）を `attachments/新規活用法レポート.pdf` に生成し、テキスト抽出で内容を確認してRyoへ受け渡し。

## 成果物
- レポートHTML： `AI/新規活用法レポート.html`（Claude Code作成）
- レポートPDF： `attachments/新規活用法レポート.pdf`（Museがレンダリング）
- ソース： `00-inbox/source-new-private-uses-2026-11-21.md`

## 備考
- commit / push はRyoの承認後に実施（調査成果物のため自動push対象外）。
