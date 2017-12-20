case "$1" in
	"vr1tx-split1")
		ifconfig eth0 192.168.10.101
		sed -i '/split1/!b;n;cip=192.168.10.101' default
		nohup python /root/fg-stuff/tx_split/split1.py > /dev/null 2>&1 &
		;;
	"vr1tx-split2")
		ifconfig eth0 192.168.10.102
		sed -i '/split2/!b;n;cip=192.168.10.102' default
		nohup python /root/fg-stuff/tx_split/split2.py > /dev/null 2>&1 &
		;;
	"vr1tx-split3")
		ifconfig eth0 192.168.10.103
		sed -i '/split3/!b;n;cip=192.168.10.103' default
		nohup python /root/fg-stuff/tx_split/split3.py > /dev/null 2>&1 &
		;;
	"vr2tx-split1")
		ifconfig eth0 192.168.10.111
		sed -i '/split1/!b;n;cip=192.168.10.111' default
		nohup python /root/fg-stuff/tx_split/split1.py > /dev/null 2>&1 &
		;;
	"vr2tx-split2")
		ifconfig eth0 192.168.10.112
		sed -i '/split2/!b;n;cip=192.168.10.112' default
		nohup python /root/fg-stuff/tx_split/split2.py > /dev/null 2>&1 &
		;;
	"vr2tx-split3")
		ifconfig eth0 192.168.10.113
		sed -i '/split3/!b;n;cip=192.168.10.113' default
		nohup python /root/fg-stuff/tx_split/split3.py > /dev/null 2>&1 &
		;;
	"vr1tx")
		ifconfig eth0 192.168.10.103
		sed -i '/vr1tx/!b;n;cip=192.168.10.103' default
		nohup python /root/fg-stuff/tx_single/vr1_tx.py > /dev/null 2>&1 &
		;;
	"vr2tx")
		ifconfig eth0 192.168.10.113
		sed -i '/vr1tx/!b;n;cip=192.168.10.113' default
		nohup python /root/fg-stuff/tx_single/vr2_tx.py > /dev/null 2>&1 &
		;;
	"usrp")
		ifconfig eth0 192.168.10.104
		nohup python /root/fg-stuff/usrp/usrp.py > /dev/null 2>&1 &
		;;
	"usrphydra")
		ifconfig eth0 192.168.10.104
		nohup python /root/fg-stuff/usrp/usrp_hydra.py > /dev/null 2>&1 &
		;;
	*)
		echo "1 argument is required"
		;;
esac
