# -*- coding: utf-8 -*-
"""
This script is designed to access the SQLite database file that stores the
temperature/pressure data in the calculable capacitor area.

This is a hand-crafted, non-GUI version that assumes the data structure is as
expected.

The logger programme might eventually be improved by dumping csv files as the
storage system and instead easing multithreading overhead in Python by relying
on SQLite to manage multiple accesses to common data.

Created on Tue Jan 29 16:07:40 2013

@author: k.jones
"""

import sqlite3
import time
import matplotlib.pyplot as plt

alpha = 0.00385 # for quick conversion to temperature

fig, axs = plt.subplots(8, 1, sharex = True, sharey = False)
fig.set_facecolor('white')
axs[0].set_title('Capacitor Environment')
for i in range(8):
    axs[i].set_axis_bgcolor('white')
    axs[i].grid(True, color = 'black')
    axs[i].tick_params(axis = 'both', labelsize = 8)
fig.tight_layout()


db_name = "dist\\cap_environment_2012_on.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

sql = "SELECT name FROM sqlite_master WHERE type = 'table'" #ORDER BY name"
cursor.execute(sql)
tables = cursor.fetchall()
now = time.time()
then = now-3600*24*1 #1 days
i = 0
for table in tables:
    sql = "SELECT time, value FROM " + table[0]+ " WHERE time BETWEEN "+ repr(then) +" AND " + repr(now)
    cursor.execute(sql)
    rowset = cursor.fetchall()
    cx = []
    cy = []
    for row in rowset:
        cx.append(row[0])
        cy.append(row[1])
    print table[0] #table name is a tuple, just want the name!
##     print cx, cy
    axs[i].set_ylabel(table[0], size ='x-small')

    if time.localtime(time.time()).tm_isdst==0:#this flag is set by the localtime call?#time.daylight ==0: # for computer time at this instant.
        offset = time.timezone # NZST
    else:
        offset = time.altzone # NZDT

    times = [(b - offset)/(24*3600)for b in cx] #matplotlib prefers decimal days
    if i == 7:
        values = cy # for pressure
    else:
        values = [(b-100.0)/(100.0*alpha) for b in cy]
    axs[i].plot_date( times, values, 'y')   
    i = i + 1

fig.autofmt_xdate() # rotates labels for clarity
fig.tight_layout()
fig.subplots_adjust( hspace = 0.1) 
    
plt.show()