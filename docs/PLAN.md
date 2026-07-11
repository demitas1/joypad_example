# 実用化計画

ゲームパッドのボタン操作をトリガーに、Linux/X11 上でデスクトップ操作を行うツールを
実用的なものへ育てるための計画。

## 目的（確定事項）

- **主目的**: 作業記録・録画 ／ 汎用マクロ実行
- **対応環境**: Linux / X11 のみ（Wayland・他OSは対象外）
- **進め方**: Phase 1 → 2 → 3 の順で段階的に作り込む

## 現状の課題

- pygame の初期化・ポーリングループ・ワンショット判定が 4 ファイルに重複
  （`example.py` / `example_cui.py` / `gamepad_commander.py` / `gamepad-test.py`）
- ボタン→操作の割り当てが `gamepad_commander.py` にハードコード（変更にコード編集が必要）
- ディスプレイ `:0.0`・録画範囲・保存先などがべた書き
- 録画（`screen_recorder.py`）がゲームパッド操作と接続されていない
- エラー処理が薄い（`get_screen_resolution()` が `None` を返し得る、外部コマンド不在時の案内なし）

## Phase 1 ── 軽く整理（土台づくり） ← 今ここ

既存機能を壊さず、重複と散らかりを解消して再利用しやすくする。

- 共通処理を `joypad/core.py` の `GamepadReader` に集約
  （init → `Joystick(0)` 取得 → ポーリング → ワンショット判定）
- デスクトップ操作を `joypad/actions/`（screenshot / recorder / mouse）へ整理
- ハードコード値（display・録画範囲・保存先）を `joypad/settings.py` の既定値＋引数に外出し
- エラー処理補強（解像度取得失敗、`ffmpeg`/`xdotool`/`xrandr` 不在時のわかりやすいメッセージ）
- 実験スクリプトを `examples/` へ移動し、`GamepadReader` を使うよう更新
- README / CLAUDE.md を新構成に追従

## Phase 2 ── ちゃんとしたCLI（本命機能）

「作業記録・録画」＋「汎用マクロ」を設定ファイルで扱えるようにする。

- 設定ファイル（TOML）でボタン→アクションを割り当て（コード編集不要に）
- アクションレジストリ：
  `screenshot` / `record_toggle`（同一ボタンで録画開始⇄停止）/ `click` / `mouse_move` /
  `run_command`（任意シェルコマンド＝汎用マクロ）
- 録画状態などをコンソール/通知に表示
- `pyproject.toml` でパッケージ化し `joypad` コマンドとして実行、ログ出力

## Phase 3 ── 本格アプリ（拡張）

- プロファイル切替（モードボタンでマクロセットを切り替え）、複数パッド対応
- 長押し・コンボ・連射などの入力パターン
- 設定ホットリロード、状態HUD、プラグイン的なアクション追加
- テスト・CI
