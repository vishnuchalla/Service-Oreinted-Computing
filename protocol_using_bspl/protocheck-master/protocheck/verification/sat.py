import json
import pprint as pp
from .precedence import (
    consistent,
    pairwise,
    and_,
    or_,
    bx,
    sequential,
    simultaneous,
    impl,
    ordered,
    reset_stats,
    stats,
    wrap,
    var,
    name,
    onehot,
)
from . import logic
from .logic import merge, onehot0
from functools import lru_cache, partial
from ..protocol import Message
from ..commands import register_commands
from ..bspl import load_protocols


@wrap(name)
def observes(role, event):
    return var(role + ":" + event)


send = observes
recv = observes


def atomic(P):
    c = correct(P)
    m = maximal(P)

    def inner(Q, r):
        formula = logic.And(c, m, enactability(r), incomplete(Q))
        return formula

    return inner


# Role
def minimality(role, protocol):
    """Every parameter observed by a role must have a corresponding
    message transmission or reception"""
    sources = {}

    def add(m, p):
        if p in sources:
            sources[p].append(m)
        else:
            sources[p] = [m]

    outgoing = set()
    for m in role.messages(protocol).values():
        if m.recipient == role:
            for p in m.ins.union(m.outs):
                add(m, p)
        else:
            for p in m.outs:
                add(m, p)
            for p in m.ins:
                outgoing.add(p)

    # keep track of 'in' parameters being sent without sources
    # unsourced parameters cannot be observed
    unsourced = [
        logic.Name(~observes(role, p), p) for p in outgoing - set(sources.keys())
    ]

    # sourced parameters must be received or sent to be observed
    sourced = [
        logic.Name(
            impl(
                observes(role, p),
                or_(
                    *[
                        simultaneous(observes(role, m), observes(role, p))
                        for m in sources[p]
                    ]
                ),
            ),
            p,
        )
        for p in sources
    ]

    return logic.And(*(unsourced + sourced))


def nonsimultaneity(self, protocol):
    msgs = [sent(m) for m in protocol.messages.values() if m.sender == self]
    if len(msgs) > 1:
        return ordered(*msgs)
    else:
        return bx.ONE


# Protocol


@lru_cache()
def is_enactable(P, **kwargs):
    return consistent(logic.And(correct(P), enactability(P)), **kwargs)


def is_live(protocol):
    return is_enactable(protocol) and not consistent(dead_end(protocol))


def is_safe(P):
    # prove there are no unsafe enactments
    return not consistent(unsafe(P))


def recursive_property(P, prop, filter=None, **kwargs):
    default_kwargs = {"verbose": False, "filter": None}
    kwargs = {**default_kwargs, **kwargs}

    for r in P.references.values():
        if filter and not filter(r):
            continue  # skip references that do not pass the filter
        formula = prop(P, r)
        if kwargs["verbose"]:
            print_formula(formula)
        s = consistent(formula)
        if s:
            # found solution; short circuit
            return s, formula
        else:
            # recurse
            s, formula = recursive_property(r, prop, filter)
            if s:
                return s, formula

    return None, None


def check_atomicity(P, **kwargs):
    default_kwargs = {"verbose": False}
    kwargs = {**default_kwargs, **kwargs}

    def filter(ref):
        return type(ref) is not Message or ref.is_entrypoint

    return recursive_property(P, atomic(P), filter=filter, **kwargs)


def is_atomic(P):
    solution, _ = check_atomicity(P)
    return not solution


def p_cover(P, parameter):
    if type(parameter) is not str:
        parameter = parameter.name

    alts = []
    for m in P.messages.values():
        if parameter in m.parameters:
            alts.append(m)
    return alts


@logic.named
def cover(P):
    return logic.And(
        *[
            logic.Name(or_(*[received(m) for m in p_cover(P, p)]), p.name + "-cover")
            for p in P.public_parameters.values()
        ]
    )


