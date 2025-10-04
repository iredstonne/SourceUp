from typing import Optional, Iterable
from sourceup.data.library.ZoteroLibrary import ZoteroLibrary
from sourceup.model.GenericListModel import GenericListModel
from sourceup.model.provider.ZoteroLibraryItemDataProvider import ZoteroLibraryItemDataProvider
from sourceup.model.storage.StorageProtocol import StorageProtocol

class ZoteroLibraryListModel(GenericListModel[ZoteroLibrary]):
    def __init__(
        self,
        initial_row_items: Optional[Iterable[ZoteroLibrary]] = None,
        storage: Optional[StorageProtocol[ZoteroLibrary]] = None
    ):
        super().__init__(
            initial_row_items,
            storage,
            item_data_provider=ZoteroLibraryItemDataProvider()
        )
