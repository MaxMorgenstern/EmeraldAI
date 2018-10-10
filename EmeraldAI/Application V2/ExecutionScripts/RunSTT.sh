#!/bin/bash
directory=`dirname $0`
source $directory/Initialize.sh

echo "Run STT..."
python $directory/../IO/STT_Live.py
python $directory/../IO/STT.py

cd -
