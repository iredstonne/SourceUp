from PySide6.QtCore import Qt
from typing import override, Set, Final, Union, Optional
from sourceup.library.ZoteroLibrary import ZoteroLibrary
from sourceup.ui.model.data_provider.DataProviderProtocol import DataProviderProtocol

class ZoteroLibraryDataProvider(DataProviderProtocol[ZoteroLibrary]):
    LIBRARY_USER_ROLE: Final[int] = DataProviderProtocol.USER_ROLE + 1

    @override
    def roles(self) -> Set[int]:
        return {
            *super().roles(),
            ZoteroLibraryDataProvider.LIBRARY_USER_ROLE
        }

    @override
    def data(self, _library: ZoteroLibrary, _role: Qt.ItemDataRole) -> Optional[ZoteroLibrary | str]:
        match _role:
            case ZoteroLibraryDataProvider.LIBRARY_USER_ROLE:
                return _library
            case DataProviderProtocol.DISPLAY_ROLE | DataProviderProtocol.TOOLTIP_ROLE:
                return _library.model_name

    @override
    def flags(self, _library: ZoteroLibrary) -> Union[Qt.ItemFlag]:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable # type: ignore
