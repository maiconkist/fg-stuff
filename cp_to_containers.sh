for i in 30 101 102 103 104; do
	scp *.py *.grc default root@192.168.10.$i:~/fg-stuff/
done

