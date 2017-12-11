import requests
import time
#import RPi.GPIO as GPIO

#IoT - SENSOR_NET
SENSOR_NET_MESSAGE_ID = 'be4cb53c070a4aa01e96'

#IoT - INITPI_TABLE
INITPI_TABLE_MESSAGE_ID = '1b9af893f8531cfc0b71'

#IoT - STTPie
STTPIE_DEVICE_ID = '85732072-22b7-4cd1-ae8f-d363975c0f91'
STTPIE_OAUTH_TOKEN = 'a8baa42b505b82ad0455643f8bed3a6'

#IoT - IOTMMS
IOTMMS_HTTP = 'https://iotmmsp1942978066trial.hanatrial.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/'

def initGPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18, GPIO.OUT)
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

def sendLet(id_table, id_match, id_let, timestamp):
	url = IOTMMS_HTTP + STTPIE_DEVICE_ID
	payload='{"mode":"sync", "messageType": "'+ SENSOR_NET_MESSAGE_ID +'", "messages":[{"id_table": 0, "id_match": 0, "id_let": 0, "timestamp":'+ str(timestamp) +'}]}'
	headers={
		'content-type': "application/json",
		'Authorization': "Bearer " + STTPIE_OAUTH_TOKEN
	}
	response = requests.request("POST", url, data=payload, headers=headers)
	print(response.text)
	time.sleep(2)