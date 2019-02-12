#!/bin/bash
directory=`dirname $0`
source $directory/Initialize.sh master

if [[ -z "${EMERALD_MASTER_IP}" ]]; then
	echo "No master found..."
	echo ${EMERALD_MASTER_IP}

	echo "Launch roscore..."
	roscore&

	echo $! > $directory/../Main/Brain.Trigger.roscore.pid

	sleep 10
	echo "roscore has been started"
fi

echo "Run Brain, ActionTrigger..."
python $directory/../Main/Brain_ActionTrigger.py

rm $directory/../Main/Brain.Trigger.roscore.pid

cd -
