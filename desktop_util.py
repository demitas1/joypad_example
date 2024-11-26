import subprocess
from typing import Dict


def get_mouse_location() -> Dict[str, int]:
    """
    xdotoolを使用してマウスの位置情報を取得し、辞書として返す

    Returns:
        Dict[str, int]: {
            'x': x座標,
            'y': y座標,
            'screen': スクリーン番号,
            'window': ウィンドウID
        }
    """
    try:
        # xdotoolコマンドを実行
        result = subprocess.run(['xdotool', 'getmouselocation'], 
                              capture_output=True, 
                              text=True, 
                              check=True)

        # 出力を解析
        # 例: "x:652 y:1197 screen:0 window:75497479"
        location_dict = {}

        # スペースで分割して各要素を処理
        for item in result.stdout.strip().split():
            key, value = item.split(':')
            # 数値に変換して格納
            location_dict[key] = int(value)

        return location_dict

    except subprocess.CalledProcessError as e:
        print(f"Error executing xdotool: {e}")
        return None
    except Exception as e:
        print(f"Error parsing output: {e}")
        return None


def mouse_click(button_num):
    command = ['xdotool', 'click', str(button_num)]
    result = subprocess.run(command)


# 使用例
if __name__ == "__main__":
    location = get_mouse_location()
    if location:
        print("Mouse location:")
        for key, value in location.items():
            print(f"{key}: {value}")
