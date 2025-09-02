# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:24:45 2013
Investigating seconds since 1970(as in Python)to
Excel's time 'serial number'
@author: Keith
"""

import datetime as dt

import time
a = time.time()
print a

#b = dt.datetime(2013,3,11,8,15,30)
#print b
c =time.localtime(a)
print c