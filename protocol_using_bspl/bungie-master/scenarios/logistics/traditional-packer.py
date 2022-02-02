#!/usr/bin/env python3

import logging
import aiorun
from bungie import Adapter
from configuration import config_a, logistics
from bungie.statistics import stats_logger
import ijson, json, socket, asyncio

import Logistics
from Logistics import Packer, Packed, Wrapped, Labeled

adapter = Adapter(Packer, logistics, config_a)

logger = logging.getLogger("packer")
# logger.setLevel(logging.DEBUG)


socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP


class UDPReceiverProtocol:
    def datagram_received(self, data, addr):
        messages = json.loads(data)
        for m in messages:
            receive(m)

    def connection_made(self, conn):
        pass


def send(msg, dest):
    packet = json.dumps(msg, separators=(",", ":")).encode()
    socket.sendto(b"[" + packet + b"]", dest)


wrappings = {}
labels = {}
sent_items = set()


def pack_items(oID):
    for m in wrappings[oID]:
        key = (m["orderID"], m["itemID"])
        if key not in sent_items:
            sent_items.add(key)
            send(
                {"label": labels[oID]["label"], **m, "status": "ok"},
                config_a[Packed.recipient],
            )


def receive(payload):
    schema = Logistics.protocol.find_schema(payload, to=Packer)

    oID = payload["orderID"]
    if schema == Wrapped:
        if wrappings.get(oID):
            wrappings[oID].append(payload)
        else:
            wrappings[oID] = [payload]
        if labels.get(oID):
            pack_items(oID)

    if schema == Labeled:
        labels[oID] = payload
        if wrappings.get(oID):
            pack_items(oID)


async def main():
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPReceiverProtocol(),
        local_addr=config_a[Packer],
    )


if __name__ == "__main__":
    logger.info("Starting Packer")
    aiorun.run(main(), stop_on_unhandled_errors=True, use_uvloop=True)
