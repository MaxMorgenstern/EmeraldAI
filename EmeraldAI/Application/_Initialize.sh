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
	while :
	do
		echo "Search Master Server..."
		#export EMERALD_MASTER_IP=`nmap $EMERALD_IP/24 -sS -p 11311 | grep '11311/tcp open' -B3 | grep 'Nmap scan report for'| awk '{print $5}'`
		MASTER_HOSTNAME=`nmap $EMERALD_IP/24 -p 11311 | grep '11311/tcp open' -B3 | grep 'Nmap scan report for'| awk '{print $5}'`
		if [ "$MASTER_HOSTNAME" != "" ]
		then    
			export EMERALD_MASTER_IP=$MASTER_HOSTNAME
			echo "Set Master Server: 'http://$MASTER_HOSTNAME:11311'"
			export ROS_MASTER_URI=http://$MASTER_HOSTNAME:11311
			break
		fi
	done
fi

