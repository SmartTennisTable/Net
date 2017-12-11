#!/usr/bin/python
import requests
import json
import time
import os
import signal
import subprocess
# import RPi.GPIO as GPIO
import sttiot

# SET GPIO to default
# sttiot.initGPIO()
status = False

print("Waiting instructions from SAP Cloud Platform - IOTMMS - P1942978066")

while status == False:
    response = sttiot.initPi()

    contentMsg = json.loads(response.text)
    taille = len(contentMsg)

    if taille >= 0:
        for i in range(0, taille):
            function = contentMsg[i]['messages'][0]['function']
            action = contentMsg[i]['messages'][0]['action']
            print(function)

            if function == "init":
                execfile("./netApp.py")
            elif function == "shutdown":
                execfile("./shutdown.sh")
            else:
                print("ERROR 101 : WRONG FUNCTION")

    time.sleep(0.5)
