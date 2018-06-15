#!/bin/bash

set -x

case $1 in
    "stop")
        ssh vr1rx "killall -9 python2; killall -9 python3; killall -9 python"
        ssh vr2rx "killall -9 python2; killall -9 python3; killall -9 python"
        ssh usrp  "killall -9 python2; killall -9 python3; killall -9 python"
        ssh localhost "killall -9 python3"
    	;;

    "restart")
        ;;

    "start")
        ssh -CY vr1rx "cd ~/fg-stuff/wishful && ./agent.py > vr1rx.log &" & 
        ssh -CY vr2rx "cd ~/fg-stuff/wishful && ./agent.py > vr2rx.log &" & 
        ssh -CY usrp  "cd ~/fg-stuff/wishful && ./agent.py > usrp.log &" & 
        pushd ~/fg-stuff/wishful/ ; ./controller.py
        ;;

    *)
        echo "Usage: $0 [stop|start|restart]"
    ;;

esac

