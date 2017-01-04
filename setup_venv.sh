#!/usr/bin/env bash

echo "------------------------------------ Installing dependencies"
sudo apt-get install python3 virtualenv -y

echo "------------------------------------ Creating virtual environment to venv directory"
virtualenv venv

echo "------------------------------------ Updating pip and installing PySerial to venv"
venv/bin/pip install -U pip PySerial

echo "Done! You can now run the control script with the following command:
venv/bin/python controller.py"
