# セットアップ手順（デバイス別）

正本は GitHub Private リポジトリ `ry0-EN/second-brain`。どのデバイスも、このリポジトリを同期して同じフォルダを Obsidian で開く。

## Android（閲覧＋軽い編集）— GitSync 方式

1. Play ストアで **GitSync** をインストールする。
2. GitSync を開き、GitHub アカウント（ry0-EN）でログインする。
3. 先に端末内に空フォルダ `Documents/second-brain` を作っておき、GitSync でそのフォルダを指定して **直接クローン** する（ネスト方式は当環境で固まったため、この方式が実績あり）。
4. 同期を1回実行して、ファイルが降りてきたことを確認する。
5. Obsidian アプリで「フォルダーを保管庫として開く」から、そのフォルダを選ぶ。
6. GitSync 側は定期同期を ON にする（実績設定：15分間隔）。大事な確認の前は手動同期が確実。

注意：
- 同期は準リアルタイム：アプリ開閉時・手動・ウィジェットなら数秒〜数分、定期チェックだけだと最短30分間隔（GitSync公式仕様）。確実に最新が欲しい時は、見る前に手動で1回同期するのが安全。
- VM 側で Claude が作業している最中は、同じノートをスマホで編集しない（競合防止）。

## Windows PC（閲覧＋編集）— チェックリスト（2026-11-20 完了済み）

初回セットアップは2026-11-20夜に全ステップ完了。以後は再セットアップ時の手順書として使う。所要の目安：30〜45分。詰まった画面はスクショを Muse チャットに送ればその場で案内する。

### 0. 始める前の確認
- スマホのGitSyncで1回**手動同期**しておく（PC側が最新版をcloneするため）。
- PCではObsidianを開く前に、まずcloneまで済ませる（空フォルダを保管庫として開くと後で面倒）。

### 1. インストール（2つ）
- **Git for Windows** — https://git-scm.com/download/win からダウンロードして、基本デフォルト設定でインストール（エディタ選択は「Use Visual Studio Code」でも「Use Vim」でもOK。PATHは「Git from the command line and also from 3rd-party software」を選ぶ）。
- **Obsidian** — https://obsidian.md/download からWindows版をインストール。

### 2. GitHub認証（大事：パスワードではcloneできない）
GitHubはHTTPSのgit操作でパスワード認証を廃止済みのため、次のどちらかで認証する：
- **推し：GitHub CLI** — https://cli.github.com/ から `gh` を入れて、PowerShellで `gh auth login` を実行（GitHub → SSHではなくHTTPSを選択）。これでclone時の認証が自動で通る。
- または **Personal Access Token（classic、repo権限）** を作り、clone時のパスワード欄にトークンを貼る。

### 3. clone
PowerShellで任意の場所（例：`C:\Users\<ユーザー名>\Documents\second-brain`）にcloneする：
```
git clone https://github.com/ry0-EN/second-brain.git
cd second-brain
git log --oneline -3
```
`git log` で今日のcommit（ダッシュボード追加など）が見えれば最新版が取れている。

### 4. Obsidianで保管庫として開く
- Obsidian → 「フォルダーを保管庫として開く」→ cloneした `second-brain` フォルダを選択。
- 最初に開くノートはルートの **`ダッシュボード.md`** にする（今日の要約・残タスク・レポート一覧が1枚で見える）。
- `Knowledge/mistakes.md` と `SETUP.md` が見えることを確認する。

