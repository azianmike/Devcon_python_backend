#! /usr/bin/python
import MySQLdb
import json
import collections

def getClosestLocation(data, conn, cursor):
	lat=float(data['latitude'])
	lng=float(data['longitude'])
	execMe='SELECT *, ( 3959 * acos( cos( radians('+str(lat)+') ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians('+str(lng)+') ) + sin( radians('+str(lat)+') ) * sin( radians( latitude ) ) ) ) AS distance FROM Location HAVING distance < 25 ORDER BY distance LIMIT 0 , 1'
	#execMe='select thumbsUp from Rating where user_id=44 and location_id=2
	cursor.execute(execMe)
	location=cursor.fetchone()
	
        cursor.execute('select location_id,user_id,comment from Comment where location_id = ' + str(location[0]))
        comments = cursor.fetchall()
	
	commentArray=[]
        for comment in comments:
      		commentDict = collections.OrderedDict()
        	commentDict['user_id'] = str(comment[1])
                commentDict['comment'] = str(comment[2])
                commentArray.append(commentDict)
		print 'enter1'	
	
	if(location==None):
		return -1
	d=collections.OrderedDict()
	d['location_id'] = str(location[0])
        d['location_name'] = location[1]
        d['latitude'] = str(location[2])
        d['longitude'] = str(location[3])
        d['thumbsUp'] = str(location[4])
        d['thumbsDown'] = str(location[5])
        d['user_id'] = str(location[6])
        d['commentArray']=commentArray
	returnData=json.dumps(d)
	print returnData
	return returnData

	
