#!/bin/bash
directory=`dirname $0`
source $directory/Initialize.sh

echo "Run TTS..."
python $directory/../IO/TTS.py

cd -
