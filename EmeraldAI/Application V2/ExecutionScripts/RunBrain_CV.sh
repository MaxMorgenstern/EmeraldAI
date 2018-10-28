#!/bin/bash
directory=`dirname $0`
source $directory/Initialize.sh master

if [[ -z "${EMERALD_MASTER_IP}" ]]; then
	echo "No master found..."
	echo ${EMERALD_MASTER_IP}

	echo "Launch roscore..."
	roscore&

	echo $! > $directory/../Main/Brain.CV.roscore.pid
	
	sleep 10
	echo "roscore has been started"
fi

echo "Run Brain, CV..."
python $directory/../Main/Brain_CV.py

rm $directory/../Main/Brain.CV.roscore.pid

cd -
