#!/bin/bash
directory=`dirname $0`
source $directory/Initialize.sh

echo "Run CV..."
python $directory/../IO/CV.py

cd -
