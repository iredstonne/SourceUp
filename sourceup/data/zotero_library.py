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
        library_type = self.library_type.name.capitalize()
        library_id = self.library_id
        access_level = "Private" if self.private_key else "Public"
        return f"{library_type} · {library_id} ({access_level})"