@logic.named
def unsafe(P):
    clauses = []
    for p in P.all_parameters:
        sources = [m for m in p_cover(P, p) if m.parameters[p].adornment == "out"]
        if len(sources) > 1:
            alts = []
            for r in P.roles.values():
                # assume an agent can choose between alternative messages
                msgs = [sent(m) for m in sources if m.sender == r]
                if msgs:
                    alts.append(or_(*msgs))
            # at most one message producing this parameter can be sent
            more_than_one = or_(*pairwise(and_, alts))

            # only consider cases where more than one at once is possible
            if more_than_one:
                clauses.append(logic.Name(more_than_one, p + "-unsafe"))
    if clauses:
        # at least one conflict
        return logic.And(correct(P), logic.Name(clauses, "unsafe"))
    else:
        # no conflicting pairs; automatically safe -> not unsafe
        return bx.ZERO


def enactable(P):
    "Some message must be received containing each parameter"
    clauses = []
    for p in P.public_parameters:
        clauses.append(or_(*[received(m) for m in p_cover(P, p)]))
    return and_(*clauses)


@logic.named
def enactability(P):
    return enactable(P)


@logic.named
def dead_end(protocol):
    return logic.And(correct(protocol), maximal(protocol), incomplete(protocol))


@logic.named
def correct(P):
    clauses = {}
    msgs = P.messages.values()
    roles = P.roles.values()
    clauses["Emission"] = {m.name: emission(m) for m in msgs}
    clauses["Reception"] = {m.name: reception(m) for m in msgs}
    clauses["Transmission"] = {m.name: transmission(m) for m in msgs}
    clauses["Non-lossy"] = {m.name: non_lossy(m) for m in msgs}
    clauses["Non-simultaneity"] = {r.name: nonsimultaneity(r, P) for r in roles}
    clauses["Minimality"] = {r.name: minimality(r, P) for r in roles}
    clauses["Uniqueness"] = {k: uniqueness(P, k) for k in P.keys}
    return clauses


@logic.named
def maximal(P):
    "Each message must be sent, or it must be blocked by a prior binding"
    clauses = []
    for m in P.messages.values():
        clauses.append(sent(m) | blocked(m))
    return and_(*clauses)


@logic.named
def begin(P):
    return or_(*[sent(m) for m in P.messages.values()])


def uniqueness(P, key):
    "Bindings to key parameters uniquely identify enactments, so there should never be multiple messages with the same out key in the same enactment"

    candidates = set()
    for m in P.messages.values():
        if key in m.outs:
            candidates.add(simultaneous(sent(m), observes(m.sender, key)))
    if candidates:
        return onehot0(*candidates)
    else:
        return True


def complete(P):
    "Each out parameter must be observed by at least one role"
    clauses = []
    for p in P.outs:
        clauses.append(
            or_(
                *[
                    received(m)
                    for m in p_cover(P, p)
                    if m.parameters[p].adornment == "out"
                ]
            )
        )
    return and_(*clauses)


@logic.named
def incomplete(P):
    return ~complete(P)


###### Message ######
def sent(m):
    return send(m.sender, m.qualified_name)


def received(m):
    return recv(m.recipient, m.qualified_name)


def blocked(msg):
    s = partial(observes, msg.sender)
    ins = [~s(p) for p in msg.ins]
    nils = [
        and_(s(p), ~(sequential(s(p), sent(msg)) | simultaneous(s(p), sent(msg))))
        for p in msg.nils
    ]
    outs = [s(p) for p in msg.outs]
    return or_(*(nils + outs + ins))


def transmission(msg):
    "Each message reception is causally preceded by its emission"
    return impl(received(msg), sequential(sent(msg), received(msg)))


def non_lossy(msg):
    "Each message emission results in reception"
    return impl(sent(msg), received(msg))


def emission(msg):
    """Sending a message must be preceded by observation of its ins,
    but cannot be preceded by observation of any nils or outs"""
    s = partial(observes, msg.sender)
    ins = [impl(sent(msg), sequential(s(p), sent(msg))) for p in msg.ins]
    nils = [impl(and_(sent(msg), s(p)), sequential(sent(msg), s(p))) for p in msg.nils]
    outs = [impl(sent(msg), simultaneous(s(p), sent(msg))) for p in msg.outs]
    return and_(*(ins + nils + outs))


def reception(msg):
    "Each message reception is accompanied by the observation of its parameters; either they are observed, or the message is not"
    clauses = [
        impl(
            received(msg),
            or_(sequential(p, received(msg)), simultaneous(p, received(msg))),
        )
        for p in map(partial(observes, msg.recipient), msg.ins | msg.outs)
    ]
    return and_(*clauses)


