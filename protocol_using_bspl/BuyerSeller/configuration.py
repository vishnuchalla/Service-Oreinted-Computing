from protocheck import bspl

buyerseller = bspl.load_file("buyer-seller-protocol.bspl").export("BuyerSeller")
from BuyerSeller import eBay, Paypal, Merchant, Shipping
from BuyerSeller import Buyer as Buyer_A
from BuyerSeller import Buyer as Buyer_B

from BuyerSeller import (
    initiateReleasePayment,
    releasePayment,
    receiveItem,
    acceptOrder,
    rejectOrder,
    orderRejection,
    sendDeliveryConfirmation,
    notifyBuyerAboutShipping,
    sendToShipping,
    initiateRefundForCancelledOrder,
    reportDefectiveItem,
    cancelOrder,
    placeOrder,
    uploadTrackingDetails,
    initiateRefundForDefectiveItem,
    submitPayment,
    receiveDeliveryConfirmation,
    notifyDefectiveItem,
    notifyCancelledOrder,
    submitBuyerReview,
    submitMerchantReview,
    notifyMerchantAboutPayment,
    submitOrder,
    packAndShipItem,
    doRefundForCancelledOrder,
    paymentRequest,
    provideTrackingInfo,
    doRefundForDefectiveItem,
)

config_a = {
    Buyer_A: ("0.0.0.0", 8000),
    eBay: ("0.0.0.0", 8001),
    Paypal: ("0.0.0.0", 8002),
    Merchant: ("0.0.0.0", 8003),
    Shipping: ("0.0.0.0", 8004),
    Buyer_B: ("0.0.0.0", 8005),
}
