#!/usr/bin/env bash
set -euo pipefail

# python traditional-packer.py &
python3 packer.py &
PACKER=$!

python3 wrapper.py &
WRAPPER=$!

python3 labeler.py &
LABELER=$!

sleep 2
python3 merchant.py &
MERCHANT=$!

read -n1 -rsp $'Press any key to stop...\n'

kill $PACKER $WRAPPER $LABELER $MERCHANT



