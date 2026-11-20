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
