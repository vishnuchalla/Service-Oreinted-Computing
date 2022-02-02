from .utils import merge
import inspect
import sys
import re
from types import ModuleType


class ProtoMod(ModuleType):
    def __setitem__(self, name, value):
        return self.__setattr__(name, value)

    def __getitem__(self, name):
        return self.__getattribute__(name)


def camelize(name):
    if re.match(r"[ -]", name):
        return "".join(map(lambda s: s.capitalize(), re.split(r"[ -]", name)))
    else:
        return name


class Specification:
    def __init__(self, protocols=None):
        self.protocols = {}  # name : protocol
        self.type = "specification"
        if protocols:
            self.add_protocols(protocols)

    def add_protocols(self, protocols=list()):
        # store protocol by name
        for p in protocols:
            self.protocols[p.name] = p

        for p in self.protocols.values():
            p.resolve_references(self)

    def export(self, protocol):
        p = self.protocols[protocol]
        pname = camelize(p.name)
        frm = inspect.stack()[1]
        module = ProtoMod(pname)
        for name, message in p.messages.items():
            module[camelize(name)] = message
        for name, role in p.roles.items():
            module[camelize(name)] = role
        module.protocol = p
        sys.modules[pname] = module
        p.module = module
        return p

    # @classmethod
    # def from_json(cls, protocols):
    #     return cls([Protocol.from_dict(p, self) for p in protocols])

    @property
    def messages(self):
        return set(m for p in self.protocols.values() for m in p.messages.values())


class Base:
    """Class containing elements common to protocols, messages, etc."""

    def __init__(self, name, parent, kind):
        self.raw_name = name.strip()
        self.parent = parent
        self.type = kind
        if type(parent) is Specification:
            self.spec = parent
            self.parent_protocol = None
        elif type(parent) is Protocol:
            self.spec = parent.spec
            self.parent_protocol = parent
        elif parent:
            self.spec = parent.spec
            self.parent_protocol = parent.parent_protocol

    @property
    def name(self):
        return self.raw_name

    # @classmethod
    # def from_dict(cls, data, parent=None):
    #     return cls(data["name"].strip(), parent, schema["type"])


class Role(Base):
    def __init__(self, name, parent=None):
        super().__init__(name, parent, "role")

    def messages(self, protocol=None):
        protocol = protocol or self.parent
        return {
            m.name: m
            for m in protocol.messages.values()
            if m.sender == self or m.recipient == self
        }

    def sent_messages(self, protocol):
        return [m for m in protocol.messages.values() if m.sender == self]


class Reference(Base):
    def __init__(self, name, parameters=None, parent=None):
        self.parameters = parameters  # list(Parameter)
        super().__init__(name, parent, "reference")

    def format(self, ref=True):
        return "{}({}, {})".format(
            self.name,
            ", ".join([r.name for r in self.roles]),
            ", ".join([p.format() for p in self.parameters]),
        )


