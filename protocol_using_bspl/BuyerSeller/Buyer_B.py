from bungie import Adapter, Remind, Scheduler
from configuration import config_a
import asyncio
import logging
import BuyerSeller
from BuyerSeller import placeOrder, cancelOrder, submitPayment, submitBuyerReview, notifyBuyerAboutShipping, \
    doRefundForCancelledOrder, doRefundForDefectiveItem, packAndShipItem, receiveItem, orderRejection
from BuyerSeller import Buyer as Buyer_B

adapter = Adapter(Buyer_B, BuyerSeller.protocol, config_a)
logger = logging.getLogger("buyer_b")
logging.getLogger('bungie').setLevel(logging.INFO)

@adapter.reaction(orderRejection)
async def order_rejection_notification(message):
    logger.info(str(message['orderID']) + " Notification received at buyer end about merchant rejected order")

@adapter.reaction(doRefundForCancelledOrder)
async def refund_notification_for_cancelled_order(message):
    logger.info(str(message['orderID']) + " refund received by the buyer for the cancelled order")

# Case where merchant rejects the order.
async def enactment_1():
    await asyncio.sleep(1)
    logger.info("placing order_ID7")
    adapter.send(
        placeOrder(
            buyerID='buyer id',
            orderID='order_ID7',
            itemName='item name',
            buyerAddress='buyer address',
            buyerName='buyer name',
        )
    )
    await asyncio.sleep(1)
    logger.info("submitting payment for the order_ID7")
    adapter.send(
        submitPayment(
            buyerID='buyer id',
            orderID='order_ID7',
            itemPrice='item price',
            paymentDone='success',
        )
    )
    await asyncio.sleep(1)
    logger.info("submitting buyer review for the order_ID7")
    adapter.send(
        submitBuyerReview(
            buyerID='buyer id',
            orderID='order_ID7',
            buyerReviewMessage='buyer review message',
            buyerReviewDone='true',
        )
    )

# Case where buyer cancels the order before merchant tries to reject it.
async def enactment_2():
    await asyncio.sleep(5)
    logger.info("placing order_ID8")
    adapter.send(
        placeOrder(
            buyerID='buyer id',
            orderID='order_ID8',
            itemName='item name',
            buyerAddress='buyer address',
            buyerName='buyer name',
        )
    )

    await asyncio.sleep(1)
    logger.info("submitting payment for the order_ID8")
    adapter.send(
        submitPayment(
            buyerID='buyer id',
            orderID='order_ID8',
            itemPrice='item price',
            paymentDone='success',
        )
    )

    await asyncio.sleep(1)
    logger.info("submitting buyer review for the order_ID8")
    adapter.send(
        submitBuyerReview(
            buyerID='buyer id',
            orderID='order_ID8',
            buyerReviewMessage='buyer review message',
            buyerReviewDone='true',
        )
    )

    await asyncio.sleep(1)
    logger.info("cancel requested for the order_ID8")
    adapter.send(
        cancelOrder(
            buyerID='buyer id',
            orderID='order_ID8',
            isCancelled='true',
        )
    )


if __name__ == "__main__":
    logger.info("Starting Buyer B...")
    adapter.start(enactment_1(), enactment_2())
