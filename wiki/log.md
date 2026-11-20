---
title: wiki log
created: 2026-11-20
type: log
status: active
tags: [meta]
description: 取り込み・検索・lintの append-only 作業記録。
---

# wiki log

取り込み（ingest）・検索（query）・点検（lint）の記録。追記のみで、過去の行は書き換えない。

## 2026-11-20

- Vaultスターターを作成。構成は PARA ＋ Karpathy流 LLM Wiki（`raw/` → `wiki/`）。方式2（Claude Codeヘッドレス実行をPro付属のAgent SDK枠内で使う）を主軸に運用開始予定。Extra UsageはOFF。
- ミス記録の仕組みを追加：`wiki/mistake.md` を新設し、AGENTS.md に「作業前のミス確認」と「ミス発生時の追記必須」を明記。初回エントリとして本日の課金制度の誤案内を記録。
- SessionStartフック（inject-memory）を追加：全セッション開始時に index / DECISIONS / log直近 / mistake を自動注入。ヘッドレス実行で注入のみから回答できることを実測で確認。
- 実行ごとのセッションレポート（`AI/sessions/`）を必須化。履歴をデバイス問わず辿れるように。
- 課金説明の訂正をVault内に反映：README.mdとDECISIONS.mdに残っていた「Pro月$20 Agent SDKクレジット」表記を修正（正しくはPro通常利用枠、別枠なし）。DECISIONS.mdのA-1〜A-3を決定済みに更新（GitHub Private／Windows／新規Vault）。`templates/session-report.md` を追加し、`AI/sessions/` の報告書式を固定。SETUP.mdのGitSync同期タイミングを公式仕様（定期は最短30分間隔）に合わせて訂正。
- SETUP.md を追加：Android=GitSync方式、Windows=clone+Obsidian Git の手順を明記。
- AndroidのGitSync同期が完了（Documents/second-brainへ直接クローン、定期同期15分間隔）。SETUP.mdを実績手順に更新。
- デイリーノート `50-daily/2026/11/2026-11-20.md` を作成（残タスク2件・今日の実績5件）。セッションレポート：`AI/sessions/2026-11-20-1740-daily-note.md`。
- プライベート用途のMuse/Claude Code/Obsidian連携をWeb調査し、[[private-second-brain-with-muse-claude-code-obsidian]] を新規作成（index登録済み）。趣味・買い物・Muse単体の事例は見つからず、推測と明記。セッションレポート：`AI/sessions/2026-11-20-1745-private-second-brain-research.md`。
- ダッシュボード.md を新設：会話要約とClaude活動レポートを一目で確認するノート。AGENTS.md に「作業の最後に最新化」を義務付け。
- 行動ルール（Ryo指定：読み取り手順／Knowledge・Decisions・Preferencesへの即時書き込み／命名・形式／mistakes追記条件／読み書きの明示報告／作業スタイル）をAGENTS.mdに正本化。mistakesを Knowledge/mistakes.md へ移転し、Preferences/profile.md を新設。注入フックも追随。
- プロファイル第1弾を記録：Preferences/communication.md、decision-making.md、work-style.md を新設（Ryoの回答9件）。
- プロファイル第2弾を記録：Preferences/lifestyle.md、development.md、interests.md を新設し、communication.md に調べ物の深さの好みを追記。
- 地雷（提案の作法）を Preferences/communication.md に追記：推測で提案せず、根拠情報を整理してから提案する。
