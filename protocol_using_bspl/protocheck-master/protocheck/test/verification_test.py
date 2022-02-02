import pytest
from boolexpr import not_
from protocheck.bspl import *
from protocheck.verification import precedence, logic
from protocheck.verification.sat import *


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


def test_observes(Bid, A):
    assert str(observes(A, Bid)) == "A:Auction/Bid"


def test_transmission(Bid, A, B):
    assert logic.compile(transmission(Bid)).equiv(
        or_(not_(observes(A, Bid)), sequential(observes(B, Bid), observes(A, Bid)))
    )


def test_reception(Bid, B):
    # Unreliable even with exhaustive enabled
    assert precedence.consistent(reception(Bid), exhaustive=True)


def test_role_messages(A):
    assert A.messages


def test_minimality(A, Auction):
    print(minimality(A, Auction))
    # Seems to require exhaustive checking
    assert consistent(minimality(A, Auction), exhaustive=True)


def test_enactable(Auction):
    assert enactability(Auction)
    assert consistent(enactability(Auction))


def test_correct(Auction):
    c = correct(Auction)
    assert c
    # Unreliable without exhaustive
    assert consistent(correct(Auction), exhaustive=True)


def test_maximal(Auction):
    assert maximal(Auction)
    assert consistent(maximal(Auction))


def test_begin(Auction):
    assert begin(Auction)
    assert consistent(begin(Auction))


def test_complete(Auction):
    print(complete(Auction))
    assert complete(Auction)
    assert consistent(complete(Auction))


def test_is_enactable(Auction):
    assert is_enactable(Auction)


def test_protocol_dead_end(Auction):
    assert dead_end(Auction)
    print(dead_end(Auction))
    o = consistent(dead_end(Auction))
    if o:
        print([k for k, v in o.items() if v])
    assert not o


def test_is_live(Auction):
    assert is_live(Auction)


def test_protocol_unsafe(Auction):
    o = consistent(unsafe(Auction))
    if o:
        print([k for k, v in o.items() if v == 1])
    assert not o


def test_protocol_safe(Auction):
    assert is_safe(Auction)


def test_protocol_is_atomic(Auction):
    assert is_atomic(Auction)


def test_protocol_cover(Auction):
    assert cover(Auction)
