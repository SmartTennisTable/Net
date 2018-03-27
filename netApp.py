#!/usr/bin/python
import requests
import time
import os
import subprocess
from adxl345 import ADXL345
from statistics import mean
import sttiot
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt


TOPIC_PUSH = "iot/data/iotmmsp1942978066trial/v1/85732072-22b7-4cd1-ae8f-d363975c0f91"
TOPIC_PULL = "iot/push/iotmmsp1942978066trial/v1/85732072-22b7-4cd1-ae8f-d363975c0f91"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if (rc == 0):
        print("Ready to push data to SAP Cloud Platform - IOTMMS - P1942978066")
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

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("capllkmg", password="TYk-UHLw95TH")
client.connect("m14.cloudmqtt.com", 15839, 60)

client.loop_start()

sttiot.initGPIO()

liste_valeurs = list()  # on cree une liste vide
liste_seuil = list()  # on cree une liste seuil

adxl345 = ADXL345()
seuil = 0
indice_let = 1
ID_TABLE = 0
ID_MATCH = 0

#on demande un ID de match et de table
ID_MATCH = int(input("ID match : "))
ID_TABLE = int(input("ID table : "))

# on calibre l'accelerometre. il s'agit de trouver le seuil du LET. La calibration dure 3s.
print("Calibration [IN PROGRESS]")

while seuil == 0:
	if len(liste_seuil) >= 3000:
		seuil = mean(liste_seuil)
		seuil = seuil + seuil * 0.1
		print("Calibration [OK]")
		GPIO.output(sttiot.GREENPIN, True)
		time.sleep(0.5)
		GPIO.output(sttiot.GREENPIN, False)

	axes = adxl345.getAxes(True)
	x = axes['x']
	y = axes['y']
	z = axes['z']
	somme_seuil = abs(z)

	liste_seuil.append(somme_seuil)  # on ajoute la somme des valeurs seuils en fin de liste
	time.sleep(0.001)

# on lance le programme Accelerometre
while True:
	if len(liste_valeurs) >= 100:
		moyenne = mean(liste_valeurs)

		if moyenne > seuil:
			timeStampPrint = time.ctime()
			timeStamp = str(int(time.time()))
			print("LET n {}; {}".format(indice_let, timeStampPrint))

			payload = '{"mode":"sync", "messageType": "' + sttiot.SENSOR_NET_MESSAGE_ID + '", "messages":[{"id_table": ' + str(
				ID_TABLE) + ', "id_match": ' + str(ID_MATCH) + ', "id_let": ' + str(
				indice_let) + ', "timestamp":' + str(timestamp) + '}]}'

			client.publish(TOPIC_PULL, payload)

			for j in range (0, 5):
				GPIO.output(sttiot.REDPIN, True)
				time.sleep(0.1)
				GPIO.output(sttiot.REDPIN, False)
				time.sleep(0.1)


			indice_let = indice_let + 1
		del liste_valeurs[:]

	axes = adxl345.getAxes(True)
	x = axes['x']
	y = axes['y']
	z = axes['z']
	somme_axes = abs(z)

	liste_valeurs.append(somme_axes)  # on ajoute la somme des axes en fin de liste
	time.sleep(0.001)
