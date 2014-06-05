#! /usr/bin/python
import MySQLdb
import json
import collections

import apikeys
import boto.dynamodb

def getPicture(decodedData, conn, cursor):
	location_id = decodedData['location_id']
	
	#getting from dynamodb
	conn2 = boto.dynamodb.connect_to_region(
        'us-east-1',
        aws_access_key_id=apikeys.AWSAccessKeyId,
        aws_secret_access_key=apikeys.AWSSecretKey)
	table = conn2.get_table('Picture')
	#queries dynamodb for all urls that have key of location_id
	pictureList = conn2.query(table, location_id)
	objectList = []
	for row in pictureList:
		d = collections.OrderedDict()
		d['url'] = str(row['url'])
		objectList.append(d)

	temp = collections.OrderedDict()
	temp['pictures'] = objectList
	returnData = json.dumps(temp)
	return returnData
