from typing import Optional, Iterable
from sourceup.library.ZoteroLibrary import ZoteroLibrary
from sourceup.ui.model.GenericListModel import GenericListModel
from sourceup.ui.model.data_provider.ZoteroLibraryDataProvider import ZoteroLibraryDataProvider
from sourceup.ui.model.storage.StorageProtocol import StorageProtocol

class ZoteroLibraryListModel(GenericListModel[ZoteroLibrary]):
    def __init__(
        self,
        _initial_row_items: Optional[Iterable[ZoteroLibrary]] = None,
        _storage_impl: Optional[StorageProtocol[ZoteroLibrary]] = None
    ):
        super().__init__(
            _initial_row_items,
            _storage_impl=_storage_impl,
            _data_provider_impl=ZoteroLibraryDataProvider()
        )
