### set this up as per your IP Address
if env | grep -q ^EMERALD_IP=
then
    echo ""
else
    export EMERALD_IP=`ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1 -d'/'`
fi
echo "My IP='$EMERALD_IP'"
export ROS_HOSTNAME=$EMERALD_IP
export ROS_IP=$EMERALD_IP

# set mater uri on slave machines
if [ "$1" != "master" ]
then
    echo "Search Master Server..."
    # TODO
    # nmap -n -sn $EMERALD_IP/24 | grep ‘Nmap scan report for’ | awk '{print $5}'
    export ROS_MASTER_URI=http://1.2.3.4:11311
fi
