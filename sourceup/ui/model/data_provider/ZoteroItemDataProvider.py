from PySide6.QtCore import Qt
from typing import override, Set, Final, Union, Optional
from sourceup.item.ZoteroItem import ZoteroItem
from sourceup.ui.model.data_provider.DataProviderProtocol import DataProviderProtocol

class ZoteroItemDataProvider(DataProviderProtocol[ZoteroItem]):
    ITEM_USER_ROLE: Final[int] = DataProviderProtocol.USER_ROLE + 1

    @override
    def roles(self) -> Set[int]:
        return {
            *super().roles(),
            ZoteroItemDataProvider.ITEM_USER_ROLE
        }

    @override
    def data(self, _item: ZoteroItem, _role: Qt.ItemDataRole) -> Optional[ZoteroItem | str]:
        match _role:
            case ZoteroItemDataProvider.ITEM_USER_ROLE:
                return _item
            case DataProviderProtocol.DISPLAY_ROLE | DataProviderProtocol.TOOLTIP_ROLE:
                return _item.model_name

    @override
    def flags(self, _item: ZoteroItem) -> Union[Qt.ItemFlag]:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable # type: ignore