### 5. Obsidian Gitプラグインの設定（2026-11-20 実績版）
1. 設定 → コミュニティプラグイン → 制限付きモードをOFF → 「閲覧」で **Git** とだけ検索（作者は Vinzent。表示名は「Obsidian Git」ではないため、フルネーム検索ではヒットしない）→ インストール → 有効化。
2. 設定 → Git で次を設定する（AndroidのGitSync 15分間隔に合わせた値）：
   - **Automatic**：
     - Use separate commit and push intervals：**ON**（OFFだと Auto push / Auto pull がグレーアウトして変更できない）
     - Auto commit-and-sync interval (minutes)：**15**
     - Auto commit-and-sync after stopping file edits：**ON**
     - Auto push interval (minutes)：**15** ／ Auto pull interval (minutes)：**15**
   - **Sync**：
     - Merge strategy：**Merge** ／ Merge strategy on conflicts：**None (Git default)**
     - Pull on startup：**ON**
     - Push on commit-and-sync：**ON** ／ Pull on commit-and-sync：**ON** ／ Squash commits before push：**OFF**
   - **Identity**：
     - Repository author name：**ry0-EN** ／ Repository author email：**既存コミットと同じメール**（空欄だとグローバル設定を参照する。PCでグローバル未登録のままだとコミットできない）
   - その他のカテゴリ（Commit / Editor / Views / Interface / Advanced）はデフォルトのまま。
3. コマンドパレット（Obsidianの画面上で `Ctrl+P`）→ **`Git: Commit-and-sync`** を1回実行して、GitHubにcommitがpushされることを確認する（旧称の `Create backup` は現行バージョンには無い）。Obsidianの通知はすぐ消えて履歴も残らないため、到達確認は Git の履歴ビュー（`Git: Open history view`）か GitHub 側で行う。
   - 実績（2026-11-20）：`vault backup` コミット2件がGitHubに到達し、`00-inbox/pc-test.md` がスマホのObsidianでも確認できた。

### 6. Claude Code Remote Controlの確認（PC対話セッションをスマホから見る用）
- 起動方式は CLI版と **Claude Desktopアプリ版** の2通りあり、公式でもどちらからでも Remote Control を開始できる。2026-11-20 に Ryo が **Desktopアプリ版** を選択し、そちらで確認完了（判断の記録は [[Decisions/2026-11-20-pc-claude-code-desktop]]）。
- Desktopアプリ版の手順（実績）：
  1. Claudeアプリ（Windows）を入れ、Proアカウントでサインイン → **Codeタブ** → 新規セッション。
  2. 入力欄下の設定：Environment＝**このコンピューター（Local）**、フォルダ＝`second-brain`、権限モード＝**手動（Manual）**（入力欄右下の「自動」をクリックして切り替える）。
  3. 「このワークスペースを信頼しますか？」が出たら **ワークスペースを信頼**。信頼後にフォルダ名の右へ出る **ワークツリー** のチェックボックスは **OFFのまま**（ONだと隔離コピーが作られ、Obsidianで開いているフォルダとズレる）。
  4. `/remote-control` を打つと `/remote-control isn't available in this environment.` と返る場合がある（2026-11-20 実績）。その時はセッション右パネル「環境」カードの **Remote Control スイッチをON** にする。「Remote Control がオンになりました」と表示されれば成功。
  5. スマホのClaudeアプリ → **Codeタブ** のセッション一覧に、PCアイコン＋緑ドットのセッションが出る。スマホから送った文がPCにリアルタイム表示され、返事がスマホに返ればOK（実績済み）。
- 注意：Remote ControlはPCが起動中でセッションが動いている間だけ使える。PCがスリープすると切れ、復帰時に再接続される。**ヘッドレス実行（`claude -p`）はClaudeアプリには出ない**ので、履歴は従来どおり `AI/sessions/` とこのチャットで辿る。
- 参考：公式ドキュメント https://code.claude.com/docs/en/remote-control

### 7. 完了チェック（2026-11-20 全項目クリア）
- [x] `ダッシュボード.md` がPCのObsidianで開ける
- [x] Obsidian Gitのcommit・pushが動く（手動 Commit-and-sync で到達確認済み。自動も15分間隔で設定済み）
- [x] スマホのGitSyncで手動同期 → PCでの編集（`00-inbox/pc-test.md`）がスマホのObsidianに反映される
- [x] Remote ControlでスマホからPCセッションが見え、メッセージも送れる

## 共通ルール

- 書き手は同時に1つだけ（VM の Claude／PC／スマホの競合を避ける）。
- 競合したら、どちらか一方の変更を正として、もう一方は手で取り込む。分からなければ Muse チャットで相談。
