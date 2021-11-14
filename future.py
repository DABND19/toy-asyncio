import logging


class Future:
    def __init__(self) -> None:
        self.result = None
        self.done = False
        self.done_callbacks = set()
        self.exception = None

    def _handle_callbacks(self):
        for callback in self.done_callbacks:
            try:
                callback(self)
            except Exception:
                logging.exception(f'Unhandled exception in {callback}')

    def set_result(self, result):
        self.done = True
        self.result = result
        self._handle_callbacks()

    def set_exception(self, exception):
        self.done = True
        self.exception = exception
        self._handle_callbacks()

    def get_result(self):
        if self.exception:
            raise self.exception
        return self.result

    def __await__(self):
        while not self.done:
            yield None
        return self.get_result()
