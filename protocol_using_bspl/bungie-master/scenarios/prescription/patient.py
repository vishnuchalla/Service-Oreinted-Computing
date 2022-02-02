import random
import asyncio
import logging
from bungie import Adapter

# from configuration import config, prescription, Patient, Complain, Filled
from bungie.policies import Remind
from configuration_remind import config, prescription, Patient, Complain, Map, Filled

# from configuration_ack import config, prescription, Patient, Complain, Map, Filled

logging.getLogger("bungie").setLevel(logging.DEBUG)

# adapter
adapter = Adapter(Patient, prescription, config)


async def request_generator():
    cID = 0
    symptoms = [
        "Sneezing",
        "Cough",
        "Stomache ache",
        "Nausea",
        "Hemorrhage",
        "Death",
    ]
    while cID <= 0:
        # construct mesage
        msg = Complain(cID=cID, symptoms=random.sample(symptoms, 1)[0])

        # send message
        adapter.send(msg)

        cID += 1
        await asyncio.sleep(2)


@adapter.reaction(Complain)
async def complained(message):
    print(message)


@adapter.reaction(Filled)
async def filled(message):
    print(message)


if __name__ == "__main__":
    print("Starting Patient...")

    # remind policy
    adapter.add_policies(
        Remind(Complain).With(Map).after(1).until.received(Filled), when="every 1s"
    )

    # acknowledgment policy
    # adapter.add_policies(
    #     Remind(Complain).With(Map).after(1).until.acknowledged,
    #     when='every 1s')

    # start adapter
    adapter.start(request_generator())
