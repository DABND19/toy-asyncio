from queue import SimpleQueue

from callback_handler import CallbackHandler
from future import Future

class EventLoop:
    def __init__(self):
        self.events = SimpleQueue()
        self.callbacks = CallbackHandler()

    def call_later(self, delay, callback, *args) -> Future:
        return self.callbacks.call_later(delay, callback, *args)

    def step(self, coro):
        try:
            next(coro)
        except StopIteration as e:
            return e.value
        self.events.put(coro)

    def run(self):
        while not self.events.empty():
            self.callbacks.step()
            self.step(self.events.get())

    def create_task(self, coro):
        future = Future()

        def wrapper():
            try:
                result = yield from coro
                future.set_result(result)
            except Exception as error:
                future.set_exception(error)
        
        gen = wrapper()
        self.events.put(gen)
        return future

    def run_until_complete(self, coro):
        future = self.create_task(coro)
        self.run()
        return future.get_result()
