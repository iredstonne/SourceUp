import os
import shutil
from pathlib import Path
from PyInstaller.__main__ import run

def main():
    _root_path = Path(__file__).parent
    _app__module_path = _root_path / "sourceup"
    _app_module_entrypoint_path = _app__module_path / "app.py"
    _app_module_assets_path = _app__module_path / "assets"
    _build_path = _root_path / "build"
    _build_icon_path = _build_path / "favicon.ico"
    _dist_path = _root_path / "dist"
    _build_cache_path = _root_path / "build_cache"
    if _dist_path.exists():
        shutil.rmtree(_dist_path)
    if _build_cache_path.exists():
        shutil.rmtree(_build_cache_path)
    run([
        str(_app_module_entrypoint_path),
        '--onefile',
        '--noconsole',
        '-n', "SourceUp",
        '-s',
        f"--add-data={str(_app_module_assets_path)}{os.pathsep}assets",
        f"--icon={str(_build_icon_path)}",
        '--distpath', str(_dist_path),
        '--workpath', str(_build_cache_path),
        '--specpath', str(_build_cache_path)
    ])
    shutil.rmtree(_build_cache_path)

if __name__ == '__main__':
    main()
