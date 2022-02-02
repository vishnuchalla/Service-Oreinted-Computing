from protocheck import bspl

logistics = bspl.load_file("logistics.bspl").export("Logistics")
from Logistics import Merchant, Wrapper, Labeler, Packer

from Logistics import (
    RequestLabel,
    RequestWrapping,
    Labeled,
    Wrapped,
    Packed,
)

config = {
    Merchant: ("0.0.0.0", 8000),
    Wrapper: ("0.0.0.0", 8001),
    Labeler: ("0.0.0.0", 8002),
    Packer: ("0.0.0.0", 8003),
}
