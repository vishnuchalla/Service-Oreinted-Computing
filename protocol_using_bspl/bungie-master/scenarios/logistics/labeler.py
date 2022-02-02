from bungie import Adapter, Remind
from configuration import config_a, logistics, Labeled
import uuid
import logging

logger = logging.getLogger("labeler")
# logging.getLogger('bungie').setLevel(logging.DEBUG)

adapter = Adapter(logistics.roles["Labeler"], logistics, config_a)
RequestLabel = logistics.messages["RequestLabel"]


@adapter.reaction(RequestLabel)
async def labeled(msg):
    adapter.send(Labeled(label=str(uuid.uuid4()), **msg.payload))


if __name__ == "__main__":
    logger.info("Starting Labeler...")
    # adapter.load_policy_file("policies.yaml")
    adapter.start()
