from bungie import Adapter, Remind, Scheduler
from configuration import config_a
import asyncio
import logging
import BuyerSeller
from BuyerSeller import placeOrder, cancelOrder, submitPayment, submitBuyerReview, notifyBuyerAboutShipping, doRefundForCancelledOrder, doRefundForDefectiveItem, packAndShipItem, receiveItem, orderRejection
from BuyerSeller import Buyer as Buyer_A

adapter = Adapter(Buyer_A, BuyerSeller.protocol, config_a)
logger = logging.getLogger("buyer_a")
logging.getLogger('bungie').setLevel(logging.INFO)

@adapter.reaction(packAndShipItem)
async def item_received(message):
    await asyncio.sleep(5)
    logger.info(str(message['orderID']) + " Item received by the buyer")
    adapter.send(
        receiveItem(deliveryConfirmation='success', **message.payload)
    )

@adapter.reaction(notifyBuyerAboutShipping)
async def shipping_details_received(message):
    logger.info(str(message['orderID']) + " Received shipping details and tracking id from eBay website")

@adapter.reaction(doRefundForCancelledOrder)
async def refund_notification_for_cancelled_order(message):
    logger.info(str(message['orderID']) + " refund received by the buyer for the cancelled order")

@adapter.reaction(doRefundForDefectiveItem)
async def refund_notification_for_defective_order(message):
    logger.info(str(message['orderID']) + " refund received by the buyer for the defective order")

# Case where an order is placed successfully.
async def enactment_1():
    await asyncio.sleep(1)
    logger.info("placing order_ID1")
    adapter.send(
        placeOrder(
            buyerID='buyer id',
            orderID='order_ID1',
            itemName='item name',
            buyerAddress='buyer address',
            buyerName='buyer name',
        )
    )
    await asyncio.sleep(1)
    logger.info("submitting payment for the order_ID1")
    adapter.send(
        submitPayment(
            buyerID='buyer id',
            orderID='order_ID1',
            itemPrice='item price',
            paymentDone='success',
        )
    )
    await asyncio.sleep(1)
    logger.info("submitting buyer review for the order_ID1")
    adapter.send(
        submitBuyerReview(
            buyerID='buyer id',
            orderID='order_ID1',
            buyerReviewMessage='buyer review message',
            buyerReviewDone='true',
        )
    )

# Case where buyer tries to submit review without properly placing an order.
async def enactment_2():
    await asyncio.sleep(2)
    logger.info("placing order_ID2")
    adapter.send(
        placeOrder(
            buyerID='buyer id',
            orderID='order_ID2',
            itemName='item name',
            buyerAddress='buyer address',
            buyerName='buyer name',
        )
    )

    await asyncio.sleep(1)
    logger.info("submitting buyer review for the order_ID2")
    adapter.send(
        submitBuyerReview(
            buyerID='buyer id',
            orderID='order_ID2',
            buyerReviewMessage='buyer review message',
            buyerReviewDone='true',
        )
    )

    await asyncio.sleep(1)
    logger.info("submitting payment for the order_ID2")
    adapter.send(
        submitPayment(
            buyerID='buyer id',
            orderID='order_ID2',
            itemPrice='item price',
            paymentDone='success',
        )
    )

# Case where buyer cancels the order without payment.
async def enactment_3():
    await asyncio.sleep(3)
    logger.info("placing order_ID3")
    adapter.send(
        placeOrder(
            buyerID='buyer id',
            orderID='order_ID3',
            itemName='item name',
            buyerAddress='buyer address',
            buyerName='buyer name',
        )
    )

    await asyncio.sleep(1)
    logger.info("cancel requested for the order_ID3")
    adapter.send(
        cancelOrder(
            buyerID='buyer id',
            orderID='order_ID3',
            isCancelled='true',
        )
    )

# Case where buyer cancels the order before shipping.
async def enactment_4():
    await asyncio.sleep(5)
    logger.info("placing order_ID4")
    adapter.send(
        placeOrder(
            buyerID='buyer id',
            orderID='order_ID4',
            itemName='item name',
            buyerAddress='buyer address',
            buyerName='buyer name',
        )
    )

    await asyncio.sleep(1)
    logger.info("submitting payment for the order_ID4")
    adapter.send(
        submitPayment(
            buyerID='buyer id',
            orderID='order_ID4',
            itemPrice='item price',
            paymentDone='success',
        )
    )

    await asyncio.sleep(1)
    logger.info("submitting buyer review for the order_ID4")
    adapter.send(
        submitBuyerReview(
            buyerID='buyer id',
            orderID='order_ID4',
            buyerReviewMessage='buyer review message',
            buyerReviewDone='true',
        )
    )

    await asyncio.sleep(1)
    logger.info("cancel requested for the order_ID4")
    adapter.send(
        cancelOrder(
            buyerID='buyer id',
            orderID='order_ID4',
            isCancelled='true',
        )
    )

# Case where buyer tries to cancel the order after shipping.
async def enactment_5():
    await asyncio.sleep(10)
    logger.info("placing order_ID5")
    adapter.send(
        placeOrder(
            buyerID='buyer id',
            orderID='order_ID5',
            itemName='item name',
            buyerAddress='buyer address',
            buyerName='buyer name',
        )
    )

    await asyncio.sleep(1)
    logger.info("submitting payment for the order_ID5")
    adapter.send(
        submitPayment(
            buyerID='buyer id',
            orderID='order_ID5',
            itemPrice='item price',
            paymentDone='success',
        )
    )


    await asyncio.sleep(10)
    logger.info("cancel requested for the order_ID5")
    adapter.send(
        cancelOrder(
            buyerID='buyer id',
            orderID='order_ID5',
            isCancelled='true',
        )
    )

    await asyncio.sleep(1)
    logger.info("submitting buyer review for the order_ID5")
    adapter.send(
        submitBuyerReview(
            buyerID='buyer id',
            orderID='order_ID5',
            buyerReviewMessage='buyer review message',
            buyerReviewDone='true',
        )
    )

# Case where an defective item is reported while shipping.
async def enactment_6():
    await asyncio.sleep(5)
    logger.info("placing order_ID6")
    adapter.send(
        placeOrder(
            buyerID='buyer id',
            orderID='order_ID6',
            itemName='item name',
            buyerAddress='buyer address',
            buyerName='buyer name',
        )
    )
    await asyncio.sleep(1)
    logger.info("submitting payment for the order_ID6")
    adapter.send(
        submitPayment(
            buyerID='buyer id',
            orderID='order_ID6',
            itemPrice='item price',
            paymentDone='success',
        )
    )
    await asyncio.sleep(1)
    logger.info("submitting buyer review for the order_ID6")
    adapter.send(
        submitBuyerReview(
            buyerID='buyer id',
            orderID='order_ID6',
            buyerReviewMessage='buyer review message',
            buyerReviewDone='true',
        )
    )


if __name__ == "__main__":
    logger.info("Starting Buyer A...")
    adapter.start(enactment_1(), enactment_2(), enactment_3(), enactment_4(), enactment_6(), enactment_5())