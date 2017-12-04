#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setwarnings(False)

#Boucle 3 secondes
for i in range(0, 15):
	print("LED on")
	GPIO.output(18, True)
	time.sleep(0.2)
	print("LED off")
	GPIO.output(18, False)
	time.sleep(0.2)
	i = i + 1

GPIO.output(18, False)
GPIO.cleanup()
sys.exit()