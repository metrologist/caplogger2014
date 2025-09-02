"""
Run this to create the database file for 34970_cap_logger.
Be careful not to overwrite an existing db file!!!
Initially this is intended as a secondary store along with the csv files.
Assuming that sqlite is inherently thread safe, then it should be the safe
way to allow another program (or thread) to access the db file data while the
logging is still running.

This could become an initialisation process available from the GUI.
"""
import sqlite3


db_name = "cap_environment_May_2022_on.db"
table_names = ['Reference', 'S_ball', 'Cropico_temp', 'AH11', 'GR_inner',
		'GR_outer', 'Permutable', 'Pressure']
conn =sqlite3.connect(db_name)
cursor = conn.cursor()

for x in table_names:
	command = "CREATE TABLE "+ x + "(time float, value float)"
	print command
	cursor.execute(command)
	
conn.commit()


#create tables

## cursor.execute("""CREATE TABLE albums
## 		(title text, artist text, release_date text, publisher text,
## 		media_type text)""")
## 		
## # insert some data
## cursor.execute("INSERT INTO albums VALUES ('Glow', 'Andy Hunter', '7/24/2012', 'Xplore Records', 'MP3')")
##  
## # save data to database
## conn.commit()
##  
## # insert multiple records using the more secure "?" method
## albums = [('Exodus', 'Andy Hunter', '7/9/2002', 'Sparrow Records', 'CD'),
##           ('Until We Have Faces', 'Red', '2/1/2011', 'Essential Records', 'CD'),
##           ('The End is Where We Begin', 'Thousand Foot Krutch', '4/17/2012', 'TFKmusic', 'CD'),
##           ('The Good Life', 'Trip Lee', '4/10/2012', 'Reach Records', 'CD')]
## cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?)", albums)
## conn.commit()
