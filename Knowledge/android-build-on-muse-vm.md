---
date: 2026-11-21
tags: [android, build, muse-vm]
project: home-screen-avatar-app
related: [[home-screen-avatar-app]]
---

# Muse VM上でAndroidアプリをビルドする（環境制約と確立した手順）

2026-11-21、ホーム画面アバターアプリのPhase 0で確立。VM再構築後もこの手順で再現できる。

## 環境制約（実測で判明）

- **Javaプロセスのネットワーク通信はVMの出口プロキシに遮断される**：JavaのTLSは接続リセット、HttpURLConnectionのCONNECTはプロキシ応答の解析で例外（NoSuchElementException）。curl / Python (OpenSSL) は同じプロキシ経由で正常に通る。
- **localhost宛のJavaソケット通信もリセットされる**（Gradleデーモンのプロトコルが文字化け＝遮断メッセージの先頭 'm' を受信）。→ Gradleデーモンは使えない。
- **アシスタントの直接TCPは権限 `other_tcp` が既定で拒否**：設定で「確認する」に変えてもJava TLSのリセットは解消しなかった（遮断メッセージは消える）。
- **/tmp は512MBのtmpfs**：大きなダウンロードを置くと途中で切れる（26MBで止まって見えたのはこれ）。ダウンロードは必ずホーム配下へ。
- 作業ユーザーはrootだがHOME=/home/hatch。Javaのuser.homeは/rootになるため、Gradleは `GRADLE_USER_HOME=/home/hatch/.gradle` を明示する。

## 確立した手順（オフライン・ミラー方式）

1. ツールチェーンはホーム配下（永続領域）に手置き：JDK 17 (Temurin) = `~/.local/jdk17`、Gradle 8.9 = `~/.local/gradle-8.9`、Android SDK = `~/android-sdk`（cmdline-tools / platform-tools / platforms;android-35 / build-tools;34.0.0 / licenses）。sdkmanagerはJava製で通信できないため、zipをcurlで取得して配置する（build-tools 35のzip名は404だったので34を使用）。
2. 依存はPythonで事前にミラーする：`~/workspace/projects/tools/mirror_deps.py` が「Gradleを `--offline` で実行 → 不足モジュールを解析 → 公式repo（Google Maven / Maven Central / Plugin Portal）からcurl相当で取得 → `~/maven-repo` に配置」を繰り返す。プロジェクトの `settings.gradle.kts` は `file:///home/hatch/maven-repo` のみを参照。
3. ビルド条件：`--offline --no-daemon`、`GRADLE_OPTS="-Xmx2048m -Dfile.encoding=UTF-8"`、プロジェクトの `gradle.properties` に `kotlin.compiler.execution.strategy=in-process`（Kotlinデーモン回避）と空の `org.gradle.jvmargs`（フォーク回避）。
4. 中継プロキシ方式（Gradle→localhost Python中継→HTTPS）は、localhost TCPのリセットのため不採用。スクリプトは `~/workspace/projects/tools/relay.py` に残置。

## 実績

- 空アプリ（jp.ryo.museavatar）のdebug APK（約813KB）のビルド成功まで、ミラーループ8周・部品156個超。
- 成果物やアプリの内容に方式の影響はない（部品は全て公式repoから取得）。
