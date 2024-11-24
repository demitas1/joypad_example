import pygame
import sys
import os
import argparse

# Pygameの初期化
pygame.init()

# ジョイスティックの初期化
pygame.joystick.init()

# アナログスティックの値を格納する変数
analog_x = 0
analog_y = 0

def clear_console():
    # OSに応じてクリアコマンドを実行
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_arguments():
    parser = argparse.ArgumentParser(description='ジョイパッド入力検出プログラム')
    parser.add_argument('--one-shot', action='store_true',
                      help='ボタンが押されたら1回だけメッセージを表示し、リリースまで待機します')
    return parser.parse_args()

def main():
    args = parse_arguments()
    one_shot = args.one_shot

    # ジョイスティックが接続されているか確認
    if pygame.joystick.get_count() == 0:
        print("ジョイパッドが接続されていません")
        return

    # 最初のジョイスティックを取得
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"ジョイパッド入力待機中... (終了するにはESCキーを押してください)")
    print(f"モード: {'ワンショット' if one_shot else '通常'}")

    clock = pygame.time.Clock()

    # ボタンの状態を記録する辞書（ワンショットモード用）
    button_states = {i: False for i in range(4)}  # 0: A, 1: B, 2: X, 3: Y

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # キーボード入力の確認
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        # アナログスティックの値を取得
        global analog_x, analog_y
        analog_x = round(joystick.get_axis(0), 2)  # 左右
        analog_y = round(joystick.get_axis(1), 2)  # 上下

        # ボタン入力の確認とメッセージ表示
        messages = []

        # ボタンの状態を確認
        current_states = [joystick.get_button(i) for i in range(4)]
        button_names = ['A', 'B', 'X', 'Y']

        if one_shot:
            # ワンショットモード: ボタンが押されてから離されるまで1回だけ表示
            for i, (current, previous) in enumerate(zip(current_states, button_states.values())):
                if current and not previous:  # ボタンが押された瞬間
                    messages.append(f"{button_names[i]}ボタンが押されました！ スティック座標: ({analog_x}, {analog_y})")
                button_states[i] = current
        else:
            # 通常モード: ボタンが押されている間は常に表示
            for i, current in enumerate(current_states):
                if current:
                    messages.append(f"{button_names[i]}ボタンが押されました！ スティック座標: ({analog_x}, {analog_y})")

        # メッセージがある場合のみ画面をクリアして表示
        if messages:
            # コンソールのクリア
            # clear_console()

            print(f"モード: {'ワンショットモード' if one_shot else '通常モード'}")
            for message in messages:
                print(message)

        clock.tick(60)  # 60FPS

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
        print("\nプログラムを終了しました")
