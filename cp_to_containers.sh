for i in 101 102 103 104; do
	echo "Copying file to 192.168.10.$i"
	scp *.py *.grc default root@192.168.10.$i:~/fg-stuff/ > /dev/null
done

for i in 20 30; do
	echo "Copying file to 192.168.10.$i"
	scp *.py *.grc default connect@192.168.10.$i:~/fg-stuff/ > /dev/null
done
