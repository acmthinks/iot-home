# Install as a system Service
Place 'publishGateOpen.service` in /etc/systemd/system/
Install the service 
```
systemctl enable publishGateOpen
systemctl daemon-reload
systemctl start publishGateOpen
```

## Check to validate service is running
```
systemctl | grep running
```