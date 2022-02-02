import asyncio
import logging
import socket
import json
from asyncio.queues import Queue

logger = logging.getLogger("bungie")


def encode(msg):
    s = json.dumps(msg.payload, separators=(",", ":"))
    b = s.encode()
    return b


class Emitter:
    """An Emitter just needs one method: send(message)."""

    def __init__(self, encoder=encode, mtu=1500 - 48):
        """Each component is a function that """
        self.encode = encoder
        self.mtu = mtu

        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM  # Internet
        )  # UDP
        self.stats = {"bytes": 0, "packets": 0}

    async def send(self, message):
        """Send bun via UDP"""
        packet = self.encode(message)
        self.transmit(b"[" + packet + b"]", message.dest)

    async def bulk_send(self, messages):
        packets = {}
        for m in messages:
            data = self.encode(m)
            if m.dest in packets:
                if len(packets[m.dest]) + len(data) + 3 > self.mtu:
                    if len(packets[m.dest]) + 2 > self.mtu:
                        raise Exception(
                            f"Message is too long to fit in a single packet: {packets[m.dest]}"
                        )
                    else:
                        # send what we have so far and reset
                        packet = b"[" + packets[m.dest] + b"]"
                        self.transmit(packet, m.dest)
                        packets[m.dest] = data
                else:
                    # add one more message
                    packets[m.dest] += b"," + data
            else:
                packets[m.dest] = data
        # all messages have been encoded and sorted; send any remaining
        for dest in packets:
            self.transmit(b"[" + packets[dest] + b"]", dest)

    def transmit(self, packet, dest):
        logger.debug("Sending packet {} to {}".format(packet, dest))
        self.stats["bytes"] += len(packet)
        self.stats["packets"] += 1
        self.socket.sendto(packet, dest)

    async def stop(self):
        self.socket.close()


class Bundle:
    def __init__(self, max_size):
        self.max_size = max_size
        self.contents = b""

    def add(self, message):
        """
        Add a message to contents, using ',' as the separator.
        """
        if type(message) is str:
            message = bytes(message, "utf-8")

        if len(self.contents) > 0:
            self.contents += b"," + message
        else:
            self.contents = message

    def test(self, message):
        if len(self.contents) + len(message) + 2 <= self.max_size:
            return True
        return False

    def pack(self, deque):
        while len(deque) > 0:
            if self.test(deque[0]):
                self.add(deque.popleft())
            else:
                if self.contents:
                    break
                else:
                    raise Exception(
                        "Message is too long to fit in a single packet: {}".format(
                            deque[0]
                        )
                    )

        return b"[" + self.contents + b"]"


def bundle(mtu, queue):
    b = Bundle(mtu)
    return b.pack(queue)


class BundlingEmitter:
    """An Emitter just needs the send(message) method."""

    def __init__(self, encoder=encode, bundler=bundle, mtu=1500 - 48):
        """Each component is a function that """
        self.encode = encoder
        self.bundle = bundler
        self.mtu = mtu
        self.running = False

        self.channels = {}
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM  # Internet
        )  # UDP
        self.stats = {"bytes": 0, "packets": 0}

    async def sort(self):
        while self.running:
            message = await self.queue.get()
            m = self.encode(message)
            if message.dest in self.channels:
                await self.channels[message.dest].put(m)
            else:
                loop = asyncio.get_running_loop()
                queue = self.channels[message.dest] = Queue()
                loop.create_task(self.process(message.dest, queue))
                await self.channels[message.dest].put(m)

    async def process(self, dest, queue):
        while self.running:
            message = await queue.get()
            q = queue._queue
            q.appendleft(message)
            packet = self.bundle(self.mtu, q)
            self.transmit(packet, dest)

    async def task(self):
        """Start loop for transmitting messages in outgoing queue"""
        loop = asyncio.get_running_loop()
        self.queue = Queue()
        self.running = True
        loop.create_task(self.sort())

    async def send(self, message):
        # Do mangling and encoding first; then bundler can process the queue directly
        await self.queue.put(message)

    def transmit(self, packet, dest):
        """Send binary-encoded bun via UDP"""
        logger.debug("Sending packet {} to {}".format(packet, dest))
        self.stats["bytes"] += len(packet)
        self.stats["packets"] += 1
        self.socket.sendto(packet, dest)

    async def stop(self):
        self.running = False
        self.socket.close()


class TCPEmitter:
    """An Emitter just needs the send(message) method."""

    def __init__(self, encoder=encode):
        """Each component is a function that """
        self.encode = encoder
        self.channels = {}
        self.stats = {"bytes": 0, "packets": 0}
        self.running = False

    async def process(self):
        while self.running:
            message = await self.queue.get()
            m = self.encode(message)
            if message.dest in self.channels:
                writer = self.channels[message.dest]
            else:
                _, writer = await asyncio.open_connection(*message.dest)
                self.channels[message.dest] = writer
                writer.write(b"[")
                self.stats["bytes"] += 1

            writer.write(m + b",")
            self.stats["bytes"] += len(m) + 1
            # await writer.drain()

    async def task(self):
        """Start loop for transmitting messages in outgoing queue"""
        loop = asyncio.get_running_loop()
        self.queue = Queue()

        self.running = True
        loop.create_task(self.process())

    async def send(self, message):
        # Do mangling and encoding first; then bundler can process the queue directly
        await self.queue.put(message)

    async def stop(self):
        self.running = False
        for writer in self.channels.values():
            writer.close()
            await writer.wait_closed()
