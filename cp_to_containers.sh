#!/bin/bash

curdir=`dirname ${BASH_SOURCE[*]}`

for i in 101 102 104; do
	echo "Copying file to 192.168.10.$i"
	scp ${curdir}/*.py ${curdir}/*.grc ${curdir}/default root@192.168.10.$i:~/fg-stuff/ > /dev/null
done

for i in 20 30; do
	echo "Copying file to 192.168.10.$i"
	scp ${curdir}/*.py ${curdir}/*.grc ${curdir}/default connect@192.168.10.$i:~/fg-stuff/ > /dev/null
done
