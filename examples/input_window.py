"""ゲームパッド入力を pygame ウィンドウに表示する。

押されたボタンとスティック座標を画面に描画する。
~/.fonts/Orbitron-VariableFont_wght.ttf があれば使用する（無ければ標準フォント）。
ESC またはウィンドウを閉じると終了。
"""

import _bootstrap  # noqa: F401
import os

import pygame

from joypad import GamepadReader, NoGamepadError

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_PATH = os.path.expanduser("~/.fonts/Orbitron-VariableFont_wght.ttf")


def load_font() -> pygame.font.Font:
    try:
        return pygame.font.Font(FONT_PATH, 18)
    except FileNotFoundError:
        print(f"warning: Font file {FONT_PATH} is not found.")
        return pygame.font.Font(None, 18)


def main() -> None:
    try:
        pad = GamepadReader()
        pad.open()  # ここで pygame.init() 済み
    except NoGamepadError as e:
        print(e)
        return

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Gamepad Input Display")
    font = load_font()
    clock = pygame.time.Clock()

    try:
        while True:
            state = pad.poll()
            if state.should_quit:
                break

            screen.fill(BLACK)
            x, y = state.stick
            messages = [
                f"Button {state.name_of(i)} is pressed. stick coordinate = ({x}, {y})"
                for i in range(min(4, len(state.buttons)))
                if state.buttons[i]
            ]

            y_position = 50
            for message in messages:
                text_surface = font.render(message, True, WHITE)
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH / 2, y_position))
                screen.blit(text_surface, text_rect)
                y_position += 50

            pygame.display.flip()
            clock.tick(60)
    finally:
        pad.close()


if __name__ == "__main__":
    main()
