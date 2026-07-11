"""デスクトップ操作アクション（X11 依存）。

外部コマンド（xdotool / ffmpeg / xrandr）へのラッパー群。
"""

from ._util import MissingCommandError
from .mouse import get_mouse_location, mouse_click
from .screenshot import get_screen_resolution, take_screenshot
from .recorder import ScreenRecorder

__all__ = [
    "MissingCommandError",
    "get_mouse_location",
    "mouse_click",
    "get_screen_resolution",
    "take_screenshot",
    "ScreenRecorder",
]
