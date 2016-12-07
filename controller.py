# -*- coding: utf-8 -*-
import logging

from canusb import CanUSB
from time import sleep

logger = logging.getLogger(__name__)

PADDING = 16


class RMP:
    HEADER = 0x0413  # Header - 11 bits valid
    DLC = 0x0008  # Data Length Code - 4 bits valid
    # Payload length: 64bits / 8 bytes

    SPEED_MIN = -1176
    SPEED_MAX = 1176
    TURN_MIN = -1024
    TURN_MAX = 1024

    SPEED = 147  # ~0,5 m/s
    DURATION = 1000  # ms
    SMOOTH = True

    def __init__(self, port):
        self.can = CanUSB(port)

    def _compose_message(self, velocity, turn, config_command=0, config_parameters=0):
        # Config values can't be negative
        config_command = max(0, config_command)
        config_parameters = max(0, config_parameters)
        # Make sure velocity and turn rate are kept in the allowed range
        if velocity < 0:
            velocity = max(self.SPEED_MIN, velocity)
        else:
            velocity = min(self.SPEED_MAX, velocity)
        if turn < 0:
            turn = max(self.TURN_MIN, turn)
        else:
            turn = min(self.TURN_MAX, turn)
        return {
            "data": "t{0:03X}{1:X}{0:04X}{0:04X}{0:04X}{0:04X}\r".format(
                self.HEADER, self.DLC, velocity, turn, config_command, config_parameters).encode()
        }

    def right(self, speed=SPEED, duration=DURATION, smooth=SMOOTH):
        if speed <= 0:
            return
        self.can.send(self._compose_message(0, speed), raw=True)

    def left(self, speed=SPEED, duration=DURATION, smooth=SMOOTH):
        if speed >= 0:
            return
        self.can.send(self._compose_message(0, speed), raw=True)

    def forward(self, speed=SPEED, duration=DURATION, smooth=SMOOTH):
        if speed <= 0:
            return
        self.can.send(self._compose_message(speed, 0), raw=True)

    def backward(self, speed=-SPEED, duration=DURATION, smooth=SMOOTH):
        if speed >= 0:
            return
        self.can.send(self._compose_message(speed, 0), raw=True)


def ones_complement(number, padding=PADDING):
    try:
        bits = max(len(bin(number)) - 2, padding)
    except TypeError:
        logger.critical("Complement calculation failed: got {}, expected a number...".format(number))
        return -2
    mask = int("0b" + (bits * "1"), 2)
    return number ^ mask


def twos_complement(number, padding=PADDING, allow_overflow=False):
    complement = ones_complement(number, padding=padding)
    if allow_overflow:
        return complement + 1
    try:
        bits = max(len(bin(number)) - 2, padding)
    except TypeError:
        logger.critical("Complement calculation failed: got {}, expected a number...".format(number))
        return -2
    mask = int("0b" + (bits * "1"), 2)
    return (complement + 1) & mask


def hex_string(number, prefix=False, padding=int(PADDING / 4)):
    try:
        hex_number = hex(number)[2:]
    except TypeError:
        logger.critical("Couldn't transform {} into a hexadecimal number".format(number))
        hex_number = "0"
    hex_str = "{:0>{width}}".format(hex_number, width=padding)
    if prefix:
        return "0x{}".format(hex_str)
    return hex_str


def debug():
    rmp = RMP("/dev/ttyUSB0")
    while True:
        rmp.forward()
        sleep(0.015)


if __name__ == "__main__":
    debug()
