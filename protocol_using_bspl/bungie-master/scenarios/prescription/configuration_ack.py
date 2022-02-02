from protocheck import bspl

prescription = bspl.load_file("prescription-ack.bspl").export("PrescriptionAck")

with open("/proc/self/cgroup", "r") as cgroups:
    from Prescription import (
        Patient,
        Doctor,
        Pharmacist,
        Complain,
        Prescribe,
        Filled,
        RepeatComplaint,
        Confirm,
        RepeatPrescription,
        RepeatFilled,
    )

    in_docker = "docker" in cgroups.read()

if in_docker:
    config = {
        Patient: ("patient", 8000),
        Doctor: ("doctor", 8000),
        Pharmacist: ("pharmacist", 8000),
    }
else:
    config = {
        Patient: ("0.0.0.0", 8000),
        Doctor: ("0.0.0.0", 8001),
        Pharmacist: ("0.0.0.0", 8002),
    }

Map = {
    "forwards": {Complain: (Repeat, "rID")},
    "acknowledgments": {Complain: (Confirm, "ackID"), Repeat: (Confirm, "ackID")},
}
