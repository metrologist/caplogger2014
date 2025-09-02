"""
Add data from previous csv files into sqlite database.
"""

import csv
import sqlite3
import os


conn = sqlite3.connect('cap_environment_2012_on.db')
table_names = ['Reference', 'S_ball', 'Cropico_temp', 'AH11', 'GR_inner',
		'GR_outer', 'Permutable', 'Pressure']
file_names =['ref.csv', 's_ball.csv', 'ref_temp.csv', 'ah11.csv', 'GR_inner.csv',
            'GR_outer.csv', 'permutable.csv', 'pressure.csv']

curs = conn.cursor()

for i in range(len(file_names)):
    reader = csv.reader(open(os.path.join('Data', file_names[i]), 'r'), delimiter=',')
    for row in reader:
        command = "INSERT INTO " + table_names[i] + " VALUES(?,?)"
        curs.execute(command, [row[0], row[1]])

    
conn.commit()