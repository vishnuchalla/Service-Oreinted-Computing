import asyncio

from bungie import Adapter, Remind, Scheduler
from configuration import config_a
import logging
import BuyerSeller
from BuyerSeller import eBay, placeOrder, acceptOrder, rejectOrder, cancelOrder, submitPayment, submitBuyerReview, submitOrder, paymentRequest, initiateReleasePayment, notifyBuyerAboutShipping, initiateRefundForCancelledOrder, initiateRefundForDefectiveItem, notifyCancelledOrder, uploadTrackingDetails, receiveDeliveryConfirmation, notifyDefectiveItem, submitMerchantReview, orderRejection

adapter = Adapter(eBay, BuyerSeller.protocol, config_a)
logger = logging.getLogger("eBay")
logging.getLogger('bungie').setLevel(logging.INFO)

def get_bindings(adapter, orderIDKey):

    return adapter.history.contexts.subcontexts['orderID'][orderIDKey].bindings

@adapter.reaction(placeOrder)
async def receive_order(message):
    logger.info(str(message['orderID']) + " Order received and waiting for the payment")

@adapter.reaction(acceptOrder)
async def updating_order_status_as_in_progress(message):
    logger.info(str(message['orderID']) + " Order accepted by merchant and status is updated as in progress in eBay website")

@adapter.reaction(uploadTrackingDetails)
async def notify_buyer_about_shipping(message):
    logger.info(str(message['orderID']) + " tracking id updated in the eBay website. notifying shipping details to the buyer")
    adapter.send(
        notifyBuyerAboutShipping(shippingStatus='shipping status', **message.payload)
    )

@adapter.reaction(submitBuyerReview)
async def submit_buyer_review(message):
    if {'itemPrice', 'orderID', 'paymentDone'}.issubset(set(get_bindings(adapter, message['orderID']).keys())):
        logger.info(str(message['orderID']) + " transaction review submitted by the buyer")
    else:
        logger.info(str(message['orderID']) + " buyer transaction review cannot be submitted before both placing order and submitting payment are done")

@adapter.reaction(submitMerchantReview)
async def submit_merchant_review(message):
    if {'itemPrice', 'orderID', 'paymentDone'}.issubset(set(get_bindings(adapter, message['orderID']).keys())):
        logger.info(str(message['orderID']) + " transaction review submitted by the merchant")
    else:
        logger.info(str(message['orderID']) + " merchant transaction review cannot be submitted before properly before receiving both order and payment")

@adapter.enabled(submitOrder)
async def submit_order(message):
    logger.info(str(message['orderID']) + " Order placed and payment done. So being forwarded to the merchant")
    message["merchantID"] = "merchant id"
    adapter.send(submitOrder(**message.payload))

@adapter.enabled(paymentRequest)
async def submit_payment_request(message):
    logger.info(str(message['orderID']) + " Submitting payment request to the paypal")
    message['onHold'] = 'true'
    adapter.send(paymentRequest(**message.payload))

@adapter.reaction(receiveDeliveryConfirmation)
async def initiate_payment_release(message):
    logger.info(str(message['orderID']) + " Delivery confirmation received. Requesting paypal to release payment hold")
    adapter.send(
        initiateReleasePayment(releaseHold='true', **message.payload)
    )

@adapter.reaction(notifyDefectiveItem)
async def defective_item_notification_from_merchant(message):
    logger.info(str(message['orderID']) + " Defective item notified by the merchant. Requesting refund with paypal for this defective item")
    adapter.send(
        initiateRefundForDefectiveItem(
            itemPrice=get_bindings(adapter, message['orderID'])['itemPrice'],
            defectiveRefund='refund for defective item',
            **message.payload
        )
    )

@adapter.reaction(rejectOrder)
async def notify_and_pay_for_order_rejection_to_buyer(message):
    logger.info(str(message['orderID']) + " Notifying about order rejection to the buyer")
    adapter.send(
        orderRejection(
            merchantID=get_bindings(adapter, message['orderID'])['merchantID'],
            **message.payload
        )
    )
    await asyncio.sleep(2)
    adapter.send(
        initiateRefundForCancelledOrder(
            itemPrice=get_bindings(adapter, message['orderID'])['itemPrice'],
            cancelledRefund='refund for merchant cancelled order',
            **message.payload
        )
    )

@adapter.reaction(cancelOrder)
async def cancel_order(message):
    bindings = get_bindings(adapter, message['orderID'])
    context_set = set(bindings.keys())
    if {'itemPrice', 'orderID', 'paymentDone'}.issubset(context_set):
        if {'trackingID'}.issubset(context_set):
            logger.info(str(message['orderID']) + " Order cannot be cancelled now as it is already sent for shipping")
        else:
            merchant_id = bindings['merchantID']
            item_price = bindings['itemPrice']
            logger.info(str(message['orderID']) + " Order cancelled before shipping. so initiating refund")
            adapter.send(
                notifyCancelledOrder(
                    merchantID=merchant_id,
                    cancelledNotification='true',
                    **message.payload
                )
            )
            await asyncio.sleep(0)
            adapter.send(
                initiateRefundForCancelledOrder(
                    itemPrice=item_price,
                    cancelledRefund = 'refund for cancelled order',
                    **message.payload
                )
            )
    else:
        logger.info(str(message['orderID']) + " Order cancelled on eBay side as per the buyer request. No refund provided because there was not payment done for this order")

if __name__ == "__main__":
    print("Starting eBay...")
    adapter.start()
