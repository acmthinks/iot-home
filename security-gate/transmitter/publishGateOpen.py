import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient("front-gate-app")
myAWSIoTMQTTClient.configureEndpoint("a2mtj60ceepah6-ats.iot.us-east-1.amazonaws.com", 8883)
myAWSIoTMQTTClient.configureCredentials("certs/AmazonRootCA1.pem", "certs/private.pem.key", "certs/device.pem.crt")

myAWSIoTMQTTClient.connect()

print ("Publish: OPEN Gate")

myAWSIoTMQTTClient.publish("gate/control","OPEN", 0)
print ("Publish: End")

myAWSIoTMQTTClient.disconnect()
