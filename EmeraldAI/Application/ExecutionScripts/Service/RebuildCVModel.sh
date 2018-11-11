#!/bin/bash
directory=`dirname $0`
echo "Start rebuilding CV Model..."

./$directory/../KillCV.sh
killout=$?

echo "Rebuild Model..."
python $directory/../../Service/CVModelRebuilder.py

echo "Rebuild Complete..."

#if [ "$restart" = "1" ] ; then
if [ "$killout" = "1" ] ; then
	echo "Restart CV..."
	source $directory/../RunCV.sh&
fi
