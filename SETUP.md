# セットアップ手順（デバイス別）

正本は GitHub Private リポジトリ `ry0-EN/second-brain`。どのデバイスも、このリポジトリを同期して同じフォルダを Obsidian で開く。

## Android（閲覧＋軽い編集）— GitSync 方式

1. Play ストアで **GitSync** をインストールする。
2. GitSync を開き、GitHub アカウント（ry0-EN）でログインする。
3. リポジトリ `second-brain` を選び、端末内のフォルダ（例：`Documents/second-brain`）に clone する。
4. 同期を1回実行して、ファイルが降りてきたことを確認する。
5. Obsidian アプリで「フォルダーを保管庫として開く」から、そのフォルダを選ぶ。
6. GitSync 側で自動同期（ファイル変更時／間隔）を ON にする。

注意：
- 同期は準リアルタイム（数秒〜数分）。編集前に手動で1回 pull（同期）すると安全。
- VM 側で Claude が作業している最中は、同じノートをスマホで編集しない（競合防止）。

## Windows PC（閲覧＋編集）

1. **Git for Windows** と **Obsidian** をインストールする。
2. 任意のフォルダで次を実行して clone する（GitHub Desktop でも可）：
   `git clone https://github.com/ry0-EN/second-brain.git`
3. Obsidian で clone したフォルダを保管庫として開く。
4. コミュニティプラグイン **Obsidian Git** を有効化し、起動時 pull と定期 push を設定する。
5. 編集後は Obsidian Git が自動で commit / push する。大きな編集の前は pull を忘れずに。

## 共通ルール

- 書き手は同時に1つだけ（VM の Claude／PC／スマホの競合を避ける）。
- 競合したら、どちらか一方の変更を正として、もう一方は手で取り込む。分からなければ Muse チャットで相談。
