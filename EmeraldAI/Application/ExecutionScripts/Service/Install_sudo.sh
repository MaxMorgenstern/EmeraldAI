#!/bin/bash
directory=`dirname $0`

if [ "$EUID" -ne 0 ]
  then echo "Please run as root so we can install dependencies."
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
apt-get install nmap -y
apt-get install flac -y
apt-get install python-pip -y
