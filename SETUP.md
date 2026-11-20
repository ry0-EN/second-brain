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

## Windows PC（閲覧＋編集）— 今夜のチェックリスト

所要の目安：30〜45分。終わったらこのチャットで「できた」と声をかけて。詰まった画面はスクショを送ればその場で案内する。

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

### 5. Obsidian Gitプラグインの設定
1. 設定 → コミュニティプラグイン → 制限付きモードをOFF → 「閲覧」から **Obsidian Git** を検索してインストール → 有効化。
2. 設定 → Git で次を設定する（AndroidのGitSync 15分間隔に合わせた値）：
   - Auto commit-and-sync interval (minutes)：**15**
   - Auto commit-and-sync after stopping file edits：**ON**
   - Auto pull interval (minutes)：**15**
   - Pull on startup：**ON**
   - Push on commit-and-sync：**ON**
   - Merge strategy：**Merge**
   - Author name / Author email：RyoのGitHubと同じ名前・メール（`ry0-EN` のアカウントに合わせる）
3. コマンドパレット（`Ctrl+P`）→ `Obsidian Git: Create backup` を1回実行して、GitHubにcommitがpushされることを確認する。

### 6. Claude Code Remote Controlの確認（PC対話セッションをスマホから見る用）
- PCに **Claude Code** をインストールし、Proアカウントでログインする（VM側と同じ手順。ログインリンクはチャットで出す）。
- Vaultフォルダで `claude` を起動し、セッション内で `/remote-control` を実行する（または `claude remote-control` で起動）。
- 表示されるQRコードをスマホのClaudeアプリで読み取るか、Claudeアプリの **Codeタブ** からセッションを選ぶ。
- 確認ポイント：スマホからPCセッションの進行が見えること、メッセージを送れること。
- 注意：Remote ControlはPCが起動中で `claude` プロセスが動いている間だけ使える。PCがスリープすると切れ、復帰時に再接続される。**ヘッドレス実行（`claude -p`）はClaudeアプリには出ない**ので、履歴は従来どおり `AI/sessions/` とこのチャットで辿る。
- 参考：公式ドキュメント https://code.claude.com/docs/en/remote-control

### 7. 完了チェック
- [ ] `ダッシュボード.md` がPCのObsidianで開ける
- [ ] Obsidian Gitの自動commit・pushが動く（編集 → 15分以内にGitHubへ反映）
- [ ] スマホのGitSyncで手動同期 → PCでの編集がスマホのObsidianに反映される
- [ ] Remote ControlでスマホからPCセッションが見える

## 共通ルール

- 書き手は同時に1つだけ（VM の Claude／PC／スマホの競合を避ける）。
- 競合したら、どちらか一方の変更を正として、もう一方は手で取り込む。分からなければ Muse チャットで相談。
