from bungie import Adapter
from configuration import config_a, logistics, Wrapped, RequestWrapping
import logging

logger = logging.getLogger("wrapper")
# logging.getLogger("bungie").setLevel(logging.DEBUG)

adapter = Adapter(logistics.roles["Wrapper"], logistics, config_a)


@adapter.reaction(RequestWrapping)
async def wrap(msg):
    adapter.send(
        Wrapped(
            wrapping="bubblewrap" if msg["item"] in ["plate", "glass"] else "paper",
            **msg.payload
        )
    )
    return msg


if __name__ == "__main__":
    logger.info("Starting Wrapper...")
    adapter.start()
