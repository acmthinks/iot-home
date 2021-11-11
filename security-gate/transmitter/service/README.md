# Install as a system Service

## Configure and Install the "Front Gate Controller Transmitter Service"
1. update `publishGateOpen.service` with the correct (absolute) path for `ExecStart`. 
2. Place `publishGateOpen.service` in `/etc/systemd/system/`. If you have placed this repo in /home/pi, you can use the following copy command.
```
sudo cp ~/iot-home/security-gate/transmitter/service/publsihGateOpen.service /etc/systemd/system/
chmod 755 /etc/systemd/system/publishGateOpen.service
```

##Enable the "Front Gate Controller Transmitter Service"
Use the `systemctl` command to enable the service to automatically run at system start up and if the service should go down.
```
systemctl enable publishGateOpen
systemctl daemon-reload
systemctl start publishGateOpen
```

## Check to validate service is running
```
systemctl | grep publishGateOpen
```
Validate that the status is "running"