#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#

'''
根据关键字拆分日志
1、python merge_log_files.py input output
2、input 为想要拆分日志的目录
3、output 为拆分后日志存放的目录，目录不存在则自动创建
'''

import glob
import os
import sys

try:
    logInput = sys.argv[1]
    logOutput = sys.argv[2]
except BaseException as e:
    print("Usage:python "+sys.argv[0]+ "logInput" + " logOutput")
    exit(1)
else:
    if not os.path.exists(sys.argv[1]):
        print("logInputpath not exist!")
        exit(1)
    elif not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])


def IsNewLog(txt_line):
    if -1 != txt_line.find("ClearCleanRecord"):
        return True
    return False

def IgnoreLine(txt_line):
    if -1 != txt_line.find("RecvRun"):
        return True
    if -1 != txt_line.find("SendRun"):
        return True
    return False

filelist = glob.glob(sys.argv[1] + '/LOG.*.log')
filelist.sort()

new_log_file = None
for item in filelist:
    print(item)
    for txt_line in open(item, 'r'):
        if IsNewLog(txt_line):
            timestamp = txt_line.split(' ')[1]
            timestamp = timestamp.replace(":", "_")
            timestamp = timestamp.replace(".", "_")
            new_log_file_name = sys.argv[2] + "/LOG." + timestamp + ".log"
            new_log_file = open(new_log_file_name, 'w')
        if IgnoreLine(txt_line):
            continue
        if new_log_file:
            new_log_file.write(txt_line)

if new_log_file:
    new_log_file.close()
