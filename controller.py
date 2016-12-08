import sys
import locale
from curses import wrapper
from rmp import RMP
from time import sleep
from serial import SerialException

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

forward = ["KEY_UP", "w", ","]
backward = ["KEY_DOWN", "s", "o"]
right = ["KEY_RIGHT", "d", "e"]
left = ["KEY_LEFT", "a"]


def main(stdscr, port="/dev/ttyUSB0"):
    stdscr.clear()
    try:
        rmp = RMP(port, debug=False)
    except SerialException:
        stdscr.addstr(0, 0, "{:50}".format("RMP init failed, exiting..."))
        sys.exit(1)
    old_command = ""
    while True:
        output = ""
        command = stdscr.getkey()
        if command != old_command:
            sleep(0.25)
        if command == "KEY_ESC":
            break
        elif command in forward:
            rmp.forward()
            output = "FORWARD"
        elif command in backward:
            rmp.backward()
            output = "BACKWARD"
        elif command in left:
            rmp.left()
            output = "LEFT"
        elif command in right:
            rmp.right()
            output = "RIGHT"
        stdscr.addstr(0, 0, "{:50}".format(output))
        old_command = command


if __name__ == "__main__":
    try:
        port = sys.argv[1]
    except IndexError:
        port = "/dev/ttyUSB0"
    wrapper(main, port)
