#-*- coding: utf-8 -*-
#!usr/bin/python

import time


f = open('result.txt','w')
for i in range(10):
    f.write(str(i) + '\n')
    time.sleep(10)

f.close()


open('__success__','w').close()

