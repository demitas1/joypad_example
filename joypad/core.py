"""ゲームパッド入力の共通処理。

これまで example.py / example_cui.py / gamepad_commander.py / gamepad-test.py に
重複していた「pygame 初期化 → Joystick 取得 → ポーリング → ワンショット判定」を
GamepadReader に集約する。
"""

from dataclasses import dataclass, field
from typing import List, Tuple

import pygame

from . import settings


class NoGamepadError(RuntimeError):
    """ゲームパッドが 1 台も接続されていないときに送出する。"""


@dataclass
class GamepadState:
    """1 フレーム分の入力状態。"""

    buttons: List[int] = field(default_factory=list)   # 現在押されているか（0/1）
    pressed: List[int] = field(default_factory=list)   # 押した瞬間だけ 1（ワンショット）
    axes: List[float] = field(default_factory=list)    # アナログ軸の値
    hats: List[Tuple[int, int]] = field(default_factory=list)  # ハット（十字キー）
    should_quit: bool = False                          # QUIT / ESC を検出したか

    def name_of(self, index: int) -> str:
        """ボタン番号を A/B/X/Y などの名前に変換する。"""
        if 0 <= index < len(settings.BUTTON_NAMES):
            return settings.BUTTON_NAMES[index]
        return f"Button {index}"

    @property
    def stick(self) -> Tuple[float, float]:
        """左スティックの (x, y)。軸が無ければ (0.0, 0.0)。"""
        x = self.axes[0] if len(self.axes) > 0 else 0.0
        y = self.axes[1] if len(self.axes) > 1 else 0.0
        return (x, y)


class GamepadReader:
    """1 台のゲームパッドを開き、毎フレームの状態を返す。

    コンテキストマネージャとして使うと open()/close() を自動で行う。

        with GamepadReader() as pad:
            while True:
                state = pad.poll()
                if state.should_quit:
                    break
    """

    def __init__(self, index: int = 0, axis_ndigits: int = 2):
        self.index = index
        self.axis_ndigits = axis_ndigits
        self.joystick = None
        self._prev_buttons: List[int] = []

    def __enter__(self) -> "GamepadReader":
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def open(self) -> None:
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            raise NoGamepadError("ジョイパッドが接続されていません")
        self.joystick = pygame.joystick.Joystick(self.index)
        self.joystick.init()
        self._prev_buttons = [0] * self.joystick.get_numbuttons()

    def close(self) -> None:
        pygame.quit()
        self.joystick = None

    @property
    def info(self) -> dict:
        """接続中のゲームパッドの基本情報。"""
        if self.joystick is None:
            raise RuntimeError("open() が呼ばれていません")
        return {
            "name": self.joystick.get_name(),
            "id": self.joystick.get_id(),
            "buttons": self.joystick.get_numbuttons(),
            "axes": self.joystick.get_numaxes(),
            "hats": self.joystick.get_numhats(),
        }

    def poll(self) -> GamepadState:
        """イベントを処理し、現在の入力状態を返す。"""
        if self.joystick is None:
            raise RuntimeError("open() が呼ばれていません")

        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                should_quit = True

        buttons = [
            self.joystick.get_button(i)
            for i in range(self.joystick.get_numbuttons())
        ]
        # ワンショット: 前フレーム 0 → 今 1 の立ち上がりだけ 1 にする
        pressed = [
            cur * (1 - prev)
            for cur, prev in zip(buttons, self._prev_buttons)
        ]
        self._prev_buttons = buttons

        axes = [
            round(self.joystick.get_axis(i), self.axis_ndigits)
            for i in range(self.joystick.get_numaxes())
        ]
        hats = [
            self.joystick.get_hat(i)
            for i in range(self.joystick.get_numhats())
        ]

        return GamepadState(
            buttons=buttons,
            pressed=pressed,
            axes=axes,
            hats=hats,
            should_quit=should_quit,
        )
