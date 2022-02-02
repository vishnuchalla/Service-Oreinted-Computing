from ..protocol import Message, Role, Parameter
from pprint import pformat
from ttictoc import Timer
from ..commands import register_commands
from ..bspl import load_protocols


def empty_path():
    """The empty path is a list with no message instances"""
    return tuple()


External = Role("*External*")


class Emission:
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return f"{self.sender.name}!{self.msg.name}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.msg == other.msg
        else:
            return False

    def __hash__(self):
        return (self.msg).__hash__()

    def __getattr__(self, attr):
        return getattr(self.msg, attr)


def key_sets(path):
    keys = set()
    for i in path:
        keys.add(tuple(i.msg.keys))
    return keys


def known(path, keys, R):
    """Compute the set of parameters observed by role R after enacting path"""
    time = 0
    k = set()
    for instance in path:
        if set(instance.msg.parameters).intersection(set(keys)) and (
            isinstance(instance, Emission)
            and instance.sender.name == R.name
            or (isinstance(instance, Reception) and instance.recipient.name == R.name)
        ):
            k.update(instance.ins)
            k.update(instance.outs)
        time += 1
    return k


def sources(path, p):
    """The set of all roles that produce p as an out parameter in path"""
    return set(i.msg.sender.name for i in path if p in i.msg.outs)


def viable(path, msg):
    msg_count = len([i.msg for i in path if i.msg == msg])
    if (
        not msg.ins.union(msg.nils).symmetric_difference(
            {p.name for p in msg.parameters.values()}
        )
        and msg_count > 0
    ):
        # only allow one copy of an all "in"/"nil" message
        # print("Only one copy of all in message allowed")
        return False
    if msg.sender == External:
        # only send external messages if they would contribute
        k = known(path, (), msg.recipient)
        if not k.issuperset(msg.ins):
            return True
        else:
            print("Only send external messages if they would contribute")
            return False
    out_keys = set(msg.keys).intersection(msg.outs)
    # print(msg.name)
    # print(msg.keys, msg.outs, out_keys)
    # print(msg.outs)
    # print(out_keys)
    if out_keys and all(sources(path, p) for p in out_keys):
        # don't allow multiple key bindings in the same path; they're different enactments
        # print("Don't allow multiple key bindings on the same path; they're different enactments")
        return False
    k = known(path, msg.keys, msg.sender)
    return k.issuperset(msg.ins) and k.isdisjoint(msg.outs) and k.isdisjoint(msg.nils)


def disables(a, b):
    "Return true if message a directly disables message b"

    if isinstance(a, Emission) and isinstance(b, Emission) and a.sender == b.sender:
        for p in a.outs:
            # out disables out or nil
            if p in b.parameters:
                if b.parameters[p].adornment in ["out", "nil"]:
                    return True

    if isinstance(a, Reception) and isinstance(b, Emission) and a.recipient == b.sender:
        for p in a.outs.union(a.ins):
            # out or in disables out or nil
            if p in b.parameters:
                if b.parameters[p].adornment in ["out", "nil"]:
                    return True


def enables(a, b):
    "Return true if message a directly enables message b"
    if isinstance(a, Emission) and isinstance(b, Reception) and a.msg == b.msg:
        # emissions enable their reception
        return True

    if (
        not isinstance(b, Emission)
        or isinstance(a, Emission)
        and a.sender != b.sender
        or isinstance(a, Reception)
        and a.recipient != b.sender
    ):
        # only emissions can be enabled by other messages, and only at the sender
        return False

    if not disables(a, b):
        # out enables in
        for p in a.outs:
            if p in b.parameters:
                if b.parameters[p].adornment == "in":
                    return True


