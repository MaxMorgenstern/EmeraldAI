#!/bin/bash
directory=`dirname $0`

if [ "$EUID" -eq 0 ]
  then echo "Please do not run this script root initially. We will ask for sudo password in a second."
  exit
fi

sudo -s source $directory/Install_sudo.sh

# pip installs need to run after apt-get installs due to references
echo "Install requirements via pip"
pip install --user -r install_requirements.txt

sudo -s source $directory/Install_sudo2.sh

echo "Done!"
