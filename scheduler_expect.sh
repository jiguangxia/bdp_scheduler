#!/usr/bin/expect

spawn ssh xiajg@192.168.1.111
expect "*password:"
send "111111\r"
expect "*~$ "
send "nohup python mytask.py&\r"
expect "*nohup.out'"
send "\rexit\r"
expect eof

