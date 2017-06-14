#!/bin/bash
source _Initialize.sh master

echo "Activating ROS..."
roscore&

sleep 10
echo "roscore has been started"

echo "Run Brain..."
python Brain.py
