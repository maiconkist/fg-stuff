for i in 101 102 103 104 105; do
	scp *.py *.grc default root@192.168.10.$i:~/fg-stuff/
done

