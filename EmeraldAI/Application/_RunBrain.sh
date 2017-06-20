#!/bin/bash
directory=`dirname $0`
source $directory/_Initialize.sh master

echo "Activating ROS..."
roscore&

sleep 10
echo "roscore has been started"

echo "Run Brain..."
python $directory/Brain.py

cd -