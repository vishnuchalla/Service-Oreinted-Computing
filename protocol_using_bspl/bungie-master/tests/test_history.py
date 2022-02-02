import asyncio
import logging
import pytest
from protocheck import bspl
from bungie.adapter import Adapter
from bungie.history import History

specification = bspl.parse(
    """
Logistics {
  roles Merchant, Wrapper, Labeler, Packer
  parameters out orderID key, out itemID key, out item, out status
  private address, label, wrapping

  Merchant -> Labeler: RequestLabel[out orderID key, out address]
  Merchant -> Wrapper: RequestWrapping[in orderID key, out itemID key, out item]
  Wrapper -> Packer: Wrapped[in orderID key, in itemID key, in item, out wrapping]
  Labeler -> Packer: Labeled[in orderID key, in address, out label]
  Packer -> Merchant: Packed[in orderID key, in itemID key, in wrapping, in label, out status]
}
"""
)

logistics = specification.export("Logistics")
from Logistics import Packer, Wrapped, Labeled, Packed

config = {
    Packer: ("localhost", 8001),
}

a = Adapter(Packer, logistics, config)  # for injection

logger = logging.getLogger("bungie")
logger.setLevel(logging.DEBUG)


def test_observe():
    h = History()
    m = Labeled(orderID=1, address="home", label="0001")
    h.observe(m)
    assert m in h.messages[Labeled].values()


def test_context_messages():
    h = History()
    m = Labeled(orderID=1, address="home", label="0001")
    h.observe(m)
    print(h.contexts)
    assert m in h.contexts["orderID"][1].messages


def test_context_all_messages():
    h = History()
    m2 = Wrapped(orderID=1, itemID=0, item="ball", wrapping="paper")
    h.observe(m2)
    print(h.contexts)
    print([m for m in h.contexts["orderID"][1].all_messages])
    assert m2 in h.contexts["orderID"][1].all_messages


def test_context_bindings():
    h = History()

    m = Wrapped(orderID=1, itemID=0, item="ball", wrapping="paper")
    h.observe(m)
    print(h.contexts["orderID"][1].bindings)
    assert h.contexts["orderID"][1].bindings.get("orderID") == None
    assert (
        h.contexts["orderID"][1].subcontexts["itemID"][0].bindings.get("orderID") == 1
    )


def test_context_all_bindings():
    h = History()
    m = Wrapped(orderID=1, itemID=0, item="ball", wrappeng="paper")
    h.observe(m)
    m2 = Wrapped(orderID=1, itemID=1, item="bat", wrappeng="paper")
    h.observe(m2)
    print(h.contexts["orderID"][1].all_bindings)
    items = h.contexts["orderID"][1].all_bindings["itemID"]
    assert not items.isdisjoint([0, 1])
    assert h.contexts["orderID"][1].all_bindings["orderID"] == [1]


def test_matching_contexts():
    h = History()
    m = Wrapped(orderID=1, itemID=0, item="ball", wrappeng="paper")
    h.observe(m)
    m2 = Wrapped(orderID=1, itemID=1, item="bat", wrappeng="paper")
    h.observe(m2)
    m3 = Labeled(orderID=1, address="home", label="0001")
    h.observe(m3)
    contexts = h.matching_contexts(**m3.payload)
    print([c.bindings for c in contexts])
    assert len(contexts) == 3
