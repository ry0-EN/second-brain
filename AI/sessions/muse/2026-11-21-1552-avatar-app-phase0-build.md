---
date: 2026-11-21
tags: [session, muse, android]
project: home-screen-avatar-app
related: [[home-screen-avatar-app]], [[android-build-on-muse-vm]]
---

# アバターアプリ Phase 0a：ビルド環境構築と空アプリのビルド成功

- 実施：Muse（プロジェクト雛形の作成のみClaude Code）
- 内容：
  - アニメーション方式は「3方式の小実験で比較してから決める」で確定（たたき台§7に記録、commit 61e176e）
  - VMにJDK 17／Android SDK（API 35）／Gradle 8.9を永続領域へ配置
  - Java通信の遮断（出口プロキシによるTLSリセット、localhostリセット、other_tcp権限）を切り分け。Ryoが `other_tcp` を「確認する」に変更したがJava TLSのリセットは残ったため、最終的にオフライン・ミラー方式を確立（詳細は [[android-build-on-muse-vm]]）
  - 空アプリ `jp.ryo.museavatar`（Muse Avatar）のdebug APK（813KB）ビルド成功。aapt2でパッケージ名・ラベルを検証済み
- 成果物：`~/workspace/projects/home-screen-avatar-app/`（APK: `muse-avatar-phase0.apk` をチャットでRyoへ送付）
- 次：Phase 0b＝Fold5へのインストールと起動確認（Ryoの操作待ち）
