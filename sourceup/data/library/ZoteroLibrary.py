from enum import Enum, auto
from dataclasses import dataclass

class LibraryType(int, Enum):
    USER = auto()
    GROUP = auto()

@dataclass
class ZoteroLibrary:
    library_type: LibraryType
    library_id: str
    private_key: str | None

    def __repr__(self):
        access_level = "Private" if self.private_key else "Public"
        return f"{self.library_type.name.capitalize()} · {self.library_id} ({access_level})"
