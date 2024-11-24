import pygame
import sys
import os

# Pygameの初期化
pygame.init()

# ジョイスティックの初期化
pygame.joystick.init()

# 画面設定
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gamepad Input Display")

# フォント設定
FONT_PATH = os.path.expanduser('~/.fonts/Orbitron-VariableFont_wght.ttf')
#FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
try:
    font = pygame.font.Font(FONT_PATH, 18)
except FileNotFoundError:
    print(f"warning: Font file {FONT_PATH} is not found.")
    font = pygame.font.Font(None, 18)

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# アナログスティックの値を格納する変数
analog_x = 0
analog_y = 0

def main():
    # ジョイスティックが接続されているか確認
    if pygame.joystick.get_count() == 0:
        print("No joypad is available.")
        return

    # 最初のジョイスティックを取得
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)  # 画面をクリア

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # キーボード入力の確認
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # アナログスティックの値を取得
        global analog_x, analog_y
        analog_x = round(joystick.get_axis(0), 2)  # 左右
        analog_y = round(joystick.get_axis(1), 2)  # 上下

        # ボタン入力の確認とメッセージ表示
        messages = []

        # Aボタン（ボタン0）
        if joystick.get_button(0):
            messages.append(f"Button A is pressed. stick coordinate = ({analog_x}, {analog_y})")

        # Bボタン（ボタン1）
        if joystick.get_button(1):
            messages.append(f"Button B is pressed. stick coordinate = ({analog_x}, {analog_y})")

        # Xボタン（ボタン2）
        if joystick.get_button(2):
            messages.append(f"Button X is pressed. stick coordinate = ({analog_x}, {analog_y})")

        # Yボタン（ボタン3）
        if joystick.get_button(3):
            messages.append(f"Button Y is pressed. stick coordinate = ({analog_x}, {analog_y})")

        # メッセージの表示
        y_position = 50
        for message in messages:
            text_surface = font.render(message, True, WHITE)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH/2, y_position))
            screen.blit(text_surface, text_rect)
            y_position += 50

        pygame.display.flip()
        clock.tick(60)  # 60FPS

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
