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
from Contracting import Government, Offer, Bid, Accept, Reject

adapter = Adapter(Government, Contracting.protocol, config_a)
logger = logging.getLogger("government")


async def main():
    await adapter.signal({"contractID": str(uuid.uuid4()), "spec": "Build a bridge"})


def accepts(enabled, contractID):
    return [
        m
        for m in enabled.messages
        if m.schema == Accept and m["contractID"] == contractID
    ]


def rejects(enabled, contractID):
    return [
        m
        for m in enabled.messages
        if m.schema == Reject and m["contractID"] == contractID
    ]


async def decision_handler(enabled, event):
    if "contractID" in event:
        offers = [Offer(**event, bidID=i) for i in range(3)]
        logger.info(f"Inviting bids: {offers}")
        return offers
    elif "added" in event:
        for contractID in set(m["contractID"] for m in event["added"]):
            if len(accepts(enabled, contractID)) >= 3:
                await adapter.signal({"decide": contractID})
    elif "decide" in event:
        contractID = event["decide"]
        accept_ms = accepts(enabled, contractID)
        low_bid = min(m["amount"] for m in accept_ms)
        winner = next(
            m.bind(accepted=True, closed=True)
            for m in accept_ms
            if m["amount"] == low_bid
        )
        losers = [
            m.bind(rejected=True, closed=True)
            for m in rejects(enabled, contractID)
            if m["bidID"] is not winner["bidID"]
        ]

        results = [winner, *losers]
        logger.debug(f"results: {results}")
        return results


adapter.decision_handler = decision_handler

if __name__ == "__main__":
    adapter.start(main())
