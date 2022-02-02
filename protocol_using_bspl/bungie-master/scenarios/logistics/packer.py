import logging
from bungie import Adapter, Remind
from configuration import config_a, logistics
from bungie.statistics import stats_logger

from Logistics import Packer, Packed

adapter = Adapter(Packer, logistics, config_a)

logger = logging.getLogger("bungie")
# logger.setLevel(logging.DEBUG)


@adapter.enabled(Packed)
async def pack(msg):
    msg["status"] = "packed"
    return msg


if __name__ == "__main__":
    logger.info("Starting Packer...")
    adapter.start()
