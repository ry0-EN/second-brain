---
date: 2026-11-20
tags: [setup, obsidian, git, windows]
project: second-brain
related: [[SETUP]]
---

# Windows版 Obsidian Git セットアップのハマりどころ（2026-11-20 実績）

Windows PCセットアップ中に実際に詰まって解決した点。詳細手順は [[SETUP]] のステップ5・6が正本。

- **プラグインの表示名は「Git」（作者 Vinzent）**。「Obsidian Git」で検索してもヒットしない。検索は「Git」の3文字で。
- **Auto push / Auto pull がグレーアウトする** → Automatic の「Use separate commit and push intervals」をONにすると解除される。ONにしたら commit / push / pull の間隔を全部15分に揃える。
- **旧称 `Create backup` コマンドは現行バージョンに無い** → 後継は `Git: Commit-and-sync`。Obsidianの通知はすぐ消えて履歴機能もないため、到達確認は Git の履歴ビューか GitHub 側で行う。
- **Identity（Repository author name / email）が空欄**だとグローバル Git 設定を参照する。PCでグローバル未登録なら、既存コミットと同名義をリポジトリ専用欄に入力する。
- **Claude Desktop版の Remote Control**：`/remote-control` が「isn't available in this environment」と返る場合がある。その時はセッション右パネル「環境」カードの Remote Control スイッチでONにできる。
- **Desktop版のワークツリーチェックボックス**は、フォルダ選択後の信頼ダイアログを通過してから表示される。デフォルトOFFのまま使う（ONだと隔離コピーになり、Obsidianで開くフォルダとズレる）。
