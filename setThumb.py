#! /usr/bin/python
import MySQLdb
import json

def setThumb(data, conn, cursor):
	decodedData=data
	user_ID=decodedData['user_id']
	location_ID=decodedData['location_id']
	thumbsUp=decodedData['thumbsUp']
	alreadyVote = False
	voteThumbs = 100
	
	#check to see if it exists in database or not
	cursor.execute('select thumbsUp from Rating where user_id='+str(user_ID)+' and location_id='+str(location_ID))
	queryCount=cursor.fetchone()
	if(queryCount==None): #does not exist
		cursor.execute('insert into Rating(user_id, location_id, thumbsUp) values('+str(user_ID)+', '+str(location_ID)+', '+str(thumbsUp)+')')
		conn.commit()	
	else: #does exist
		voteThumbs = queryCount[0]
		print voteThumbs
		cursor.execute('update Rating set thumbsUp='+str(thumbsUp)+' where user_id='+str(user_ID)+' and location_id='+str(location_ID))
		conn.commit()
		alreadyVote = True
	cursor.execute('select thumbsUp, thumbsDown from Location where location_id='+str(location_ID))
	query=cursor.fetchone()
	if(int(thumbsUp)==1): #thumbsUp
		if alreadyVote == False or voteThumbs == 0:
			cursor.execute('update Location set thumbsUp=thumbsUp+1 where location_id='+str(location_ID))
		if voteThumbs == 0:
			cursor.execute('update Location set thumbsDown=thumbsDown-1 where location_id='+str(location_ID))
	else: #thumbsDown
		if alreadyVote == False or voteThumbs == 1:
			cursor.execute('update Location set thumbsDown=thumbsDown+1 where location_id='+str(location_ID))
		if voteThumbs == 1:
			cursor.execute('update Location set thumbsUp=thumbsUp-1 where location_id='+str(location_ID))
	conn.commit()
