from bungie import Adapter, schema

# from configuration import config, prescription, Doctor, Complain, Prescribe
from configuration_resend import (
    config,
    prescription,
    Doctor,
    Complain,
    Repeat,
    Prescribe,
    Map,
)
from bungie.policies import Acknowledge

# from configuration_ack import config, prescription, Doctor, Complain, Repeat, Confirm, Prescribe, Map

adapter = Adapter(Doctor, prescription, config)

treatment = {
    "Stomach ache": "Calcium carbonate",
    "Sneezing": "Diphenhydramine",
    "Cough": "Dextromethorphan",
    "Nausea": "Bismuth sub-salicylate",
    "Hemorrhage": "Vitamins",
    "Death": "Condolences",
}


@adapter.reaction(Complain)
async def request(message):
    print(message)

    msg = Prescribe(
        cID=message.cID, symptoms=message.symptoms, Rx=treatment[message.symptoms]
    )

    adapter.send(msg)


if __name__ == "__main__":
    print("Starting Doctor...")

    # acknowledge Complain
    # adapter.add_policies(Acknowledge(Complain).Map(Map),
    #                      Acknowledge(Repeat).With(Confirm, 'ackID'))

    adapter.start()
