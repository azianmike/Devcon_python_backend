#! /usr/bin/python
import MySQLdb
import json

#do not use code, sql injection attacks
def thumbsUp(data, conn, cursor):
	cursor.execute('update Location set thumbsUp = thumbsUp + 1 where location_id='
	+ str(data['location_id']))
	conn.commit()
	
