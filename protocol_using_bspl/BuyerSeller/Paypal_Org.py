from bungie import Adapter, Remind, Scheduler
from configuration import config_a
import logging
import BuyerSeller
from BuyerSeller import Paypal, paymentRequest, initiateReleasePayment, initiateRefundForCancelledOrder, initiateRefundForDefectiveItem, notifyMerchantAboutPayment, doRefundForCancelledOrder, doRefundForDefectiveItem, releasePayment

adapter = Adapter(Paypal, BuyerSeller.protocol, config_a)
logger = logging.getLogger("Paypal")
logging.getLogger('bungie').setLevel(logging.INFO)

@adapter.reaction(paymentRequest)
async def receive_payment_request(message):
    logger.info(str(message['orderID']) + " Payment request received by paypal. Putting the order payment on hold until the delivery")
    adapter.send(notifyMerchantAboutPayment(**message.payload))

@adapter.enabled(releasePayment)
async def release_payment(message):
    adapter.send(
        releasePayment(**message.payload)
    )
    logger.info(str(message['orderID']) + " Releasing the payment on hold. As the eBay has confirmed the delivery")

@adapter.reaction(initiateRefundForCancelledOrder)
async def refund_for_cancelled_order(message):
    logger.info(str(message['orderID']) + " deleting the previous payment request to merchant which was on hold")
    logger.info(str(message['orderID']) + " performing refund to the buyer for a cancelled order")
    adapter.send(
        doRefundForCancelledOrder(**message.payload)
    )

@adapter.reaction(initiateRefundForDefectiveItem)
async def refund_for_defective_order(message):
    logger.info(str(message['orderID']) + " deleting the previous payment request to merchant which was on hold")
    logger.info(str(message['orderID']) + " performing refund to the buyer for a defective order")
    adapter.send(
        doRefundForDefectiveItem(**message.payload)
    )

if __name__ == "__main__":
    print("Starting PayPal...")
    adapter.start()
