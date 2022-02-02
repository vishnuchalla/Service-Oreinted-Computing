import pos
import json
import yaml
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

name = "Buyer"

with open("buyer-seller-protocol.json") as stream:
    protocol = json.load(stream)
with open(os.environ['CONFIG']) as conf:
    configuration = yaml.safe_load(conf)

adapter = pos.Adapter(name, protocol, configuration, 'BuyerHistory')


def translate_dynamo(obj):
    result = {}
    for k in obj:
        type = list(obj[k].keys())[0]
        if type == "N":
            result[k] = int(obj[k]["N"])
        else:
            result[k] = obj[k][type]
    return result


def handle_order(event, context):
    """
    Handle a stream event from DynamoDB.
    Receives a newly submitted order from the customer, and sends RequestLabel and RequestWrapping messages.
    """
    for record in event["Records"]:
        logger.info(record)
        update = record.get('dynamodb', {}).get('NewImage')
        if not update:
            logger.info("Buyer: No updates: {}".format(record))
            return
        order = translate_dynamo(update)

        logger.info("Buyer: Received order: {}".format(order))
        request_quote = {
            "buyerID": 'buyerID',
            "orderID": order["orderID"],
            "itemName": order["itemName"],
            "buyerName": 'buyerName',
            "merchantID": order["merchantID"]
        }
        logger.info("Buyer: Sending requestQuote to merchant: {}".format(request_quote))
        ok, msg = adapter.send("Merchant", request_quote)
        if not ok:
            logger.info("Buyer: " + msg)


@adapter.sent(protocol['messages']['requestQuote'])
def handleRequestQuote(message, enactment):
    logger.info("Buyer: requestQuote sent: " + json.dumps(message))


@adapter.received(protocol['messages']['sendQuote'])
def handleQuote(message, enactment):
    logger.info("Buyer: Quote received from merchant: " + json.dumps(message))
    quote = {
        "orderID": message["orderID"],
        "buyerID": message["buyerID"],
        "quote": message["quote"],
        "buyerAccept": "buyerAcceptance"
    }
    logger.info("Buyer: Sending acceptance: {}".format(quote))
    ok, msg = adapter.send("Merchant", quote)
    if not ok:
        logger.info("Buyer: " + msg)

    orderDetails = {
        "orderID": message["orderID"],
        "buyerID": message["buyerID"],
        "itemName": message["itemName"],
        "buyerName": message["buyerName"],
        "shippingAddress": "shipping address"
    }
    logger.info("Buyer: Placing the order: {}".format(orderDetails))
    ok, msg = adapter.send("Merchant", orderDetails)
    if not ok:
        logger.info("Buyer: " + msg)


def cancelOrder(message):
    cancel_order = {
        "orderID": message['orderID'],
        "buyerID": message['buyerID'],
        "isCancelled": True
    }
    logger.info("Buyer: Cancelling the order: {}".format(cancel_order))
    ok, msg = adapter.send("Merchant", cancel_order)
    if not ok:
        logger.info("Buyer: " + msg)


@adapter.received(protocol['messages']['notifyBuyerAboutPendingPayment'])
def handleRequestQuote(message, enactment):
    logger.info("Buyer: pending payment notification received: " + json.dumps(message))
    submit_payment = {
        "orderID": message["orderID"],
        "buyerID": message["buyerID"],
        "itemName": message["itemName"],
        "itemPrice": "100USD",
        "paymentDone": True
    }
    logger.info("Buyer: Submitting payment for the order: {}".format(submit_payment))
    ok, msg = adapter.send("Merchant", submit_payment)
    if not ok:
        logger.info("Buyer: " + msg)

@adapter.received(protocol['messages']['acceptOrder'])
def acceptanceNotification(message, enactment):
    logger.info("Buyer: Order accepted by merchant: {}".format(json.dumps(message)))
    if message["orderID"] == 2:
        cancelOrder(message)


@adapter.received(protocol['messages']['notifyBuyerAboutShipping'])
def receiveShippingNotification(message, enactment):
    logger.info("Buyer: Tracking information received from merchant: {}".format(message))


@adapter.received(protocol['messages']['packAndShipItem'])
def receiveItem(message, enactment):
    logger.info("Buyer: Receiving item from shipping service: {}".format(message))
    delivery_confirmation = {
        "buyerID": message['buyerID'],
        "orderID": message['orderID'],
        "merchantID": message['merchantID'],
        "itemName": message['itemName'],
        "receivedDate": '11/19/2021'
    }
    logger.info("Buyer: Confirming the delivery to the shipping: {}".format(delivery_confirmation))
    ok, msg = adapter.send("Shipping", delivery_confirmation)
    if not ok:
        logger.info("Buyer: " + msg)


@adapter.received(protocol['messages']['remindBuyer'])
def receiveDeliveryReminder(message, enactment):
    logger.info("Buyer: delivery reminding message received from merchant: {}".format(message))


@adapter.received(protocol['messages']['notifyDefectiveItem'])
def defectiveItemNotification(message, enactment):
    logger.info("Buyer: notification received about the defective item: {}".format(message))


@adapter.received(protocol['messages']['doRefundForDefectiveItem'])
def receiveDefectiveRefund(message, enactment):
    logger.info("Buyer: refund received for the defective item: {}".format(message))


@adapter.received(protocol['messages']['rejectOrder'])
def acceptanceNotification(message, enactment):
    logger.info("Buyer: Notification for the order rejected by merchant: {}".format(json.dumps(message)))


@adapter.received(protocol['messages']['doRefundForRejectedItem'])
def acceptanceNotification(message, enactment):
    logger.info("Buyer: Refund received for the rejected order: {}".format(json.dumps(message)))


def lambda_handler(*args):
    return adapter.handler(*args)
