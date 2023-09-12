#!/bin/bash

echo "Start RTC Test Script"
echo "Connected RTC : "
cat /sys/class/rtc/rtc0/name

python3 rtc.py > log.txt &
