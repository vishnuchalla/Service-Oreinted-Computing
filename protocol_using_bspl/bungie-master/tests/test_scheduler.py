from bungie.adapter import Message
from bungie.scheduler import *


def test_exponential_backoff():
    backoff = exponential()
    m = Message(None, None)

    # no backoff if retries = 0
    assert backoff(m) == 0

    for i in range(5):
        m.meta['retries'] = i
        assert backoff(m) <= 2 ** i - 1


def test_schedule_format():
    Scheduler('* * * * *')

    Scheduler('every second')

    Scheduler('every 1s')

    Scheduler('every 3.5s')

    Scheduler('every 4 seconds')
