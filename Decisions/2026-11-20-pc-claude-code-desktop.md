---
date: 2026-11-20
tags: [decision, claude-code, windows, remote-control]
project: second-brain
related: [[SETUP]]
---

# 2026-11-20 PCローカルのClaude CodeはDesktopアプリ版を使う

## 決めたこと
- Windows PCでローカルに Claude Code を使う時は、CLI版ではなく **Claude Desktopアプリ版（Codeタブ）** を使う（Ryo決定、2026-11-20）。
- Remote Control の確認も Desktop版で実施し、成功した（スマホからPCセッションへ送信→PCにリアルタイム表示を確認）。
- 主軸の運用（Muse の VM 上でヘッドレス CLI を回し、Vault に蓄積する方式）は不変。Desktop版は「PCの前にいる時・スマホからPCセッションを覗きたい時」の入口。

## 根拠
- 公式ドキュメントで、Remote Control は CLI / Desktopアプリ / VS Code拡張のいずれからでも開始できると確認した（Desktopは `/remote-control` コマンドまたはセッションの Remote Control スイッチ）。
- Ryoはプログラミング未経験寄りで、ターミナル操作より GUI で完結する方が扱いやすい。
- Desktop版はフォルダ選択・権限モード（手動）・ワークツリーOFF を画面で確認しながら進められた。
