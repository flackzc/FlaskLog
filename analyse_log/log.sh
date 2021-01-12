#!/bin/bash
#get log by time and linenum

if [ $# != 2 ];then	
	echo "Usage:./$0 time(xx:xx:xx) linenum"  
	exit 1

elif [ -n "$(echo $2| sed -n "/^[0-9]\+$/p")" ];then 
	logName="LOG.`echo $1|sed 's/:/-/g'`_$2.log"
	logPath="log/LOG*.log"
	for i in `ls $logPath`
	do	
		result=`cat $i|awk '{print$2}'|grep -w $1` 
		if [[ "$result" != ""  ]] ;then
			cat $i|grep -w $1 -A $2 > $logName
			echo "logfile: $logName"
		fi
done

if [ ! -f $logName ];then
	echo "No result"
	exit 1
fi
else 
	echo '$2 must be number '
	echo "Usage:./$0 time(xx:xx:xx) linenum"  
	exit 1
fi 
