#!/usr/bin/env python3


from bungie import Adapter, Remind, Scheduler
from bungie.statistics import stats_logger
from configuration import config_a
import random
import time
import datetime
import asyncio
import logging
import uuid

import Contracting
from Contracting import Contractor, Offer, Bid, Accept, Reject

adapter = Adapter(Contractor, Contracting.protocol, config_a)
logger = logging.getLogger("contractor")


@adapter.enabled(Bid)
async def make_bid(msg):
    msg["amount"] = random.randint(1000, 100000)
    return msg


@adapter.reaction(Accept)
async def won(msg):
    logger.info(f"Bid {msg['bidID']} won with amount {msg['amount']}")


@adapter.reaction(Reject)
async def lost(msg):
    logger.info(f"Bid {msg['bidID']} lost with amount {msg['amount']}")


if __name__ == "__main__":
    adapter.start()