class Tangle:
    "Graph representation of entanglements between messages"

    def __init__(self, messages, roles, **kwargs):
        default_kwargs = {"debug": False}
        kwargs = {**default_kwargs, **kwargs}
        self.emissions = {Emission(m) for m in messages}
        self.receptions = {Reception(e) for e in self.emissions}
        self.events = self.emissions.union(self.receptions)

        # sources for parameters, for computing endowment
        self.sources = {}
        for R in roles:
            self.sources[R] = {}
            for e in self.events:
                if (
                    isinstance(e, Emission)
                    and e.sender != R
                    or isinstance(e, Reception)
                    and e.recipient != R
                ):
                    continue

                for p in e.outs:
                    if p not in self.sources[R]:
                        self.sources[R][p] = [e]
                    else:
                        self.sources[R][p].append(e)

        # track messages that are the sole source of a given parameter
        self.source = {}
        for R in roles:
            self.source[R] = {
                p: ms[0] for p, ms in self.sources[R].items() if len(ms) == 1
            }

        # a endows b if a is the sole source of an 'in' parameter of b
        self.endows = {e: {Reception(e)} for e in self.emissions}
        for b in self.emissions:
            for p in b.ins:
                a = self.source[b.sender].get(p)
                if not a:
                    continue
                if a in self.endows:
                    self.endows[a].add(b)
                else:
                    self.endows[a] = {b}

        # propagate endowment, since it is transitive
        def propagate(a, b):
            self.endows[a].update(self.endows.get(b, []))
            for c in self.endows.get(b, []).copy():
                propagate(a, c)

        for a in self.endows:
            propagate(a, a)

        if kwargs["debug"]:
            print(f"endows: {pformat(self.endows)}")

        # initialize graph with direct enable and disablements, O(m^2)
        self.enables = {
            a: {b for b in self.events if a != b and enables(a, b)} for a in self.events
        }
        self.disables = {
            a: {
                b
                for b in self.events
                if a != b and not a in self.endows.get(b, []) and disables(a, b)
            }
            for a in self.events
        }

        if kwargs["debug"]:
            print(f"disables: {pformat(self.disables)}")
            print(f"enables: {pformat(self.enables)}")

        # propagate enablements; a |- b & b |- c => a |- c
        def enablees(m):
            es = self.enables[m]
            return es.union(*[enablees(b) for b in es])

        for m, es in self.enables.items():
            es.update(enablees(m))

        # compute entanglements:
        # a -|| c if:
        #  1. a does not endow c
        #  2. a -| c or a -| b and c |- b
        self.tangles = {
            a: self.disables[a].union(
                {
                    c
                    for c in self.enables
                    if c not in self.endows.get(a, [])
                    and self.enables[c].intersection(self.disables[a])
                }
            )
            for a in self.events
        }

        # initialize incompatibility graph
        self.incompatible = {}
        for e in self.events:
            self.incompatible[e] = set()

        # a and b are incompatible if
        #  1. one is an emission
        #  2. one tangles with the other
        for a in self.tangles:
            for b in self.tangles[a]:
                if isinstance(a, Emission):
                    if (
                        isinstance(b, Emission)
                        and a.sender == b.sender
                        or isinstance(b, Reception)
                        and a.sender == b.recipient
                    ):
                        self.incompatible[a].add(b)
                        self.incompatible[b].add(a)
                elif isinstance(a, Reception):
                    if (
                        isinstance(b, Emission)
                        and a.recipient == b.sender
                        or isinstance(b, Reception)
                        and a.recipient == b.recipient
                    ):
                        self.incompatible[a].add(b)
                        self.incompatible[b].add(a)

    def safe(self, possibilities, path):
        ps = possibilities.copy()
        risky = {
            e
            for e in self.events
            if self.disables[e].difference(path)
            or any(e in self.disables[b] for b in self.events)
        }
        return ps.difference(risky)


class UoD:
    def __init__(self, messages=set(), roles={}, **kwargs):
        self.messages = set(messages)
        self.roles = set(roles)
        self.tangle = Tangle(messages, roles, **kwargs)

    @staticmethod
    def from_protocol(protocol, **kwargs):
        if not protocol.ins.union(protocol.nils) or not kwargs.get("external", True):
            return UoD(
                list(protocol.messages.values()), protocol.roles.values(), **kwargs
            )
        else:
            dependencies = {}
            for r in protocol.roles.values():
                if r.name is External.name:
                    continue
                keys = protocol.ins.intersection(protocol.keys)
                # generate messages that provide p to each sender
                msg = Message(
                    "external->{r.name}",
                    External,
                    r,
                    [Parameter(k, "in", True, parent=protocol) for k in keys]
                    + [
                        Parameter(p, "in", parent=protocol)
                        for p in protocol.ins.difference(keys)
                    ],
                )
                dependencies[r.name] = msg
            # hmmm; probably shouldn't modify protocol...
            protocol.roles[External.name] = External
            uod = UoD(
                list(protocol.messages.values()) + list(dependencies.values()),
                protocol.roles.values(),
                **kwargs,
            )
            return uod

    def __add__(self, other):
        return UoD(self.messages.union(other.messages), self.roles.union(other.roles))


class Reception:
    def __init__(self, emission):
        self.emission = emission
        self.msg = emission.msg

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.msg == other.msg
        else:
            return False

    def __hash__(self):
        return hash(self.msg)

    def __getattr__(self, attr):
        return getattr(self.emission, attr)

    def __repr__(self):
        return f"{self.recipient.name}?{self.msg.name}"


def unreceived(path):
    sent = set(e for e in path if isinstance(e, Emission))
    received = set(r.emission for r in path if isinstance(r, Reception))
    return sent.difference(received)


