import os
from pathlib import Path

def _NT_KERNEL_try_set_hidden_flag(path: Path, value: bool):
    if os.name != "nt":
        return
    try:
        import ctypes
        from ctypes import wintypes
        kernel32 = ctypes.windll.kernel32
        # Windows NT kernel terminology
        # LPCWSTR = Long Pointer Constant Wide (UTF-16) String (= Unicode string)
        # DWORD = Double 16-bit value (= 32 bit unsigned int)
        get_file_attributes = kernel32.GetFileAttributesW  # type: ignore[attr-defined]
        get_file_attributes.argtypes = (wintypes.LPCWSTR,)
        get_file_attributes.restype = wintypes.DWORD
        set_file_attributes = kernel32.SetFileAttributesW  # type: ignore[attr-defined]
        set_file_attributes.argtypes = (wintypes.LPCWSTR, wintypes.DWORD)
        set_file_attributes.restype = wintypes.BOOL
        FILE_ATTRIBUTE_HIDDEN = 0x02
        INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF
        file_attributes = get_file_attributes(str(path))
        if file_attributes == INVALID_FILE_ATTRIBUTES:
            return
        new_file_attributes = (file_attributes | FILE_ATTRIBUTE_HIDDEN) if value else (
                    file_attributes & ~FILE_ATTRIBUTE_HIDDEN)
        set_file_attributes(str(path), new_file_attributes)
    except (OSError, ImportError, AttributeError, TypeError):
        pass
