import pytest
from protocheck.verification.refinement import *
from protocheck.verification.paths import Emission, Reception, empty_path, viable
from protocheck.verification import paths


@pytest.fixture(scope="module")
def BasicRefinement():
    return load_file("samples/bspl/refinement/basic.bspl")


@pytest.fixture(scope="module")
def P(BasicRefinement):
    return BasicRefinement.protocols["P"]


@pytest.fixture(scope="module")
def Q(BasicRefinement):
    return BasicRefinement.protocols["Q"]


@pytest.fixture(scope="module")
def ConcurrencyElimination():
    return load_file("samples/bspl/refinement/concurrency-elimination.bspl")


@pytest.fixture(scope="module")
def Flexible(ConcurrencyElimination):
    return ConcurrencyElimination.protocols["Flexible-Purchase"]


@pytest.fixture(scope="module")
def ShipFirst(ConcurrencyElimination):
    return ConcurrencyElimination.protocols["Ship-First"]


@pytest.fixture(scope="module")
def KeyReduction():
    return load_file("samples/bspl/refinement/key-reduction.bspl")


@pytest.fixture(scope="module")
def AddIntermediary():
    return load_file("samples/bspl/refinement/add-intermediary.bspl")


@pytest.fixture(scope="module")
def AllIn():
    return load_file("samples/bspl/refinement/all-in.bspl")


@pytest.fixture(scope="module")
def PurchaseComposition():
    return load_file("samples/bspl/refinement/purchase-composition.bspl")


def test_subsumes(P, Q):
    U = UoD.from_protocol(P)
    params = {"id", "data"}
    assert subsumes(UoD(), set(), empty_path(), empty_path())
    assert subsumes(U, params, empty_path(), empty_path())

    e = Emission(Q.messages["test"])
    assert subsumes(U, params, [e, Reception(e)], [e, Reception(e)])

    assert not subsumes(U, params, empty_path(), [e])

    assert not subsumes(U, params, [e], empty_path())


def test_subsumes_initiation_reduction():
    spec = load_file("samples/bspl/refinement/initiation-reduction.bspl")
    EitherStarts = spec.protocols["Either-Starts"]
    BuyerStarts = spec.protocols["Buyer-Starts"]

    rfq1 = Emission(BuyerStarts.messages["rfq"])
    rfq2 = Emission(EitherStarts.messages["rfq"])
    assert subsumes(
        UoD.from_protocol(EitherStarts),
        EitherStarts.public_parameters.keys(),
        [rfq1, Reception(rfq1)],
        [rfq2, Reception(rfq2)],
        verbose=True,
    )


def test_subsumes_key_reduction(KeyReduction):
    KeyP = KeyReduction.protocols["P"]
    KeyQ = KeyReduction.protocols["Q"]

    test_q = Emission(KeyQ.messages["test"])
    test_p = Emission(KeyP.messages["test"])
    path_q = (test_q, Reception(test_q))
    path_p = (test_p, Reception(test_p))
    print(known(path_q, KeyQ.messages["test"].keys, KeyQ.roles["A"]))
    print(known(path_p, KeyQ.messages["test"].keys, KeyQ.roles["A"]))
    assert subsumes(
        UoD.from_protocol(KeyP),
        KeyP.public_parameters.keys(),
        path_q,
        path_p,
        verbose=True,
    )


def test_refines(Q, P):
    U = UoD()
    params = {"id", "data"}

    assert refines(U, P.public_parameters.keys(), Q, P) == {"ok": True}


def test_concurrency_elimination(Flexible, ShipFirst):
    print(all_paths(UoD.from_protocol(Flexible)))
    print(all_paths(UoD.from_protocol(ShipFirst)))
    assert refines(UoD(), Flexible.public_parameters.keys(), ShipFirst, Flexible) == {
        "ok": True
    }

    assert refines(UoD(), Flexible.public_parameters.keys(), Flexible, ShipFirst) != {
        "ok": True
    }


def test_initiation_reduction():
    spec = load_file("samples/bspl/refinement/initiation-reduction.bspl")
    EitherStarts = spec.protocols["Either-Starts"]
    BuyerStarts = spec.protocols["Buyer-Starts"]

    result = refines(
        UoD(),
        EitherStarts.public_parameters.keys(),
        BuyerStarts,
        EitherStarts,
        verbose=True,
    )
    assert result == {"ok": True}

    result = refines(
        UoD(),
        BuyerStarts.public_parameters.keys(),
        EitherStarts,
        BuyerStarts,
        verbose=True,
    )
    assert result != {"ok": True}


def test_message_split():
    spec = load_file("samples/bspl/refinement/message-split.bspl")
    RFQ = spec.protocols["RFQ"]
    RefinedRFQ = spec.protocols["Refined-RFQ"]
    assert not refines(UoD(), RFQ.public_parameters.keys(), RefinedRFQ, RFQ)["ok"]

    # {"ok": False,
    #  'path': (Instance(RefinedRFQ.messages['Introduction'], 0),),
    #  'reason': 'Refined-RFQ has path that does not subsume any path in RFQ'}

    assert refines(UoD(), RefinedRFQ.public_parameters.keys(), RFQ, RefinedRFQ) != {
        "ok": True
    }


def test_dependent():
    spec = load_file("samples/bspl/refinement/basic-dependent.bspl")
    P = spec.protocols["P"]
    Q = spec.protocols["Q"]
    assert refines(UoD(), P.public_parameters.keys(), Q, P) == {"ok": True}

    assert refines(UoD(), Q.public_parameters.keys(), P, Q) == {"ok": True}


def test_polymorphism_reduction():
    spec = load_file("samples/bspl/refinement/polymorphism.bspl")
    P = spec.protocols["Polymorphic-RFQ"]
    Q = spec.protocols["RFQ"]
    assert refines(UoD(), P.public_parameters.keys(), Q, P) == {"ok": True}

    assert refines(UoD(), Q.public_parameters.keys(), P, Q)["ok"] == False


def test_key_reduction():
    spec = load_file("samples/bspl/refinement/key-reduction.bspl")
    P = spec.protocols["P"]
    p_test = P.messages["test"]
    Q = spec.protocols["Q"]
    q_test = Q.messages["test"]
    print("P test keys: ", p_test.keys)
    print("Q test keys: ", q_test.keys)

    assert refines(UoD(), P.public_parameters.keys(), Q, P) == {"ok": True}

    assert refines(UoD(), Q.public_parameters.keys(), P, Q) != {"ok": True}


def test_all_in():
    spec = load_file("samples/bspl/refinement/all-in.bspl")
    P = spec.protocols["P"]
    p_test = P.messages["test"]
    Q = spec.protocols["Q"]
    q_test = Q.messages["test"]

    assert refines(UoD(), P.public_parameters.keys(), Q, P) == {"ok": True}

    assert refines(UoD(), Q.public_parameters.keys(), P, Q) == {"ok": True}


def test_add_intermediary(AddIntermediary):
    P = AddIntermediary.protocols["Simple-Payment"]
    Q = AddIntermediary.protocols["Escrowed-Payment"]

    print(all_paths(UoD.from_protocol(P)))
    assert refines(UoD(), P.public_parameters, Q, P) == {"ok": True}

    assert refines(UoD(), Q.public_parameters, P, Q) != {"ok": True}


def test_composition(PurchaseComposition):
    P = PurchaseComposition.protocols["Commerce"]
    Q = PurchaseComposition.protocols["Refined-Commerce"]

    assert refines(UoD(), P.public_parameters.keys(), Q, P) == {"ok": True}

    assert refines(UoD(), Q.public_parameters.keys(), P, Q) != {"ok": True}
