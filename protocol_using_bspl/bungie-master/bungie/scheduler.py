import asyncio
import aiocron
from croniter import croniter
import uuid
import datetime
import random
import re
import logging
from . import policies

logger = logging.getLogger("bungie")


def exponential(interval=1):
    def inner(message):
        delay = interval * random.randint(0, 2 ** message.meta.get("retries", 0) - 1)
        return delay

    return inner


class Scheduler:
    def __init__(self, schedule="* * * * *", policies=None, backoff=None):
        self.ID = uuid.uuid4()

        if croniter.is_valid(schedule):
            self.schedule = schedule
        elif re.match(r"(?:every\s?)?(\d+\.?\d*)?\s?(?:s|seconds?)", schedule):
            self.schedule = None
            match = re.match(
                r"(?:every\s?)?(\d+\.?\d*)?\s?(?:s|seconds?)", schedule
            ).groups()
            if match[0] is not None:
                self.interval = float(match[0])
            else:
                self.interval = 1
        else:
            raise Exception("Unknown schedule format: {}".format(schedule))

        self.policies = policies or set()
        self._backoff = backoff

    def add(self, policy):
        self.policies.add(policy)
        return self

    def backoff(self, message):
        if "last-retry" in message.meta:
            delta = datetime.datetime.now() - message.meta["last-retry"]
            delay = self._backoff(message)
            return delta.total_seconds() > delay
        else:
            return True

    async def task(self, adapter):
        self.adapter = adapter

        while True:
            if self.schedule:
                logger.debug(
                    f"scheduler: Waiting for next occurrence of ({self.schedule})"
                )
                await aiocron.crontab(self.schedule).next()
            else:
                logger.debug(f"scheduler: Waiting {self.interval} seconds")
                await asyncio.sleep(self.interval)
            await self.run()

    async def run(self):
        for p in self.policies:
            # give policy access to full history for conditional evaluation
            messages = p.run(self.adapter.history)
            if self._backoff:
                await self.adapter.bulk_send([m for m in messages if self.backoff(m)])
            else:
                await self.adapter.bulk_send(messages)
