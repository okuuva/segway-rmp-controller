# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)

PADDING = 16

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
