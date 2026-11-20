# セッションレポート 2026-11-21 05:01 — TimeTreeへのGoogleカレンダー表示設定（Muse直接作業）

## 指示内容
- Ryo: 「時間設定したいタスクはGoogleカレンダーの予定にしたい」（2026-11-20 22:55）→ 使い分けルールを記録。
- Ryo: 「TimeTreeにGoogleカレンダーの情報って同期できる？」→ 公式ヘルプで確認し、設定を一緒に実施。
- Ryo: 「各アプリの設定完了したけどTimeTree側にGoogleカレンダーの予定が見当たらない」→ 切り分け支援。

## 処理の流れ
1. Google Tasksの時刻仕様を訂正：Web UIでは時刻設定可。ただしAPI/コネクタ経由は日付のみ保持（実データでも確認：お薬タスクの due は日付のみ）。
2. 使い分けルールを [[Preferences/work-style]] に追記（時刻つき＝Googleカレンダーの予定／日付のみ＝Google Tasks「涼さんのリスト」）。
3. TimeTree公式ヘルプで表示方法を確認：一方向表示（Google→TimeTree）、ホームカレンダーのみ自動更新、Web版は不可。
4. Androidで設定実施：Googleカレンダーアプリの共有ON、TimeTreeのカレンダー権限ON（Ryo実施）。
5. 予定が見えず切り分け：Googleカレンダー側の実在をAPIで確認（テスト予定 2026-11-21 3:00〜4:00）。Googleカレンダーアプリでは表示あり → スマホ同期は正常、TimeTree表示側の問題に特定。
6. Ryoが発見：TimeTree右上ドロップダウンのフィルターで `ryo.enomo@gmail.com` にチェック → テスト予定がTimeTreeに表示され、設定完了。

## 変更したファイル
- `Preferences/work-style.md`（使い分けルールを追記）
- `Knowledge/timetree-google-calendar-display.md`（新規：設定手順とハマりどころ）
- `ダッシュボード.md`（本日の要約・本レポートへのリンク・残タスク更新）
- `wiki/log.md`（作業記録を追記）
- 本レポート

## 結果
- TimeTreeにGoogleカレンダーの予定が自動表示される状態になった。今後、アタシがGoogleカレンダーへ入れた時刻つき予定はTimeTreeでも見られる。
- 成果物の場所：Vault内 `Knowledge/timetree-google-calendar-display.md`（手順の正本）。
- 作業概要：Muse直接作業（Claude Code経由なし）。時刻は深夜帯（02:02〜05:01 JST）。
- 未コミット：上記変更は次のVault commitに含める（RyoのOK待ち）。
