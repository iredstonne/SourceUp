from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from typing import Protocol, TypeVar, overload, Literal, Optional, Any, Final, Union, Set

T = TypeVar("T")

class DataProviderProtocol(Protocol[T]):
    USER_ROLE: Final[int] = int(Qt.ItemDataRole.UserRole)
    DISPLAY_ROLE: Final[int] = int(Qt.ItemDataRole.DisplayRole)
    TOOLTIP_ROLE: Final[int] = int(Qt.ItemDataRole.ToolTipRole)
    DECORATION_ROLE: Final[int] = int(Qt.ItemDataRole.DecorationRole)

    def roles(self) -> Set[int]:
        return {
            DataProviderProtocol.USER_ROLE,
            DataProviderProtocol.DISPLAY_ROLE,
            DataProviderProtocol.TOOLTIP_ROLE,
            DataProviderProtocol.DECORATION_ROLE
        }

    @overload
    def data(self, _value: T, _role: Literal[Qt.ItemDataRole.UserRole]) -> Optional[T]: ...
    @overload
    def data(self, _value: T, _role: Literal[Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole]) -> Optional[str]: ...
    @overload
    def data(self, _value: T, _role: Literal[Qt.ItemDataRole.DecorationRole]) -> Optional[QIcon]: ...
    @overload
    def data(self, _value: T, _role: Qt.ItemDataRole) -> Optional[Any]: ...
    def data(self, _value: T, _role: Qt.ItemDataRole) -> Optional[Any]: ...

    def flags(self, _value: T) -> Union[Qt.ItemFlag]: ...
