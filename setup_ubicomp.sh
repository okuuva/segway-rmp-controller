#!/usr/bin/env bash

echo "------------------------------------ Installing dependencies"
sudo apt-get update
sudo apt-get install chromium xdotool -y

./setup_venv.sh
