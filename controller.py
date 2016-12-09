import sys
import locale
from curses import wrapper
from rmp import RMP
from time import sleep
from serial import SerialException
from subprocess import call

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

forward = ["KEY_UP", "w"]
backward = ["KEY_DOWN", "s"]
right = ["KEY_RIGHT", "d"]
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
        if command == "KEY_BACKSPACE":
            break
        elif command == "KEY_F(12)":
            restart_browser()
            output = "Restart browser"
        elif command == " ":
            click_screen()
            output = "Click screen"
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


def click_screen():
    click = ["xdotool", "mousemove", "960", "920", "click", "1"]
    call(click)


def restart_browser():
    call(["pkill", "chromium-browse"])
    sleep(1)
    call(["/home/pi/ubicomp.sh"])


if __name__ == "__main__":
    try:
        port = sys.argv[1]
    except IndexError:
        port = "/dev/ttyUSB0"
    wrapper(main, port)
