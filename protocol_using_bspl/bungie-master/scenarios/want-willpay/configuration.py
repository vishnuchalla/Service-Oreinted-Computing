from protocheck import bspl

spec = bspl.load_file("want-willpay.bspl")
protocol = spec.protocols["Want-Willpay"]

Buyer = protocol.roles["Buyer"]
Seller = protocol.roles["Seller"]

Want = protocol.messages["Want"]
WillPay = protocol.messages["WillPay"]
RemindWillPay = protocol.messages["RemindWillPay"]
WillPayAck = protocol.messages["WillPayAck"]

with open("/proc/self/cgroup", "r") as cgroups:
    in_docker = "docker" in cgroups.read()

if in_docker:
    config = {
        Buyer: ("buyer", 8000),
        Seller: ("seller", 8001),
    }
else:
    config = {
        Buyer: ("0.0.0.0", 8000),
        Seller: ("0.0.0.0", 8001),
    }
