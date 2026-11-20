---
title: private-second-brain-with-muse-claude-code-obsidian
created: 2026-11-20
type: research
status: draft
tags: [research, private, obsidian, claude-code, muse, second-brain]
description: 仕事ではなくプライベートで Muse（チャット型AI）/ Claude Code / Obsidian を連携させる定番手法の調査。日記と振り返り、読書の知識化、趣味、個人開発、生活タスクの型と、このVaultへの適用案を整理。
---

# プライベートで Muse / Claude Code / Obsidian を連携させる方法

Webの実例（英語・日本語、全てブログ・コミュニティ製で公式資料ではない。手順の細部は未検証）を、プライベート用途に絞って整理した。

## 基本の役割分担（実例に共通）

- **Obsidian** = 保存先とビューア（Markdownの置き場）。**Claude Code** = 読み書き・整理を行う処理層。`CLAUDE.md` に常設ルールを書く。
- Karpathy流 LLM Wiki：`raw/`（元資料）と `wiki/`（AIが育てる層）を分け、Obsidianは「IDE」、LLMは「プログラマ」、wikiは「コードベース」という喩え。定期的に健全性チェック（lint）を頼む。このVaultの構成と同じ。
- YAMLフロントマター（日付・タグ）を付けるとAIが絞り込みやすい。フォルダは浅く保つとトークン節約になるという指摘がある。
- **Muse（チャット）の位置づけ**：Muse専用の事例は今回の調査では見つからなかった。以下は上記の役割分担からの**推測**：Museは外出先・スマホでの会話型の入口（思いつきの相談・口述）、Claude Codeは机の前での整理・一括処理、という分担が自然。

## 用途別のおすすめ

### 1. 日々の記録と振り返り（実例が最も多い）
- 朝：前日の「明日やる」とGoogle Calendarの予定を読み込んでデイリーノートを作成。夜：カレンダーと照合し、質問に答えてノートを更新（Classmethod記事）。「今日やる3つ」を決める運用はlibecity記事側の事例として報告されている（Classmethod原文にはない。2026-11-20 原文確認で訂正）。
- 自由記述のデイリーノートを入口にし、夜間にClaude Codeが構造化する（MindStudio）。`/process-daily` でアイデア文書化する例もある（Rob Dodson）。
- 注意：振り返りは約2ヶ月で毎日同じパターンになりがち（半年運用しての気づき、Classmethod。2026-11-20 原文確認で訂正）。目標に連動したKPT形式に変える・質問を時々変える等の工夫が必要。
- 適用案：このVaultの `50-daily/` を入口に、Museで口述→ `00-inbox/` →整理、週次レビューを `AI/` に下書き。

### 2. 学習・読書の知識化
- 読書ノート専用の事例は見つからなかった。Karpathy流では、自分が書いた読書・視聴メモをそのまま `raw/` 扱いにし、別フォルダにAI生成のwikiを作って原本と分離する実例がある（diyazy）。
- 適用案：本の感想は自分の言葉のまま `raw/` 側に残し、AIの要約・概念ページは `wiki/` に。自分の言葉と混ぜない（AGENTS.mdの規則と一致）。

### 3. 趣味（音楽・旅行・創作）
- 旅行・趣味に特化した事例は**見つからなかった**。近いものとして、daily/project/study/course/health/finance/family/hobby の8テンプレートを持つ個人用スキャフォールド（vinipx/brain）や、年間目標に「新しい国2つ」を置くライフトラッカー（claudecodehq）がある。
- 適用案：趣味ごとに1ページ（ログ・リスト・次にやること）。新しい型は `templates/` のルール上、Ryoの指示があるときだけ追加。

### 4. 買い物・調べ物の蓄積
- 買い物リスト専用の事例は見つからなかった。調べ物は「Query結果を wiki に残す」Karpathy流がそのまま使える。
- 適用案：比較検討（家電・旅行先など）を1トピック1ページで蓄積し、`wiki/index.md` で検索。価格・制度は変わりやすいので日付と出典を必ず残す（[[mistake]] の再発防止ルールと整合）。

### 5. 個人アプリ開発
- 各リポジトリに `CLAUDE.md` を置き、frontmatter（プロジェクト名・スタック・状態）をDataviewで一覧化（starmorph）。プロジェクトごとにフォルダを作りデイリーと紐づける（mibii）。
- セッション記録（obsx）や、プロジェクトのノートから論点・未解決事項を要約させる使い方（Claudesidian）。
- `CLAUDE.md` は短く、ミス防止の指示だけに絞る（mibii）。

### 6. 家族・生活のタスク管理
- 受信箱ファイル＋タスクDB（LifeOS-OSS）、「期限切れは？」「今すぐできるのは？」と聞けるタスク管理（artemxtech, TaskNotes）。
- 家族・健康・家計は機密性が高い。Git同期するなら Private リポジトリ前提で、秘密情報はVaultに書かない（AGENTS.md）。

## 落とし穴
- 振り返りの形骸化、ノートの増えすぎ（古い主張・孤立ページ → 定期lint）。
- セッションをまたぐ文脈は失われる。Vault（と SessionStart フック）を永続メモリとして使う。
- 記事は商用・個人ブログが中心で、メンテ状況は不明。導入前にリポジトリを確認。

## このVaultでの最初の一歩（提案）
1. デイリーノート運用（朝の3つ／夜の振り返り）を1週間試す。
2. 調べ物ページを1つ作り、出典と日付を残す。
3. 2〜3週間後にlintと週次レビューを試し、続くものだけ型にする。

## 出典
- https://dev.classmethod.jp/ja/articles/claude-code-daily-note-three-improvements/
- https://library.libecity.com/articles/01KPWBVC7APQ1Q0WC3H4PHMC3Y
- https://www.mindstudio.ai/blog/build-ai-second-brain-claude-code-obsidian-2
- https://dev.to/mibii/claude-code-obsidian-build-a-second-brain-that-actually-thinks-d61
- https://robdodson.me/posts/i-gave-my-second-brain-a-gardener/
- https://kennethreitz.org/essays/2026-03-06-obsidian_vaults_and_claude_code
- https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- https://diyazy.github.io/2026/04/07/I-Built-a-KarpathyStyle-Knowledge-Wiki-From-8-Months-of-Obsidian-Notes-Heres-How.html
- https://github.com/vinipx/brain
- https://claudecodehq.com/playbooks/personal-os-life-tracker
- https://github.com/kcwoodfield/LifeOS-OSS
- https://artemxtech.substack.com/p/ai-powered-task-management-in-obsidian
- https://dev.to/starmorph/obsidian-claude-code-the-complete-integration-guide-8c7
- https://docsearch.algolia.com/mcp/docs/repo/heyitsnoah/claudesidian
- https://pypi.org/project/obsx/
