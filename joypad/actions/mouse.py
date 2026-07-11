"""マウス操作（xdotool ラッパー）。"""

import subprocess
from typing import Dict, Optional

from ._util import MissingCommandError, ensure_command, run


def get_mouse_location() -> Optional[Dict[str, int]]:
    """xdotool を使用してマウスの位置情報を取得し、辞書として返す。

    Returns:
        {'x': x座標, 'y': y座標, 'screen': スクリーン番号, 'window': ウィンドウID}
        取得に失敗した場合は None。
    """
    try:
        # 例: "x:652 y:1197 screen:0 window:75497479"
        result = run(
            ["xdotool", "getmouselocation"],
            capture_output=True,
            text=True,
            check=True,
        )
        location = {}
        for item in result.stdout.strip().split():
            key, value = item.split(":")
            location[key] = int(value)
        return location
    except MissingCommandError as e:
        print(e)
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error executing xdotool: {e}")
        return None
    except Exception as e:
        print(f"Error parsing output: {e}")
        return None


def mouse_click(button_num: int = 1) -> None:
    """指定ボタンでクリックする（1:左, 2:中, 3:右）。"""
    try:
        ensure_command("xdotool")
        subprocess.run(["xdotool", "click", str(button_num)])
    except MissingCommandError as e:
        print(e)
