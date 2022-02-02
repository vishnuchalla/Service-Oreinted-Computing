import asyncio
import aiorun
import logging
import json
import datetime
import sys
import os
import math
import socket
import inspect
import yaml
from types import MethodType
from asyncio.queues import Queue
from .store import Store, Message
from functools import partial
from .emitter import Emitter
from .receiver import Receiver
from .scheduler import Scheduler, exponential
from .statistics import stats, increment
from . import policies
import bungie

FORMAT = "%(asctime)-15s %(module)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger("bungie")

logging.getLogger("aiorun").setLevel(logging.CRITICAL)


class ObservationEvent:
    type = None
    pass


class ReceptionEvent(ObservationEvent):
    def __init__(self, message):
        self.type = "reception"
        self.messages = [message]


class EmissionEvent(ObservationEvent):
    def __init__(self, messages):
        self.type = "emission"
        self.messages = messages


class Adapter:
    def __init__(self, role, protocol, configuration, emitter=Emitter(), receiver=None):
        """
        Initialize the agent adapter.

        role: name of the role being implemented
        protocol: a protocol specification
          {name, keys, messages: [{name, from, to, parameters, keys, ins, outs, nils}]}
        configuration: a dictionary of roles to endpoint URLs
          {role: url}
        """
        self.role = role
        self.protocol = protocol
        self.configuration = configuration
        self.reactors = {}  # dict of message -> [handlers]
        self.generators = {}  # dict of (scheema tuples) -> [handlers]
        self.history = Store()
        self.emitter = emitter
        self.receiver = receiver or Receiver(self.configuration[self.role])
        self.schedulers = []
        self.projection = protocol.projection(role)

        self.inject(protocol)

        self.enabled_messages = Store()
        self.decision_handler = None

    def inject(self, protocol):
        """Install helper methods into schema objects"""

        from protocheck.protocol import Message

        Message.__call__ = bungie.schema.instantiate(self)

        for m in protocol.messages.values():
            m.match = MethodType(bungie.schema.match, m)
            m.adapter = self

    async def receive(self, payload):
        logger.debug(f"Received payload: {payload}")
        if not isinstance(payload, dict):
            logger.warn("Payload does not parse to a dictionary: {}".format(payload))
            return

        schema = self.protocol.find_schema(payload, to=self.role)
        logger.debug(f"Found schema: {schema}")
        if not schema:
            logger.warn("No schema matching payload: {}".format(payload))
            return
        message = Message(schema, payload)
        message.meta["received"] = datetime.datetime.now()
        increment("receptions")
        if self.history.is_duplicate(message):
            logger.debug("Duplicate message: {}".format(message))
            increment("dups")
            # Don't react to duplicate messages
            # message.duplicate = True
            # await self.react(message)
        elif self.history.check_integrity(message):
            logger.debug("Observing message: {}".format(message))
            increment("observations")
            self.history.add(message)
            await self.signal(ReceptionEvent(message))

    def send(self, *payloads, schema=None, name=None, to=None):
        messages = []
        for payload in payloads:
            if isinstance(payload, Message):
                m = payload
            else:
                schema = schema or self.protocol.find_schema(payload, name=name, to=to)
                m = Message(schema, payload)

            messages.append(m)
        loop = asyncio.get_running_loop()
        loop.create_task(self.process_send(*messages))

    async def process_send(self, *messages):
        def prep(message):
            if not message.dest:
                message.dest = self.configuration[message.schema.recipient]
            return message

        emissions = set(prep(m) for m in messages if not self.history.is_duplicate(m))
        if len(emissions) < len(messages):
            logger.info(
                f"({self.role.name}) Skipped duplicate messages: {set(messages).difference(emissions)}"
            )

        if self.history.check_emissions(emissions):
            for m in emissions:
                self.history.add(m)
            if hasattr(self.emitter, "bulk_send"):
                logger.debug(f"bulk sending {len(emissions)} messages")
                await self.emitter.bulk_send(emissions)
            else:
                for m in emissions:
                    await self.emitter.send(message)
            await self.signal(EmissionEvent(emissions))

    def register_reactor(self, schema, handler, index=None):
        if schema in self.reactors:
            rs = self.reactors[schema]
            if handler not in rs:
                rs.insert(index if index is not None else len(rs), handler)
        else:
            self.reactors[schema] = [handler]

    def register_reactors(self, handler, schemas=[]):
        for s in schemas:
            self.register_reactor(s, handler)

    def reaction(self, *schemas):
        """
        Decorator for declaring reactor handler.

        Example:
        @adapter.reaction(MessageSchema)
        async def handle_message(message):
            'do stuff'
        """
        return partial(self.register_reactors, schemas=schemas)

    async def react(self, message):
        """
        Handle emission/reception of message by invoking corresponding reactors.
        """
        reactors = self.reactors.get(message.schema)
        if reactors:
            for r in reactors:
                logger.debug("Invoking reactor: {}".format(r))
                message.adapter = self
                await r(message)

    def enabled(self, *schemas, **options):
        """
        Decorator for declaring enabled message generators.

        Example:
        @adapter.enabled(MessageSchema)
        async def generate_message(msg):
            msg.bind("param", value)
            return msg
        """
        return partial(self.register_generators, schemas=schemas, options=options)

    def register_generators(self, handler, schemas, options={}):
        if schemas in self.generators:
            gs = self.generators[schemas]
            if handler not in gs:
                gs.insert(index if index is not None else len(gs), handler)
        else:
            self.generators[schemas] = [handler]

    async def handle_enabled(self, message):
        """
        Handle newly observed message by checking for newly enabled messages.

        1. Cycle through all registered schema tuples
        2. Check if all messages in tuple are enabled
        3. If so, invoke the handlers in sequence
        4. Continue until a message is returned
        5. Break loop after the first handler returns a message, and send it

        Note: sending a message triggers the loop again
        """
        for tup in self.generators.keys():
            for group in zip(*(schema.match(**message.payload) for schema in tup)):
                for handler in self.generators[tup]:
                    # assume it returns only one message for now
                    msg = await handler(*group)
                    if msg:
                        self.send(msg)
                        # short circuit on first message to send
                        return

    async def task(self):
        loop = asyncio.get_running_loop()

        loop.create_task(self.update_loop())

        await self.receiver.task(self)

        if hasattr(self.emitter, "task"):
            await self.emitter.task()
        for s in self.schedulers:
            # todo: add stop event support
            loop.create_task(s.task(self))

    def add_policies(self, *ps, when="reactive"):
        for policy in ps:
            # action = policy.get('action')
            # if type(action) is str:
            #     action = policies.parse(self.protocol, action)
            for schema, reactor in policy.reactors.items():
                self.register_reactor(schema, reactor, policy.priority)
            if when != "reactive":
                s = Scheduler(when)
                self.schedulers.append(s)
                s.add(policy)

    def load_policies(self, spec):
        if type(spec) is str:
            spec = yaml.full_load(spec)
        if self.role.name in spec:
            for condition, ps in spec[self.role.name].items():
                self.add_policies(*ps, when=condition)
        else:
            # Assume the file contains policies only for agent
            for condition, ps in spec.items():
                self.add_policies(*ps, when=condition)

    def load_policy_file(self, path):
        with open(path) as file:
            spec = yaml.full_load(file)
            self.load_policies(spec)

    def start(self, *tasks, use_uvloop=True):
        async def main():
            await self.task()
            loop = asyncio.get_running_loop()
            for t in tasks:
                loop.create_task(t)

        self.running = True
        aiorun.run(main(), stop_on_unhandled_errors=True, use_uvloop=use_uvloop)

    async def stop(self):
        await self.receiver.stop()
        await self.emitter.stop()
        self.running = False

    async def signal(self, event):
        """
        Publish an event for triggering the update loop
        """
        await self.events.put(event)

    async def update_loop(self):
        self.events = Queue()

        while self.running:
            event = await self.events.get()
            logger.debug(f"event: {event}")
            emissions = await self.process(event)
            if emissions:
                if self.history.check_emissions(emissions):
                    await self.process_send(*emissions)

    async def process(self, event):
        """
        Process a single functional step in a decision loop

        (state, observations) -> (state, enabled, event) -> (state, emissions) -> state
        - state :: the local state, history of observed messages + other local information
        - event :: an object representing the new information that triggered the processing loop; could be an observed message or a signal from the agent internals or environment
        - enabled :: a set of all currently enabled messages, indexed by their keys; the enabled set is incrementally constructed and stored in the state
        - emissions :: a list of message instance for sending

        State can be threaded through the entire loop to make it more purely functional, or left implicit (e.g. a property of the adapter) for simplicity
        Events need a specific structure;
        """

        if isinstance(event, ObservationEvent):
            # Update the enabled messages if there was an emission or reception
            observations = event.messages
            event = self.compute_enabled(observations)
            for m in observations:
                logger.debug(m)
                await self.react(m)
                await self.handle_enabled(m)

        if self.decision_handler:
            return await self.decision_handler(self.enabled_messages, event)

    def compute_enabled(self, observations):
        """
        Compute updates to the enabled set based on a list of an observations
        """

        # clear out matching keys from enabled set
        removed = set()
        for msg in observations:
            context = self.enabled_messages.context(msg)
            removed.update(context.messages)
            context.clear()

        added = set()
        for o in observations:
            for schema in self.projection.messages.values():
                added.update(schema.match(**o.payload))
        for m in added:
            self.enabled_messages.add(m)
        removed.difference_update(added)

        return {"added": added, "removed": removed, "observations": observations}
