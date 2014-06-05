#! /usr/bin/python
import MySQLdb
import json

def signup(data, conn, cursor):
	
	cursor.execute('select user_id from User where user_email = "' + data['user_email'] +'"')
	queryData = cursor.fetchone()
	print queryData

	# this means the email is not being used
	if(queryData == None):
		cursor.execute('insert into User (user_email, password) values("' + data['user_email'] + '", "' + data['password'] + '")')
		conn.commit()
		return 1
	else:
		return -1

