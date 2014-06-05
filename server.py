#! /usr/bin/python
import MySQLdb
import socket
import json
import login
import signup
import addLocation
import thumbsUp
import thumbsDown
import getLocation
import setThumb
import getThumb
import addComment
import addPicture
import getPicture
import getClosestLocation
import apikeys

size = 1024

#starts server to listen to port 5687
def startServer():
	port = 5687
	backlog = 5
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',port))
	s.listen(backlog)
	return s
#end function

def shutdownServer(s):
	s.close()
#end function

#opens database connection to mysql database
#I only use dynamodb for urls and pictures because otherwise its expensive
def openDatabaseConnection():
	connection = MySQLdb.connect(host="engr-cpanel-mysql.engr.illinois.edu",
			user = "msluo2_user",
			passwd = apikeys.password,
			db = "msluo2_poopify")
	return connection
#end function

#parses out the json 'function' field and sends data to correct function
def parse(data, conn, cursor):
	decodedData = json.loads(data)
	function = decodedData['function']

	if(function == 'login'):
		print 'login'
		return login.loginTo(decodedData, conn, cursor)
	elif(function == 'signup'):
		print 'signup'
		return signup.signup(decodedData, conn,cursor)
	elif(function == 'addLocation'):
		print 'Add Location'
		return addLocation.addLocation(decodedData, conn, cursor)
	elif(function == 'thumbsUp'):
		print 'thumbsUp'
		thumbsUp.thumbsUp(decodedData, conn, cursor)
	elif(function == 'thumbsDown'):
		print 'thumbsDown'
		thumbsDown.thumbsDown(decodedData, conn, cursor)
	elif(function == 'getLocation'):
		print 'getLocation'
		return getLocation.getLocation(decodedData, conn, cursor)
	elif(function=='setThumb'):
		print 'setThumb'
		setThumb.setThumb(decodedData, conn, cursor)
	elif(function=='getThumb'):
		print 'getThumb'
		return getThumb.getThumb(decodedData, conn,cursor)
	elif(function == 'addComment'):
		print 'addComment'
		return addComment.addComment(decodedData, conn, cursor)
	elif(function == 'addPicture'):
		print 'addPicture'
		return addPicture.testPicture(decodedData, conn, cursor)
	elif(function == 'getPicture'):
		print 'getPicture'
		return getPicture.getPicture(decodedData, conn, cursor)
	elif(function=='getClosestLocation'):
		print 'getClosestLocation'
		return getClosestLocation.getClosestLocation(decodedData, conn, cursor)
	else:
		print 'Bad function'
		return

#main
socket = startServer()
while 1:
	client, address = socket.accept()
	finalData = ''
	while 1:
		#keeps receiving data
		data = client.recv(size)
		if not data:
			break
		finalData+=data
		#used to find end of json, esp useful for image transfer
		if "\r\n\r\n" in finalData:
			break

	if finalData:
		print "\r\n\r\n"+finalData
		conn = openDatabaseConnection()
		cursor = conn.cursor()
		#sends json to be parsed
		sendToUser = parse(finalData, conn, cursor)
		print sendToUser
		#sends response back to user
		client.send(str(sendToUser))
		conn.close()
	client.close()
shutdownServer(socket)
