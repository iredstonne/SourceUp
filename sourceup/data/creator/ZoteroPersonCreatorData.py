from dataclasses import dataclass
from typing import Dict, Any
from sourceup.casts import map_to_str
from sourceup.data.creator.ZoteroBaseCreatorData import ZoteroBaseCreatorData

@dataclass(frozen=True, slots=True)
class ZoteroPersonCreatorData(ZoteroBaseCreatorData):
    first_name: str
    last_name: str

    @classmethod
    def supports_data(cls, data: Dict[str, Any]) -> bool:
        has_first_name =  "firstName" in data
        has_last_name = "lastName" in data
        return has_first_name and has_last_name

    @classmethod
    def map_from_data(cls, data: Dict[str, Any]) -> "ZoteroPersonCreatorData":
        _first_name = map_to_str(data.get("firstName"))
        _last_name = map_to_str(data.get("lastName"))
        return cls(_first_name, _last_name)
