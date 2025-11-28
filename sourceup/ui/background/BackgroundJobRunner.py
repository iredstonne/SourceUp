from PySide6.QtCore import QThread, QObject
from PySide6.QtWidgets import QWidget
from sourceup.ui.background.BackgroundJobPresentation import BackgroundJobPresentation
from sourceup.ui.background.BackgroundJobWorker import BackgroundJobWorker

class BackgroundJobRunner(QObject):
    def __init__(self, _parent: QWidget, _presentation: BackgroundJobPresentation):
        super().__init__()
        self._parent = _parent
        self._presentation = _presentation

    def run(self, fetch_fn, on_success, on_error, *args, **kwargs):
        _worker = BackgroundJobWorker(fetch_fn, *args, **kwargs)
        _thread = QThread(self.parent())
        _thread.started.connect(_worker.run)
        _worker.moveToThread(_thread)
        _worker.success.connect(on_success)
        _worker.error.connect(on_error)
        _worker.success.connect(_thread.quit)
        _worker.error.connect(_thread.quit)
        def _on_finished():
            self._presentation.on_finish()
            _worker.deleteLater()
            _thread.deleteLater()
        _thread.finished.connect(_on_finished)
        self._presentation.on_start(self._parent)
        _thread.start()
