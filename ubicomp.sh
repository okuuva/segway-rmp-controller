#!/usr/bin/env bash

chromium-browser --noerrordialogs --incognito --kiosk http://localhost/ubicomp/ &> /dev/null &
xdotool mousemove 9999 9999
