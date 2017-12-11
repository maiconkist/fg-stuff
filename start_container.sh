

case "$1" in
	"split1")
		nohup python /root/fg-stuff/tx_split/split1.py > /dev/null 2>&1 &
		;;
	"split2")
		nohup python /root/fg-stuff/tx_split/split2.py > /dev/null 2>&1 &
		;;
	"split3")
		nohup python /root/fg-stuff/tx_split/split3.py > /dev/null 2>&1 &
		;;
	"vr1tx")
		nohup python /root/fg-stuff/tx_single/vr1_tx.py > /dev/null 2>&1 &
		;;
	"vr2tx")
		nohup python /root/fg-stuff/tx_single/vr2_tx.py > /dev/null 2>&1 &
		;;
	"vr1rx")
		nohup python /root/fg-stuff/rx/vr1_rx.py > /dev/null 2>&1 &
		;;
	"vr2rx")
		nohup python /root/fg-stuff/rx/vr2_rx.py > /dev/null 2>&1 &
		;;
	"usrp")
		nohup python /root/fg-stuff/usrp/usrp.py > /dev/null 2>&1 &
		;;
	"usrphydra")
		nohup python /root/fg-stuff/usrp/usrp_hydra.py > /dev/null 2>&1 &
		;;
	*)
		echo "1 argument is required"
		;;
esac
