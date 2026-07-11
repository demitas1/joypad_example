"""スクリーンショット撮影（ffmpeg x11grab ラッパー）。"""

import os
import subprocess
from datetime import datetime
from typing import Optional

from .. import settings
from ._util import MissingCommandError, ensure_command, run


def get_screen_resolution() -> str:
    """xrandr を使用して現在の画面解像度を取得する。

    取得できない場合は settings.FALLBACK_RESOLUTION を返す。
    """
    try:
        output = run(
            ["xrandr", "--current"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        for line in output.split("\n"):
            if "*" in line:  # アクティブな解像度を示す
                return line.split()[0]
    except (MissingCommandError, subprocess.CalledProcessError, IndexError) as e:
        print(f"warning: 解像度の取得に失敗しました（{e}）")
    return settings.FALLBACK_RESOLUTION


def take_screenshot(
    save_dir: str = settings.SCREENSHOT_DIR,
    display: str = settings.DISPLAY,
) -> Optional[str]:
    """画面全体をキャプチャして save_dir に保存し、保存先パスを返す。

    失敗した場合は None を返す。
    """
    os.makedirs(save_dir, exist_ok=True)

    filename = datetime.now().strftime("screenshot_%y%m%d_%H%M%S.jpg")
    filepath = os.path.join(save_dir, filename)

    try:
        ensure_command("ffmpeg")
        command = [
            "ffmpeg",
            "-f", "x11grab",
            "-video_size", get_screen_resolution(),
            "-i", display,
            "-frames:v", "1",
            "-q:v", "2",       # 品質（1-31, 低いほど高品質）
            "-y",
            filepath,
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Screenshot saved: {filepath}")
            return filepath
        print(f"Error taking screenshot: {result.stderr}")
        return None
    except MissingCommandError as e:
        print(e)
        return None
