#! /usr/bin/python
import MySQLdb
import json

def loginTo(data, conn, cursor):
	cursor.execute('Select user_id,password from User where user_email = "' + data['user_email'] + '" and password = "' + data['password'] + '"')
	queryData = cursor.fetchone()
	if(queryData == None):
		return -1
	else:
		return queryData[0]

