import requests
import json
import time
import os
import signal
import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setwarnings(False)

#HTTP Get pour recuperer les messages dans SCP
url = "https://iotmmsp1942964683trial.hanatrial.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/5658888b-3302-490c-a813-004ad9645613"

headers = {
	'content-type': "application/json;charset=utf-8",
	'authorization': "Bearer 4298a54b80cd4d3d2f4c448db253c9",
	'cache-control': "no-cache",
	}

print("En attente du lancement programme depuis SCP")

status = False

while status == False:
	response = requests.request("GET", url, headers=headers)
	responseTable = json.loads(response.text)
	taille = len(responseTable)

	for i in range(0, taille):
		print(responseTable[i]['messages'][0]['status'])
		status = responseTable[i]['messages'][0]['status']

	if status == True:
		subprocess.Popen("python ./netApp.py", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

	time.sleep(0.5)