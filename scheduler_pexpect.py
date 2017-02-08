#-*- coding: utf-8 -*-
#!usr/bin/python

import sys
import time
sys.path.append('/home/mart_cis/xia/local/lib/python2.7/site-packages/')
import pexpect

#-------------- parameters
hostname="192.168.1.111"
username="xiajg"
password="111111\n"
work_dir="~"
statfile="__success__"



#-------------- download data from bdp

os.system("""
hive -e "SELECT * FROM gdm.gdm_m03_item_sku_da LIMIT 100;" > input.txt
""")


#-------------- send data (and scipt) to remote, and calculation

# 上传文件到远程主机
# 如果文件较大，需要将timeout参数设置大一些
pexpect.run('scp input.txt %s@%s:%s' % (username,hostname,work_dir) ,timeout=300, withexitstatus=1,events={'password': password})


# 初始化状态
(command_output, exitstatus) = pexpect.run('ssh %s@%s "ls %s"' % (username,hostname,work_dir) ,withexitstatus=1,events={'password': password})
if statfile in command_output.split('\r\n'):
    pexpect.run('ssh %s@%s "rm %s"' % (username,hostname,statfile) ,withexitstatus=1,events={'password': password})

# 在远程机执行shell命令
pexpect.run('ssh %s@%s "python mytask.py"' % (username,hostname) ,withexitstatus=1,events={'password': password})

#-------------- task monitor

# 等待程序运行完成
# 如果程序运行时间较长，可以尝试每次循环内建立连接，检查状态，再关闭
while True:
    time.sleep(30)   # 60 seconds or more for big task
    (command_output, exitstatus) = pexpect.run('ssh %s@%s "ls %s"' % (username,hostname,work_dir) ,withexitstatus=1,events={'password': password})
    if statfile in command_output.split('\r\n'):
        break

# 从远程主机下载文件或者目录
pexpect.run('scp %s@%s:%s/result.txt result.txt' % (username,hostname,work_dir) ,withexitstatus=1,events={'password': password})


#-------------- load data into bdp

os.system("""
hive -e "LOAD DATA LOCAL INPATH result.txt [OVERWRITE] INTO TABLE table_name;"
""")
