from protocheck import bspl

prescription = bspl.load_file("prescription-remind.bspl").export("PrescriptionRemind")

with open("/proc/self/cgroup", "r") as cgroups:
    from PrescriptionRemind import (
        Patient,
        Doctor,
        Pharmacist,
        Complain,
        Repeat,
        Prescribe,
        Filled,
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

Map = {"forwards": {Complain: (Repeat, "rID")}}
