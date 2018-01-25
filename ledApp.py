#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys
import sttiot

sttiot.initGPIO()

#Boucle 1 secondes
for i in range(0, 5):
	print("LED on")
	GPIO.output(sttiot.REDPIN, True)
	time.sleep(0.1)
	print("LED off")
	GPIO.output(sttiot.REDPIN, False)
	time.sleep(0.1)
	i = i + 1

GPIO.output(sttiot.REDPIN, False)
GPIO.cleanup()
sys.exit()