class Protocol(Base):
    def __init__(
        self,
        name,
        roles=None,
        public_parameters=None,
        references=None,
        parent=None,
        private_parameters=None,
        type="protocol",
    ):
        super().__init__(name, parent, type)
        self.public_parameters = {}
        self.private_parameters = {}
        self.roles = {}
        self.references = {}
        Protocol.configure(
            self, roles, public_parameters, private_parameters, references
        )

    def configure(
        self,
        roles=None,
        public_parameters=None,
        private_parameters=None,
        references=None,
        parent=None,
    ):
        parent = self.parent = getattr(self, "parent", parent)
        if roles:
            for r in roles or []:
                if type(r) is Role:
                    self.roles[r.name] = r
                elif type(r) is str:
                    self.roles[r] = Role(r, self)
                else:
                    raise ("{} is unexpected type: {}".format(r, type(r)))
        if public_parameters:
            self.set_parameters(public_parameters)
        if private_parameters:
            self.private_parameters = {p.name: p for p in private_parameters}
            self.update()
        if references:
            self.references = {}
            name_counts = {}
            for r in references:
                if r.name in name_counts:
                    name_counts[r.name] += 1
                    r.idx = name_counts[r.name]
                else:
                    name_counts[r.name] = 1
                self.references[r.name] = r

    def set_parameters(self, parameters):
        self.public_parameters = {p.name: p for p in parameters}
        self.update()

    def update(self):
        "Recompute some basic parameter information"
        if hasattr(self, "private_parameters"):
            self.parameters = self.public_parameters.copy()
            self.parameters.update(self.private_parameters)
        else:
            self.parameters = self.public_parameters.copy()
        self.ins = self.adorned("in")
        self.outs = self.adorned("out")
        self.nils = self.adorned("nil")
        self.keys = self.get_keys()

    @property
    def all_parameters(self):
        return {p for m in self.messages.values() for p in m.parameters}

    def get_keys(self):
        return {
            p.name: p
            for p in self.parameters.values()
            if p.key
            or self.parent
            and self.parent.type == "protocol"
            and p.name in self.parent.parameters
            and self.parent.parameters[p.name].key
        }

    def adorned(self, adornment):
        "helper method for selecting parameters with a particular adornment"
        return {
            p.name for p in self.public_parameters.values() if p.adornment == adornment
        }

    @property
    def messages(self):
        if not hasattr(self, "_messages") or not self._messages:
            self._messages = {
                k: v for r in self.references.values() for k, v in r.messages.items()
            }
        return self._messages

    @property
    def is_entrypoint(self):
        "A protocol is an entry point if it does not have any \
        dependencies on sibling protocols"
        return not self.ins - self.parent.ins

    @property
    def entrypoints(self):
        return [m for m in self.messages.values() if m.is_entrypoint]

    def format(self, ref=False):
        if ref:
            return "{}({}, {})".format(
                self.name,
                ", ".join(self.roles),
                ", ".join([p.format() for p in self.public_parameters.values()]),
            )
        else:
            return """{} {{
  roles {}
  parameters {}
{}
  {}
}}""".format(
                self.name,
                ", ".join(self.roles.keys()),
                ", ".join([p.format() for p in self.public_parameters.values()]),
                "  private " + ", ".join([p for p in self.private_parameters]) + "\n"
                if self.private_parameters
                else "",
                "\n  ".join([r.format(ref=True) for r in self.references.values()]),
            )

    def to_dict(self):
        data = {
            "name": self.name,
            "type": self.type,
            "parameters": [p for p in self.public_parameters.keys()],
            "keys": [k for k in self.keys],
            "ins": [i for i in self.ins],
            "outs": [i for i in self.outs],
            "nils": [i for i in self.nils],
        }
        if self.roles:
            data["roles"] = [r for r in self.roles.keys()]
        # should we output references, or just flatten to messages?
        if self.references:
            data["messages"] = {r.name: r.to_dict() for r in self.messages.values()}
        return data

    def projection(protocol, role):
        references = [
            r
            for r in protocol.references.values()
            if role in r.roles.values()
            or r.type == "message"
            and (role == r.sender or role == r.recipient)
        ]

        messages = [m for m in references if m.type == "message"]

        if len(messages) > 0:
            return Protocol(
                protocol.name,
                public_parameters=[
                    p
                    for p in protocol.public_parameters.values()
                    if any(p.name in m.parameters for m in messages)
                ],
                private_parameters=[
                    p
                    for p in protocol.private_parameters.values()
                    if any(p.name in m.parameters for m in messages)
                ],
                roles=[
                    r
                    for r in protocol.roles.values()
                    if any(
                        m.sender.name == r.name or m.recipient.name == r.name
                        for m in messages
                    )
                ],
                references=[r for r in references],
                parent=protocol.parent,
            )

    def resolve_references(self, spec):
        refs = {}
        for r in self.references.values():
            if r.type == "protocol" or r.type == "reference":
                protocol = spec.protocols.get(r.name)
                if not protocol:
                    raise LookupError(f"Undefined protocol {r.name}")
                refs[r.name] = protocol.instance(spec, self, r)
            elif r.type == "message":
                refs[r.name] = r.instance(self)
            else:
                print(f"Unexpected reference type: {r.type}")
        self.references = refs

    def instance(self, spec, parent, reference):
        p = Protocol(
            self.name,
            self.roles.values(),
            public_parameters=self.public_parameters.values(),
            private_parameters=self.private_parameters.values(),
            references=self.references.values(),
            parent=parent,
        )
        for i, r in enumerate(self.roles.values()):
            # print(f"{reference}[{i}]: {r}")
            p.roles[r.name] = parent.roles.get(reference.parameters[i].name)
        for i, par in enumerate(self.public_parameters.values()):
            ref_name = reference.parameters[i + len(p.roles)].name
            if ref_name not in parent.parameters:
                raise LookupError(
                    f"Parameter {ref_name} from reference {reference.name} not declared in parent {parent.name}"
                )
            p.public_parameters[par.name] = parent.parameters[ref_name]
        p.resolve_references(spec)
        return p

    def find_schema(self, payload=None, name=None, to=None):
        if name:
            return self.messages[name]

        for schema in self.messages.values():
            if to and schema.recipient is not to:
                continue
            # find schema with exactly the same parameters (except nils, which should not be bound)
            if (
                not set(schema.ins)
                .union(schema.outs)
                .symmetric_difference(payload.keys())
            ):
                return schema

    def determines(self, a, b):
        """
        a determines b if a is 'in' in all messages b is 'out'
        Expects a and b as str names
        """
        sources = {m for m in self.messages.values() if b in m.outs}
        for m in sources:
            if a not in m.ins:
                return False
        return True

    def ordered_params(self):
        return sorted(self.parameters.values())


