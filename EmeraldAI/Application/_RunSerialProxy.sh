#!/bin/bash
source $HOME/.profile

directory=`dirname $0`

source $directory/_Initialize.sh

echo "Start SerialTFRepeater..."
python $directory/SerialProxy/SerialTFRepeater.py&

echo "Start SerialToRos..."
python $directory/SerialProxy/SerialToRos.py

cd -
