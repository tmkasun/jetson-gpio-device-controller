#!/usr/bin/env python3
import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)

while True:
    print("Turning on")
    GPIO.output(7, GPIO.LOW)
    time.sleep(2*60)
    print("turning off")
    GPIO.output(7, GPIO.LOW)
    time.sleep(2*60)


GPIO.cleanup()

