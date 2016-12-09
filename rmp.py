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

    TURN = 147
    SPEED = 100  # ~0,5 m/s
    DURATION = 1000  # ms
    SMOOTH = True

    def __init__(self, port, debug=False):
        self.can = CanUSB(port, debug=debug)

    def _compose_message(self, velocity, turn, config_command=0, config_parameters=0):
        # Config values can't be negative
        config_command = max(0, config_command)
        config_parameters = max(0, config_parameters)
        # Make sure velocity and turn rate are kept in the allowed range
        if velocity < 0:
            velocity = twos_complement(abs(max(self.SPEED_MIN, velocity)))
        else:
            velocity = min(self.SPEED_MAX, velocity)
        if turn < 0:
            turn = twos_complement(abs(max(self.TURN_MIN, turn)))
        else:
            turn = min(self.TURN_MAX, turn)
        params = [self.HEADER, self.DLC, velocity, turn, config_command, config_parameters]
        return {"data": "t{:03X}{:X}{:04X}{:04X}{:04X}{:04X}\r".format(*params).encode()}

    def right(self, speed=max(-TURN, TURN_MIN), duration=DURATION, smooth=SMOOTH):
        if speed >= 0:
            return
        if smooth:
            goal = speed
            speed = 0
            while True:
                speed = self.smoother(speed, goal)
                if not speed:
                    return
                self.can.send(self._compose_message(0, -speed), raw=True)
                sleep(0.1)
        self.can.send(self._compose_message(0, speed), raw=True)

    def left(self, speed=min(TURN, TURN_MAX), duration=DURATION, smooth=SMOOTH):
        if speed <= 0:
            return
        if smooth:
            goal = speed
            speed = 0
            while True:
                speed = self.smoother(speed, goal)
                if not speed:
                    return
                self.can.send(self._compose_message(speed, 0), raw=True)
                sleep(0.1)
        self.can.send(self._compose_message(0, speed), raw=True)

    def forward(self, speed=min(SPEED, SPEED_MAX), duration=DURATION, smooth=SMOOTH):
        if speed <= 0:
            return
        if smooth:
            goal = speed
            speed = 0
            while True:
                speed = self.smoother(speed, goal)
                if not speed:
                    return
                self.can.send(self._compose_message(speed, 0), raw=True)
                sleep(0.1)
        self.can.send(self._compose_message(speed, 0), raw=True)

    def backward(self, speed=max(-SPEED, SPEED_MIN), duration=DURATION, smooth=SMOOTH):
        if speed >= 0:
            return
        if smooth:
            goal = speed
            speed = 0
            while True:
                speed = self.smoother(speed, goal)
                if not speed:
                    return
                self.can.send(self._compose_message(-speed, 0), raw=True)
                sleep(0.1)
        self.can.send(self._compose_message(speed, 0), raw=True)

    @staticmethod
    def smoother(start, goal):
        start = abs(start)
        goal = abs(goal)
        if start == goal:
            return
        if start < goal:
            return min(start + 50, goal)


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

