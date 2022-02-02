#!/usr/bin/env bash
set -euo pipefail

python3 Merchant_A.py &
MERCHANT=$!

python3 Ebay_Org.py &
EBAY=$!

python3 Paypal_Org.py &
PAYPAL=$!

python3 Shipping_A.py &
SHIPPING=$!

sleep 2
python3 Buyer_A.py &
BUYER_A=$!

read -n1 -rsp $'Press any key to stop...\n'

kill $BUYER_A

python3 Buyer_B.py &
BUYER_B=$!

read -n1 -rsp $'Press any key to stop...\n'

kill $MERCHANT, $BUYER_B, $EBAY, $SHIPPING, $PAYPAL