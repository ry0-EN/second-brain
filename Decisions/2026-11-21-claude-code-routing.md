---
date: 2026-11-21
tags: [decision, routing, claude-code]
project: second-brain
related: ["[[Decisions/2026-11-20-document-routing]]"]
---

# 作業の振り分け：寄せ気味ハイブリッドに決定

## 背景
- 2026-11-20の決定（[[Decisions/2026-11-20-document-routing]]）では「デザイン資料はClaude、その他はClaude Code向きなら提案してRyoが判断」が基本だったが、「定常業務をどれだけClaude Codeに寄せるか」は未決定のままだった（判断材料＝同一ソースでの作り比べテスト結果を見て決める、としていた）。
- テスト結果：Claude Code版は検証ラベルが厳密で、元wikiページの誤り2件（「今日やる3つ」の出典誤認、形骸化「半年」→正しくは約2ヶ月）を検出。一方でClaude CodeはWeb取得・Googleコネクタが使えず、ソースはファイル渡しが必要。Pro利用枠はチャットと共有。

## 決定（2026-11-21、初回週次レビューでRyoが承認）
- **寄せ気味ハイブリッド**を採用する。
  - Claude Codeに寄せる：Vaultのバッチ作業、検証が重い調査、コーディング、繰り返し処理。実行は従来どおり「Claudeが提案 → Ryoが承認」で行う。
  - Museが担う：デザイン資料（PDF等）、Google連携（Gmail / Tasks / Calendar）、日常の相談・チャット。
- 狙い：Claude Proの利用枠を活かしつつ、Claude Codeが届かない領域（Web・コネクタ・デザイン）をMuseがカバーする。

## 備考
- 枠の消費ペースを見て、運用しながら見直す。日次バッチはSonnet指定（Opusは消費が重い）。
