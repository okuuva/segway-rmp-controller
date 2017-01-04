# segway-rmp-controller

A simple remote control script for Segway RMP platform utilizing Python and Lawicel CANUSB. This
was made for Ubiquitous Computing Fundamentals course on University of Oulu. While the control
script is really specific for this course, the *canusb* and *rmp* modules might be useful for
someone wishing to utilize Lawicel CANUSB adapter and/or programmatically control Segway
RMP platform in their project.

## Contents

* canusb.py, a PySerial wrapper for Lawicel CANUSB adapter based on
[spiralray's CANUSB ROS plugin][wrapper]
* rmp.py, a control API for Segway RMP platform
* controller.py, a curses client for controlling the Segway RMP platform

## Requirements
* Segway RMP platform (Duh)
* Lawicel CANUSB (Also duh)
* Python 3.4 or newer

This project is Python 3 only. It might run on Python 2.7 with little tweaking but hasn't been
tested nor is supported. Using Debian GNU/Linux on the controller machine is recommended as it has
been proven to be working, other distributions are probably fine too but no automatic installation
scripts are provided. Windows and macOS are not tested nor supported.

## Dependencies
The only non-standard module dependency is PySerial, which can be installed with pip:

`pip install PySerial`

Some of the school project specific stuff also require Chromium web browser and xdotool, but
they are not required for the control script to run.

## Setup
1. Connect Lawicel CANUSB adapter to your Segway RMP platform per instructions on Segway RMP
   Interface Guide
2. Connect Lawicel CANUSB adapter to your control machine
3. Find the device path of the Lawicel CANUSB adapter with e.g. the following command:

    `sudo blkid`

    It is usually something like `/dev/ttyUSB0`. It is easiest to first run the command
    with the adapter plugged out, then plugging the adapter in and then running the command again
    and diff the output. If you can't identify the path of the adapter you might need to install
    drivers for it. I wasn't able to find any for macOS and the Windows drivers were outdated and
    uncompatible with Windows 8 and newer, so good luck...

4. Install control script to your control machine, see next section.

## Installation

If for some reason you need the Chromium restart feature of the controller, run
`./setup_ubicomp.sh` in the project directory. Otherwise `./setup_venv.sh` is enough to install
Python 3 interpreter, creating a virtual environment and installing dependencies to it. For
those running something else than Debian/Ubuntu, you need to manually install Python 3 and
optionally Chromium and xdotool and creating the virtual environment with PySerial installed.

## Running

Start controller with the following command:

`python3 controller.py <CANUSB device path>`

If you don't provide path to CANUSB adapter, the script assumes it is located at `/dev/ttyUSB0`.
If communication with the adapter can't be estabilished, the control script displays an error
message and exits with status code 1.

## Keymap
* W, Up arrow: Forward
* S, Down arrow: Backward
* A, Left arrow: Left turn
* D, Right arrow: Right turn
* Space: click screen (requires xdotool)
* F5: Restart Chromium (requires Chromium browser (duh))
* F12: Exit

## Todo:
* Clean up the mess that is message sending method in canusb.py
* Add more multipurpose moving command to RMP API
* Add smooth start to movements (started on a separate branch)

## Useful links and references:
* [Lawicel CANUSB documentation][CANUSB]
* [CANUSB ROS plugin by spiralray containing the original PySerial wrapper][wrapper]

[CANUSB]: http://www.can232.com/docs/canusb_manual.pdf
[wrapper]: https://github.com/spiralray/canusb
