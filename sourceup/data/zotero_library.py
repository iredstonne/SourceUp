from enum import Enum, auto
from dataclasses import dataclass

class LibraryType(int, Enum):
    USER = auto()
    GROUP = auto()

@dataclass
class ZoteroLibrary:
    library_type: LibraryType
    library_id: str
    private_key: str
