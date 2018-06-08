#!/bin/bash

curdir=`dirname ${BASH_SOURCE[*]}`

for i in 101 102 103 104 113; do
	echo "Copying file to 192.168.10.$i"
	scp -r ${curdir}/* root@192.168.10.$i:~/fg-stuff/ > /dev/null
done

for i in 20; do
	echo "Copying file to 192.168.10.$i"
	scp -r ${curdir}/* connect@192.168.10.$i:~/fg-stuff/ > /dev/null
done