def possibilities(U, path):
    b = set()
    for msg in U.messages:
        if viable(path, msg):
            # default messages to unreceived, progressively receive them later
            inst = Emission(msg)
            b.add(inst)
    ps = b.union(Reception(e) for e in unreceived(path))
    return ps


def any_unreceived(path):
    return len(unreceived(path)) > 0


class Color(set):
    def __hash__(self):
        return id(self)


def partition(graph, ps):
    """
    Partition a set of possibilities into incompatible subsets.
      graph: a dictionary from a vertex to its set of neighbors
      ps: a list of possibilities"""

    # alias graph to neighbors for readability
    neighbors = graph

    def degree(m):
        return len(neighbors[m])

    # Sort vertices by degree in descending order
    vs = sorted(ps, key=degree, reverse=True)

    parts = set()
    coloring = {}
    for vertex in vs:
        # Assign a color to each vertex that isn’t assigned to its neighbors
        options = parts.difference({coloring.get(n) for n in neighbors[vertex]})

        # generate a new color if necessary
        if not len(options):
            color = Color()
            parts.add(color)
        elif len(options) > 1:
            # Choose a color that
            #  (1) has the highest cardinality (number of vertices)
            max_cardinality = max(len(c) for c in parts)
            options = {o for o in options if len(o) == max_cardinality}

            #  (2) within such, the color whose vertex of highest degree has the smallest degree
            if len(options) > 1:

                def max_degree(color):
                    return max(degree(v) for v in color)

                min_max = min(max_degree(c) for c in parts)
                options = {o for o in options if max_degree(o) == min_max}

            # choose color from options (randomly?)
            color = next(o for o in options)
        else:
            color = next(o for o in options)

        # color vertex
        color.add(vertex)
        coloring[vertex] = color

    return parts


def extensions(U, path, **kwargs):
    default_kwargs = {
        "by_degree": False,
        "reduction": True,
        "safe": True,
        "debug": False,
    }
    kwargs = {**default_kwargs, **kwargs}
    ps = possibilities(U, path)
    safe_events = U.tangle.safe(ps, path)
    # default to selecting branches by message name
    def sort(p):
        return p.name

    if kwargs["by_degree"]:
        # select events by degree instead
        def sort(p):
            return len(U.tangle.incompatible[p])

    if not kwargs["reduction"]:
        # all the possibilities
        xs = {path + (p,) for p in ps}
    elif not kwargs["safe"] and safe_events:
        # expand all non-disabling events first
        xs = {path + (min(safe_events, key=sort),)}
    else:
        parts = partition(U.tangle.incompatible, ps)
        if kwargs["debug"]:
            print(f"parts: {parts}")
        branches = {min(p, key=sort) for p in parts}
        xs = {path + (b,) for b in branches}
    return xs


def max_paths(U):
    max_paths = []
    new_paths = [empty_path()]
    while len(new_paths):
        p = new_paths.pop()
        xs = extensions(U, p)
        if xs:
            new_paths.extend(xs)
        else:
            max_paths.insert(len(max_paths), p)
    return max_paths


def liveness(protocol, **kwargs):
    default_kwargs = {"debug": False, "verbose": False}
    kwargs = {**default_kwargs, **kwargs}
    t = Timer()
    t.start()
    U = UoD.from_protocol(protocol, **kwargs)
    if kwargs["debug"]:
        print(f"incompatibilities: {pformat(U.tangle.incompatible)}")
    new_paths = [empty_path()]
    checked = 0
    max_paths = 0
    while len(new_paths):
        p = new_paths.pop()
        if kwargs["debug"]:
            print(p)
        checked += 1
        xs = extensions(U, p, **kwargs)
        if xs:
            new_paths.extend(xs)
        else:
            max_paths += 1
            if kwargs["verbose"] and not kwargs["debug"]:
                print(p)
            if total_knowledge(U, p).intersection(protocol.outs) < protocol.outs:
                return {
                    "live": False,
                    "reason": "Found path that does not extend to completion",
                    "path": p,
                    "checked": checked,
                    "maximal paths": max_paths,
                    "elapsed": t.stop(),
                }
    return {
        "live": True,
        "checked": checked,
        "maximal paths": max_paths,
        "elapsed": t.stop(),
    }


