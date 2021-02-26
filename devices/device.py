import Jetson.GPIO as GPIO
import os
# from mockGPIO import GPIO
import time
import logging


# For board pin number to GPIO file name
# mapping refer https://www.jetsonhacks.com/nvidia-jetson-nano-j41-header-pinout/
class Device(object):
    PIN_TO_FILE = {7: "gpio216", 11: "gpio50", 14: "gpio14"}
    # sysfs root
    _SYSFS_ROOT = "/sys/class/gpio"

    def __init__(self, name, pin, direction=GPIO.OUT, initialState=GPIO.LOW):
        """
        Initialize a device to be controlled via GPIO
        """
        self.name = name
        GPIO.setmode(GPIO.BOARD)
        self.pin = pin
        self.direction = direction
        GPIO.setup(pin, direction, initial=initialState)

    def turnOn(self, duration=0):
        """
        Time in minutes
        """
        logging.debug("Turning on {} for {} minutes".format(
            self.name, duration))
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(duration * 60)

    def turnOff(self, duration=0):
        logging.debug("Turning off {} for {} minutes".format(
            self.name, duration))
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(duration * 60)

    def status(self):
        info = GPIO.JETSON_INFO
        info['isLow'] = -1
        info['name'] = self.name
        info['pin'] = self.pin
        gpio_fd = "{}/{}/value".format(Device._SYSFS_ROOT,
                                       Device.PIN_TO_FILE[self.pin])
        if os.path.exists(gpio_fd):
            with open(gpio_fd, 'r') as value_file:
                flag = value_file.readline()
                logging.debug("{} flag value is {}".format(gpio_fd, flag))
                info['isLow'] = True if int(flag) == 0 else False
        return info

    def shutdown(self):
        """
        Cleanups
        """
        logging.info("Shuting down the {} on pin number {}".format(
            self.name, self.pin))
        self.turnOff()
        GPIO.cleanup()