#Security Gate Receiver

0. Validate your version of `python` and `pip`. You will need minimal python 3.6. 

1. Install the [AWS IoT Python SDK](https://github.com/aws/aws-iot-device-sdk-python-v2)
```
sudo pip3 install awsiotsdk
```

2. Clone this repo. I prefer to install in my home directory under `dev`.
```
mkdir ~/dev
cd ~/dev
git clone https://github.com/acmthinks/iot-home.git
```
4. Optional. Install the ["Front Gate Controller Service"](service/README.md) 


3. Optional. If you want to have remote ssh access to your transmitter, remember to `sudo raspi-config` and enable SSH.