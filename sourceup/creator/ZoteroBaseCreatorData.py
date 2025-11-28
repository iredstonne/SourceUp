from typing import Dict, Any

class ZoteroBaseCreatorData:
    def display_name(self) -> str:
        raise NotImplementedError

    @classmethod
    def supports_data(cls, _data: Dict[str, Any]) -> bool:
        raise NotImplementedError

    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroBaseCreatorData":
        raise NotImplementedError
