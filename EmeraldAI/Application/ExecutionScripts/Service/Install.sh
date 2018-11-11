#!/bin/bash
directory=`dirname $0`

echo "Install requirements via pip"
pip install --user -r install_requirements.txt

echo "Update apt-get"
apt-get update

echo "Install requirements via apt-get"
apt-get install python-opencv -y
apt-get install pyaudio -y
apt-get install pocketsphinx -y
apt-get install portaudio19-dev -y
apt-get install ros-kinetic-rosserial-python -y

echo "Trigger Setup"
python $directory/../../Service/Setup.py

echo "Trigger Conversation Setup"
python $directory/../../Service/Setup_Conversation.py

echo "Build CV Model"
python $directory/../../Service/CVModelRebuilder.py

echo "Done!"

