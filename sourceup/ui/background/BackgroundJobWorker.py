import traceback
from PySide6.QtCore import QObject, Signal, Slot

class BackgroundJobWorker(QObject):
    success = Signal(object)
    error = Signal(Exception)

    def __init__(
        self,
        _worker_fn,
        *_args,
        _parent: QObject | None = None,
        **_kwargs
    ):
        super().__init__(_parent)
        self._worker_fn = _worker_fn
        self._args = _args
        self._kwargs = _kwargs

    @Slot()
    def run(self):
        try:
            _worker_fn_result = self._worker_fn(*self._args, **self._kwargs)
        except Exception as exc:
            traceback.print_exc()
            self.error.emit(exc)
        else:
            self.success.emit(_worker_fn_result)
