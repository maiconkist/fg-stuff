#!/bin/bash

# this script is called by monit.
# monit configuration file is 'monitrc'

PIDFILE=/var/run/split.pid

case "$1" in
	"vr1tx-split1")
		ifconfig eth0 192.168.10.101
		cd /root/fg-stuff/
		sed -i '/split1/!b;n;cip=192.168.10.101' default
		#python /root/fg-stuff/tx_split/split1.py 2> /dev/null &
		python3 /root/fg-stuff/wishful/agent.py 2> /dev/null &
		echo $! > ${PIDFILE}
		;;
	"vr1tx-split2")
		ifconfig eth0 192.168.10.102
		cd /root/fg-stuff/
		sed -i '/split2/!b;n;cip=192.168.10.102' default
		#python /root/fg-stuff/tx_split/split2.py 2> /dev/null &
		python3 /root/fg-stuff/wishful/agent.py 2> /dev/null &
		echo $! > ${PIDFILE}
		;;
	"vr1tx-split3")
		ifconfig eth0 192.168.10.103
		cd /root/fg-stuff/
		sed -i '/split3/!b;n;cip=192.168.10.103' default
		#python /root/fg-stuff/tx_split/split3.py 2> /dev/null &
		python3 /root/fg-stuff/wishful/agent.py 2> /dev/null &
		echo $! > ${PIDFILE}
		;;
	"vr1tx")
		ifconfig eth0 192.168.10.103
		cd /root/fg-stuff/
		sed -i '/vr1_tx/!b;n;cip=192.168.10.103' default
		#python /root/fg-stuff/tx_single/vr1_tx.py 2> /dev/null &
		python3 /root/fg-stuff/wishful/agent.py 2> /dev/null &
		echo $! > ${PIDFILE}
		;;
	"vr2tx")
		ifconfig eth0 192.168.10.113
		cd /root/fg-stuff/
		sed -i '/vr2_tx/!b;n;cip=192.168.10.113' default
		#python /root/fg-stuff/tx_single/vr2_tx.py 2> /dev/null &
		python3 /root/fg-stuff/wishful/agent.py 2> /dev/null &
		echo $! > ${PIDFILE}
		;;
	"usrp")
		ifconfig eth0 192.168.10.104
		cd /root/fg-stuff/
		#python /root/fg-stuff/usrp/usrp.py 2> /dev/null &
		python3 /root/fg-stuff/wishful/agent.py 2> /dev/null &
		echo $! > ${PIDFILE}
		;;
	"usrphydra")
		ifconfig eth0 192.168.10.104
		cd /root/fg-stuff/
		#python /root/fg-stuff/usrp/usrp_hydra.py 2> /dev/null &
		python3 /root/fg-stuff/wishful/agent.py 2> /dev/null &
		echo $! > ${PIDFILE}
		;;
	*)
		echo "1 argument is required"
		;;
esac

exit 0
