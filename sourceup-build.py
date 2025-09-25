import shutil
from PyInstaller.__main__ import run

def main():
    build_cache_path = "build_cache"
    run([
        'sourceup/app.py',
        '--onefile',
        '--noconsole',
        '-n', 'SourceUp',
        '-s',
        '--distpath', 'dist',
        '--workpath', build_cache_path,
        '--specpath', build_cache_path
    ])
    shutil.rmtree(build_cache_path)

if __name__ == '__main__':
    main()
