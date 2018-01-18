# bdp_scheduler

---------------------------
this scheduler mainly deal with data transfer and program scheduling on
Hadoop-Jumperserver-GPUsever structure.

Based on different environment of Jumpsever, there are three methods to do this
job:

script                    | dependencies
--------------------------|------------------------------
scheduler_paramiko.py     | paramiko package in python
scheduler_pexpect.py      | pexpect package in python
scheduler_sshpass.sh      | sshpass tool in linux
scheduler.sh              | expect tool in linux

### install python package offline
1. download source code from here (I choosed release-3.2):
    https://github.com/pexpect/pexpect/releases
2. decompress it
    tar -zxvf pexpect-3.2.tar.gz
2. install use python
    cd pexpect-3.2
    python setup.py install --prefix=/home/mart_rmb/data_dir/xiajiguang/usr
