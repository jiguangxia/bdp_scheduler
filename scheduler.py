#-*- coding: utf-8 -*-
#!/usr/bin/python

import ssh
import time
import os


#-------------- download data from bdp

os.system("""
hive -e "SELECT * FROM gdm.gdm_03_item_sku_da LIMIT 100;" > input.txt
""")


#-------------- send data (and scipt) to remote, and calculation

# 新建一个ssh客户端对象
client = ssh.SSHClient()

# 设置成默认自动接受密钥
client.set_missing_host_key_policy(ssh.AutoAddPolicy())

# 连接远程主机
client.connect("192.168.1.111", port=22, username="xiajg", password="111111")

# 新建 sftp session
sftp = client.open_sftp()

# 上传文件到远程主机
sftp.put('mytask.py', 'mytask.py')
sftp.put('input.txt', 'input.txt')

# 初始化状态
if '__success__' in sftp.listdir():
    sftp.remove('__success__')

# 在远程机执行shell命令
stdin, stdout, stderr = client.exec_command("python mytask.py")


#-------------- task monitor

# 等待程序运行完成
# 如果程序运行时间较长，可以尝试每次循环内建立连接，检查状态，再关闭
while True:
    time.sleep(5)   # 60 seconds or more for big task
    if '__success__' in sftp.listdir():
        break

# 从远程主机下载文件或者目录
sftp.get('result.txt', 'result.txt')


#-------------- load data into bdp

os.system("""
hive -e "LOAD DATA LOCAL INPATH result.txt [OVERWRITE] INTO TABLE table_name;"
""")


