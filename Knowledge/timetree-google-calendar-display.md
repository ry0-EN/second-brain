---
date: 2026-11-21
tags: [knowledge, setup, calendar, timetree]
project: second-brain
related: [[Preferences/work-style]]
---

TimeTreeにGoogleカレンダーを表示する設定（Android、2026-11-21に完了・実証済み）

- 仕組み：Googleカレンダー → スマホの標準カレンダー経由 → TimeTreeに一方向表示（自動更新あり）。逆向き（TimeTree→Google）は不可。Web版TimeTreeでは外部カレンダーを利用できない（アプリ専用）。共有相手には表示されない（自分だけ）。
- 手順：
  1. Googleカレンダーアプリ：設定で「Googleカレンダーのデータを他のアプリと共有する」をON。
  2. スマホの設定 → アプリ → TimeTree → 許可 → カレンダーをON。
  3. TimeTree：ホームカレンダー画面の右上ドロップダウン（フィルター）で、チェックボックス一覧から `ryo.enomo@gmail.com` にチェックを入れる。
- ハマりどころ：手順3のチェックを入れるまで予定が見えなかった。「設定は全部終わったのに見えない」場合は、まずこのフィルターのチェックを確認する。
- 検証：Googleカレンダーのテスト予定（2026-11-21 3:00〜4:00）がTimeTree上に表示されることを確認。さらに実予定（同日15:00の服薬予定をClaudeがGoogleカレンダーへ登録）も、GoogleカレンダーアプリとTimeTreeの両方で表示を確認し、パイプライン全体が実証済み。
- 同期タイミング：公式に固定間隔の公表なし（「自動更新」とのみ）。反映は2段階（Googleサーバー→スマホ標準カレンダー→TimeTreeがアプリ起動時に読み直し）。削除時は特にラグが出ることがある。急ぐ場合は、Googleカレンダーアプリを開く／TimeTreeを再起動する／端末のアカウント同期で「今すぐ同期」。
- 運用との関係：時刻つきの頼みはGoogleカレンダーの予定にする（[[Preferences/work-style]] の使い分けルール）ため、アタシが入れた予定はこの経路でTimeTreeにも自動表示される。
