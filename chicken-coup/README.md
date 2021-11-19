#Chicken Coup Light

0. Install the [Astral](https://pypi.org/project/astral/1.2/)
```
pip install astral
```

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
4. Optional. Install the ["Chicken Coup Light Service"](service/README.md) 


3. Optional. If you want to have remote ssh access to your transmitter, remember to `sudo raspi-config` and enable SSH.