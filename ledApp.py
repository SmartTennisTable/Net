#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys
import sttiot

sttiot.initGPIO()

#Boucle 3 secondes
for i in range(0, 15):
	print("LED on")
	GPIO.output(sttiot.REDPIN, True)
	time.sleep(0.2)
	print("LED off")
	GPIO.output(sttiot.REDPIN, False)
	time.sleep(0.2)
	i = i + 1

GPIO.output(sttiot.REDPIN, False)
GPIO.cleanup()
sys.exit()
