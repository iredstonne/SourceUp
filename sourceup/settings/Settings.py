import atexit
import os
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from sourceup.platform import _NT_KERNEL_try_set_hidden_flag
from sourceup.settings.data.SettingsData import SettingsData

class Settings:
    def __init__(self, _path: Path):
        self._tmp_path = _path.with_suffix(_path.suffix + ".tmp")
        self._tmp_path.parent.mkdir(parents=True, exist_ok=True)
        self._path = _path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        atexit.register(self._dispose)

    @staticmethod
    def try_load(_path: Path) -> Optional[SettingsData]:
        try:
            if not _path.is_file():
                return None
            return SettingsData.model_validate_json(_path.read_bytes())
        except (OSError, IOError, ValueError, ValidationError):
            return None

    def load(self) -> SettingsData:
        _tmp_data = self.try_load(self._tmp_path)
        if _tmp_data is not None:
            self._commit()
            return _tmp_data
        _data = self.try_load(self._path)
        return _data or SettingsData()

    def save(self, _settings_data: SettingsData):
        try:
            self._tmp_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._tmp_path, "wb") as _file:
                _file.write(_settings_data.model_dump_json(indent=2).encode("utf-8"))
                _file.flush()
                os.fsync(_file.fileno())
            _NT_KERNEL_try_set_hidden_flag(self._tmp_path, True)
        except (OSError, IOError):
            pass

    def _commit(self) -> bool:
        try:
            if self._tmp_path.is_file():
                self._tmp_path.parent.mkdir(parents=True, exist_ok=True)
                self._path.parent.mkdir(parents=True, exist_ok=True)
                os.replace(self._tmp_path, self._path)
                _NT_KERNEL_try_set_hidden_flag(self._path, False)
            return True
        except (OSError, IOError):
            return False

    def _dispose(self):
        try:
            if self._tmp_path.is_file() and self._commit():
                self._tmp_path.unlink()
        except (OSError, IOError):
            pass
