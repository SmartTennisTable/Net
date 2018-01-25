#!/usr/bin/python
import requests
import json
import time
import os
import signal
import subprocess
import RPi.GPIO as GPIO
import sttiot
import paho.mqtt.client as mqtt

# SET GPIO to default
sttiot.initGPIO()
taille = 0

client = mqtt.Client()
client.on_connect = sttiot.on_connect
client.on_message = sttiot.on_message
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




