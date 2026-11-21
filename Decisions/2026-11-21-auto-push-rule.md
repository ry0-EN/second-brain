---
date: 2026-11-21
tags: [decision, git, workflow]
project: second-brain
related: []
---

# Vaultのpushは事前確認なし（自動push）に変更

## 背景
- 従来のGitルールは「作業後は git diff を見せ、RyoがOKしたら commit / push」だった（AGENTS.md「Gitと承認」）。
- 運用が安定してきたため、Ryoから「pushの事前確認は以降なしで、新しい決め事や運用ルール変更、修正を行った時は自動でpushしてほしい」と指示があった（2026-11-21）。

## 決定
- 新しい決め事・運用ルールの変更・修正を行ったときは、事前確認なしで自動的に commit / push する。対象は変更自体と、それに伴う記録（Decisions / Knowledge / Preferences / ダッシュボード / wiki/log / セッションレポート）。
- push後は結果（commitハッシュと内容）をチャットで報告する。diffの確認はClaude側で行う。
- 対象外（新規の調査・下書き等）の commit / push は従来どおりRyoのOK後。
- `git push --force` や履歴の書き換えは引き続き禁止。

## 備考
- 本決定の記録自体も、この新ルールの適用第1号として自動pushした。
