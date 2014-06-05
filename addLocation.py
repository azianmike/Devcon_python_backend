#! /usr/bin/python
import MySQLdb
import json
import addComment
import setThumb

def addLocation(data, conn, cursor):
	user_id = data['user_id']
	thumbsUp = 0
	thumbsDown = 0
	if(data['thumbsUp'] == 'True'):
		thumbsUp = 1
	else:
		thumbsDown = 1
	lat = data['latitude']
	long = data['longitude']
	name = data['location_name']
	
	latMax = lat + .0001
	latMin = lat - .0001
	longMax = long + .0001
	longMin = long - .0001
	
	#check to see if there is already this GPS location in the database
	cursor.execute('select location_id from Location where latitude Between ' + str(latMin) + ' and ' + str(latMax) + ' and longitude between ' + str(longMin) + ' and ' + str(longMax))
	queryData = cursor.fetchone()
	if(queryData == None):
		#add location to the Location table
		cursor.execute('insert into Location(location_name,latitude,longitude,thumbsUp,thumbsDown,user_id) Values("' + name + '", ' + str(lat) + ', ' + str(long) + ', ' + str(0) + ', ' + str(0) + ', ' + str(user_id) + ')')
		conn.commit()
		#gets the id of the location inserted
		cursor.execute('SELECT LAST_INSERT_ID()')
		location_id = cursor.fetchone()
		#add comment to the Comment table
		commentData = json.dumps({'user_id': user_id, 'location_id': location_id[0], 'comment': data['comment']})
		addComment.addComment(json.loads(commentData), conn, cursor)
		#add rating to the Rating table
		ratingData = json.dumps({'user_id': user_id, 'location_id': location_id[0], 'thumbsUp': thumbsUp})
		ratingDataLoad = json.loads(ratingData)
		setThumb.setThumb(ratingDataLoad, conn, cursor)
		return 1
	else:
		return -1
