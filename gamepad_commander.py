import pygame
import sys
import os
import argparse
import subprocess

from screenshot import take_screenshot
from desktop_util import get_mouse_location, mouse_click


# Pygameの初期化
pygame.init()

# ジョイスティックの初期化
pygame.joystick.init()

# ボタンの状態
button_states = [0] * 4  # 0: A, 1: B, 2: X, 3: Y
button_states_one_shot =  [0] * 4  # 0: A, 1: B, 2: X, 3: Y

# アナログスティックの値を格納する変数
analog_x = 0
analog_y = 0


def main():
    # ジョイスティックが接続されているか確認
    if pygame.joystick.get_count() == 0:
        print("ジョイパッドが接続されていません")
        return

    # 最初のジョイスティックを取得
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # ジョイパッドの基本情報を表示
    print(f"\nジョイパッド情報:")
    print(f"名前: {joystick.get_name()}")
    print(f"ID: {joystick.get_id()}")
    print(f"ボタン数: {joystick.get_numbuttons()}")
    print(f"軸の数: {joystick.get_numaxes()}")
    print(f"ハット数: {joystick.get_numhats()}")
    print("-" * 50)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # キーボード入力の確認
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        # 現在押されているボタンの状態を取得
        buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
        axes = [round(joystick.get_axis(i), 2) for i in range(joystick.get_numaxes())]
        hats = [joystick.get_hat(i) for i in range(joystick.get_numhats())]

        # アナログスティックの値を取得
        global analog_x, analog_y
        analog_x = round(joystick.get_axis(0), 2)  # 左右
        analog_y = round(joystick.get_axis(1), 2)  # 上下

        # ボタンの状態を確認
        current_states = [joystick.get_button(i) for i in range(4)]
        button_names = ['A', 'B', 'X', 'Y']
        for i, (current, previous) in enumerate(zip(current_states, button_states)):
            button_states_one_shot[i] = current * (1 - previous)
            button_states[i] = current_states[i]

        # 状態の表示
        #print(button_states_one_shot + button_states)
        if button_states_one_shot[0] == 1:
            print('A button')
            print(f'hats: {hats}')
            take_screenshot()
        if button_states_one_shot[1] == 1:
            print('B button')
            print(f'buttons: {buttons}')
            mouse_click(1)
        if button_states_one_shot[2] == 1:
            print('X button')
            result = get_mouse_location()
            print(f' mouse at: {result}')
        if button_states_one_shot[3] == 1:
            print('Y button')

        clock.tick(30)  # 30FPS


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
        print("\nプログラムを終了しました")
