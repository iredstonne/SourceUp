from typing import List
from pydantic import BaseModel, Field
from sourceup.settings.data.ZoteroLibraryData import ZoteroLibraryData

class SettingsData(BaseModel):
    version: int = 1
    libraries: List[ZoteroLibraryData] = Field(default_factory=list)
