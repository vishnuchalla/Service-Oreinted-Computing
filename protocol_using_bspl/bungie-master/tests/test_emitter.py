from protocheck import bspl
from bungie.emitter import Bundle
from collections import deque
import pytest

specification = bspl.parse("""
Order {
  roles C, S // Customer, Seller
  parameters out item key, out done

  C -> S: Buy[out item]
  S -> C: Deliver[in item, out done]
}

With-Reject {
  roles C, S
  parameters out item key, out done

  Order(C, S, out item, out done)
  S -> C: Reject[in item, out done]
}
""")

with_reject = specification.protocols['With-Reject']

config = {
    with_reject.roles['C']: ('localhost', 8001),
    with_reject.roles['S']: ('localhost', 8002)
}


def test_bundle():
    b = Bundle(1500)
    queue = deque([b'a'])
    b.pack(queue)
    assert(b.contents == b'a')

    b = Bundle(1500)
    queue = deque([b'a', b'b'])
    b.pack(queue)
    assert(b.contents == b'a,b')

    b = Bundle(1500)
    queue = deque([b'a', b'b', b'a'*1500])
    b.pack(queue)
    assert(b.contents == b'a,b')

    b = Bundle(1500)
    queue = deque([b'a'*1500])
    with pytest.raises(Exception):
        b.pack(queue)
