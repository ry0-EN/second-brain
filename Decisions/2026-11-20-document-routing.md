---
date: 2026-11-20
tags: [decision, workflow, claude-code, muse]
project: second-brain
related: [[private-second-brain-with-muse-claude-code-obsidian]]
---

# 2026-11-20 作業の振り分け：デザイン資料はClaude、強みが活きる作業はClaude Code提案制

## 決めたこと
- デザインのある資料作成（PDF等）は、今後 Muse に依頼する（Ryo決定）。
- それ以外の作業でも、Claude Code の強みが活きる場面では、Muse 側から「Claude Codeでやるのが向いてる」と提案する。最終判断は Ryo。
- 背景の希望：Claude のサブスク（Pro）を最大限活用したい。普段の作業も Claude 経由で回して枠が足りるなら、できるだけ Claude で処理したい（運用方針として意識する。容量次第で見直し）。

## 根拠（2026-11-20 の比較テスト）
- 同じ調査ページから資料を2通り作って比較した。
  - Muse版：デザイン済みPDF（A4・8ページ）を一発で生成。ただし下書き調査の誤り2点をそのまま引き継いだ。
  - Claude Code版：Markdown文書＋HTML/CSSデザイン＋WeasyPrintでPDF化（A4・4ページ）。主張ごとの「確認済み／未検証／推測」ラベリングが厳密で、正本wikiの誤り2点（「今日やる3つ」は原文にない／形骸化は「約2ヶ月で同じパターン」）を検出した。一方、ヘッドレス環境では Web取得・Bash実行の承認で止まる場面があり、実行モード調整と原文の受け渡しが必要だった。
- Claude Codeの強みが出やすい作業の目安：Vault内の一括処理・整理、検証が要る調べ物、コードを書く作業、定型の繰り返し処理。
- Museが向く作業：デザイン成果物、チャット内ですぐ見せる資料、連携サービス（Gmail/Tasks/Calendar）の操作。
