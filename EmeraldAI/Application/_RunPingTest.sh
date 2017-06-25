#!/bin/bash
directory=`dirname $0`
source $directory/_Initialize.sh

echo "Run Ping Test..."
python $directory/PingTest.py

cd -
