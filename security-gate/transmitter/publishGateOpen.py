import sys
import configparser
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import RPi.GPIO as GPIO
import time

scriptName = sys.argv[0]
print ("Running: " + scriptName)
localPath = scriptName.rsplit('/', 1)[0]
if scriptName == localPath: 
    localPath = ""
else:
    localPath = localPath + "/"
print ("localPath: " + localPath)


# read configuration file
config = configparser.ConfigParser()
configFilePath = localPath + 'transmitter.ini'
config.read(configFilePath)

# read configuration parms
clientId = config.get('aws-iot-config', 'clientId')
awsEndpoint = config.get('aws-iot-config', 'awsEndpoint')
topic = config.get('aws-iot-config', 'MQTTtopic')
buttonPin = int(config.get('raspberry-pi', 'buttonPin'))
buttonLEDPin = int(config.get('raspberry-pi', 'buttonLEDPin'))
key = localPath + config.get('aws-iot-config', 'key')
cert = localPath + config.get('aws-iot-config', 'cert')
rootCA = localPath + config.get('aws-iot-config', 'rootCA')
print ("ClientId: " + clientId)
print ("AWSEndPoint: " + awsEndpoint)
print ("topic:" + topic)
print ("key: " + key)
print ("cert: " + cert)
print ("rootCA" + rootCA)
print ("buttonPin: " + str(buttonPin))
print ("buttonLEDPin: " + str(buttonLEDPin))

#initialize button
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#listen for button event
GPIO.add_event_detect(buttonPin,GPIO.RISING)

#connect to Cloud MQTT service endpoint (with certs)
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(awsEndpoint, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCA, key, cert)

while True:
    
    # waiting for button press
    if GPIO.event_detected(buttonPin) :
        #connect to MQTT Gateway
        myAWSIoTMQTTClient.connect()
        print ("Publish: OPEN Gate")
        myAWSIoTMQTTClient.publish(topic,"OPEN", 0)
        print ("Publish: End")
        myAWSIoTMQTTClient.disconnect()
        time.sleep(1)
