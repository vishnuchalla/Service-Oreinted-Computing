from bungie import Adapter
from bungie.statistics import stats_logger, stats
from bungie.policies import Acknowledge
from bungie.receiver import TCPReceiver
from configuration import config_a, protocol, Want, WillPay, Seller
import random
import logging
import asyncio
import datetime
import argparse

logger = logging.getLogger("seller")
# logging.getLogger('bungie').setLevel(logging.DEBUG)

parser = argparse.ArgumentParser(description="Run the seller agent")
parser.add_argument(
    "version",
    type=str,
    help="The version of the agent to run",
    choices=["no-recovery", "ack", "tcp", "forward"],
    default="ack",
)

adapter = Adapter(Seller, protocol, config_a)

Want = protocol.messages["Want"]
WillPay = protocol.messages["WillPay"]

stats.update({"finished": 0})


@adapter.reaction(WillPay)
async def will_pay(msg):
    stats["finished"] += 1
    if "first" not in stats:
        stats["first"] = datetime.datetime.now()
    stats["duration"] = (datetime.datetime.now() - stats["first"]).total_seconds()
    stats["rate"] = stats["finished"] / stats["duration"]


if __name__ == "__main__":
    logger.info("Starting Seller...")
    args = parser.parse_args()
    if args.version == "ack":
        adapter.add_policies(Acknowledge(WillPay))
    elif args.version == "tcp":
        adapter.receiver = TCPReceiver(config_a[Seller])
    elif args.version == "forward":
        adapter.add_policies(
            """
            action: forward ForwardWillPay to Buyer upon received WillPay
            autoincrement:
              - fwpID
            """
        )
    adapter.start(stats_logger(3, hide=["first"]))
