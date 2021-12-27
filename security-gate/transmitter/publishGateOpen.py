"""
Provides publishing capability to an MQTT Topic
"""

import sys
import logging
import time
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from RPi import GPIO
import defs


#set localPath and accommodate invocation by systemd or by local
LOCAL_PATH=defs.setLocalPath(sys.argv[0])

# read configuration file
config = defs.getConfig(LOCAL_PATH, 'transmitter.ini')


FORMAT = '%(asctime)s - %(name)s - %(levelname)s:  %(message)s'
logger = logging.getLogger('publishGateOpen')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(FORMAT)
logger.addHandler(ch)

#logging.basicConfig(format=FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
#logging.basicConfig(filename="publishGateOpen.log", level=logging.INFO)

# read configuration parms
clientId = config.get('aws-iot-config', 'clientId')
awsEndpoint = config.get('aws-iot-config', 'awsEndpoint')
topic = config.get('aws-iot-config', 'MQTTtopic')
BUTTON_PIN = int(config.get('raspberry-pi', 'buttonPin'))
BUTTON_LED_PIN = int(config.get('raspberry-pi', 'buttonLEDPin'))
key = LOCAL_PATH + config.get('aws-iot-config', 'key')
cert = LOCAL_PATH + config.get('aws-iot-config', 'cert')
rootCA = LOCAL_PATH + config.get('aws-iot-config', 'rootCA')
print ("ClientId: " + clientId)
print ("AWSEndPoint: " + awsEndpoint)
print ("topic:" + topic)
print ("key: " + key)
print ("cert: " + cert)
print ("rootCA" + rootCA)
print ("buttonPin: " + str(BUTTON_PIN))
print ("buttonLEDPin: " + str(BUTTON_LED_PIN))

#initialize button
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#listen for button event
GPIO.add_event_detect(BUTTON_PIN,GPIO.RISING)

#connect to Cloud MQTT service endpoint (with certs)
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(awsEndpoint, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCA, key, cert)

while True:
    # waiting for button press
    if GPIO.event_detected(BUTTON_PIN) :
        #connect to MQTT Gateway
        logging.info("Connect to AWS IoT")
        myAWSIoTMQTTClient.connect()
        print ("Publish: OPEN Gate")
        logging.info("Gate OPEN")
        myAWSIoTMQTTClient.publish(topic,"OPEN", 0)
        print ("Publish: End")
        logging.info("Connect to AWS IoT")
        myAWSIoTMQTTClient.disconnect()
        time.sleep(1)
