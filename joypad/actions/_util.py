"""アクション共通のユーティリティ。"""

import shutil
import subprocess
from typing import List


class MissingCommandError(RuntimeError):
    """必要な外部コマンドが見つからないときに送出する。"""


def ensure_command(name: str) -> None:
    """外部コマンドが PATH 上に存在することを確認する。

    見つからない場合はインストール方法を添えて MissingCommandError を送出する。
    """
    if shutil.which(name) is None:
        raise MissingCommandError(
            f"外部コマンド '{name}' が見つかりません。"
            f"インストールしてください（例: sudo apt install {name}）。"
        )


def run(command: List[str], **kwargs) -> subprocess.CompletedProcess:
    """外部コマンドを実行する。先頭コマンドの存在を確認してから実行する。"""
    ensure_command(command[0])
    return subprocess.run(command, **kwargs)
