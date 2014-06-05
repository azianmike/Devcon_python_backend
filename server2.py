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
import thread
import getClosestLocation
import apikeys

size = 1024

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

def openDatabaseConnection():
	connection = MySQLdb.connect(host="engr-cpanel-mysql.engr.illinois.edu", #YOURSQL.SERVER.COM
			user = "eckles2_poopify", #USERNAME
			passwd = apikeys.password, #PASSWORD
			db = "eckles2_poopify") #DB_Poopify
	return connection
#end function

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
		
def newAcceptedConnection(client, address):
	try:
		finalData = ''
		while 1:
			data = client.recv(size)
			if not data:
				break
			print data
			finalData+=data
			if "\r\n\r\n" in finalData:
				break
		if finalData:
			print finalData
			conn = openDatabaseConnection()
			cursor = conn.cursor()
			sendToUser = parse(finalData, conn, cursor)
			print sendToUser
			client.send(str(sendToUser))
			conn.close()
		client.close()
	except:
		print 'Caught timeout'
		
socket = startServer()
while 1:
	client, address = socket.accept()
	client.settimeout(10)
	print 'Accepted Connection from ', address
	thread.start_new_thread(newAcceptedConnection, (client, address))
shutdownServer(socket)