class Message(Protocol):
    def __init__(
        self, name, sender=None, recipient=None, parameters=None, parent=None, idx=1
    ):
        self.idx = idx
        if sender and recipient:
            super().__init__(
                name, roles=[sender, recipient], parent=parent, type="message"
            )
            self.configure(sender, recipient, parameters, parent)
        else:
            super().__init__(name, parent=parent, type="message")

        self.msg = self

    def configure(self, sender=None, recipient=None, parameters=None, parent=None):
        parent = parent or getattr(self, "parent", None)
        if parent:
            self.sender = parent.roles.get(sender) or parent.roles.get(
                getattr(sender, "name", None)
            )
            self.recipient = parent.roles.get(recipient) or parent.roles.get(
                getattr(recipient, "name", None)
            )
            for p in parameters or []:
                if p.name not in parent.parameters:
                    raise LookupError(
                        f"Undeclared parameter {p.name} in {self.type} {self.name}"
                    )
                elif parent.parameters[p.name].key:
                    p.key = True
        else:
            self.sender = sender if isinstance(sender, Role) else Role(sender, self)
            self.recipient = (
                recipient if isinstance(recipient, Role) else Role(recipient, self)
            )

        if not self.sender:
            raise LookupError("Role not found", sender, self.name, parent)
        if not self.recipient:
            raise LookupError("Role not found", recipient, self.name, parent)

        super().configure(
            roles=[self.sender, self.recipient],
            public_parameters=parameters,
            parent=parent,
        )

    @property
    def qualified_name(self):
        return self.parent.name + "/" + self.name

    @property
    def name(self):
        return self.raw_name + (str(self.idx) if self.idx > 1 else "")

    def __repr__(self):
        return self.name
        return "Message('{}', {}, {}, {})".format(
            self.name,
            self.sender.name,
            self.recipient.name,
            [p.format() for p in self.parameters.values()],
        )

    def instance(self, parent):
        msg = Message(
            self.raw_name,
            self.sender,
            self.recipient,
            self.parameters.values(),
            idx=self.idx,
            parent=parent,
        )

        # propagate parameters from parent protocol
        for i, par in enumerate(self.public_parameters.values()):
            # Make a new parameter, to preserve message adornments
            parent_parameter = parent.parameters[par.name]
            msg.public_parameters[par.name] = Parameter(
                parent_parameter.raw_name, par.adornment, par.key, parent=self
            )

        return msg

    @property
    def messages(self):
        return {self.name: self}

    def format(self, ref=False):
        return "{} -> {}: {}[{}]".format(
            self.sender.name,
            self.recipient.name,
            self.name,
            ", ".join([p.format() for p in self.parameters.values()]),
        )

    def to_dict(self):
        data = super(Message, self).to_dict()
        data["to"] = self.recipient.name
        data["from"] = self.sender.name
        return data

    @property
    def contents(self):
        return [
            p for p in self.parameters.values() if p.adornment in ["out", "any", "in"]
        ]

    def acknowledgment(self):
        name = "@" + self.raw_name
        if name in self.parent.messages:
            return self.parent.messages[name]
        else:
            m = Message(
                "@" + self.raw_name, self.recipient, self.sender, parent=self.parent
            )
            m.set_parameters(
                [Parameter(k, "in", key=True, parent=m) for k in self.keys]
                + [Parameter("$ack", "out", key=True, parent=m)]
            )
            return m

    def validate(self, payload):
        return set(payload) == set(self.parameters.keys())

    def disabled_by(self, parameters):
        """
        Return true if parameters do not interfere with outs or nils

        parameters: set of parameter names
        """
        return self.outs.union(self.nils).intersection(parameters)

    def zip_params(self, *params):
        """Construct a payload from a list of parameter values"""
        return dict(
            zip(
                [
                    p
                    for p in self.public_parameters.keys()
                    if self.public_parameters[p].adornment in ("in", "out")
                ],
                params,
            )
        )

    def order_params(self, payload, default=None):
        """Yield each parameter from payload in the order the parameters appear
        in the message schema
        """
        for p in self.public_parameters.keys():
            if p in payload:
                yield payload[p]
            elif self.public_parameters[p].adornment != "nil":
                if not default:
                    yield None
                elif callable(default):
                    yield default()
                else:
                    yield default


class Parameter(Base):
    def __init__(self, name, adornment, key=False, parent=None):
        self.adornment = adornment
        self.key = key
        super().__init__(name, parent, "parameter")

    def format(self, adornment=True):
        if adornment:
            base = "{} {}".format(self.adornment, self.name)
        else:
            base = "{}".format(self.name)

        if self.key:
            return base + " key"
        else:
            return base

    def __lt__(self, other):
        return self.parent_protocol.determines(self.name, other.name)
