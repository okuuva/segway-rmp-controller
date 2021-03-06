
# Courtesy of spralray: https://github.com/spiralray/selfusb/blob/master/script/selfusb.py

import serial
import logging

logging.basicConfig(format="%(asctime)s:%(name)s:%(levelname)s: %(message)s", level=logging.INFO)


class CanUSB(serial.Serial):
    """
    Wrapper for Serial
    """

    def __init__(self, port, debug=False, check_responses=True, **kwargs):
        self.check_responses = check_responses
        self.logger = logging.getLogger(__name__)
        try:
            super().__init__(port, timeout=0.1, **kwargs)
        except serial.SerialException as e:
            raise ValueError("Could not open serial communication with Segway RMP, reason: {}".format(e))
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.init()

    def _check_response(self, expected=b"\r"):
        if not self.check_responses:
            return True
        response = self.readline()
        if response == expected:
            self.logger.debug("Response OK")
            return True
        else:
            self.logger.error("Incorrect response! Was expecting {}, got {}".format(expected, response))
            return False

    def readline(self):
        """
        Overrides io.RawIOBase.readline which cannot handle with b"\r" delimiters
        """
        message = b""
        while True:
            c = self.read(1)
            if c == b"":
                return message
            elif c == b"\r":
                return message + c
            elif c == chr(7):
                return c
            else:
                message += c

    def init(self):
        try:
            self.logger.debug("Opening serial port...")
            serial.Serial.open(self)  # Call method of super class
        except serial.SerialException:
            pass
        self.logger.debug("Starting initialization")
        self.write(b"\r\r\r")
        while True:
            line = self.readline()
            if line == b"":
                break
        self.logger.debug("CANUSB initialized")
        self.logger.debug("Closing CAN communication")
        self.write(b"C\r")  # Close port
        self.readline()
        self.set_speed(6)  # RMP does a panic shutdown on 1Mbps speed
        self.set_filter()
        self.open()

    def get_version(self):  # Check version
        self.write(b"V\r")
        return self.readline()

    def get_serial(self):
        self.write(b"N\r")
        return self.readline()

    def set_timestamp(self, enable=0):
        if enable:
            self.write(b"Z1\r")
        else:
            self.write(b"Z0\r")
        return self._check_response()

    def set_baud(self, baud):
        self.write("s{}\r".format(baud).encode())
        return self._check_response()

    def set_speed(self, speed):
        self.logger.debug("Setting CAN communication speed to {}".format(speed))
        if not (0 <= speed <= 8):
            self.logger.error("Invalid communication speed, must be between 0 and 8")
            return False
        self.write("S{}\r".format(speed).encode())
        return self._check_response()

    def set_filter(self):
        # set a filter to only receive all 11bit ID’s from 0x300 to 0x3FF
        # this way the heartbeats and status messages don't flood the input filter
        # TODO: make this generic in order to remove the hardcoded values
        self.logger.debug("Setting filtering")
        success = []
        self.write(b"M00006000\r")
        success.append(self._check_response())
        self.write(b"m00001FF0\r")
        success.append(self._check_response())
        if False in success:
            self.logger.error("Setting filter failed!")
            return False
        else:
            self.logger.debug("Set filters successfully")
            return True

    def open(self):
        try:
            self.logger.debug("Opening Serial port")
            serial.Serial.open(self)  # Call method of super class
        except serial.SerialException:
            pass
        self.logger.debug("Opening CAN communication")
        self.write(b"O\r")  # Open port
        return self._check_response()

    def close(self):
        # Close port
        self.write(b"C\r")  # Close port
        if self._check_response():
            self.logger.info("Close port: Success")
        else:
            self.logger.error("Close port: Fail")

        try:
            serial.Serial.close(self)  # Call method of super class
        except serial.SerialException:
            pass

    def send(self, msg, raw=False):
        # TODO: Simplify and clean the message format
        # This is currently overly complex and hackish, the value conversion should be
        # completely rewritten and separate arguments should be used instead of the dictionary
        # format
        try:
            raw_data = msg["data"]
        except KeyError:
            self.logger.error("Data missing from message!")
            return

        try:
            frame_length = int(msg["frame-length"])
        except KeyError:
            self.logger.debug("CAN frame length missing from the message dict, assuming 11 bits")
            frame_length = 11
        except ValueError:
            self.logger.error("CAN frame length must be integer")
            return

        if not raw:
            data = ""
            length = len(msg["data"])
            for i in range(0, length):
                data += "{0:02X}".format(ord(raw_data[i])).encode()

        if frame_length == 11:  # Standard format
            if raw:
                message = raw_data
            else:
                message = "t{0:03X}{1:d}{2:s}\r".format(msg["stdId"], len(raw_data), raw_data).encode()
            expected_response = b"z\r"
        elif frame_length == 29:  # Extended format
            if raw:
                message = raw_data
            else:
                message = "T{0:08X}{1:d}{2:s}\r".format(msg["stdId"] + (msg["extId"] * 0x400), len(raw_data), raw_data).encode()
            expected_response = b"Z\r"
        else:
            self.logger.error(
                "Incorrect CAN frame length! Frame length must be either 11 or 29 bits, got {}".format(frame_length)
            )
            return

        self.write(message)
        self.logger.debug(message)
        return self._check_response(expected_response)
