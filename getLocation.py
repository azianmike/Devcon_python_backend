#! /usr/bin/python
import MySQLdb
import json
import collections

def getLocation(data, conn, cursor):
	lat = float(data['latitude'])
	long = float(data['longitude'])
	
	latMax = lat + .333333
	latMin = lat - .333333
	
	longMax = long + .333333
	longMin = long - .333333
	
	cursor.execute('select * from Location where latitude between ' + str(latMin) + ' and ' + str(latMax) + ' and longitude between ' + str(longMin) + ' and ' + str(longMax))
	locationList = cursor.fetchall()
	#print locationList
	#print locationList[0][2]
	objectList = []
	for row in locationList:
		commentArray = []
		d = collections.OrderedDict()
		cursor.execute('select location_id,user_id,comment from Comment where location_id = ' + str(row[0]))
		comments = cursor.fetchall()
		for comment in comments:
			commentDict = collections.OrderedDict()
			commentDict['user_id'] = str(comment[1])
			commentDict['comment'] = str(comment[2])
			commentArray.append(commentDict)
		d['location_id'] = str(row[0])
		d['location_name'] = row[1]
		d['latitude'] = str(row[2])
		d['longitude'] = str(row[3])
		d['thumbsUp'] = str(row[4])
		d['thumbsDown'] = str(row[5])
		d['user_id'] = str(row[6])
		d['commentArray']=commentArray
		objectList.append(d)
	temp = collections.OrderedDict()
	temp['locations'] = objectList
	#temp['comments'] = commentArray
	returnData = json.dumps(temp)
	return returnData
