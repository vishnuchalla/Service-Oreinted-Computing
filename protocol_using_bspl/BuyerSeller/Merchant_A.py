from bungie import Adapter, Remind, Scheduler
from configuration import config_a
import asyncio
import logging
import BuyerSeller
from BuyerSeller import Merchant, submitOrder, acceptOrder, rejectOrder, notifyCancelledOrder, notifyMerchantAboutPayment, releasePayment, sendToShipping, uploadTrackingDetails, receiveDeliveryConfirmation, notifyDefectiveItem, submitMerchantReview, provideTrackingInfo, sendDeliveryConfirmation, reportDefectiveItem

adapter = Adapter(Merchant, BuyerSeller.protocol, config_a)
logger = logging.getLogger("merchant")
logging.getLogger('bungie').setLevel(logging.INFO)

def get_bindings(adapter, orderIDKey):

    return adapter.history.contexts.subcontexts['orderID'][orderIDKey].bindings

@adapter.reaction(notifyMerchantAboutPayment)
async def notification_to_merchant_on_payment_hold(message):
    logger.info(str(message['orderID']) + " Notification received at the merchant end on payment hold")
    if message['orderID'] == 'order_ID1':
        submit_review(message)

@adapter.reaction(provideTrackingInfo)
async def upload_tracking_info(message):
    logger.info(str(message['orderID']) + " Tracking info shared with merchant from the shipping service")
    adapter.send(
        uploadTrackingDetails(**message.payload)
    )
    if message['orderID'] == 'order_ID2':
        submit_review(message)

@adapter.reaction(submitOrder)
async def acknowledge_order(message):
    if message['orderID'] == 'order_ID7':
        if {'isCancelled', 'cancelledNotification'}.issubset(set(get_bindings(adapter, message['orderID']).keys())):
            logger.info(str(message['orderID']) + " Not taking any further action on the order because it is cancelled before sending to shipping")
        else:
            logger.info(str(message['orderID']) + " Order rejected by merchant due to out of stock!")
            adapter.send(
                rejectOrder(
                    buyerID=message['buyerID'],
                    orderID=message['orderID'],
                    itemName=message['itemName'],
                    buyerAddress=message['buyerAddress'],
                    merchantReject='true',
                )
            )
    else:
        logger.info(str(message['orderID']) + " Order received and acknowledged by the merchant")
        adapter.send(
            acceptOrder(
                buyerID = message['buyerID'],
                orderID = message['orderID'],
                itemName = message['itemName'],
                buyerAddress = message['buyerAddress'],
                merchantAccept = 'true',
            )
        )
        await asyncio.sleep(3)
        if {'isCancelled', 'cancelledNotification'}.issubset(set(get_bindings(adapter, message['orderID']).keys())):
            logger.info(str(message['orderID']) + " Not taking any further action on the order because it is cancelled before sending to shipping")
        else:
            logger.info(str(message['orderID']) + " Sending order to shipping service")
            adapter.send(
                sendToShipping(merchantAccept = 'true', **message.payload)
        )
        if message['orderID'] == 'order_ID3':
            submit_review(message)

@adapter.reaction(sendDeliveryConfirmation)
async def delivery_confirmation(message):
    logger.info(str(message['orderID']) + " sending delivery confirmation to the eBay website")
    adapter.send(
        receiveDeliveryConfirmation(**message.payload)
    )
    if message['orderID'] == 'order_ID4':
        submit_review(message)

@adapter.reaction(notifyCancelledOrder)
async def cancelled_order_notification(message):
    logger.info(str(message['orderID']) + " notification received at merchant end about the cancelled order")
    if message['orderID'] == 'order_ID5':
        submit_review(message)

def submit_review(message):
    logger.info(str(message['orderID']) + " submitting merchant review for the order")
    adapter.send(
        submitMerchantReview(
            merchantID='merchant id',
            orderID=message['orderID'],
            merchantReviewMessage='merchant review message',
            merchantReviewDone='true',
        )
    )

@adapter.reaction(releasePayment)
async def payment_credit_notification(message):
    logger.info(str(message['orderID']) + " Payment credit notification received by merchant")
    if message['orderID'] == 'order_ID6':
        submit_review(message)

@adapter.reaction(reportDefectiveItem)
async def defective_item_notification_from_shipping(message):
    logger.info(str(message['orderID']) + " Defective item notified by the shipping. Updating the same to eBay")
    adapter.send(
        notifyDefectiveItem(
            buyerID=get_bindings(adapter, message['orderID'])['buyerID'],
            **message.payload
        )
    )
    if message['orderID'] == 'order_ID6':
        submit_review(message)

if __name__ == "__main__":
    print("Starting Merchant...")
    adapter.start()
