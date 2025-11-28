from typing import Optional, Iterable
from sourceup.item.ZoteroItem import ZoteroItem
from sourceup.ui.model.GenericListModel import GenericListModel
from sourceup.ui.model.storage.StorageProtocol import StorageProtocol
from sourceup.ui.model.data_provider.ZoteroItemDataProvider import ZoteroItemDataProvider

class ZoteroItemListModel(GenericListModel[ZoteroItem]):
    def __init__(
        self,
        _initial_row_items: Optional[Iterable[ZoteroItem]] = None,
        _storage_impl: Optional[StorageProtocol[ZoteroItem]] = None
    ):
        super().__init__(
            _initial_row_items,
            _storage_impl=_storage_impl,
            _data_provider_impl=ZoteroItemDataProvider()
        )
