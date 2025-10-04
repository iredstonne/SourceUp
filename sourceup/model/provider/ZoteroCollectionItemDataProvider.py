from typing import override, Set, Final
from PySide6.QtCore import Qt
from sourceup.data.collection.ZoteroCollection import ZoteroCollection
from sourceup.model.provider.ItemDataProviderProtocol import ItemDataProviderProtocol, T


class ZoteroCollectionItemDataProvider(ItemDataProviderProtocol[ZoteroCollection]):
    COLLECTION_ROLE: Final[int] = ItemDataProviderProtocol.USER_ROLE + 1

    @override
    def roles(self) -> Set[int]:
        return {
            *super().roles(),
            ZoteroCollectionItemDataProvider.COLLECTION_ROLE
        }

    @override
    def data(self, collection: ZoteroCollection, role: Qt.ItemDataRole) -> object | None:
        match role:
            case ZoteroCollectionItemDataProvider.COLLECTION_ROLE:
                return collection
            case (ItemDataProviderProtocol.DISPLAY_ROLE, ItemDataProviderProtocol.TOOLTIP_ROLE):
                return collection.name

    @override
    def flags(self, value: T) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable # type: ignore
