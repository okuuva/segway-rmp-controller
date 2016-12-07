import locale
from curses import wrapper
from rmp import RMP

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

forward = ["KEY_UP", "w", ","]
backward = ["KEY_DOWN", "s", "o"]
right = ["KEY_RIGHT", "d", "e"]
left = ["KEY_LEFT", "a"]


def main(stdscr):
    stdscr.clear()
    rmp = RMP("/dev/ttys006", debug=False)
    while True:
        c = stdscr.getkey()
        output = ""
        if c == "ESC":
            break
        elif c in forward:
            rmp.forward()
            output = "FORWARD"
        elif c in backward:
            rmp.backward()
            output = "BACKWARD"
        elif c in left:
            rmp.left()
            output = "LEFT"
        elif c in right:
            rmp.right()
            output = "RIGHT"
        stdscr.addstr(0, 0, "{:50}".format(output))


if __name__ == "__main__":
    # stdscr = curses.initscr()
    wrapper(main)
