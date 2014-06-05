#! /usr/bin/python
import MySQLdb
import json

def addComment(data, conn, cursor):
	decodedData = data
	cursor.execute('insert into Comment(location_id, user_id, comment) Values(' + str(decodedData['location_id']) + ', ' + str(decodedData['user_id']) + ', "' + decodedData['comment'] + '")')
	conn.commit()
	return 1
