from ..bspl import load_file
from . import paths
from .paths import (
    key_sets,
    UoD,
    all_paths,
    possibilities,
    sources,
    known,
)
import sys
from ..commands import register_commands


def handle_refinement(path, Q, P, verbose=False):
    """
    Given a specification file and protocol names Q and P, check whether Q refines P

    Args:
      path: File containing protocols
      Q: Name of protocol that should refine P
      P: Name of protocol that should be refined by Q
      verbose: Print more details
    """
    spec = load_file(path)
    Q = spec.protocols[Q]
    P = spec.protocols[P]

    result = refines(UoD(), P.public_parameters.keys(), Q, P, verbose=verbose)
    if result["ok"] == True:
        print("  {} Refines {}".format(Q.name, P.name))
        return True
    else:
        print(result)
        return False


register_commands({"refinement": handle_refinement})


def subsumes(U, params, a, b, verbose=False):
    """Path a subsumes path b"""
    if verbose:
        print("path a: ", a)
        print("path b: ", b)
    for p in params:
        sources_a = sources(a, p)
        sources_b = sources(b, p)
        if sources_a != sources_b:
            if verbose:
                print("sources don't match: {} != {}".format(sources_a, sources_b))
            return False

    for r in U.roles:
        for keys in key_sets(a):
            if verbose:
                print(keys)
            known_a = known(a, keys, r).intersection(params)
            known_b = known(b, keys, r).intersection(params)
            if known_a != known_b:
                if verbose:
                    print(
                        "{}'s knowledge doesn't match: {} != {}".format(
                            r.name, known_a, known_b
                        )
                    )
                return False
            elif verbose:
                print("{} knows: {}".format(r.name, known_a))
    if len(b) > 1:
        b2 = b[:-1]
        return any(subsumes(U, params, a[:end], b2, verbose) for end in range(len(a)))
    else:
        return True


def refines(U, params, Q, P, verbose=False):
    """Check that Q refines P"""

    U_Q = U + UoD.from_protocol(Q)
    U_P = U + UoD.from_protocol(P)

    p_keys = set()
    q_keys = set()
    for m in U_P.messages:
        p_keys.update(m.keys)
    for m in U_Q.messages:
        q_keys.update(m.keys)
    if not p_keys >= q_keys:
        return {
            "ok": False,
            "p_keys": p_keys,
            "q_keys": q_keys,
            "diff": p_keys.symmetric_difference(q_keys),
            "reason": "{} uses keys that do not appear in {}".format(Q.name, P.name),
        }

    paths_Q = all_paths(U_Q, verbose=verbose, reduction=False)
    paths_P = all_paths(U_P, verbose=verbose, reduction=False)

    longest_Q = longest_P = []
    for q in paths_Q:
        if len(q) > len(longest_Q):
            longest_Q = q
    for p in paths_P:
        if len(p) > len(longest_P):
            longest_P = p

    if verbose:
        print("{}: {} paths, longest path: {}".format(P.name, len(paths_P), longest_P))
        # print(paths_P)
        print("{}: {} paths, longest path: {}".format(Q.name, len(paths_Q), longest_Q))
        # print(paths_Q)

    checked = 0
    for q in paths_Q:
        # print("q: ", q)
        match = None
        for p in paths_P:
            # print("p: ", p)
            if subsumes(U_P, params, q, p, False):
                match = p
                # print("p branches: ", branches(U_P, p))
                # print("q branches: ", branches(U_Q, q))
                if not possibilities(U_P, p) or possibilities(U_Q, q):
                    break  # only try again if p has branches but q doesn't
        if match == None:
            return {
                "ok": False,
                "path": q,
                "reason": "{} has path that does not subsume any path in {}".format(
                    Q.name, P.name
                ),
            }
        if possibilities(U_P, match) and not possibilities(U_Q, q):
            # subsumes(U_P, params, q, match, True)
            return {
                "ok": False,
                "path": q,
                "match": match,
                "reason": "path in {} has branches, but path in {} does not".format(
                    P.name, Q.name
                ),
            }
        checked += 1
        if verbose:
            print(
                "\r checked: {} of {} paths ({:.1f}%)".format(
                    checked, len(paths_Q), checked / len(paths_Q) * 100
                ),
                end="",
            )
    if verbose:
        print()
    return {"ok": True}
