#!/bin/bash
directory=`dirname $0`

rosrun rosserial_python serial_node.py /dev/ttyUSB0&

echo "Run Movement..."
python $directory/Movement.py

