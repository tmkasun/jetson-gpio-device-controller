import Jetson.GPIO as GPIO
# from mockGPIO import GPIO
import time
import logging

class Device(object):
    def __init__(self, name, pin, direction=GPIO.OUT, initialState=GPIO.LOW):
        """
        Initialize a device to be controlled via GPIO
        """
        self.name = name
        GPIO.setmode(GPIO.BOARD)
        self.pin = pin
        self.direction = direction
        GPIO.setup(pin, direction, initial=initialState)

    def turnOn(self, duration=0.1):
        """
        Time in minutes
        """
        logging.debug("Turning on {} for {} minutes".format(
            self.name, duration))
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(duration*60)

    def turnOff(self, duration=0):
        logging.debug("Turning off {} for {} minutes".format(
            self.name, duration))
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(duration*60)
    
    def status(self):
        return GPIO.input(self.pin) == GPIO.LOW

    def shutdown(self):
        """
        Cleanups
        """
        logging.info("Shuting down the {} on pin number {}".format(self.name,self.pin))
        self.turnOff()
        GPIO.cleanup()