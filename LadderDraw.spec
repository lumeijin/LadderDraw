# -*- mode: python ; coding: utf-8 -*-
"""LadderDraw PyInstaller 打包配置（onefile -> 单个可执行文件，便于分发）。

用法:
    pip install pyinstaller
    pyinstaller LadderDraw.spec

产物:
    dist/LadderDraw.exe        (Windows)
    dist/LadderDraw            (macOS / Linux)

说明:
    * onefile 模式：所有依赖 + resources/ 打进一个文件，启动稍慢但分发最简单。
    * 资源通过 app._resource_dir() 中的 sys._MEIPASS 定位，故 datas 里
      必须把 resources/ 放到运行时顶层 'resources' 路径下。
    * 想要启动更快的 onedir 模式：把 EXE(...) 内的 a.binaries 与 a.datas
      移到 COLLECT(...) 中（参见 PyInstaller 文档）。
    * Windows 下 exe 图标需要 .ico；仓库目前只有 png/svg，缺省时自动忽略。
      如需自定义图标，把 huagong.ico 放到 resources/icons/ 下即可生效。
"""
from pathlib import Path

ROOT = Path(SPECPATH).resolve()
RESOURCES = ROOT / 'resources'
ICON = RESOURCES / 'icons' / 'huagong.ico'   # Windows 需要 .ico；缺省则忽略

block_cipher = None

a = Analysis(
    ['ladderdraw/__main__.py'],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[(str(RESOURCES), 'resources')],   # 整个 resources/ -> 运行时 resources/
    hiddenimports=[
        'matplotlib.backends.backend_qt5agg',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LadderDraw',
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,                            # GUI 程序：不弹控制台
    icon=str(ICON) if ICON.exists() else None,
)
