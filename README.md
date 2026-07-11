# Joypad example (pygame)

ゲームパッド（ジョイパッド）の入力を pygame で読み取り、そのボタン操作をきっかけに
Linux/X11 上でデスクトップ操作（スクリーンショット・画面録画・マウス操作）を行うツールです。

現在 **Phase 1（土台づくり）** まで実装済み。ロードマップは [docs/PLAN.md](docs/PLAN.md) を参照。

## 構成

```
joypad/               再利用可能なパッケージ
  core.py             GamepadReader … 入力の共通処理（ポーリング・ワンショット判定）
  settings.py         既定値（ディスプレイ・録画範囲・保存先など）
  actions/            デスクトップ操作（X11 依存）
    mouse.py          マウス位置取得・クリック（xdotool）
    screenshot.py     スクリーンショット（ffmpeg / xrandr）
    recorder.py       画面録画（ffmpeg）
examples/             実行可能なサンプル
  gamepad_test.py     接続確認・入力テスト
  input_console.py    入力をコンソール表示（--one-shot 対応）
  input_window.py     入力を pygame ウィンドウ表示
  commander.py        ボタンでデスクトップ操作（本命）
docs/PLAN.md          実用化ロードマップ
```

## 動作環境

- Linux + **X11**（Wayland では動作しません。マウス操作・画面キャプチャが X11 依存のため）
- Python 3.10+
- 外部コマンド（`actions/` で使用）
  - `xdotool` — マウス位置取得・クリック
  - `ffmpeg`（`x11grab` 対応ビルド）— スクリーンショット・画面録画
  - `xrandr` — 画面解像度の取得
  ```
  sudo apt install xdotool ffmpeg x11-xserver-utils
  ```
  （未インストールの場合は、その操作を実行したときに案内メッセージを表示します）
- ゲームパッド（USB / Bluetooth 接続。ボタン 0〜3 を A/B/X/Y として扱います）

## セットアップ

```
python -m venv venv
. ./venv/bin/activate

pip install -r requirements.txt
```

## 使い方

サンプルはリポジトリ直下から実行してください（`examples/_bootstrap.py` が `joypad`
パッケージへのパスを通します）。いずれも `ESC` キーまたはウィンドウを閉じると終了します。

### 接続確認・入力テスト

まずはこれで動作確認するのがおすすめです。

```
python examples/gamepad_test.py
```

### 入力の可視化

```
python examples/input_console.py            # コンソール表示
python examples/input_console.py --one-shot # 押した瞬間に 1 回だけ表示
python examples/input_window.py             # pygame ウィンドウ表示
```

`input_window.py` は `~/.fonts/Orbitron-VariableFont_wght.ttf` があれば使用します
（無ければ標準フォント）。

### ゲームパッドでデスクトップ操作（本命）

| ボタン | 操作 |
| --- | --- |
| A | スクリーンショットを撮影し `screenshots/` に保存 |
| B | 左クリック（現在のマウス位置） |
| X | 現在のマウス位置をコンソールに表示 |
| Y | 画面録画のトグル（開始 / 停止） |

```
python examples/commander.py
```

> 注意: ディスプレイは `:0.0`、録画範囲は `joypad/settings.py` の既定値を使用します。
> 環境に合わせて `joypad/settings.py` を編集してください（Phase 2 で設定ファイル化予定）。

## ライブラリとして使う

```python
from joypad import GamepadReader
from joypad.actions import take_screenshot

with GamepadReader() as pad:
    while True:
        state = pad.poll()
        if state.should_quit:
            break
        if state.pressed and state.pressed[0]:   # A ボタンを押した瞬間
            take_screenshot()
```

## 補足

- コード内のコメント・出力・docstring は日本語で記述しています。
- `xkbmap` は `xkbcomp` で書き出したキーマップのダンプで、Python コードとは無関係です。

## Copyright

- The program code is licensed under the MIT License.
