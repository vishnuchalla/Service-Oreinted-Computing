import pytest
from boolexpr import not_
from protocheck.bspl import *
from protocheck.verification import logic, precedence


@pytest.fixture(scope="module")
def Auction():
    return load_file("samples/bspl/auction").protocols["Auction"]


@pytest.fixture(scope="module")
def A(Auction):
    return Auction.roles["A"]


@pytest.fixture(scope="module")
def B(Auction):
    return Auction.roles["B"]


@pytest.fixture(scope="module")
def Bid(Auction):
    return Auction.messages["Bid"]


@pytest.fixture(scope="module")
def WithReject():
    return load_file("samples/bspl/composition").protocols["With-Reject"]


def test_keys(Bid, Auction):
    print(Auction.keys)
    assert [p for p in Auction.keys] == ["id"]
    # id explicitly declared key in P, but not message. Should still be considered a key
    print(Bid.keys)
    assert len({p for p in Bid.keys}) == 2


def test_parameter(Bid, Auction):
    assert len(Bid.parameters.values()) > 0
    p = Bid.parameters.get("id", None)
    assert p
    assert p.adornment


def test_params(Bid):
    assert len(Bid.ins) == 1
    assert "id" in Bid.ins

    assert len(Bid.outs) == 2
    assert "bidID" in Bid.outs
    assert "bid" in Bid.outs

    assert len(Bid.nils) == 1
    assert "done" in Bid.nils


def test_msg_roles(Bid):
    assert Bid.sender.name == "B"
    assert Bid.recipient.name == "A"


def test_protocol_roles(Auction):
    assert len(Auction.roles.keys()) == 2
    assert Auction.roles["A"].name == "A"


def test_protocol_messages(Auction):
    assert len(Auction.messages) == 3
    assert Auction.messages.get("Bid")


def test_parameter_format(Bid):
    assert Bid.parameters["bidID"].format() == "out bidID key"


def test_message_format(Bid):
    assert Bid.format() == "B -> A: Bid[in id key, out bidID key, out bid, nil done]"


def test_protocol_format(Auction, WithReject):
    assert (
        Auction.format()
        == """Auction {
  roles A, B
  parameters out id key, out done
  private bidID, bid

  A -> B: Start[out id key]
  B -> A: Bid[in id key, out bidID key, out bid, nil done]
  A -> B: Stop[in id key, out done]
}"""
    )

    assert (
        WithReject.format()
        == """With-Reject {
  roles C, S
  parameters out item key, out done

  Order(C, S, out item key, out done)
  S -> C: Reject[in item key, out done]
}"""
    )
