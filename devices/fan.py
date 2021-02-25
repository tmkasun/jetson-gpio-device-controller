#!/usr/bin/env python3
import logging
import os
import signal
import sys

from .device import Device


class Fan(Device):
    @staticmethod
    def logTemperature():
        process = os.popen(
            "cat /sys/devices/virtual/thermal/thermal_zone*/temp")
        stdout = process.read()
        zones = [
            "AO-therm",
            "CPU-therm",
            "GPU-therm",
            "PLL-therm",
            "PMIC-Die (Not real)",
            "thermal-fan-est"
        ]
        temperatures = stdout.split("\n")
        for temperature_index in range(len(temperatures)):
            c_temp = temperatures[temperature_index]
            if c_temp is not '':
                logging.info(
                    "{}  ----> {} C".format(zones[temperature_index], int(c_temp)/1000))


logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    handlers=[
        logging.FileHandler("test.log"),
        logging.StreamHandler()
    ])

PID_FILE = "pro.pid"


def refreshPID(killOnly=False):
    current_pid = os.getpid()
    with open(PID_FILE, 'w+') as pid:
        previous_pid = pid.readline()
        if not len(previous_pid) is 0:
            os.kill(int(previous_pid), signal.SIGTERM)
        if not killOnly:
            logging.info(
                "Starting A/C controller in PID {}".format(current_pid))
            pid.write(str(current_pid))


def cleanup(device):
    device.shutdown()
    logging.shutdown()
    os.remove(PID_FILE)


def main(argv):
    fan = Fan("Normal Fan", 11)

    if len(argv) is 1 and argv[0] == "stop":
        refreshPID(True)
        cleanup(fan)
        logging.warning(
            "Killed existing stale process and stopping the device !!")
        return
    onTime = 2
    offTime = 2
    if len(argv) is 2:
        onTime = float(argv[0])
        offTime = float(argv[1])
    refreshPID()
    try:
        while True:
            Fan.logTemperature()
            fan.turnOn(onTime)
            Fan.logTemperature()
            fan.turnOff(offTime)
    except KeyboardInterrupt as identifier:
        logging.error("Keyboard interrupt occurred, Gracefully closing . . .")
    finally:
        cleanup(fan)


if __name__ == "__main__":
    main(sys.argv[1:])
