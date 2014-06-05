#! /usr/bin/python
import MySQLdb
import json

def thumbsDown(data, conn, cursor):
	cursor.execute('update Location set thumbsDown = thumbsDown + 1 where location_id='
	+ str(data['location_id']))
	conn.commit()
	
