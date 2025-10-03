from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Any
if TYPE_CHECKING: from sourceup.data.item.ZoteroBaseItemData import ZoteroBaseItemData

class ZoteroBaseCreatorData(ABC):
    @classmethod
    @abstractmethod
    def supports_data(cls, data: Dict[str, Any]) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def map_from_data(cls, data: Dict[str, Any]) -> "ZoteroBaseItemData":
        raise NotImplementedError
