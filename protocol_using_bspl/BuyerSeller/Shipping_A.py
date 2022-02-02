from bungie import Adapter, Remind, Scheduler
from configuration import config_a
import asyncio
import logging
import BuyerSeller
from BuyerSeller import Shipping, sendToShipping, packAndShipItem, provideTrackingInfo, receiveItem, sendDeliveryConfirmation, reportDefectiveItem

adapter = Adapter(Shipping, BuyerSeller.protocol, config_a)
logger = logging.getLogger("Shipping")
logging.getLogger('bungie').setLevel(logging.INFO)
trackingID = 'tracking id'

@adapter.reaction(sendToShipping)
async def provide_tracking_info(message):
    logger.info(str(message['orderID']) + " Received shipping request from merchant")
    logger.info(str(message['orderID']) + " Providing tracking info to the merchant")
    adapter.send(
        provideTrackingInfo(trackingID=trackingID, **message.payload)
    )

@adapter.reaction(sendToShipping)
async def shipping_request(message):
    logger.info(str(message['orderID']) + " Packing and shipping the item to buyer")
    await asyncio.sleep(3)
    if message['orderID'] == 'order_ID6':
        logger.info(str(message['orderID']) + " Identified a defective item. Reporting it to the merchant")
        adapter.send(
            reportDefectiveItem(
                defectFound='true',
                **message.payload
            )
        )
    else:
        adapter.send(
            packAndShipItem(trackingID=trackingID, **message.payload)
    )

@adapter.enabled(sendDeliveryConfirmation)
async def delivery_confirmation(message):
    logger.info(str(message['orderID']) + " Confirming delivery with the merchant")
    adapter.send(
        sendDeliveryConfirmation(**message.payload)
    )

if __name__ == "__main__":
    print("Starting Shipping...")
    adapter.start()
