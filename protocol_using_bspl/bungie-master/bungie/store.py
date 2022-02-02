import logging
import itertools

logger = logging.getLogger("bungie")


def get_key(schema, payload):
    # schema.keys should be ordered, or sorted for consistency
    return ",".join(k + ":" + str(payload[k]) for k in schema.keys)


class Message:
    schema = None
    payload = {}
    acknowledged = False
    dest = None
    adapter = None
    meta = {}
    key = None

    def __init__(self, schema, payload, acknowledged=False, dest=None, adapter=None):
        self.schema = schema
        self.payload = payload
        self.acknowledged = acknowledged
        self.dest = dest
        self.adapter = adapter
        self.meta = {}

    @property
    def key(self):
        return get_key(self.schema, self.payload)

    def __repr__(self):
        payload = ",".join("{0}={1!r}".format(k, v) for k, v in self.payload.items())
        return f"{self.schema.name}({payload})"

    def __eq__(self, other):
        return self.payload == other.payload and self.schema == other.schema

    def __hash__(self):
        return hash(self.schema.qualified_name + self.key)

    def __getitem__(self, name):
        return self.payload[name]

    def __setitem__(self, name, value):
        if name not in self.schema.parameters:
            raise Exception(f"Parameter {name} is not in schema {self.schema}")
        adornment = self.schema.parameters[name].adornment
        if adornment == "out":
            self.payload[name] = value
            return value
        else:
            raise Exception(f"Parameter {name} is {adornment}, not out")

    def bind(self, **kwargs):
        for k, v in kwargs.items():
            self[k] = v
        return self

    def instance(self, **kwargs):
        """
        Return new instance of message, binding new parameters from kwargs
        """
        return self.schema(**self.payload).bind(**kwargs)

    def keys_match(self, other):
        return all(
            self.payload[k] == other.payload[k]
            for k in self.schema.keys
            if k in other.schema.parameters
        )

    def keys(self):
        return self.payload.keys()

    def project_key(self, schema):
        """Give the subset of this instance's keys that match the provided schema, in the order of the provided schema"""
        key = []
        # use ordering from other schema
        for k in schema.keys:
            if k in self.schema.keys:
                key.append(k)
        return ",".join(k + ":" + str(self.payload[k]) for k in key)

    def send(self):
        self.adapter.send(self)


class Context:
    def __init__(self, parent=None):
        self.subcontexts = {}
        self._bindings = {}
        self._messages = {}
        self.parent = parent

    def add(self, message):
        self._bindings.update(message.payload)
        self._messages[message.schema] = message

    def clear(self):
        """Remove all content of the context"""
        self.__init__(self.parent)

    @property
    def bindings(self):
        """Return all parameters bound directly in this context or its ancestors"""
        # may not be efficient enough, since it collects all of the
        # bindings every time it's accessed
        if self.parent:
            return {**self.parent.bindings, **self._bindings}
        else:
            return self._bindings.copy()

    def _all_bindings(self):
        """
        Return all bindings accessible from a context - including all bindings from subcontexts
        """
        bs = {}
        for p in self.subcontexts:
            bs[p] = self.subcontexts[p].keys()
            for sub in self.subcontexts[p].values():
                bs.update(**{k: v for k, v in sub.all_bindings.items() if k != p})
        return bs

    @property
    def all_bindings(self):
        return {**{k: [v] for k, v in self.bindings.items()}, **self._all_bindings()}

    @property
    def messages(self):
        if self.parent:
            yield from self.parent.messages
        yield from self._messages.values()

    def _all_messages(self):
        yield from self._messages.values()
        for p in self.subcontexts:
            for sub in self.subcontexts[p].values():
                yield from sub._all_messages()

    @property
    def all_messages(self):
        if self.parent:
            return set(itertools.chain(self.parent.messages, self._all_messages()))
        else:
            return set(self._all_messages())

    def __repr__(self):
        return f"Context(bindings={self.bindings},messages={[m for m in self.messages]},subcontexts={self.subcontexts})"

    def instance(self, schema):
        payload = {}
        for k in schema.parameters:
            payload[k] = self.bindings[k]
        return Message(schema, payload)

    def __getitem__(self, key):
        return self.subcontexts[key]

    def __setitem__(self, key, value):
        self.subcontexts[key] = value
        return value

    def __contains__(self, key):
        return key in self.subcontexts

    def keys(self):
        return self.subcontexts.keys()

    def flatten_subs(self):
        for p in self.subcontexts:
            for v in self.subcontexts[p]:
                yield self.subcontexts[p][v]

    def flatten(self):
        yield self
        yield from self.flatten_subs()


