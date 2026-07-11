"""画面録画（ffmpeg x11grab ラッパー）。"""

import signal
import subprocess
from typing import Optional

from .. import settings
from ._util import ensure_command


class ScreenRecorder:
    """ffmpeg の画面録画をラップするコンテキストマネージャ。

    例外が発生しても __exit__ で確実に録画を停止する。
    """

    def __init__(self):
        self.process: Optional[subprocess.Popen] = None

    def __enter__(self) -> "ScreenRecorder":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.process is not None:
            self.stop_recording()

    @property
    def is_recording(self) -> bool:
        return self.process is not None

    def start_recording(
        self,
        output_file: str = "output.mp4",
        source_size: str = settings.RECORD_SOURCE_SIZE,
        video_size: str = settings.RECORD_VIDEO_SIZE,
        framerate: int = settings.RECORD_FRAMERATE,
        offset_x: int = settings.RECORD_OFFSET_X,
        offset_y: int = settings.RECORD_OFFSET_Y,
        display: str = settings.DISPLAY,
    ) -> None:
        """画面録画を開始する。"""
        if self.process is not None:
            raise RuntimeError("Recording is already in progress")

        ensure_command("ffmpeg")
        command = [
            "ffmpeg",
            "-s", source_size,
            "-video_size", video_size,
            "-framerate", str(framerate),
            "-f", "x11grab",
            "-i", f"{display}+{offset_x},{offset_y}",
            "-y",
            output_file,
        ]
        self.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def stop_recording(self) -> None:
        """録画を停止する。ffmpeg に SIGINT を送り出力を正しく終了させる。"""
        if self.process is None:
            raise RuntimeError("No recording in progress")
        self.process.send_signal(signal.SIGINT)
        self.process.wait()
        self.process = None
