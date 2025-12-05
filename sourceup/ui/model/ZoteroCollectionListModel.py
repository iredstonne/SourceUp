from typing import Optional, Iterable
from sourceup.collection.ZoteroCollection import ZoteroCollection
from sourceup.ui.model.GenericListModel import GenericListModel
from sourceup.ui.model.data_provider.ZoteroCollectionDataProvider import ZoteroCollectionDataProvider
from sourceup.ui.model.storage.StorageProtocol import StorageProtocol

class ZoteroCollectionListModel(GenericListModel[ZoteroCollection]):
    def __init__(
        self,
        _initial_row_items: Optional[Iterable[ZoteroCollection]] = None,
        _storage_impl: Optional[StorageProtocol[ZoteroCollection]] = None
    ):
        super().__init__(
            _initial_row_items,
            _storage_impl=_storage_impl,
            _data_provider_impl=ZoteroCollectionDataProvider()
        )
