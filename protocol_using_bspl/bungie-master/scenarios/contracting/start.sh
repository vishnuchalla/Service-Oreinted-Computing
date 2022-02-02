#!/usr/bin/env bash
set -euo pipefail

python contractor.py &
CONTRACTOR=$!

sleep 2
python government.py &
GOVERNMENT=$!



read -n1 -rsp $'Press any key to stop...\n'

kill $CONTRACTOR $GOVERNMENT
