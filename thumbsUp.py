#! /usr/bin/python
import MySQLdb
import json

def thumbsUp(data, conn, cursor):
	cursor.execute('update Location set thumbsUp = thumbsUp + 1 where location_id='
	+ str(data['location_id']))
	conn.commit()
	
