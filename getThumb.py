#! /usr/bin/python
import MySQLdb
import json

def getThumb(data, conn, cursor):
        decodedData=data
        user_ID=decodedData['user_id']
        location_ID=decodedData['location_id']
	cursor.execute('select thumbsUp from Rating where user_id='+str(user_ID)+' and location_id='+str(location_ID))
	query=cursor.fetchone()
	print query
	if(query==None):
		return -1
	print int(query[0])
	return int(query[0])
        
	
