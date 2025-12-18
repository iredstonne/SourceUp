from PySide6.QtCore import Qt
from typing import override, Set, Final, Union, Optional
from sourceup.collection.ZoteroCollection import ZoteroCollection
from sourceup.ui.model.data_provider.DataProviderProtocol import DataProviderProtocol

class ZoteroCollectionDataProvider(DataProviderProtocol[ZoteroCollection]):
    COLLECTION_USER_ROLE: Final[int] = DataProviderProtocol.USER_ROLE + 1

    @override
    def roles(self) -> Set[int]:
        return {
            *super().roles(),
            ZoteroCollectionDataProvider.COLLECTION_USER_ROLE
        }

    @override
    def data(self, _collection: ZoteroCollection, _role: Qt.ItemDataRole) -> Optional[ZoteroCollection | str]:
        match _role:
            case ZoteroCollectionDataProvider.COLLECTION_USER_ROLE:
                return _collection
            case DataProviderProtocol.DISPLAY_ROLE | DataProviderProtocol.TOOLTIP_ROLE:
                return _collection.model_name

    @override
    def flags(self, _collection: ZoteroCollection) -> Union[Qt.ItemFlag]:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable # type: ignore
