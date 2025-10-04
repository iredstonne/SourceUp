from typing import override, Set, Final
from PySide6.QtCore import Qt
from sourceup.data.library.ZoteroLibrary import ZoteroLibrary
from sourceup.model.provider.ItemDataProviderProtocol import ItemDataProviderProtocol, T

class ZoteroLibraryItemDataProvider(ItemDataProviderProtocol[ZoteroLibrary]):
    LIBRARY_USER_ROLE: Final[int] = ItemDataProviderProtocol.USER_ROLE + 1

    @override
    def roles(self) -> Set[int]:
        return {
            *super().roles(),
            ZoteroLibraryItemDataProvider.LIBRARY_USER_ROLE
        }

    @override
    def data(self, library: ZoteroLibrary, role: Qt.ItemDataRole) -> object | None:
        match role:
            case ZoteroLibraryItemDataProvider.LIBRARY_USER_ROLE:
                return library
            case (ItemDataProviderProtocol.DISPLAY_ROLE, ItemDataProviderProtocol.TOOLTIP_ROLE):
                return library.library_type.name + " " + library.id + ("Private" if library.private_key else "Public")

    @override
    def flags(self, value: T) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable # type: ignore
