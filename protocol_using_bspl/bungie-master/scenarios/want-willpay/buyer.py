from bungie import Adapter
from bungie.statistics import stats, stats_logger
from bungie.emitter import TCPEmitter
from configuration import (
    config_a,
    protocol,
    Buyer,
    Want,
    WillPay,
    RemindWillPay,
    WillPayAck,
)
import random
import logging
import asyncio
import datetime
import argparse

parser = argparse.ArgumentParser(description="Run the buyer agent")
parser.add_argument(
    "version",
    type=str,
    help="The version of the agent to run",
    choices=["no-recovery", "ack", "tcp", "forward"],
    default="ack",
)

adapter = Adapter(Buyer, protocol, config_a)

logger = logging.getLogger("buyer")
# logging.getLogger('bungie').setLevel(logging.DEBUG)


async def order_generator():
    for orderID in range(100000):
        item = random.sample(["ball", "bat", "car", "cat"], 1)[0]
        adapter.send({"ID": orderID, "item": item}, Want)
        adapter.send(
            {"ID": orderID, "item": item, "price": random.randint(10, 100)}, WillPay
        )
        await asyncio.sleep(0.0002)


stats.update({"initiated": 0})


@adapter.reaction(Want)
async def want(msg):
    stats["initiated"] += 1
    if "first" not in stats:
        stats["first"] = datetime.datetime.now()
    stats["duration"] = (datetime.datetime.now() - stats["first"]).total_seconds()
    stats["rate"] = stats["initiated"] / stats["duration"]


if __name__ == "__main__":
    logger.info("Starting Buyer...")
    args = parser.parse_args()
    if args.version == "ack":
        adapter.add_policies(
            "resend WillPay after 1s until acknowledged", when="every 0.5s"
        )
    elif args.version == "tcp":
        adapter.emitter = TCPEmitter()
    elif args.version == "forward":
        pass
    # no special handling for no-recovery case
    adapter.start(order_generator(), stats_logger(3, hide=["first"]))
