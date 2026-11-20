---
date: 2026-11-21
tags: [decisions, workflow, memory]
project: second-brain
related: [[Knowledge/mistakes]]
---

# Muse（チャット）にもVault読み取りプロトコルを義務付ける

## 背景
- Claude Codeは SessionStart フックで Vault のルール・mistakes・Preferences が自動注入される。
- 一方、Claude Codeを経由しない Muse 単独の作業では、自動で Obsidian を読み込む仕組みがなかった（Muse側メモリの要約と、ルールとしての申し合わせのみ）。
- AI側メモリには上限があり、負担をかけないために外部記憶として Obsidian を連携させている、というのがこの環境の設計思想（Ryo指摘、2026-11-21）。
- Ryoの考え（2026-11-21）：全ての処理を Claude Code 経由で実行するなら、読み取りはフックで担保されるため Muse 側に読ませる必要はない。ただし現状はハイブリッド運用（資料作成は Muse 等）で進める以上、Muse も Obsidian の内容を踏まえたうえで実行してほしい。

## 決定（Ryo指示、2026-11-21）
- Muse がタスクを実行するときは、今回の資料作成のような Muse 単独作業も含め、**必ず事前に Vault のエージェントルール（AGENTS.md）を読み**、あわせて `Knowledge/mistakes.md` と `Preferences/` を確認し、関連キーワードで Vault を検索してから思考・実行する。Claude Code と同じ扱いとする。
- 正本は Vault に置く。Muse 側メモリは要約層として扱い、詳細を抱え込まない。

## 実装メモ
- Vault 側：AGENTS.md の行動ルール1に Muse への義務付けを明記した。
- Muse 側：Muse 自身の運用ノート（~/AGENTS.md、毎セッション注入される）にも同ルールを記録し、新しいチャットでも開始時点から有効な状態にした。
- 検証可能性：読み取りは作業報告・セッションレポートに明記する（AGENTS.md ルール6）。
