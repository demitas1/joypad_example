"""examples/ 内のスクリプトからリポジトリ直下の joypad パッケージを import できるようにする。

各サンプルの先頭で `import _bootstrap  # noqa` するだけでよい。
インストール（Phase 2 でパッケージ化予定）すればこのファイルは不要になる。
"""

import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
