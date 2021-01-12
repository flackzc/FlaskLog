#!/bin/bash
for i in `seq 100 250`
do 
	ck=`ping -c 1 10.158.96.$i|grep "1 received"`
	if [[ -n $ck ]];then 
		echo 10.158.96.$i
	fi
done 
