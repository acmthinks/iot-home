import configparser
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import RPI.GPIO as GPIO
import time


# read configuration file
config = configparser.ConfigParser()
configFilePath = 'transmitter.ini'
config.read(configFilePath)
# read configuration parms
clientId = config.get('aws-iot-config', 'clientId')
awsEndpoint = config.get('aws-iot-config', 'awsEndpoint')
topic = config.get('aws-iot-config', 'MQTTtopic')
buttonPin = config.get('raspberry-pi', 'buttonPin')
buttonLEDPin = config.get('raspberry-pi', 'buttonLEDPin')
#print ("ClientId: " + clientId)
#print ("AWSEndPoint: " + awsEndpoint)
#print ("topic:" + topic)
print ("buttonPin: " + buttonPin)
print ("buttonLEDPin: " + buttonLEDPin)

#initialize button
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN)
#GPIO.setup(buttonLEDPin, GPIO.OUT)

#connect to Cloud MQTT service endpoint (with certs)
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(awsEndpoint, 8883)
myAWSIoTMQTTClient.configureCredentials("certs/AmazonRootCA1.pem", "certs/private.pem.key", "certs/device.pem.crt")

while True:
    myAWSIoTMQTTClient.connect()

    # Turn LED off
    #print ("LED off")
    #GPIO.output(21, GPIO.LOW)

    # waiting for button press
    while GPIO.input(buttonPin) == 1:
        time.sleep(0.2)
        
    # Open Gate/send signal
    #print ("LED on")
    #GPIO.output(21, GPIO.HIGH)

    print ("Publish: OPEN Gate")
    myAWSIoTMQTTClient.publish(topic,"OPEN", 0)
    print ("Publish: End")

    # waiting for button release
    while GPIO.input(buttonPin) == 0:
        time.sleep(0.2)  

    myAWSIoTMQTTClient.disconnect()
