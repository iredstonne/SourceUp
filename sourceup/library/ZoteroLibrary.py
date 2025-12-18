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

    @property
    def model_name(self):
        return f"{self.library_type.upper()}: {self.library_id} ({self.access_level})"
