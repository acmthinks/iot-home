# Install as a system Service

## Configure and Install the "Front Gate Controller Service"
1. update `subscribeGateOpen.service` with the correct (absolute) path for `ExecStart`. 
2. Place `subscribeGateOpen.service` in `/etc/systemd/system/`. If you have placed this repo in /home/pi, you can use the following copy command.
```
sudo cp ~/iot-home/security-gate/receiver/service/subscribeGateOpen.service /etc/systemd/system/
chmod 755 /etc/systemd/system/subscribeGateOpen.service
```

##Enable the "Front Gate Controller Service"
Use the `systemctl` command to enable the service to automatically run at system start up and if the service should go down.
```
systemctl enable subscribeGateOpen
systemctl daemon-reload
systemctl start subscribeGateOpen
```

## Check to validate service is running
```
systemctl | grep subscribeGateOpen
```
Validate that the status is "running"