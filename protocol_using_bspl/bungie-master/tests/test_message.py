#!/usr/bin/env python3

import asyncio
import logging
import pytest
from protocheck import bspl
from bungie.history import Message

specification = bspl.parse(
    """
RFQ {
  roles C, S // Customer, Seller
  parameters out item key, out ship
  private price, payment

  C -> S: req[out item]
  S -> C: quote[in item, out price]
  C -> S: pay[in item, in price, out payment]
  S -> C: ship[in item, in payment, out ship]
}
"""
)
rfq = specification.export("RFQ")
from RFQ import C, S, req


config = {
    C: ("localhost", 8001),
    S: ("localhost", 8002),
}

logger = logging.getLogger("bungie")
logger.setLevel(logging.DEBUG)