def print_formula(*formulas):
    print("\nFormula:")
    print(json.dumps(logic.merge(*formulas), default=str, sort_keys=True, indent=2))
    print()


class SATCommands:
    """Commands that use the SAT-solving method.

    The SAT-solving algorithms are not very efficient, and scale rapidly with
    the number of terms (messages, parameters, etc.) in the protocol.

    Args:
      verbose: Enable additional output
      quiet: Disable detailed output, printing only results
      stats: Print detailed runtime statistics
      debug: Enable additional debug output
      tseytin: Apply the Tseytin transformation to the logic before solving
      exhaustive: Generate exhaustive logical relationships between terms, instead of iteratively deepening relationships
      depth: Longest transitive relationship to generate. Only need log2(max-chain) to prevent cycles.
    """

    def __init__(
        self,
        verbose=False,
        debug=False,
        stats=False,
        quiet=False,
        tseytin=False,
        exhaustive=False,
        depth=1,
    ):
        self._verbose = verbose
        self._debug = debug
        self._stats = stats
        self._quiet = quiet
        self._tseytin = quiet
        self._exhaustive = exhaustive
        self._depth = depth

        self._opts = {
            "depth": depth,
            "tseytin": tseytin,
            "verbose": verbose,
            "exhaustive": exhaustive,
        }

    def enactability(self, *files):
        """
        Compute whether each protocol is enactable or not

        A protocol is enactable if there are any enactments that bind all of its public parameters, completing the protocol

        Note: Inherits flags from sat; see `bspl sat -h` for details
        """
        for P in load_protocols(files):
            reset_stats()
            e = is_enactable(P, **self._opts)
            print("  Enactable: ", bool(e))
            if self._verbose or self._stats:
                print("    stats: ", stats)
            if self._verbose or not e and not self._quiet:
                print_formula(logic.And(correct(P), enactability(P)))
            if e and self._verbose:
                pp.pprint(e)

    def liveness(self, *files):
        """
        Compute whether each protocol is live or not

        A protocol is live if every enactment is complete or can be extended to a complete enactment

        Note: Inherits flags from sat; see `bspl sat -h` for details
        """
        for protocol in load_protocols(files):
            reset_stats()
            e = is_enactable(protocol)
            violation = consistent(dead_end(protocol), **self._opts)
            print("  Live: ", e and not violation)
            if self._verbose or self._stats:
                print("    stats: ", stats)
            if violation and not self._quiet or self._verbose:
                print_formula(dead_end(protocol))
            if violation and not self._quiet:
                print("\n    Violation:")
                pp.pprint(violation)
                print()

    def safety(self, *files):
        """
        Compute whether or not every protocol is safe

        A protocol is safe if there are no enactments in which multiple roles bind the same parameter

        Note: Inherits flags from sat; see `bspl sat -h` for details
        """
        for protocol in load_protocols(files):
            reset_stats()
            expr = unsafe(protocol)
            violation = consistent(expr, **self._opts)
            print("  Safe: ", not violation)
            if self._verbose or self._stats:
                print("    stats: ", stats)
            if violation and not self._quiet or self._verbose:
                print_formula(expr)
            if violation and not self._quiet:
                print("\nViolation:")
                pp.pprint(violation)
                print()

    def atomicity(self, *files, indent=2):
        """
        Compute wheter or not a protocol is atomic

        A protocol is atomic if, when any of its components is initiated, the protocol itself can be completed
        This relationship is recursive; for a protocol to be atomic, all of its subprotocols must be atomic

        Note: Inherits flags from sat; see `bspl sat -h` for details
        """
        for protocol in load_protocols(files):
            reset_stats()
            a, formula = protocol.check_atomicity(self)
            print("  Atomic: ", not a)
            if self._verbose or self._stats:
                print("    stats: ", stats)
            if a and not self._quiet:
                print("\nViolation:")
                pp.pprint(a)
                formula = json.dumps(
                    formula, default=str, sort_keys=True, indent=indent
                )
                print(f"\nFormula: {formula}\n")


register_commands({"sat": SATCommands})
