#!/bin/sh

#subscriber
python3 subscribeGateOpen.py --endpoint a2mtj60ceepah6-ats.iot.us-east-1.amazonaws.com --root-ca certs/AmazonRootCA1.pem --cert certs/device.pem.crt --key certs/private.pem.key --client-id front-gate-controller --topic "gate/control" --message "OPEN" --count 5

