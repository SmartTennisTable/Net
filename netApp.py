#!/usr/bin/python
import requests
import time
import os
import subprocess
from adxl345 import ADXL345
from statistics import mean
import sttiot
import RPi.GPIO as GPIO

sttiot.initGPIO()

liste_valeurs = list()  # on cree une liste vide
liste_seuil = list()  # on cree une liste seuil

adxl345 = ADXL345()
seuil = 0
indice_let = 1
ID_TABLE = 0
ID_MATCH = 0

#on demande un ID de match et de table
ID_MATCH = int(input("Id du match : "))
ID_TABLE = int(input("Id de la table : "))

# on calibre l'accelerometre. il s'agit de trouver le seuil du LET. La calibration dure 3s.
print("L'etalonnage du capteur est en cours.")
#GPIO.output(sttiot.BLUEPIN, True)

while seuil == 0:
    if len(liste_seuil) >= 3000:
        seuil = mean(liste_seuil)
        seuil = seuil + seuil * 0.1
        print("l'etalonnage du capteur est termine.")
        time.sleep(0.5)
        print("Le seuil est de : {}".format(seuil))
        time.sleep(0.5)
        print("Les echanges peuvent commencer.")
#        GPIO.output(sttiot.BLUEPIN, False)
        time.sleep(0.2)
        for i in range(0, 2):
#            GPIO.output(sttiot.GREENPIN, True)
            time.sleep(0.2)
#            GPIO.output(sttiot.GREENPIN, False)
            time.sleep(0.2)

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
            #diode = subprocess.Popen("python ./ledApp.py", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            #sendLetHTTP(timeStamp)
            sttiot.sendLet(ID_TABLE, ID_MATCH, indice_let, timeStamp)
            
            for j in range(0, 5):
                print("LED on")
                GPIO.output(sttiot.REDPIN, True)
                time.sleep(0.1)
                print("LED off")
                GPIO.output(sttiot.REDPIN, False)
                time.sleep(0.1)
                j = j + 1
            
            indice_let = indice_let + 1
        del liste_valeurs[:]

    axes = adxl345.getAxes(True)

    x = axes['x']
    y = axes['y']
    z = axes['z']
    somme_axes = abs(z)

    liste_valeurs.append(somme_axes)  # on ajoute la somme des axes en fin de liste
    time.sleep(0.01)
