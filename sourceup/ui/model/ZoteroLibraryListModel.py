from typing import Optional, Iterable
from sourceup.library.ZoteroLibrary import ZoteroLibrary
from sourceup.ui.model.GenericListModel import GenericListModel
from sourceup.ui.model.data_provider.ZoteroLibraryDataProvider import ZoteroLibraryDataProvider
from sourceup.ui.model.data_storage.DataListStorageProtocol import DataListStorageProtocol

class ZoteroLibraryListModel(GenericListModel[ZoteroLibrary]):
    def __init__(
        self,
        _initial_row_items: Optional[Iterable[ZoteroLibrary]] = None,
        _data_list_storage_impl: Optional[DataListStorageProtocol[ZoteroLibrary]] = None
    ):
        super().__init__(
            _initial_row_items,
            _data_list_storage_impl=_data_list_storage_impl,
            _data_provider_impl=ZoteroLibraryDataProvider()
        )
