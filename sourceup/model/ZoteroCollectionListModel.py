from typing import Optional, Iterable
from sourceup.data.collection.ZoteroCollection import ZoteroCollection
from sourceup.model.GenericListModel import GenericListModel
from sourceup.model.provider.ZoteroCollectionItemDataProvider import ZoteroCollectionItemDataProvider
from sourceup.model.storage.StorageProtocol import StorageProtocol

class ZoteroCollectionListModel(GenericListModel[ZoteroCollection]):
    def __init__(
        self,
        initial_row_items: Optional[Iterable[ZoteroCollection]] = None,
        storage: Optional[StorageProtocol[ZoteroCollection]] = None
    ):
        super().__init__(
            initial_row_items,
            storage,
            item_data_provider=ZoteroCollectionItemDataProvider()
        )
