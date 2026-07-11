"""ゲームパッドのボタンでデスクトップ操作を行う（本命サンプル）。

  A: スクリーンショットを撮影して screenshots/ に保存
  B: 左クリック
  X: 現在のマウス位置を表示
  Y: 画面録画のトグル（開始 / 停止）

ESC またはウィンドウを閉じると終了する。録画中に終了した場合も録画は停止される。

Phase 2 では、このボタン→アクションの割り当てを設定ファイルから行えるようにする予定。
"""

import _bootstrap  # noqa: F401
from datetime import datetime

import pygame

from joypad import GamepadReader, NoGamepadError
from joypad.actions import (
    ScreenRecorder,
    get_mouse_location,
    mouse_click,
    take_screenshot,
)


def toggle_recording(recorder: ScreenRecorder) -> None:
    if recorder.is_recording:
        recorder.stop_recording()
        print("録画を停止しました")
    else:
        output = datetime.now().strftime("recording_%y%m%d_%H%M%S.mp4")
        recorder.start_recording(output_file=output)
        print(f"録画を開始しました: {output}")


def main() -> None:
    try:
        pad = GamepadReader()
        pad.open()
    except NoGamepadError as e:
        print(e)
        return

    info = pad.info
    print("\nジョイパッド情報:")
    print(f"名前: {info['name']} / ボタン数: {info['buttons']} / 軸: {info['axes']}")
    print("-" * 50)
    print("A: スクショ  B: クリック  X: マウス位置  Y: 録画トグル  (ESC で終了)")

    recorder = ScreenRecorder()
    clock = pygame.time.Clock()
    try:
        while True:
            state = pad.poll()
            if state.should_quit:
                break

            if len(state.pressed) > 0 and state.pressed[0]:  # A
                print("A button")
                take_screenshot()
            if len(state.pressed) > 1 and state.pressed[1]:  # B
                print("B button")
                mouse_click(1)
            if len(state.pressed) > 2 and state.pressed[2]:  # X
                print("X button")
                print(f" mouse at: {get_mouse_location()}")
            if len(state.pressed) > 3 and state.pressed[3]:  # Y
                print("Y button")
                toggle_recording(recorder)

            clock.tick(30)
    finally:
        if recorder.is_recording:
            recorder.stop_recording()
        pad.close()
        print("\nプログラムを終了しました")


if __name__ == "__main__":
    main()