class Store:
    def __init__(self):
        # message indexes

        # recursive (key -> value -> context -> subkey -> value -> subcontext...)
        self.contexts = Context()

    @property
    def messages(self):
        return self.contexts.all_messages

    def find_context(self, **params):
        """Find context whose keys match params (ignoring extra parameters)"""

        def step(context):
            for k in set(context.keys()).intersection(params.keys()):
                # assume only one
                return context[k].get(params[k])

        context = self.contexts
        while True:
            new_context = step(context)
            if new_context:
                context = new_context
            else:
                break
        return context

    def matching_contexts(self, **params):
        """Find contexts that either have the same bindings, or don't have the parameter"""

        context = self.find_context(**params)

        if len(context.subcontexts):
            return [
                c
                for c in context.flatten()
                if all(
                    c.bindings.get(p) == params[p] or p not in c.bindings
                    for p in params
                )
            ]
        else:
            return [context]

    def check_integrity(self, message, context=None):
        """
        Make sure payload can be received.

        Each message in context should have the same keys.
        Returns true if the parameters are consistent with all messages in the matching context.
        """
        context = context or self.find_context(**message.payload)
        result = all(
            message.payload[p] == context.bindings[p]
            for p in message.payload
            if p in context.bindings
        )
        return result

    def check_outs(self, schema, context):
        """
        Make sure none of the outs have been previous bound to a different value.
        Only use this check if the message is being sent.
        Assumes message is not a duplicate.
        """
        # context may be parent, if there are no matches; possibly even the root
        return not any(p in context.bindings for p in schema.outs)

    def check_nils(self, schema, context):
        """
        Make sure none of the nils are bound.
        Only use this check if the message is being sent.
        """
        # context may be parent, if there are no matches; possibly even the root
        return not any(p in context.bindings for p in schema.nils)

    def check_dependencies(self, message, context):
        """
        Make sure that all 'in' parameters are bound and matched by some message in the history
        """
        return not any(
            # aggregate across subcontexts
            # permits 'lifting' parameters into a parent context
            message.payload[p] not in context.all_bindings.get(p, [])
            for p in message.schema.ins
        )

    def check_emissions(self, messages, use_context=None):
        # message assumed not to be duplicate; otherwise recheck unnecessary

        parameters = {}
        for message in messages:
            context = use_context or self.find_context(**message.payload)
            if not self.check_outs(message.schema, context):
                logger.info(
                    f"Failed {message.schema.name} out check: {message.payload}"
                )
                return False

            if not self.check_nils(message.schema, context):
                logger.info(
                    f"Failed {message.schema.name} nil check: {message.payload}"
                )
                return False

            if not self.check_integrity(message, context):
                logger.info(
                    f"({message.schema.sender.name}) Integrity violation: {message} not consistent with context {context}"
                )
                logger.info(self.contexts)
                return False

            if not self.check_dependencies(message, context):
                logger.info(f"Failed dependency check: {message.payload}")
                return False

            if message.schema.disabled_by(parameters.get(message.key, set())):
                logger.info(
                    f"Message {message} disabled by other emissions: {messages}"
                )
                return False
            if parameters.get(message.key):
                parameters[message.key].update(
                    message.schema.ins.union(message.schema.outs)
                )
            else:
                parameters[message.key] = message.schema.ins.union(message.schema.outs)

        return True

    def add(self, message):
        """
        Add a message instance to the store.
        """

        # log under the correct context
        context = self.context(message)
        context.add(message)

    def context(self, message):
        """Find or create a context for message"""
        parent = None
        context = self.contexts
        for k in message.schema.keys:
            v = message.payload.get(k)
            if k in context:
                if v is not None and v in context[k]:
                    new_context = context[k][v]
                else:
                    new_context = context[k][v] = Context(parent=parent)
            else:
                context[k] = {}
                context[k][v] = new_context = Context(parent=parent)
            context = new_context
            parent = context

        return context

    def is_duplicate(self, message):
        """
        Return true if payload has already been stored.
        """
        context = self.context(message)
        match = context._messages.get(message.schema)
        if match and match == message:
            return True
        elif match:
            raise Exception(
                "Message found with matching key {} but different parameters: {}, {}".format(
                    message.key, message, match
                )
            )
        else:
            return False

    def fill(self, message):
        context = self.context(message)
        bindings = context.bindings

        for p in message.schema.parameters:
            v = bindings.get(p)
            if v:
                message.payload[p] = v
            else:
                raise Exception(
                    f"Cannot complete message {message} with context {context}"
                )
        return message
