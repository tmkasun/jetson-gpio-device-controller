#!/usr/bin/env python3
import logging
import sys

from devices.ac import AC

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')


def main(args):
    tcl = AC("Testing AC")
    logging.info(tcl.status())

if __name__ == "__main__":
    main(sys.argv[1:])