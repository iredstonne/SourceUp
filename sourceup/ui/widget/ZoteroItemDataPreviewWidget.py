from dataclasses import fields
from typing import Any, Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFormLayout
from sourceup.item.ZoteroItem import ZoteroItem
from sourceup.casts import normalize_str_case_insensitive

class ZoteroItemDataPreviewWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._build_root()

    def _build_root(self):
        _root_layout = QVBoxLayout(self)
        _root_layout.addWidget(self._build_type_label())
        _root_layout.addWidget(self._build_scrollable_form_area())

    def _build_type_label(self) -> QWidget:
        self._type_label = QLabel()
        self._type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return self._type_label

    def _build_scrollable_form_area(self) -> QWidget:
        _scrollable_form_area = QScrollArea()
        _scrollable_form_area.setContentsMargins(1, 1, 1, 1)
        _scrollable_form_area.setWidgetResizable(True)
        _form_host = QWidget()
        self._form_layout = QFormLayout(_form_host)
        _scrollable_form_area.setWidget(_form_host)
        return _scrollable_form_area

    @staticmethod
    def _format_type(_type: str) -> str:
        if not _type:
            return _type
        _type_parts = []
        _type_offset_index = 0
        _type_len = len(_type)
        for _type_index in range(1, _type_len):
            _type_prev_char = _type[_type_index - 1]
            _type_current_char = _type[_type_index]
            if _type_prev_char.islower() and _type_current_char.isupper():
                _type_parts.append(normalize_str_case_insensitive(_type[_type_offset_index:_type_index]))
                _type_offset_index = _type_index
        _type_parts.append(normalize_str_case_insensitive(_type[_type_offset_index:_type_len]))
        _type_parts = [
            _type_part.capitalize()
            for _type_part in _type_parts
            if _type_part
        ]
        return " ".join(_type_parts)

    @staticmethod
    def _format_field_name(_field_name: str) -> str:
        if not _field_name:
            return _field_name
        _field_parts = _field_name.split("_")
        _field_parts = [
            _field_part.capitalize()
            for _field_part in _field_parts
            if _field_part
        ]
        return " ".join(_field_parts)

    @staticmethod
    def _format_field_value(_field_value: Any) -> str:
        if not _field_value:
            return "-"
        if isinstance(_field_value, (list, tuple)):
            return ", ".join(
                str(_field_loop_value)
                for _field_loop_value in _field_value
            )
        return str(_field_value)

    @staticmethod
    def _is_href_value(_field_value: str) -> bool:
        return normalize_str_case_insensitive(_field_value).startswith(tuple(
            _protocol + ":"
            for _protocol in ["http", "https", "ftp", "sftp", "mailto"]
        ))

    def _clear_form_layout(self):
        _form_layout = self._form_layout
        for _form_layout_row in reversed(range(_form_layout.rowCount())):
            _form_layout.removeRow(_form_layout_row)
        self._type_label.clear()

    def _populate_form_layout(self, _current_item: ZoteroItem):
        _current_item_data = _current_item.item_data
        for _current_item_data_field in fields(_current_item_data):
            _current_item_data_field_name = _current_item_data_field.name
            _current_item_data_field_value = getattr(_current_item_data, _current_item_data_field_name)
            _current_item_data_field_name = self._format_field_name(_current_item_data_field_name)
            _current_item_data_field_name_label = QLabel(_current_item_data_field_name + ":")
            _current_item_data_field_value = self._format_field_value(_current_item_data_field_value)
            _current_item_data_field_value_label = QLabel(_current_item_data_field_value)
            _current_item_data_field_value_label_font_metrics = QFontMetrics(_current_item_data_field_value_label.font())
            _current_item_data_field_elided_value = _current_item_data_field_value_label_font_metrics.elidedText(_current_item_data_field_value, Qt.TextElideMode.ElideRight, 300)
            if _current_item_data_field_elided_value:
                _current_item_data_field_value_label.setText(_current_item_data_field_elided_value)
            _current_item_data_field_value_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            _current_item_data_field_value_label.setWordWrap(True)
            _current_item_data_field_value_label.setToolTip(_current_item_data_field_value)
            if self._is_href_value(_current_item_data_field_value):
                _current_item_data_field_value_label.setText(
                    f'<a href="{_current_item_data_field_value}">{_current_item_data_field_value}</a>'
                )
                _current_item_data_field_value_label.setOpenExternalLinks(True)
                _current_item_data_field_value_label.setTextInteractionFlags(
                    Qt.TextInteractionFlag.TextBrowserInteraction # type: ignore
                    | Qt.TextInteractionFlag.TextSelectableByMouse # type: ignore
                    | Qt.TextInteractionFlag.TextSelectableByKeyboard # type: ignore
                )
            else:
                _current_item_data_field_value_label.setTextInteractionFlags(
                    Qt.TextInteractionFlag.TextSelectableByMouse # type: ignore
                    | Qt.TextInteractionFlag.TextSelectableByKeyboard # type: ignore
                )
            self._form_layout.addRow(
                _current_item_data_field_name_label,
                _current_item_data_field_value_label
            )

    def preview(self, _current_item: Optional[ZoteroItem]):
        self._clear_form_layout()
        if not _current_item:
            return
        self._type_label.setText(self._format_type(_current_item.item_type))
        self._populate_form_layout(_current_item)
