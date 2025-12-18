from typing import Optional, Iterable
from sourceup.item.ZoteroItem import ZoteroItem
from sourceup.ui.model.GenericListModel import GenericListModel
from sourceup.ui.model.data_storage.DataListStorageProtocol import DataListStorageProtocol
from sourceup.ui.model.data_provider.ZoteroItemDataProvider import ZoteroItemDataProvider

class ZoteroItemListModel(GenericListModel[ZoteroItem]):
    def __init__(
        self,
        _initial_row_items: Optional[Iterable[ZoteroItem]] = None,
        _data_list_storage_impl: Optional[DataListStorageProtocol[ZoteroItem]] = None
    ):
        super().__init__(
            _initial_row_items,
            _data_list_storage_impl=_data_list_storage_impl,
            _data_provider_impl=ZoteroItemDataProvider()
        )
