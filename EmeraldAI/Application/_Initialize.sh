### set this up as per your IP Address
if env | grep -q ^EMERALD_IP=
then
    echo ""
else
    export EMERALD_IP=`ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1 -d'/'`
fi

echo "My IP: '$EMERALD_IP'"
export ROS_HOSTNAME=$EMERALD_IP
export ROS_IP=$EMERALD_IP

# set mater uri on slave machines
if [ "$1" != "master" ]
then
    echo "Search Master Server..."
    #export EMERALD_MASTER_IP=`nmap $EMERALD_IP/24 -sS -p 11311 | grep '11311/tcp open' -B3 | grep 'Nmap scan report for'| awk '{print $5}'`
	export EMERALD_MASTER_IP=`nmap $EMERALD_IP/24 -p 11311 | grep '11311/tcp open' -B3 | grep 'Nmap scan report for'| awk '{print $5}'`

    echo "Set Master Server: 'http://$EMERALD_MASTER_IP:11311'"
    export ROS_MASTER_URI=http://$EMERALD_MASTER_IP:11311
fi
