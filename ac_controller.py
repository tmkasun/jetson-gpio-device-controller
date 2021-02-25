#!/usr/bin/env python3
import logging
import os
import signal
import sys
from devices.ac import AC

temp_dir = os.path.dirname(
            __file__)  #<-- absolute dir the script is in
log_path = "./temp/ac.log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    handlers=[logging.FileHandler(os.path.join(temp_dir, log_path)),
              logging.StreamHandler()])

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


def main(argv):
    ac = AC("TCL A/C")
    if len(argv) is 1 and argv[0] == "stop":
        refreshPID(True)
        ac.shutdown()
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
            ac.logTemperature()
            ac.turnOn(onTime)
            ac.logTemperature()
            ac.turnOff(offTime)
    except KeyboardInterrupt as identifier:
        logging.error("Keyboard interrupt occurred, Gracefully closing . . .")
    finally:
        ac.shutdown()
        os.remove(PID_FILE)


if __name__ == "__main__":
    main(sys.argv[1:])