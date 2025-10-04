from typing import Protocol, TypeVar, overload, Literal, Optional, Any, Final, Union, Set
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

T = TypeVar("T")

class ItemDataProviderProtocol(Protocol[T]):
    USER_ROLE: Final[int] = int(Qt.ItemDataRole.UserRole)
    DISPLAY_ROLE: Final[int] = int(Qt.ItemDataRole.DisplayRole)
    TOOLTIP_ROLE: Final[int] = int(Qt.ItemDataRole.ToolTipRole)
    DECORATION_ROLE: Final[int] = int(Qt.ItemDataRole.DecorationRole)

    def roles(self) -> Set[int]:
        return {
            ItemDataProviderProtocol.USER_ROLE,
            ItemDataProviderProtocol.DISPLAY_ROLE,
            ItemDataProviderProtocol.TOOLTIP_ROLE,
            ItemDataProviderProtocol.DECORATION_ROLE
        }

    @overload
    def data(self, value: T, ro: Literal[Qt.ItemDataRole.UserRole]) -> Optional[T]: ...
    @overload
    def data(self, value: T, role: Literal[Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole]) -> Optional[str]: ...
    @overload
    def data(self, value: T, role: Literal[Qt.ItemDataRole.DecorationRole]) -> Optional[QIcon]: ...
    @overload
    def data(self, value: T, role: Qt.ItemDataRole) -> Optional[Any]: ...
    def data(self, value: T, role: Qt.ItemDataRole) -> Optional[Any]: ...

    def flags(self, value: T) -> Union[Qt.ItemFlag]: ...
