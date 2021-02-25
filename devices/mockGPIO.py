
"""
Mock GPIO class
"""


class GPIO(object):
    OUT = False
    IN = True
    LOW = False
    HIGH = True
    BOARD = 2

    @staticmethod
    def setmode(a):
        pass

    @staticmethod
    def setup(pin, direction, initial):
        pass

    @staticmethod
    def output(a, b):
        pass

    @staticmethod
    def cleanup():
        pass
