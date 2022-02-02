import asyncio
import logging
import socket
import json
import ijson
import datetime
from asyncio.queues import Queue

logger = logging.getLogger("bungie")


def unbundle(bundle):
    return bundle


def decode(msg):
    return json.loads(msg)


class UDPReceiverProtocol:
    def __init__(self, queue):
        self.queue = queue

    def datagram_received(self, data, addr):
        self.queue.put_nowait(data)

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        logger.debug(f"Connection lost: {exc}")


class Receiver:
    """An Receiver just needs the send(message) method."""

    def __init__(self, address, decoder=decode, unbundler=unbundle):
        self.address = address
        self.decode = decoder
        self.unbundle = unbundler
        self.listening = False

    async def task(self, adapter):
        """Start loop for transmitting messages in outgoing queue"""
        self.adapter = adapter
        self.queue = Queue()
        loop = asyncio.get_running_loop()
        logger.debug(f"Attempting to bind: {self.address}")
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UDPReceiverProtocol(self.queue),
            local_addr=("0.0.0.0", self.address[1]),
        )
        self.listening = True
        self.transport = transport
        logger.info(f"Listening on {self.address}")
        loop.create_task(self.process())

    async def process(self):
        while self.listening:
            data = await self.queue.get()
            bundle = self.decode(data)
            messages = self.unbundle(bundle)
            for m in messages:
                await self.adapter.receive(m)
        logger.info("Stopped listening")

    async def stop(self):
        self.listening = False
        self.transport.close()


class TCPReceiver:
    def __init__(self, address, decoder=decode):
        self.address = address
        self.decode = decoder

    async def task(self, adapter):
        self.adapter = adapter
        self.queue = Queue()
        loop = asyncio.get_running_loop()

        server = await asyncio.start_server(self.process, "0.0.0.0", self.address[1])
        self.server = server

        addr = server.sockets[0].getsockname()
        logger.info(f"Listening on {addr}")

        loop = asyncio.get_running_loop()

        async def serve():
            async with server:
                await server.serve_forever()

        loop.create_task(serve())
        self.stop(adapter.stop_event)

    async def process(self, reader, writer):
        async for obj in ijson.items(reader, "item"):
            await self.adapter.receive(obj)

    async def stop(self):
        await self.server.close()
