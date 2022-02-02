import pos
import json
import yaml
import os
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

name = "Merchant"

with open("buyer-seller-protocol.json") as stream:
    protocol = json.load(stream)
with open(os.environ['CONFIG']) as conf:
    configuration = yaml.safe_load(conf)

adapter = pos.Adapter(name, protocol, configuration, 'MerchantHistory')


@adapter.received(protocol['messages']['requestQuote'])
def handleRequestQuote(message, enactment):
    logger.info("Merchant: Quote request received: " + json.dumps(message))
    quote = {
        "orderID": message["orderID"],
        "buyerID": message["buyerID"],
        "itemName": message["itemName"],
        "buyerName": message["buyerName"],
        "quote": "quote"
    }
    logger.info("Merchant: Sending quote to the buyer: {}".format(quote))
    ok, msg = adapter.send("Buyer", quote)
    if not ok:
        logger.info("Merchant: " + msg)


@adapter.received(protocol['messages']['acceptQuote'])
def handleBuyerAcceptance(message, enactment):
    logger.info("Merchant: Received buyer acceptance: " + json.dumps(message))


@adapter.received(protocol['messages']['reportDefectiveItem'])
def handleDefectiveItem(message, enactment):
    logger.info("Merchant: Received defective item report from shipping: " + json.dumps(message))
    buyer_id = [m for m in enactment if 'buyerID' in m.keys()][0]['buyerID']
    item_price = [m for m in enactment if 'itemPrice' in m.keys()][0]['itemPrice']
    notify_defective_item = {
        "buyerID": buyer_id,
        "orderID": message['orderID'],
        "itemName": message['itemName'],
        "defectFound": message["defectFound"]
    }
    logger.info("Merchant: notifying buyer about defective item: {}".format(notify_defective_item))
    ok, msg = adapter.send("Buyer", notify_defective_item)
    if not ok:
        logger.info("Merchant: " + msg)

    defective_refund = {
        "buyerID": buyer_id,
        "orderID": message['orderID'],
        "itemPrice": item_price,
        "defectFound": message["defectFound"],
        "defectiveRefund": item_price
    }
    logger.info("Merchant: refunding buyer for the defective item: {}".format(defective_refund))
    ok, msg = adapter.send("Buyer", defective_refund)
    if not ok:
        logger.info("Merchant: " + msg)


@adapter.received(protocol['messages']['cancelOrder'])
def handleCancelOrder(message, enactment):
    logger.info("Merchant: Received cancel order request from buyer: " + json.dumps(message))
    trackingID_list = [m for m in enactment if 'trackingID' in m.keys()]
    item_price = [m for m in enactment if 'itemPrice' in m.keys()][0]['itemPrice']
    if len(trackingID_list) != 0:
        logger.info("Merchant: Order cannot be cancelled now as it is already sent for shipping")
    else:
        logger.info("Merchant: Cancelling the order as it is not yet sent for shipping")
        cancelled_refund = {
            "orderID": message['orderID'],
            "buyerID": message['buyerID'],
            "isCancelled": message['isCancelled'],
            "itemPrice": item_price,
            "cancelledRefund": item_price
        }
        logger.info("Merchant: Performing refund for the cancelled order: {}".format(cancelled_refund))
        ok, msg = adapter.send("Buyer", cancelled_refund)
        if not ok:
            logger.info("Merchant: " + msg)


@adapter.received(protocol['messages']['placeOrder'])
def handlePlaceOrder(message, enactment):
    logger.info("Merchant: Received order {} but pending payment".format(json.dumps(message)))
    pendingPaymentNotification = {
        "orderID": message["orderID"],
        "buyerID": message["buyerID"],
        "itemName": message["itemName"],
        "buyerName": message["buyerName"],
        "onHold": True
    }
    logger.info("Merchant: Sending pending payment notification to buyer: {}".format(pendingPaymentNotification))
    ok, msg = adapter.send("Buyer", pendingPaymentNotification)
    if not ok:
        logger.info("Merchant: " + msg)


