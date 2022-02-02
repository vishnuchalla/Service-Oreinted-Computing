#!/usr/bin/env python3

import pytest
from protocheck.bspl import load_file
from protocheck.verification.paths import *


@pytest.fixture(scope="module")
def BasicRefinement():
    return load_file("samples/bspl/refinement/basic.bspl")


@pytest.fixture(scope="module")
def P(BasicRefinement):
    return BasicRefinement.protocols["P"]


@pytest.fixture(scope="module")
def ConcurrencyElimination():
    return load_file("samples/bspl/refinement/concurrency-elimination.bspl")


@pytest.fixture(scope="module")
def Flexible(ConcurrencyElimination):
    return ConcurrencyElimination.protocols["Flexible-Purchase"]


@pytest.fixture(scope="module")
def AllIn():
    return load_file("samples/bspl/refinement/all-in.bspl")


def test_known_empty(P):
    assert known(empty_path(), {}, P.roles["A"]) == set()


def test_known_simple(P):
    print("test keys: ", P.messages["test"].keys)
    e = Emission(P.messages["test"])
    assert known([e, Reception(e)], P.messages["test"].keys, P.roles["A"]) == {
        "data",
        "id",
    }


def test_viable(P, Flexible):
    test = P.messages["test"]
    assert viable(empty_path(), test)
    assert not viable([Emission(test)], test)

    rfq = Flexible.messages["rfq"]
    e = Emission(rfq)
    print("S knows: ", known([e, Reception(e)], rfq.keys, Flexible.roles["S"]))
    assert rfq.keys.keys() == Flexible.messages["pay"].keys.keys()
    assert viable([e, Reception(e)], Flexible.messages["pay"])


def test_viable_all_in(AllIn):
    P = AllIn.protocols["P"]
    test = P.messages["test"]

    assert not viable(empty_path(), test)
    assert not viable([Emission(test)], test)


def test_max_paths(P):
    U = UoD.from_protocol(P)

    e = Emission(P.messages["test"])
    assert max_paths(U) == [(e, Reception(e))]


def test_all_paths(P, Flexible):
    e = Emission(P.messages["test"])
    assert all_paths(UoD.from_protocol(P)) == {
        empty_path(),
        (e,),
        (e, Reception(e)),
    }
    assert len(all_paths(UoD.from_protocol(Flexible))) > 2


def test_possibilities(P):
    u = UoD.from_protocol(P)
    assert possibilities(u, empty_path()) == {Emission(P.messages["test"])}


def test_unreceived(P):
    path = [Emission(P.messages["test"])]
    assert len(unreceived(path)) == 1


def test_extensions(P):
    u = UoD.from_protocol(P)
    e = Emission(P.messages["test"])
    p1 = (e,)
    assert extensions(u, empty_path()) == {p1}
    assert extensions(u, p1) == {(e, Reception(e))}


def test_sources(P):
    assert sources(empty_path(), P.parameters["id"]) == set()
    assert sources([Emission(P.messages["test"])], "id") == {"A"}
