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

