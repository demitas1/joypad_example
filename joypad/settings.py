"""既定値の定数。

これまで各スクリプトにハードコードされていた値をここに集約する。
Phase 2 で設定ファイルから上書きできるようにする予定。
"""

# X11 ディスプレイ指定（ffmpeg x11grab / xrandr で使用）
DISPLAY = ":0.0"

# スクリーンショットの保存先ディレクトリ
SCREENSHOT_DIR = "screenshots"

# xrandr で解像度を取得できなかった場合のフォールバック
FALLBACK_RESOLUTION = "1920x1080"

# 画面録画の既定パラメータ
RECORD_SOURCE_SIZE = "3780x2120"   # 実画面サイズ
RECORD_VIDEO_SIZE = "1920x1080"    # 出力サイズ
RECORD_FRAMERATE = 30
RECORD_OFFSET_X = 0
RECORD_OFFSET_Y = 40

# ボタン番号 → 名前（0:A, 1:B, 2:X, 3:Y）
BUTTON_NAMES = ["A", "B", "X", "Y"]
