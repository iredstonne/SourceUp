from typing import TYPE_CHECKING, Type, Tuple
if TYPE_CHECKING: from sourceup.creator.ZoteroBaseCreatorData import ZoteroBaseCreatorData
from sourceup.creator.data.ZoteroPersonCreatorData import ZoteroPersonCreatorData
from sourceup.creator.data.ZoteroCorporateCreatorData import ZoteroCorporateCreatorData

class ZoteroCreatorDataRegistry:
    ENTRIES: Tuple[Type["ZoteroBaseCreatorData"], ...] = (
        ZoteroPersonCreatorData,
        ZoteroCorporateCreatorData,
    )
