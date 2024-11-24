import pygame
import sys
import os
from time import sleep


def test_gamepad_on():
    # Pygameの初期化
    pygame.init()
    pygame.joystick.init()

    # ジョイパッドの接続確認
    try:
        joystick_count = pygame.joystick.get_count()
        print(f"検出されたジョイパッド数: {joystick_count}")

        if joystick_count == 0:
            print("ジョイパッドが接続されていません")
            return False

        # システム情報の表示
        print("\nシステム情報:")
        print("-" * 40)
        try:
            with open('/proc/cpuinfo', 'r') as f:
                if 'Raspberry' in f.read():
                    print("Raspberry Pi が検出されました")
        except:
            print("システム情報の取得に失敗しました")

        # 各ジョイパッドの初期化と情報表示
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            print(f"\nジョイパッド {i + 1} の情報:")
            print("-" * 40)
            print(f"名前: {joystick.get_name()}")
            print(f"軸の数: {joystick.get_numaxes()}")
            print(f"ボタンの数: {joystick.get_numbuttons()}")
            print(f"ハットの数: {joystick.get_numhats()}")

            print("\n入力テスト開始...")
            print("ESCキーで終了")

            try:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return True
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            return True

                    # ボタンの状態を取得
                    buttons = [joystick.get_button(b) for b in range(joystick.get_numbuttons())]
                    axes = [round(joystick.get_axis(a), 2) for a in range(joystick.get_numaxes())]
                    hats = [joystick.get_hat(h) for h in range(joystick.get_numhats())]

                    # アクティブな入力のみを表示
                    active_inputs = []

                    # ボタン入力の確認
                    active_buttons = [f"Button {b}" for b, pressed in enumerate(buttons) if pressed]
                    if active_buttons:
                        active_inputs.append(f"Buttons: {', '.join(active_buttons)}")

                    # アナログスティックの確認
                    active_axes = [f"Axis {a}:{v}" for a, v in enumerate(axes) if abs(v) > 0.1]
                    if active_axes:
                        active_inputs.append(f"Axes: {', '.join(active_axes)}")

                    # ハットスイッチの確認
                    active_hats = [f"Hat {h}:{v}" for h, v in enumerate(hats) if v != (0, 0)]
                    if active_hats:
                        active_inputs.append(f"Hats: {', '.join(active_hats)}")

                    # 状態を表示
                    #os.system('clear' if os.name != 'nt' else 'cls')
                    if active_inputs:
                        print("\n".join(active_inputs))
                    else:
                        print("入力待機中...")

                    sleep(0.1)  # CPU負荷軽減のため

            except pygame.error:
                print("ジョイパッドとの通信でエラーが発生しました")
                return False

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False

    finally:
        pygame.quit()


if __name__ == "__main__":
    test_gamepad_on()
    print("\nテストを終了しました")
