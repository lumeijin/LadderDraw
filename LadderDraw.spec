# -*- mode: python ; coding: utf-8 -*-
"""LadderDraw PyInstaller 打包配置（onedir -> 文件夹分发）。

用法:
    pip install pyinstaller
    pyinstaller LadderDraw.spec

产物:
    dist/LadderDraw/              <- 整个文件夹即程序；分发时压成 zip
      ├── LadderDraw.exe          <- 双击运行的入口
      └── _internal/              <- 依赖（Qt / matplotlib / sympy / 资源等）

为什么选 onedir 而不是 onefile（单 exe）:
    * 启动更快 —— onefile 每次启动都要先把自身解压到临时目录，onedir 直接运行。
    * 杀软误报更少 —— 单文件 exe 更常被 Windows Defender / 各类杀软误判。
    * 分发方式：把 dist/LadderDraw/ 整个文件夹压缩成 zip 发给同学，解压后
      双击其中的 LadderDraw.exe 即可。

切换回 onefile（单 exe）: 删掉下方 COLLECT(...)，并把 a.binaries / a.datas
放回 EXE(...) 内、同时设 exclude_binaries=False。
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
    datas=[(str(RESOURCES), 'resources')],   # 运行时定位 resources/（见 app._resource_dir）
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
    [],
    exclude_binaries=True,                    # onedir：依赖不塞进 exe，交给 COLLECT
    name='LadderDraw',
    debug=False,
    strip=False,
    upx=True,
    console=False,                            # GUI 程序：不弹控制台
    icon=str(ICON) if ICON.exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LadderDraw',                        # 产物目录: dist/LadderDraw/
)
