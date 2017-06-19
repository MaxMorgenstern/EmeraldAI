#!/bin/bash
directory=`dirname $0`
source $directory/_Initialize.sh

echo "Run CV..."
python $directory/CV.py

cd -
