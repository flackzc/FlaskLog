#!/usr/bin/bash
if [ $# != 1 ];then
	echo "Usage:$0 commitinfo"
	exit 1
else		
	git add .
	git commit -m $1
	git push
fi
