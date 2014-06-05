#! /usr/bin/python
import MySQLdb
import json
import boto
import uuid
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import apikeys
import boto.dynamodb


def testPicture(decodedData,connection,cursor):
	#print decodedData['data']
	#Make the file locally so that it can be uploaded to S3
	fileName = str(uuid.uuid1()) + ".jpg"
	fh = open("images/" + fileName, "wb")
	fh.write(decodedData['data'].decode('base64'))
	fh.close()
	
	#upload the file to S3
	conn = S3Connection(apikeys.AWSAccessKeyId, apikeys.AWSSecretKey)
	bucket = conn.get_bucket("devcontest", False, None)
	k = Key(bucket)
	k.key = fileName
	#uploads file
	k.set_contents_from_filename("images/" + fileName, None, None)
	#sets to public
	k.set_acl('public-read')
	#gets a url back
	url = k.generate_url(expires_in=0,query_auth=False)
	conn.close()

	#putting urls into dynamodb
	conn2 = boto.dynamodb.connect_to_region(
        'us-east-1',
        aws_access_key_id=apikeys.AWSAccessKeyId,
        aws_secret_access_key=apikeys.AWSSecretKey)
	table = conn2.get_table('Picture')
	#nosql db uses key, value pair. key is location id and value is url
	item = table.new_item(hash_key=decodedData['location_id'], range_key=url)
	item.put()

	return url
