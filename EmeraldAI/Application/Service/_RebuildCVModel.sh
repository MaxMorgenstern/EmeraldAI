#!/bin/bash
directory=`dirname $0`
echo "Start rebuilding CV Model..."

./$directory/../_KillCV.sh
killout=$?

#cvpidfile=$directory/../CV.pid
#restart=0
#if [ -f $cvpidfile ] ; then
#	echo "Stop CV Process #$(cat $cvpidfile)"
#	kill -9 $(cat $cvpidfile)
#    rm $cvpidfile
#    restart=1
#fi

echo "Rebuild Model..."
python $directory/CVModelRebuilder.py

#if [ "$restart" = "1" ] ; then
if [ "$killout" = "1" ] ; then
	echo "Restart CV..."
	source $directory/../_RunCV.sh&
fi

cd -
