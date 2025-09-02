"""
My use of ticks since 1970 is not entirely compatible with matplotlib's 
0001-01-01 as start of epoch
"""

import datetime
import matplotlib
from matplotlib import dates
import time

aa = time.time()

a = aa/3600/24.0 + 1969*365.25 - 14 + 0.291666666628 # 14 days for gregorian? and 0.29 for???

b = dates.date2num(datetime.datetime.now())

print('time in ticks since 1970 ', aa)
print('calculated days ',a)
print('time in days since 0001-01-01 ', b)
print('difference calculated - matplotlib ', a-b)
print(datetime.datetime.now())