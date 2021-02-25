import logging
import os

from .device import Device
"""
*Note : This is the latest code not in fan.py
"""


class AC(Device):
    GPIO_PIN = 7

    def __init__(self, name):
        super().__init__(name, AC.GPIO_PIN)

    @staticmethod
    def logTemperature():
        process = os.popen(
            "cat /sys/devices/virtual/thermal/thermal_zone*/temp")
        stdout = process.read()
        zones = [
            "AO-therm", "CPU-therm", "GPU-therm", "PLL-therm",
            "PMIC-Die (Not real)", "thermal-fan-est"
        ]
        temperatures = stdout.split("\n")
        for temperature_index in range(len(temperatures)):
            c_temp = temperatures[temperature_index]
            if c_temp is not '':
                logging.info("{}  ----> {} C".format(zones[temperature_index],
                                                     int(c_temp) / 1000))
