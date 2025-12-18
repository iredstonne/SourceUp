import os
from pathlib import Path
from sourceup.settings.data.SettingsData import SettingsData

class Settings:
    def __init__(self, path: Path):
        self.path = path
        self.tmp_path = path.with_suffix(path.suffix + ".tmp")

    def load(self) -> SettingsData:
        if not self.path.is_file():
            return SettingsData()
        return SettingsData.model_validate_json(self.path.read_bytes())

    def save(self, settings_data: SettingsData):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = settings_data.model_dump_json(indent=2).encode("utf-8")
        with open(self.tmp_path, "wb") as file:
            file.write(data)
            file.flush()
            os.fsync(file.fileno())
        self._try_hide_tmp_file_on_nt()
        os.replace(self.tmp_path, self.path)


    def dispose(self):
        try:
            if self.tmp_path.exists():
                self.tmp_path.unlink()
        except OSError:
            pass

    def _try_hide_tmp_file_on_nt(self):
        if os.name != "nt":
            return
        try:
            import ctypes
            from ctypes import wintypes
            set_file_attributes = ctypes.windll.kernel32.SetFileAttributesW # type: ignore[attr-defined]
            # Windows NT kernel terminology
            # LPCWSTR = Long Pointer Constant Wide (UTF-16) String (= Unicode string)
            # DWORD = Double 16-bit value (= 32 bit unsigned int)
            set_file_attributes.argtypes = (wintypes.LPCWSTR, wintypes.DWORD)
            set_file_attributes.restype = wintypes.BOOL
            FILE_ATTRIBUTE_HIDDEN = 0x02
            set_file_attributes(str(self.tmp_path), FILE_ATTRIBUTE_HIDDEN)
        except (OSError, ImportError, AttributeError, TypeError):
            pass
