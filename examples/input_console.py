"""ゲームパッド入力をコンソールに表示する。

--one-shot を付けると「押した瞬間に 1 回だけ」表示する（押し続けても連続表示しない）。
ESC またはウィンドウを閉じると終了。
"""

import _bootstrap  # noqa: F401
import argparse

import pygame

from joypad import GamepadReader, NoGamepadError


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ジョイパッド入力検出プログラム")
    parser.add_argument(
        "--one-shot",
        action="store_true",
        help="ボタンが押された瞬間に 1 回だけメッセージを表示する",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    try:
        pad = GamepadReader()
        pad.open()
    except NoGamepadError as e:
        print(e)
        return

    print("ジョイパッド入力待機中... (終了するには ESC キー)")
    print(f"モード: {'ワンショット' if args.one_shot else '通常'}")

    clock = pygame.time.Clock()
    try:
        while True:
            state = pad.poll()
            if state.should_quit:
                break

            x, y = state.stick
            # ワンショットなら pressed（立ち上がり）、通常なら buttons（押下中）を見る
            source = state.pressed if args.one_shot else state.buttons
            for i in range(min(4, len(source))):
                if source[i]:
                    print(
                        f"{state.name_of(i)}ボタンが押されました！ "
                        f"スティック座標: ({x}, {y})"
                    )
            clock.tick(60)
    finally:
        pad.close()
        print("\nプログラムを終了しました")


if __name__ == "__main__":
    main()
