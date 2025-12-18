from typing import Optional, Iterable
from sourceup.collection.ZoteroCollection import ZoteroCollection
from sourceup.ui.model.GenericListModel import GenericListModel
from sourceup.ui.model.data_provider.ZoteroCollectionDataProvider import ZoteroCollectionDataProvider
from sourceup.ui.model.data_storage.DataListStorageProtocol import DataListStorageProtocol

class ZoteroCollectionListModel(GenericListModel[ZoteroCollection]):
    def __init__(
        self,
        _initial_row_items: Optional[Iterable[ZoteroCollection]] = None,
        _data_list_storage_impl: Optional[DataListStorageProtocol[ZoteroCollection]] = None
    ):
        super().__init__(
            _initial_row_items,
            _data_list_storage_impl=_data_list_storage_impl,
            _data_provider_impl=ZoteroCollectionDataProvider()
        )
