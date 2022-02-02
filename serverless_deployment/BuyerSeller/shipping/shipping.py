import pos
import json
import yaml
import os
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

name = "Shipping"

with open("buyer-seller-protocol.json") as stream:
    protocol = json.load(stream)
with open(os.environ['CONFIG']) as conf:
    configuration = yaml.safe_load(conf)

adapter = pos.Adapter(name, protocol, configuration, 'ShippingHistory')


@adapter.received(protocol['messages']['sendToShipping'])
def handleShippingRequest(message, enactment):
    logger.info("Shipping: shipping request received: " + json.dumps(message))
    if message['orderID'] == 4:
        report_defective_item = {
            "merchantID": message['merchantID'],
            "orderID": message['orderID'],
            "itemName": message['itemName'],
            "defectFound": True
        }
        logger.info("Shipping: reporting defective item to merchant: {}".format(report_defective_item))
        ok, msg = adapter.send("Merchant", report_defective_item)
        if not ok:
            logger.info("Shipping: " + msg)
    else:
        provide_tracking_info = {
            "merchantID": message["merchantID"],
            "buyerID": message['buyerID'],
            "orderID": message['orderID'],
            "trackingID": 'trackingID'
        }
        logger.info("Shipping: providing the tracking details to the merchant: {}".format(provide_tracking_info))
        ok, msg = adapter.send("Merchant", provide_tracking_info)
        if not ok:
            logger.info("Shipping: " + msg)

        time.sleep(3)
        pack_and_ship = {
            "buyerID": message['buyerID'],
            "merchantID": message['merchantID'],
            "orderID": message['orderID'],
            "itemName": message['itemName'],
            "shippingAddress": message['shippingAddress']
        }
        logger.info("Shipping: packing and shipping the item to buyer: {}".format(pack_and_ship))
        ok, msg = adapter.send("Buyer", pack_and_ship)
        if not ok:
            logger.info("Shipping: " + msg)


@adapter.received(protocol['messages']['deliveryConfirmation'])
def receivingDeliveryConfirmation(message, enactment):
    logger.info("Shipping: Delivery confirmation received from buyer: {}".format(message))
    tracking_id = [m for m in enactment if 'trackingID' in m.keys()][0]['trackingID']
    delivery_confirmation = {
        "merchantID": message['merchantID'],
        "buyerID": message['buyerID'],
        "orderID": message['orderID'],
        "receivedDate": message['receivedDate'],
        "deliveryConfirmation": "delivery confirmation",
        "trackingID": tracking_id
    }
    logger.info("Shipping: sending delivery confirmation to the merchant: {}".format(delivery_confirmation))
    ok, msg = adapter.send("Merchant", delivery_confirmation)
    if not ok:
        logger.info("Shipping: " + msg)


def lambda_handler(*args):
    return adapter.handler(*args)
