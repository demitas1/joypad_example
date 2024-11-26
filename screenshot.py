import subprocess
from datetime import datetime
import os
import sys


def get_screen_resolution():
    """xrandryを使用して画面解像度を取得"""
    try:
        # xrandrコマンドを実行して現在の解像度を取得
        command = ['xrandr', '--current']
        output = subprocess.check_output(command).decode()

        # 主要なディスプレイの解像度を検索
        for line in output.split('\n'):
            if '*' in line:  # アクティブな解像度を示す
                # 解像度を抽出 (例: 1920x1080)
                resolution = line.split()[0]
                return resolution

    except subprocess.CalledProcessError:
        # エラーの場合はデフォルト値を返す
        return "1920x1080"


def take_screenshot(save_dir='screenshots'):
    # 保存ディレクトリが存在しない場合は作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 現在時刻を取得してファイル名を生成
    current_time = datetime.now()
    filename = current_time.strftime('screenshot_%y%m%d_%H%M%S.jpg')
    filepath = os.path.join(save_dir, filename)

    try:
        # ffmpegコマンドを構築
        # X11環境で画面全体をキャプチャ
        command = [
            'ffmpeg',
            '-f', 'x11grab',  # X11キャプチャを使用
            '-video_size', get_screen_resolution(),  # 画面解像度を取得
            '-i', ':0.0',  # デフォルトディスプレイを指定
            '-frames:v', '1',  # 1フレームのみキャプチャ
            '-q:v', '2',  # 品質設定（1-31, 低いほど高品質）
            '-y',  # 確認なしで上書き
            filepath
        ]

        # ffmpegを実行（出力を非表示にする）
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Screenshot saved: {filepath}")
        else:
            print(f"Error taking screenshot: {result.stderr}")

    except subprocess.CalledProcessError as e:
        print(f"Error executing ffmpeg: {e}")