def safety(protocol, **kwargs):
    default_kwargs = {"debug": False, "verbose": False}
    kwargs = {**default_kwargs, **kwargs}
    t = Timer()
    t.start()
    U = UoD.from_protocol(protocol)
    if kwargs["debug"]:
        print(f"incompatibilities: {pformat(U.tangle.incompatible)}")
    parameters = {p for m in protocol.messages.values() for p in m.outs}
    new_paths = [empty_path()]
    checked = 0
    max_paths = 0
    while len(new_paths):
        path = new_paths.pop()
        if kwargs["debug"]:
            print(path)
        checked += 1
        xs = extensions(U, path, **kwargs)
        if xs:
            new_paths.extend(xs)
        else:
            max_paths += 1
            if kwargs["verbose"] and not kwargs["debug"]:
                print(path)

        for p in parameters:
            if len(sources(path, p)) > 1:
                return {
                    "safe": False,
                    "reason": "Found parameter with multiple sources in a path",
                    "path": path,
                    "parameter": p,
                    "checked": checked,
                    "maximal paths": max_paths,
                    "elapsed": t.stop(),
                }
    return {
        "safe": True,
        "checked": checked,
        "maximal paths": max_paths,
        "elapsed": t.stop(),
    }


def total_knowledge(U, path):
    k = set()
    for r in U.roles:
        for keys in key_sets(path):
            k.update(known(path, keys, r))
    return k


def all_paths(U, **kwargs):
    default_kwargs = {"debug": False, "verbose": False}
    kwargs = {**default_kwargs, **kwargs}
    t = Timer()
    t.start()
    paths = set()
    new_paths = [empty_path()]
    longest_path = 0
    max_paths = 0
    if kwargs["debug"]:
        print(f"incompatible: {pformat(U.tangle.incompatible)}")
    while new_paths:
        p = new_paths.pop()
        if kwargs["debug"]:
            print(p)
        if len(p) > longest_path:
            longest_path = len(p)
        if len(p) > len(U.messages) * 2:
            print("Path too long: ", p)
            exit(1)
        xs = extensions(U, p, **kwargs)
        if xs:
            new_paths.extend(xs)
        else:
            max_paths += 1
            if kwargs["verbose"] and not kwargs["debug"]:
                print(p)

        paths.add(p)  # add path to paths even if it has unreceived messages
    print(
        f"{len(paths)} paths, longest path: {longest_path}, maximal paths: {max_paths}, elapsed: {t.stop()}"
    )
    return paths


def handle_all_paths(
    *files, debug=False, verbose=False, external=False, safe=True, reduction=False
):
    """
    Compute all paths for each protocol

    By default, this does *not* use partial-order reduction, but it can be enabled via the --reduction flag.

    Args:
      files: Paths to specification files containing one or more protocols
      verbose: Enable detailed output
      debug: Print debugging information
      external: Enable external source information
      reduction: Enable reduction
      safe: If reduction is enabled, use heuristic to avoid branching on events assumed to be safe (default True); use --nosafe to disable
    """
    for protocol in load_protocols(files):
        print(f"{protocol.name} ({protocol.path}): ")
        U = UoD.from_protocol(protocol)
        all_paths(
            U,
            verbose=verbose,
            debug=debug,
            external=external,
            safe=safe,
            reduction=reduction,
        )


def handle_liveness(
    *files, verbose=False, debug=False, external=False, safe=True, reduction=True
):
    """
    Compute whether each protocol is live, using path simulation

    By default, this uses tableau-based partial order reduction to minimize the number of paths considered.

    Args:
      files: Paths to specification files containing one or more protocols
      verbose: Enable detailed output
      debug: Print debugging information
      external: Enable external source information
      reduction: Enable reduction (default True); use --noreduction to disable
      safe: If reduction is enabled, use heuristic to avoid branching on events assumed to be safe (default True); use --nosafe to disable
    """
    for protocol in load_protocols(files):
        print(f"{protocol.name} ({protocol.path}): ")
        print(
            liveness(
                protocol,
                verbose=verbose,
                debug=debug,
                external=external,
                safe=safe,
                reduction=reduction,
            )
        )


def handle_safety(
    *files, verbose=False, debug=False, external=True, safe=True, reduction=True
):
    """
    Compute whether each protocol is safe, using path simulation

    By default, this uses tableau-based partial order reduction to minimize the number of paths considered.

    Args:
      files: Paths to specification files containing one or more protocols
      verbose: Enable detailed output
      debug: Print debugging information
      external: Enable external source information (default True); use --noexternal to disable
      reduction: Enable reduction (default True); use --noreduction to disable
      safe: If reduction is enabled, use heuristic to avoid branching on events assumed to be safe (default True); use --nosafe to disable
    """
    for protocol in load_protocols(files):
        print(f"{protocol.name} ({protocol.path}): ")
        print(
            safety(
                protocol,
                verbose=verbose,
                debug=debug,
                external=external,
                safe=safe,
                reduction=reduction,
            )
        )


register_commands(
    {
        "safety": handle_safety,
        "liveness": handle_liveness,
        "all-paths": handle_all_paths,
    }
)
