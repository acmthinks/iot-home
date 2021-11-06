# Install as a system Service
Place 'subscribeGateOpen.service` in /etc/systemd/system/
Install the service 
```
systemctl enable subscribeGateOpen
systemctl daemon-reload
systemctl start subscribeGateOpen
```

## Check to validate service is running
```
systemctl | grep running
```