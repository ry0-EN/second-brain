# Obsidian 第二の脳 — スターターVault（案）

Ryo向け。2026-11-20に決めた運用（基本はClaude Code経由・方式2ヘッドレスをProの通常利用枠の中で使う、Usage creditsはOFF、枠の常態化した不足時のみ方式1ベースのハイブリッドを検討）に基づく、すぐ使えるひな形だよ。

## 構成

```
.
├── AGENTS.md            # 正本ルール（Claude Code / Muse 共通）
├── CLAUDE.md            # @AGENTS.md を参照するだけ
├── DECISIONS.md         # Ryoが決めることチェックリスト（Aの4つ＋Bの推奨デフォルト）
├── README.md            # このファイル
├── .claude/settings.json # 権限ガードレール＋hooks
├── .claude/hooks/deny-protected.py
├── .gitignore
├── 00-inbox/            # 取り込み待ち（rawへの入口）
├── raw/                 # 元資料。AIは読むだけ、絶対に編集しない
├── wiki/                # AIが整理して育てる知識
│   ├── index.md         # カタログ：1行1ページ
│   └── log.md           # 取り込み・検索・lintの append-only 記録
├── AI/                  # エージェントだけが書く場所（下書き・セッション要約）
├── 10-projects/ 20-areas/ 30-resources/ 40-archive/
├── 50-daily/            # デイリーノート
├── templates/           # daily / decision / research-note / session-report
└── attachments/
```

PARAを土台に、Karpathy流 LLM Wiki（`raw/` → `wiki/`）を重ねたハイブリッドだよ。

## 使い方（最短）

1. このフォルダを丸ごとPCにコピーして、Obsidianで「Open folder as vault」する。
2. 置き場は決定済み：GitHub Private `ry0-EN/second-brain`（2026-11-20作成・初回push済み）。PCでは `git clone https://github.com/ry0-EN/second-brain.git` するだけ。
3. Obsidian Git プラグインを入れて、auto-pull / auto-commit をオンにする。
4. kepano/obsidian-skills を入れる（`npx skills add kepano/obsidian-skills` かプラグイン経由）。これがないとエージェントが普通のMarkdownを書いて wikilink を壊しがち。
5. このチャットで「調べてObsidianにまとめて」と投げるだけ。アタシがこのVaultを読み書きして、diffを見せて、RyoがOKしたら commit / push するよ。

## お金のガードレール（Proプラン）

- 追加費用ゼロが基本。Museが直接やる方式1はClaude Codeを経由しないから費用ゼロ。
- ヘッドレス（`claude -p`）はProの通常利用枠（対話利用と共有）から消費される。Pro向けの月$20 Agent SDKクレジットという別枠は存在しない（2026年10月の制度変更で廃止／月次APIクレジットはMax・Teamのみ対象）。使い切ったら止まるだけ。
- **Usage credits（旧Extra Usage、従量課金）はOFFのままにしておくこと。** ONにしない限り、Pro以上の課金は発生しない。
- 1回のヘッドレス実行の上限は `20ターン`（AGENTS.md・DECISIONS.md参照）。

## 最初の試運転テーマ

DECISIONS.mdのA-4で1つだけ決めてね。決まるまでは、このVaultの `wiki/` に「調べ物を蓄積する」型で進められるよ。
