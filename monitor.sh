#!/bin/bash
basePath="/mnt/hgfs/p-workspace/M7log/"
while true
do
for i in `ls $basePath|grep -v "("|grep "tar.gz"`
do 
  dirnam=`echo $i|awk -F'.' '{print$1}'`
  if [[ ! -d "${basePath}/${dirnam}" ]];then
    mkdir ${basePath}/${dirnam}
    tar -zxvf ${basePath}/$i -C ${basePath}/${dirnam} 1>/dev/null 2>&1
  fi
done
sleep 5
done
