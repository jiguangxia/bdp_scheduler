#!/usr/bin/env bash

#-------------- set parameters
hostname="192.168.1.111"
username="xiajg"
password="111111"
statfile="~/__success__"

#-------------- download data from bdp

hive -e "SELECT * FROM gdm.gdm_m03_item_sku_da LIMIT 100;" > input.txt



#-------------- send data (and scipt) to remote, and calculation

# 上传文件到远程主机
expect << EOF
spawn scp input.txt $username@$hostname:~/input.txt
expect "*password:"
send "$password\r"
expect eof
EOF

# 初始化状态
expect << EOF
spawn ssh $username@$hostname "test -f $statfile && rm $statfile"
expect "*password:"
send "$password\r"
expect eof
EOF

# 在远程机执行shell命令
expect << EOF
spawn ssh $username@$hostname "python mytask.py"
expect "*password:"
send "$password\r"
expect eof
EOF


#-------------- task monitor

while :
do
    expect << EOF
    spawn ssh $username@$hostname "test -f $statfile && echo __success__"
    expect {
        "password:" {
            send "$password\n"
        }
    }
    expect __success__ { exit 55 }
EOF

    if [ $? -eq 55 ];then
        break
    else
        sleep 30
    fi
done


# 从远程主机下载文件或者目录
expect << EOF
spawn scp $username@$hostname:~/result.txt result.txt
expect "*password:"
send "$password\r"
expect eof
EOF


#-------------- load data into bdp

head result.txt
#hive -e "LOAD DATA LOCAL INPATH 'result.txt' OVERWRITE INTO TABLE table_name;"



