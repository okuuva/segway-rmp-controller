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

commands = [" ", "KEY_F(5)", "KEY_F(12)"]
movements = forward + backward + right + left


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
        key = ""
        while True:
            output = ""
            if key not in commands:
                key = self.main_window.getkey()
            if key == "KEY_F(12)":
                break
            elif key == "KEY_F(5)":
                self.restart_browser()
                output = "Restart browser"
            elif key == " ":
                self.click_screen()
                output = "Click screen"
            else:
                while key in movements:
                    key = self.check_movement_control(key, forward, "FORWARD", self.rmp.forward)
                    key = self.check_movement_control(key, backward, "BACKWARD", self.rmp.backward)
                    key = self.check_movement_control(key, left, "LEFT", self.rmp.left)
                    key = self.check_movement_control(key, right, "RIGHT", self.rmp.right)
            self.main_window.addstr(0, 0, "{:50}".format(output))

    def check_movement_control(self, key, command, output, method):
        if key in command:
            self.main_window.addstr(0, 0, "{:50}".format(output))
            method()
            while True:
                key = self.main_window.getkey()
                if key in command:
                    method(smooth=False)
                else:
                    break
        return key

    @staticmethod
    def click_screen():
        os.system("xdotool mousemove 960 920 click 1")

    @staticmethod
    def restart_browser():
        os.system("pkill chromium-browse")
        path = os.path.dirname(sys.argv[0])
        os.system(os.path.join(path, "ubicomp.sh"))


def main(stdscr, port):
    controller = UBIRMPController(stdscr, port)
    try:
        controller.main_loop()
    except KeyboardInterrupt:
        pass  # CTRL + C kills the child processes too, closing the restarted browser. Use F12 to exit


if __name__ == "__main__":
    try:
        port = sys.argv[1]
    except IndexError:
        port = "/dev/ttyUSB0"
    curses.wrapper(main, port)
