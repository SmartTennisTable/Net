#HTTP Get to retrieve SCP messages

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

url = "https://iotmmsp1942964683trial.hanatrial.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/9f7e901a-1b4d-4d3f-a92b-59a84f3adddc"

headers = {
	'content-type': "application/json;charset=utf-8",
	'authorization': "Bearer c862efa6f983b7d396a96966cbbc8f6c",
	'cache-control': "no-cache",
	}

diode = ""

while True:
	response = requests.request("GET", url, headers=headers)
	responseTable = json.loads(response.text)
	taille = len(responseTable)

	for i in range(0, taille):
		print(responseTable[i]['messages'][0]['status'])
		status = responseTable[i]['messages'][0]['status']

		if status == True:
			#print("Led on")
			if diode == "":
				diode = subprocess.Popen("python ./ledApp.py", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
			else:
				print("LED already triggered")

		elif status == False:
				os.killpg(diode.pid, signal.SIGTERM)
				GPIO.output(18, False)
				diode = ""

	time.sleep(0.5)
