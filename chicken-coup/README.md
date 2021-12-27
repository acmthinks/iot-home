# Chicken Coup Light

0. Install the [Astral](https://pypi.org/project/astral/1.2/)
```
pip install astral
```

1. Install the [AWS IoT Python SDK](https://github.com/aws/aws-iot-device-sdk-python-v2)
```
sudo pip3 install awsiotsdk
```

2. Install [Sense HAT](https://www.raspberrypi.com/documentation/accessories/sense-hat.html)
```
sudo apt-get install sense-hat
```

3. Clone this repo. I prefer to install in my home directory under `dev`.
```
mkdir ~/dev
cd ~/dev
git clone https://github.com/acmthinks/iot-home.git
```
4. Optional. Install the ["Chicken Coup Light Service"](service/README.md) 


5. Optional. If you want to have remote ssh access to your transmitter, remember to `sudo raspi-config` and enable SSH.


6. Optional. Enable PiCamera to stream video feeds.
```
sudo raspi-config
```
Select Interfaces, Enable Camera. Finish. In a Terminal window (on your Pi), launch the video camera stream
```
libcamera-vid -t 0 --inline --listen tcp://0.0.0.0.:8888
```

On a seperate computer, install [VLC](https://www.videolan.org). Open Network and enter in the following URL
```
```
Here is a great tutorial on [How To Use Raspberry Pi Cameras with Bullseye](https://www.tomshardware.com/how-to/use-raspberry-pi-camera-with-bullseye)
