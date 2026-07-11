"""ゲームパッドの接続確認・入力テスト。

検出したゲームパッドの情報を表示し、押されたボタン・軸・ハットをコンソールに表示する。
まずはこれで動作確認するのがおすすめ。ESC またはウィンドウを閉じると終了。
"""

import _bootstrap  # noqa: F401
from time import sleep

from joypad import GamepadReader, NoGamepadError


def main() -> None:
    try:
        pad = GamepadReader()
        pad.open()
    except NoGamepadError as e:
        print(e)
        return

    try:
        info = pad.info
        print("\nジョイパッド情報:")
        print("-" * 40)
        print(f"名前: {info['name']}")
        print(f"軸の数: {info['axes']}")
        print(f"ボタンの数: {info['buttons']}")
        print(f"ハットの数: {info['hats']}")
        print("\n入力テスト開始... ESC で終了")

        while True:
            state = pad.poll()
            if state.should_quit:
                break

            active = []
            buttons = [f"Button {i}" for i, v in enumerate(state.buttons) if v]
            if buttons:
                active.append("Buttons: " + ", ".join(buttons))
            axes = [f"Axis {i}:{v}" for i, v in enumerate(state.axes) if abs(v) > 0.1]
            if axes:
                active.append("Axes: " + ", ".join(axes))
            hats = [f"Hat {i}:{v}" for i, v in enumerate(state.hats) if v != (0, 0)]
            if hats:
                active.append("Hats: " + ", ".join(hats))

            if active:
                print("\n".join(active))
            sleep(0.1)  # CPU 負荷軽減
    finally:
        pad.close()
        print("\nテストを終了しました")


if __name__ == "__main__":
    main()
