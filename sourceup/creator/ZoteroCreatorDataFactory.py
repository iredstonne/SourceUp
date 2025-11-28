from typing import TYPE_CHECKING, Dict, Any
if TYPE_CHECKING: from sourceup.creator.ZoteroBaseCreatorData import ZoteroBaseCreatorData
from sourceup.creator.ZoteroCreatorDataRegistry import ZoteroCreatorDataRegistry

class ZoteroCreatorDataFactory:
    @classmethod
    def from_data(cls, _data: Dict[str, Any]) -> "ZoteroBaseCreatorData":
        for _creator_data_cls in ZoteroCreatorDataRegistry.ENTRIES:
            if _creator_data_cls.supports_data(_data):
                return _creator_data_cls.map_from_data(_data)
        raise ValueError(f"Unhandled creator data: {_data!r}")
