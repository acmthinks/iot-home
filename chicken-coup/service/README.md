# Install as a system Service

## Configure and Install the "Chicken Coup Light Service"
1. update `chickenCoupLight.service` with the correct (absolute) path for `ExecStart`. 
2. Place `chickenCoupLight.service` in `/etc/systemd/system/`. If you have placed this repo in /home/pi, you can use the following copy command.
```
sudo cp ~/iot-home/chicken-coup/service/chickenCoupLight.service /etc/systemd/system/
chmod 755 /etc/systemd/system/chickenCoupLight.service
```

##Enable the "Chicken Coup Light Service"
Use the `systemctl` command to enable the service to automatically run at system start up and if the service should go down.
```
systemctl enable chickenCoupLight
systemctl daemon-reload
systemctl start chickenCoupLight
```

## Check to validate service is running
```
systemctl | grep chickenCoupLight
```
Validate that the status is "running"