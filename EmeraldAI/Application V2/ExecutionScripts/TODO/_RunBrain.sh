#!/bin/bash
directory=`dirname $0`
source $directory/_Initialize.sh master

echo "Activating ROS..."
roscore&

sleep 5
echo "roscore has been started"

echo "Start Clock..."
python $directory/Clock.py&

echo "Start Ping Tester..."
python $directory/PingTester.py&

echo "Run Brain..."
python $directory/Brain.py

cd -
