"""joypad: ゲームパッド入力で X11 デスクトップ操作を行うツール。"""

from .core import GamepadReader, GamepadState, NoGamepadError

__all__ = ["GamepadReader", "GamepadState", "NoGamepadError"]
