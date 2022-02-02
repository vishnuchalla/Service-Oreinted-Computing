import pytest
import yaml
import asyncio
import logging
from protocheck import bspl
from bungie.policies import *
from bungie.adapter import Message, Adapter
from bungie.history import History

specification = bspl.parse(
    """
Order {
  roles C, S // Customer, Seller
  parameters out item key, out done
  private extra, ackID, remID

  C -> S: Buy[out item]
  S -> C: BuyAck[in item, out ackID key]
  C -> S: BuyReminder[in item, out remID key]

  S -> C: Deliver[in item, out done]
  S -> C: Extra[in item, out extra]
}

With-Reject {
  roles C, S
  parameters out item key, out done

  Order(C, S, out item, out done)
  S -> C: Reject[in item, out done]
}
"""
)


order = specification.export("Order")
from Order import C, S, Buy, Deliver, BuyAck, BuyReminder, Extra

config = {C: ("localhost", 8001), S: ("localhost", 8001)}
Map = {
    "forwards": {Buy: (BuyReminder, "remID")},
    "acknowledgments": {Buy: (BuyAck, "ackID")},
}

logger = logging.getLogger("bungie")
logger.setLevel(logging.DEBUG)


@pytest.mark.asyncio
async def test_remind_until_received():
    r = Remind(Buy).With(Map).until.received(Deliver)
    assert r
    assert r.proactors  # proactor for reminding
    assert r.reactors  # reactors for handling reception

    # Buy without Deliver should be resent
    a = Adapter(C, order, config)
    a.add_policies(r)
    assert a.reactors[Buy]

    m = Message(Buy, {"item": "shoe"})
    await a.prepare_send(m)
    assert r.active
    selected = r.run(a.history)
    assert selected
    assert selected[0].schema == BuyReminder

    # Buy with Deliver should not
    await a.receive({"item": "shoe", "done": "yep"})
    selected = r.run(a.history)
    assert not selected


@pytest.mark.asyncio
async def test_remind_until_ack():
    r = Remind(Buy).With(Map).until.acknowledged
    assert r
    assert r.proactors
    assert r.reactors

    # Buy without acknowledgement should be resent
    a = Adapter(C, order, config)
    a.add_policies(r)

    m = Message(Buy, {"item": "shoe"})
    await a.prepare_send(m)
    selected = r.run(a.history)
    assert selected
    assert next(selected).schema == BuyReminder

    # Should not be resent after acknowledgement
    await a.receive({"item": "shoe", "ackID": 1})
    selected = r.run(a.history)
    assert next(selected, None) == None


@pytest.mark.asyncio
async def test_remind_until_conjunction():
    r = Remind(Buy).With(Map).until.received(Deliver, Extra)
    assert r
    assert r.proactors  # proactor for reminding
    assert r.reactors  # reactors for handling reception

    # Buy without Deliver should be resent
    a = Adapter(C, order, config)
    a.add_policies(r)
    assert a.reactors[Buy]
    m = Message(Buy, {"item": "shoe"})
    await a.prepare_send(m)
    assert r.active
    selected = r.run(a.history)
    assert selected
    assert selected[0].schema == BuyReminder

    # Buy with only Deliver should still be resent
    await a.receive({"item": "shoe", "done": "yep"})
    selected = r.run(a.history)
    assert not selected

    # Buy with both Deliver and Extra should not be resent
    await a.receive({"item": "shoe", "extra": "totally"})
    selected = r.run(a.history)
    assert not selected


def test_parser():
    p = model.parse("remind labeler of RequestLabel until received Packed")
    print(p)
    assert p


def test_from_ast():
    ast = model.parse("remind seller of Buy until received Deliver")
    print(ast)
    policy = from_ast(order, ast)
    assert policy
    assert type(policy) == Remind
    assert "Buy" in [m.name for m in policy.schemas]
    assert not policy.reactive
    print([e for e in ast["events"]])
    assert policy.proactors[0].__name__ == "process"

    ast = model.parse("remind seller of Buy until received Deliver or received Extra")
    print(ast)
    policy = from_ast(order, ast)
    assert policy
    assert type(policy) == Remind
    assert "Buy" in [m.name for m in policy.schemas]
    assert not policy.reactive
    print([e for e in ast["events"]])
    assert policy.proactors[0].__name__ == "process"


def test_policy_parser():
    reminder_policy = """
    - policy: remind S of Buy until Deliver
      when: 0 0 * * *
      max tries: 5
    """
    assert parse(order, reminder_policy)

    ack_policy = """
    - policy: acknowledge Buy
    """
    assert parse(order, ack_policy)

    until_ack_policy = """
    - policy: remind S of Buy until acknowledged
    """
    assert parse(order, until_ack_policy)
