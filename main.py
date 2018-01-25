#!/usr/bin/python
import requests
import json
import time
import os
import signal
import subprocess
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import sttiot


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
    print(msg.topic)
    payload = json.loads(msg.payload)
    function = payload['messages'][0]['function']
    action = payload['messages'][0]['action']

    if function == "init":
        execfile("/home/stt/net/netApp.py")


# SET GPIO to default
sttiot.initGPIO()
taille = 0


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("capllkmg", password="TYk-UHLw95TH")
client.connect("m14.cloudmqtt.com", 15839, 60)

client.loop_start()

while True:
    continue
    #response = sttiot.initPi()

    #contentMsg = json.loads(response.text)
    #taille = len(contentMsg)

    # if taille > 0:
    #     for i in range(0, taille):
    #         function = contentMsg[i]['messages'][0]['function']
    #         action = contentMsg[i]['messages'][0]['action']
    #         print(function)
    #
    #         if function == "init":
    #             execfile("./netApp.py")
    #         elif function == "shutdown":
    #             execfile("./shutdown.sh")
    #         else:
    #             print("ERROR 101 : WRONG FUNCTION")

    #time.sleep(0.5)




