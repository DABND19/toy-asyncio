from time import monotonic

from event_loop import EventLoop
from future import Future


loop = EventLoop()


def sleep(seconds) -> Future:
    return loop.call_later(seconds, lambda: True)

def test():
    yield from sleep(2)
    print(monotonic(), 'test done')


if __name__ == '__main__':
    print(monotonic(), 'start')
    loop.create_task(test())
    loop.create_task(test())
    loop.run_until_complete(test())
    print(monotonic(), 'finish')
