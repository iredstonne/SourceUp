import requests
from requests.exceptions import (
    ConnectionError,
    ProxyError,
    SSLError,
    Timeout,
    HTTPError
)
from PySide6.QtWidgets import QMessageBox
from packaging import version
from PySide6.QtCore import QObject, Signal, QThread, QUrl
from PySide6.QtGui import QDesktopServices
from sourceup.manifest import (
    APP_NAME,
    GITHUB_API_REPO_LATEST_RELEASE_URL,
    GITHUB_REPO_URL
)

class FetchRepoVersionTagNameWorker(QObject):
    finished = Signal(str)

    def run(self):
        try:
            print("Fetching repo version tag name...")
            _repo_version_tag_name_response = requests.get(
                 GITHUB_API_REPO_LATEST_RELEASE_URL,
                 timeout=3
            )
            _repo_version_tag_name_response.raise_for_status()
            _repo_version_tag_name_response_data = _repo_version_tag_name_response.json()
            _repo_version_tag_name = _repo_version_tag_name_response_data.get("tag_name", "")
            self.finished.emit(_repo_version_tag_name)
        except (ConnectionError, ProxyError, SSLError, Timeout, HTTPError) as e:
            print("Failed to get repo version tag name.", str(e))
            print("Failing silently...")
            self.finished.emit(None)

def _show_new_update_available_dialog(_current_version_tag_name: str, _repo_version_tag_name: str):
    _new_update_available_message_box = QMessageBox()
    _new_update_available_message_box.setWindowTitle("New Update Available")
    _new_update_available_message_box.setText(
        f"A new update of {APP_NAME} is available for download.\n"
        f"Current version: {_current_version_tag_name}\n"
        f"Latest version: {_repo_version_tag_name}\n"
    )
    _new_update_available_message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    _new_update_available_message_box.button(QMessageBox.StandardButton.Yes).setText("Update now")
    _new_update_available_message_box.button(QMessageBox.StandardButton.No).setText("Remind me later")
    if _new_update_available_message_box.exec_() == QMessageBox.StandardButton.Yes:
        QDesktopServices.openUrl(QUrl(GITHUB_REPO_URL))

def _on_repo_version_tag_name_received(_current_version_tag_name: str, _repo_version_tag_name: str):
    if _repo_version_tag_name:
        if version.parse(_repo_version_tag_name) > version.parse(_current_version_tag_name):
            print(f"New update available: {_current_version_tag_name} -> {_repo_version_tag_name}")
            _show_new_update_available_dialog(_current_version_tag_name, _repo_version_tag_name)
        return
    print("You are up to date")

_fetch_repo_version_tag_name_thread: QThread
_fetch_repo_version_tag_name_worker: QThread

def check_if_new_update_is_available(_current_version_tag_name: str):
    global _fetch_repo_version_tag_name_thread, \
           _fetch_repo_version_tag_name_worker
    _fetch_repo_version_tag_name_thread = QThread()
    _fetch_repo_version_tag_name_worker = FetchRepoVersionTagNameWorker()
    _fetch_repo_version_tag_name_worker.moveToThread(_fetch_repo_version_tag_name_thread)
    _fetch_repo_version_tag_name_thread.started.connect(_fetch_repo_version_tag_name_worker.run)
    _fetch_repo_version_tag_name_worker.finished.connect(
        lambda _repo_version_tag_name: _on_repo_version_tag_name_received(
            _current_version_tag_name,
            _repo_version_tag_name
        )
    )
    _fetch_repo_version_tag_name_worker.finished.connect(_fetch_repo_version_tag_name_thread.quit)
    _fetch_repo_version_tag_name_worker.finished.connect(_fetch_repo_version_tag_name_worker.deleteLater)
    _fetch_repo_version_tag_name_thread.finished.connect(_fetch_repo_version_tag_name_thread.deleteLater)
    _fetch_repo_version_tag_name_thread.start()
