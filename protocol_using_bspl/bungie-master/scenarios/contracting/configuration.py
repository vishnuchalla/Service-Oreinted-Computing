#!/usr/bin/env python3

from protocheck import bspl

contracting = bspl.load_file("contracting.bspl").export("Contracting")
from Contracting import Government, Contractor

from Contracting import Offer, Bid, Accept, Reject

with open("/proc/self/cgroup", "r") as cgroups:

    in_docker = "docker" in cgroups.read()

if in_docker:
    config = {
        Government: ("government", 8000),
        Contractor: ("contractor", 8001),
    }
else:
    config = {
        Government: ("0.0.0.0", 8000),
        Contractor: ("0.0.0.0", 8001),
    }
