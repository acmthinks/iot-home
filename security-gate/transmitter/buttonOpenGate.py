import sys
import time
import logging
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import defs
from gpiozero import Button
from signal import pause

#set localPath and accommodate invocation by systemd or by local
LOCAL_PATH=defs.set_local_path(sys.argv[0])

# read configuration file
config = defs.get_config(LOCAL_PATH, 'transmitter.ini')

#setup logging
FORMAT = '%(asctime)s - %(name)s - %(levelname)s:  %(message)s'
logger = logging.getLogger('buttonOpenGate')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(FORMAT)
logger.addHandler(ch)

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

#configure connection to Cloud MQTT service endpoint (with certs)
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(awsEndpoint, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCA, key, cert)

def open_gate():
    print("Sending OPEN signal to Front Gate")
    #connect to Cloud MQTT service endpoint (with certs)
    logging.info("Connect to AWS IoT")
    myAWSIoTMQTTClient.connect()
    print ("Publish: OPEN Gate")
    logging.info("Gate OPEN")
    myAWSIoTMQTTClient.publish(topic,"OPEN", 0)
    print ("Publish: End")
    logging.info("Connect to AWS IoT")
    myAWSIoTMQTTClient.disconnect()
    time.sleep(2)

print("Listening for Button...")

button = Button(BUTTON_PIN)

button.when_pressed = open_gate

pause()
