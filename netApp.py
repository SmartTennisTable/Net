#!/usr/bin/python
#Marianne is better than Damien
import requests
import time
from adxl345 import ADXL345
from statistics import mean

liste_valeurs = list() #on cree une liste vide
liste_seuil = list() #on cree une liste seuil

adxl345 = ADXL345()
seuil = 0
indice_let = 1


def sendLetHTTP(let_time):
	url="https://iotmmsp1942964683trial.hanatrial.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/0f75c8e3-7852-4ab2-b561-408193b7d406"
	payload="{\"mode\":\"sync\", \"messageType\": \"db976d090e0969fcfdb6\", \"messages\":[{\"timestamp\":"+ let_time + "}]}"
	headers={
		'content-type': "application/json",
		'Authorization': "Bearer 6750b7da4256983e7780663680c0323d"
	}
	response = requests.request("POST", url, data=payload, headers=headers)
	print(response.text)
	time.sleep(2)


#on calibre l'accelerometre. il s'agit de trouver le seuil du LET. La calibration dure 3s.
print("L'etalonnage du capteur est en cours.")

while seuil == 0:
	if len(liste_seuil) >= 3000:
		seuil = mean(liste_seuil)
		seuil = seuil + seuil*0.1
		print("l'etalonnage du capteur est termine.")
		time.sleep(0.5)
		print("Le seuil est de : {}".format(seuil))
		time.sleep(0.5)
		print("Les echanges peuvent commencer.")

	axes = adxl345.getAxes(True)
	x = axes['x']
	y = axes['y']
	z = axes['z']
	somme_seuil = abs(z)

	liste_seuil.append(somme_seuil) #on ajoute la somme des valeurs seuils en fin de liste
	time.sleep(0.001)

#on lance le programme

while True:

	if len(liste_valeurs) >= 100:
		moyenne = mean(liste_valeurs)
		
		if moyenne > seuil:
			timeStamp = time.ctime()
			print("LET n{}; {}".format(indice_let, timeStamp))
			sendLetHTTP(timeStamp)
			indice_let = indice_let + 1
			time.sleep(1) #on attend 1s apres un let
		
		del liste_valeurs[:]

	axes = adxl345.getAxes(True)

	x = axes['x']
	y = axes['y']
	z = axes['z']
	somme_axes = abs(z)

	liste_valeurs.append(somme_axes) #on ajoute la somme des axes en fin de liste
	time.sleep(0.01)


