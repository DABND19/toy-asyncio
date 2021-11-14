from functools import partial
import heapq
from time import monotonic
from typing import Callable, List, Tuple

from future import Future


class CallbackHandler:
    def __init__(self):
        self.heap: List[Tuple[float, Future, Callable]] = []

    def call_later(self, delay, func, *args) -> Future:
        future = Future()
        heapq.heappush(self.heap, (delay + monotonic(), future, partial(func, *args)))
        return future

    def step(self) -> None:
        while self.heap:
            if self.heap[0][0] > monotonic():
                return
            soon, future, func = heapq.heappop(self.heap)
            try:
                future.set_result(func())
            except Exception as error:
                future.set_exception(error)
