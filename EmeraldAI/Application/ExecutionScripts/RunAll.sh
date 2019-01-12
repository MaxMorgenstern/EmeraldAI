#!/bin/bash
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

echo "Launch Core..."
mate-terminal --tab --title='roscore' -e 'bash -c "sleep 1s && roscore ; bash"'


echo "Launch Speech..."
mate-terminal --tab --title='Brain STT' --working-directory=$SCRIPTPATH -e 'bash -c "sleep 5s && ./RunBrain_STT.sh ; bash"'

mate-terminal --tab --title='Brain TTS' --working-directory=$SCRIPTPATH -e 'bash -c "sleep 5s && ./RunBrain_TTS.sh ; bash"'

mate-terminal --tab --title='STT' --working-directory=$SCRIPTPATH -e 'bash -c "sleep 5s && ./RunSTT.sh ; bash"'

mate-terminal --tab --title='TTS' --working-directory=$SCRIPTPATH -e 'bash -c "sleep 5s && ./RunTTS.sh ; bash"'


echo "Launch CV..."
mate-terminal --tab --title='Brain CV' --working-directory=$SCRIPTPATH -e 'bash -c "sleep 5s && ./RunBrain_CV.sh ; bash"'

mate-terminal --tab --title='CV' --working-directory=$SCRIPTPATH -e 'bash -c "sleep 5s && ./RunCV.sh ; bash"'


# echo "Launch Serial Proxy..."
# mate-terminal --tab --title='Serial Proxy' --working-directory=$SCRIPTPATH -e 'bash -c "sleep 5s && ./RunSerialProxy.sh ; bash"'
