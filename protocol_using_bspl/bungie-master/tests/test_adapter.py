import asyncio
import logging
import pytest
from protocheck import bspl
from bungie.adapter import Adapter, Message
from bungie.emitter import Emitter

specification = bspl.parse(
    """
RFQ {
  roles C, S // Customer, Seller
  parameters out item key, out ship
  private price, payment

  C -> S: req[out item]
  S -> C: quote[in item, out price]
  C -> S: pay[in item, in price, out payment]
  S -> C: ship[in item, in payment, out ship]
}
"""
)

RFQ = specification.protocols["RFQ"]

config = {
    RFQ.roles["C"]: ("localhost", 8001),
    RFQ.roles["S"]: ("localhost", 8002),
}

logger = logging.getLogger("bungie")
logger.setLevel(logging.DEBUG)


@pytest.mark.asyncio
async def test_receive_process():
    a = Adapter(RFQ.roles["S"], RFQ, config)
    await a.task()
    await a.receive({"item": "ball"})
    await a.stop()

    print(f"messages: {a.history.messages}")


@pytest.mark.asyncio
async def test_send_process():
    a = Adapter(RFQ.roles["C"], RFQ, config, emitter=Emitter())
    m = Message(RFQ.messages["req"], {"item": "ball"})
    await a.task()
    await a.process_send(m)
    await a.stop()


@pytest.mark.asyncio
async def test_match():
    """Test that the schema.match(**params) method works"""
    # create adapter and inject methods
    a = Adapter(RFQ.roles["S"], RFQ, config)
    await a.task()
    # make sure there's a req in the history
    await a.receive({"item": "ball"})

    # There should be one enabled 'quote'
    ms = RFQ.messages["quote"].match(item="ball")
    assert len(ms) == 1

    # But not any enabled 'ship's
    ms2 = RFQ.messages["ship"].match(item="ball")
    assert len(ms2) == 0
    await a.stop()
