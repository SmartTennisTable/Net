import requests
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from getch import getch


# IoT - SENSOR_NET
SENSOR_NET_MESSAGE_ID = 'be4cb53c070a4aa01e96'

# IoT - INITPI_TABLE
INITPI_TABLE_MESSAGE_ID = '1b9af893f8531cfc0b71'

# IoT - STTPie
STTPIE_DEVICE_ID = '85732072-22b7-4cd1-ae8f-d363975c0f91'
STTPIE_OAUTH_TOKEN = 'a8baa42b505b82ad0455643f8bed3a6'
STTPIE_OAUTH_TOKEN = '67d2e8899a1f4eb4e972af17375d3f50'

# IoT - IOTMMS
IOTMMS_HTTP = 'https://iotmmsp1942978066trial.hanatrial.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/'

# VARIABLES PIN LED RGB
BLUEPIN = 14
GREENPIN = 15
REDPIN = 18

def initGPIO():
    GPIO.setmode(GPIO.BCM)
#    GPIO.setup(BLUEPIN, GPIO.OUT)  # BLUE
#    GPIO.setup(GREENPIN, GPIO.OUT)  # GREEN
    GPIO.setup(REDPIN, GPIO.OUT)  # RED
    GPIO.setwarnings(False)


def initPi():
    url = IOTMMS_HTTP + STTPIE_DEVICE_ID
    headers = {
        'content-type': "application/json;charset=utf-8",
        'authorization': "Bearer " + STTPIE_OAUTH_TOKEN,
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)
    return response


def sendLet(ID_TABLE, ID_MATCH, indice_let, timestamp):
    url = IOTMMS_HTTP + STTPIE_DEVICE_ID
    payload = '{"mode":"sync", "messageType": "' + SENSOR_NET_MESSAGE_ID + '", "messages":[{"id_table": ' + str(ID_TABLE) + ', "id_match": ' + str(ID_MATCH) + ', "id_let": ' + str(indice_let) + ', "timestamp":' + str(
        timestamp) + '}]}'
    headers = {
        'content-type': "application/json",
        'Authorization': "Bearer " + STTPIE_OAUTH_TOKEN
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    time.sleep(2)


TOPIC_PUSH = "iot/data/iotmmsp1942978066trial/v1/85732072-22b7-4cd1-ae8f-d363975c0f91"
TOPIC_PULL = "iot/push/iotmmsp1942978066trial/v1/85732072-22b7-4cd1-ae8f-d363975c0f91"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if (rc == 0):
        print("Waiting instructions from SAP Cloud Platform - IOTMMS - P1942978066")
    else:
        print("Connection aborted")
    #FromDevice
    client.subscribe((TOPIC_PUSH, 1))
    #ToDevice
    client.subscribe((TOPIC_PULL, 1))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))