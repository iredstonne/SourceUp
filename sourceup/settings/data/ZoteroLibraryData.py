from typing import Optional
from pydantic import BaseModel

class ZoteroLibraryData(BaseModel):
    library_type: str
    library_id: str
    private_key: Optional[str] = None
