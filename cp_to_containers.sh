#!/bin/bash

curdir=`dirname ${BASH_SOURCE[*]}`

for i in 11 101 102 103 113; do
	echo "Copying file to 192.168.10.$i"
	scp -r ${curdir}/* root@192.168.10.$i:~/fg-stuff/ > /dev/null
done

for i in 20 30; do
	echo "Copying file to 192.168.10.$i"
	scp -r ${curdir}/* connect@192.168.10.$i:~/fg-stuff/ > /dev/null
done
