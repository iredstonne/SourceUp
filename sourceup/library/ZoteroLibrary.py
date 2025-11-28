from dataclasses import dataclass
from typing import Optional
from sourceup.library.ZoteroLibraryType import ZoteroLibraryType

@dataclass(frozen=True, slots=True)
class ZoteroLibrary:
    library_type: ZoteroLibraryType
    library_id: str
    private_key: Optional[str]

    @property
    def access_level(self):
        return "Private" if self.private_key else "Public"

    def __repr__(self):
        return f"{self.library_type.upper()}: {self.library_id} ({self.access_level})"

    def __str__(self):
        return self.__repr__()
