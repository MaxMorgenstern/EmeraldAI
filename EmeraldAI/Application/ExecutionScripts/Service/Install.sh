#!/bin/bash
directory=`dirname $0`

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo "Update apt-get"
apt-get update

echo "Install requirements via apt-get"
apt-get install python-opencv -y
apt-get install pyaudio -y
apt-get install pocketsphinx -y
apt-get install portaudio19-dev -y
apt-get install ros-kinetic-rosserial-python -y

# pip installs need to run after apt-get installs due to references
echo "Install requirements via pip"
pip install --user -r install_requirements.txt

echo "Trigger Setup"
python $directory/../../Service/Setup.py

echo "Trigger Conversation Setup"
python $directory/../../Service/Setup_Conversation.py

echo "Build CV Model"
python $directory/../../Service/CVModelRebuilder.py

echo "Done!"

