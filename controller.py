# -*- coding: utf-8 -*-
import serial
import logging

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
        try:
            self.serial = serial.Serial(port)
        except serial.SerialException as e:
            raise ValueError("Could not open serial communication with Segway RMP, reason: {}".format(e))

    def right(self, speed=SPEED, duration=DURATION, smooth=SMOOTH):
        pass

    def left(self, speed=SPEED, duration=DURATION, smooth=SMOOTH):
        pass

    def forward(self, speed=SPEED, duration=DURATION, smooth=SMOOTH):
        pass

    def backward(self, speed=SPEED, duration=DURATION, smooth=SMOOTH):
        pass


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


def hex_string(number, prefix=True, padding=int(PADDING / 4)):
    try:
        hex_number = hex(number)[2:]
    except TypeError:
        logger.critical("Couldn't transform {} into a hexadecimal number".format(number))
        hex_number = "0"
    hex_str = "{:0>{width}}".format(hex_number, width=padding)
    if prefix:
        return "0x{}".format(hex_str)
    return hex_str
