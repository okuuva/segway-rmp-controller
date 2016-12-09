import os
import sys
import locale
import curses

from rmp import RMP
from time import sleep
from serial import SerialException

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

forward = ["KEY_UP", "w"]
backward = ["KEY_DOWN", "s"]
right = ["KEY_RIGHT", "d"]
left = ["KEY_LEFT", "a"]


class UBIRMPController:
    def __init__(self, main_window, port):
        curses.curs_set(0)
        self.main_window = main_window
        self.main_window.clear()
        try:
            self.rmp = RMP(port, debug=False)
        except SerialException:
            self.main_window.addstr(0, 0, "{:50}".format("RMP init failed, exiting..."))
            sys.exit(1)

    def main_loop(self):
        old_command = ""
        while True:
            output = ""
            command = self.main_window.getkey()
            if command != old_command:
                sleep(0.25)
            if command == "KEY_BACKSPACE":
                break
            elif command == "KEY_F(12)":
                self.restart_browser()
                output = "Restart browser"
            elif command == " ":
                self.click_screen()
                output = "Click screen"
            elif command in forward:
                self.rmp.forward()
                output = "FORWARD"
            elif command in backward:
                self.rmp.backward()
                output = "BACKWARD"
            elif command in left:
                self.rmp.left()
                output = "LEFT"
            elif command in right:
                self.rmp.right()
                output = "RIGHT"
            self.main_window.addstr(0, 0, "{:50}".format(output))
            old_command = command

    @staticmethod
    def click_screen():
        os.system("xdotool mousemove 960 920 click 1")

    @staticmethod
    def restart_browser():
        os.system("pkill chromium-browse")
        os.system("/home/pi/ubicomp.sh")


def main(stdscr, port):
    controller = UBIRMPController(stdscr, port)
    controller.main_loop()


if __name__ == "__main__":
    try:
        port = sys.argv[1]
    except IndexError:
        port = "/dev/ttyUSB0"
    curses.wrapper(main, port)