@adapter.received(protocol['messages']['submitPayment'])
def handlePayment(message, enactment):
    logger.info("Merchant: Received payment for the order: {}".format(json.dumps(message)))
    shipping_address = [m for m in enactment if 'shippingAddress' in m.keys()][0]['shippingAddress']
    if message['orderID'] == 6:
        logger.info("Merchant: Rejecting the order")
        reject_order = {
            "buyerID": message['buyerID'],
            "orderID": message['orderID'],
            "itemName": message['itemName'],
            "itemPrice": message['itemPrice'],
            "shippingAddress": shipping_address,
            "merchantReject": True
        }
        logger.info("Merchant: Rejecting the order due to stock outage: {}".format(reject_order))
        ok, msg = adapter.send("Buyer", reject_order)
        if not ok:
            logger.info("Merchant: " + msg)

        time.sleep(2)
        rejected_refund = {
            "buyerID": message['buyerID'],
            "orderID": message['orderID'],
            "itemPrice": message['itemPrice'],
            "merchantReject": True,
            "refundForRejectedOrder": message['itemPrice']
        }
        logger.info("Merchant: Performing refund for rejected order: {}".format(rejected_refund))
        ok, msg = adapter.send("Buyer", rejected_refund)
        if not ok:
            logger.info("Merchant: " + msg)
    else:
        logger.info("Merchant: Accepting the order")
        acceptOrder = {
            "buyerID": message['buyerID'],
            "orderID": message['orderID'],
            "itemName": message['itemName'],
            "itemPrice": message['itemPrice'],
            "shippingAddress": shipping_address,
            "merchantAccept": True
        }
        logger.info("Merchant: Sending order acceptance to buyer: {}".format(acceptOrder))
        ok, msg = adapter.send("Buyer", acceptOrder)
        if not ok:
            logger.info("Merchant: " + msg)

        buyer_name = [m for m in enactment if 'buyerName' in m.keys()][0]['buyerName']
        merchant_id = [m for m in enactment if 'merchantID' in m.keys()][0]['merchantID']
        time.sleep(2)
        if message['orderID'] != 2:
            send_to_shipping = {
                "buyerID": message['buyerID'],
                "merchantID": merchant_id,
                "orderID": message['orderID'],
                "buyerName": buyer_name,
                "itemName": message['itemName'],
                "shippingAddress": shipping_address,
                "merchantAccept": True
            }
            logger.info("Merchant: Sending the order for shipping: {}".format(send_to_shipping))
            ok, msg = adapter.send("Shipping", send_to_shipping)
            if not ok:
                logger.info("Merchant: " + msg)
        else:
            logger.info("Merchant: Not taking any further action on the order as it is cancelled.")


@adapter.received(protocol['messages']['provideTrackingInfo'])
def receiveTrackingInfo(message, enactment):
    logger.info("Merchant: Received tracking info from shipping: " + json.dumps(message))
    shipping_details = {
        "buyerID": message['buyerID'],
        "orderID": message['orderID'],
        "trackingID": message['trackingID'],
        "shippingStatus": 'shipping status'
    }
    logger.info("Merchant: notifying buyer about shipping: {}".format(shipping_details))
    ok, msg = adapter.send("Buyer", shipping_details)
    if not ok:
        logger.info("Merchant: " + msg)


@adapter.received(protocol['messages']['sendDeliveryConfirmation'])
def receiveDeliveryConfirmation(message, enactment):
    logger.info("Merchant: Received delivery confirmation from the shipping: {}".format(json.dumps(message)))
    remind_buyer = {
        'buyerID': message["buyerID"],
        'orderID': message["orderID"],
        'trackingID': message['trackingID'],
        'deliveryConfirmation': message['deliveryConfirmation'],
        'remindMessage': 'reminder message to buyer'
    }
    logger.info("Merchant: reminding buyer about the delivery: {}".format(remind_buyer))
    ok, msg = adapter.send("Buyer", remind_buyer)
    if not ok:
        logger.info("Merchant: " + msg)


def lambda_handler(*args):
    return adapter.handler(*args)
