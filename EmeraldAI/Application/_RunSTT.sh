#!/bin/bash
directory=`dirname $0`
source $directory/_Initialize.sh

echo "Run STT..."
python $directory/STT.py

cd -
