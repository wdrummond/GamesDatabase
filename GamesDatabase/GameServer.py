from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from passlib.hash import bcrypt
from http import cookies
from session import SessionStore
from gamesDB import *


gSessionStore = SessionStore()


class GameServer(BaseHTTPRequestHandler):

	def do_OPTIONS(self):
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
		self.send_header('Access-Control-Allow-Headers', 'Content-Type, Content-Length, Origin, Cookie, Set-Cookie')
		self.end_headers()
		return

	def do_GET(self):
		self.load_cookie()
		print("About to load session")
		self.load_session()

		member,address = self.getMember()
		idList = self.getIDs()
		idPass = False
		#print(idList)
		if member in idList:
			idPass = True

		##Retrieve##
		#if self.gLoggedIn:
		if len(address) >= 3 and self.path.startswith("/games") and idPass:
			if "counter" in self.cookie:
				counter = int(self.cookie["counter"].value)
			else:
				counter = 0
			self.cookie["counter"] = counter + 1

			print(self.cookie['counter'])


			self.send_response(200) #status code 200, All OK
			self.send_header('Access-Control-Allow-Origin', self.headers["Origin"])
			self.send_header("Access-Control-Allow-Credentials", "true")
			self.send_header('Access-Control-Allow-Headers', 'Content-Type, Content-Length, Origin')
			self.send_header('Content-Type', 'application/json')
			self.send_cookie()

			self.end_headers()
			self.wfile.write(bytes(self.cookie["counter"].value + " times bitten.", "utf-8"))


			#member = self.path[7:]
			print("getting game", member)
			self.getGame(member)

		##Index/List##

		elif self.path.startswith("/games") and len(member) == 0:
			if 'userID' not in self.session:
				self.Handle401()
				return
			print (self.session['userID'])

			# if "counter" in self.cookie:
			# 	counter = int(self.cookie["counter"].value)
			# else:
			# 	counter = 0
			# self.cookie["counter"] = counter + 1
			# print(self.cookie['counter'])

			self.send_response(200) #status code 200, All OK
			self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
			self.send_header("Access-Control-Allow-Credentials", "true")
			self.send_header('Content-Type', 'application/json')
			self.send_cookie()
			self.end_headers()

			#self.wfile.write(bytes(self.cookie["counter"].value + " times bitten.", "utf-8"))


			self.getGamesCollection()

		else:
			self.Handle404()
		# else:
		# 	self.Handle401()


	def do_POST(self):

		self.load_cookie()
		self.load_session()

		unique = True
		member, address = self.getMember()
		print (member)

		length = int(self.headers['Content-Length'])
		data = self.rfile.read(length).decode("utf-8")
		parsedData = parse_qs(data)

		##Check for unique name
		if self.path.startswith("/users"):
			if not self.checkUniqueName(parsedData['userName']):
				unique = False
				self.Handle401()
				return


		##CREATE##
		if self.path.startswith("/games") and member == "":
			if 'userID' not in self.session:
				self.Handle401()
				return

			self.send_response(201) #status code 201, Created OK

			self.send_header('Access-Control-Allow-Origin', self.headers["Origin"])
			self.send_header("Access-Control-Allow-Credentials", "true")
			self.send_header('Access-Control-Allow-Headers', 'Content-Type, Content-Length, Origin')
			self.end_headers()

			print("creating game")

			print (parsedData)

			self.createGame(parsedData)

		##Creating Users
		elif self.path.startswith("/users") and member == "":
			if 'userID' not in self.session:
				self.Handle401()
				return

			self.send_response(201) #status code 201, Created OK

			self.send_header('Access-Control-Allow-Origin', self.headers["Origin"])
			self.send_header("Access-Control-Allow-Credentials", "true")
			self.send_header('Access-Control-Allow-Headers', 'Content-Type, Content-Length, Origin')
			self.end_headers()

			if unique:
				self.createUser(parsedData)
			else:
				self.Handle401()

		##Logging In
		elif self.path.startswith("/session"):

			##Cookie checker##
			if "counter" in self.cookie:
				counter = int(self.cookie["counter"].value)
			else:
				counter = 0
			self.cookie["counter"] = counter + 1

			print(self.cookie['counter'].value)


			#check if name exists
			nameExist = self.getUser(parsedData['userName'][0])
			if nameExist:
				matched = self.passwordMatch(parsedData)
				if matched:
					print("id = " + str(nameExist['id']))
					self.session['userID'] = nameExist['id']
					#print (self.session)
					# print("The session ID is: " + str(self.session['sessionID']))
					# print ("sessions user id is " + str(self.session['userID']))
					self.send_response(201) #status code 201, Created OK
					self.send_cookie()
					self.send_header('Access-Control-Allow-Origin', self.headers["Origin"])
					self.send_header("Access-Control-Allow-Credentials", "true")
					self.send_header('Access-Control-Allow-Headers', 'Content-Type, Content-Length, Origin')
					self.end_headers()
				else:
					self.Handle401()
			else:
				self.Handle401()

		else:
			#404 response
			self.Handle404()

	

	def do_PUT(self):
		self.load_cookie()
		self.load_session()

		member, address = self.getMember()
		idList = self.getIDs()
		idPass = False
		print(idList)
		if member in idList:
			idPass = True

		##REPLACE##
		if self.path.startswith("/games") and idPass:
			# if 'userID' not in self.session:
			# 	self.Handle401()
			# 	return

			self.send_response(204) #status code 201, Created OK

			self.send_header('Access-Control-Allow-Origin', self.headers["Origin"])
			self.send_header("Access-Control-Allow-Credentials", "true")
			self.send_header('Access-Control-Allow-Headers', 'Content-Type, Content-Length, Origin')
			self.send_header('Content-Type', 'application/json')
			self.end_headers()

			print("updating game")

			length = int(self.headers['Content-Length'])
			data = self.rfile.read(length).decode("utf-8")
			parsedData = parse_qs(data)
			print (parsedData)

			self.updateGame(parsedData, member)

		else:
			#404 response
			self.Handle404()

	def do_DELETE(self):
		self.load_cookie()
		self.load_session()

		member, address = self.getMember()
		idList = self.getIDs()
		idPass = False
		print(idList)
		if member in idList:
			idPass = True

		##DELETE##
		if len(address) >= 3 and self.path.startswith("/games") and len(member) > 0 and idPass:
			# if 'userID' not in self.session:
			# 	self.Handle401()
			# 	return

			print("deleting game", member)

			self.send_response(204) #status code 200, All OK
			self.send_header('Access-Control-Allow-Origin', '*')
			self.send_header('Content-Type', 'application/json')
			self.end_headers()

			self.deleteGame(member)

		elif self.path.startswith("/games") and len(member) == 0:
			# if 'userID' not in self.session:
			# 	self.Handle401()
			# 	return
				
			self.send_response(204) #status code 200, All OK
			self.send_header('Access-Control-Allow-Origin', '*')
			self.send_header('Content-Type', 'application/json')
			self.end_headers()

			print("deleting all games")
			self.deleteCollectionData()

		else:
			#404 response
			self.Handle404()

		return


	def getGamesCollection(self):
		db = GamesDB()
		gamesList = db.getGames()
		#print(json.dumps(gamesList))
		self.wfile.write(bytes(json.dumps(gamesList), "utf-8"))
		return

	def getGame(self, game):
		db = GamesDB()
		gameList = db.retrieveGame(game)
		print(gameList)
		self.wfile.write(bytes(json.dumps(gameList), "utf-8"))
		return


	def createGame(self,game):
		db = GamesDB()
		db.createGame(game)
		return


	def deleteCollectionData(self):
		db = GamesDB()
		db.killGames()
		return


	def deleteGame(self, game):
		db = GamesDB()
		db.deleteGame(game)
		return

	def updateGame(self, data, gameID):
		db = GamesDB()
		db.updateGame(data, gameID)
		#self.wfile.write(bytes(json.dumps(gamesList), "utf-8"))
		return



	def Handle404(self):
		self.send_response(404) #status code 404, Not OK
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write(bytes("404 Not Found", "utf-8"))


	def Handle401(self):
		self.send_response(401)
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Content-Type', 'application/json')
		self.end_headers()

	def getMember(self):
		member = ""
		address = self.path.split('/')
		collection = address[1]
		if len(address) >= 3:
			member = address[2]
			print (len(member))
		return member, address

	def getIDs(self):
		db = GamesDB()
		idList = db.getIDs()
		newList = []
		for i in idList:
			newList.append(str(i['id']))
		return newList

	def createUser(self, data):
		db = GamesDB()
		h = bcrypt.encrypt(data['encryptedPassword'][0])
		db.createUser(data, h)
		return

	def checkUniqueName(self, name):
		db = GamesDB()
		uniqueName = False
		names = db.getNames()
		newList = []
		for i in names:
			newList.append(str(i['userName']))
		if name[0] in newList:
			#print("returning False because the name is not unique")
			return False
		else:
			#print("returning True", name[0])
			return True

	def getUser(self, username):
		db = GamesDB()
		names = db.getNames()
		newList = []
		for i in names:
			newList.append(i['userName'])
			if username in newList:
				return i
		return False

	def passwordMatch(self, data):
		db = GamesDB()
		word = db.getPassword(data['userName'][0])
		if bcrypt.verify(data['password'][0], word[0]['encryptedPassword']):
			print("Passwords Match!")
			return True
		

	def load_session(self):
		# check for a session ID in a cookie
		if 'sessionID' in self.cookie:
		# try to load the session object using the sessionID
			sessionID = self.cookie['sessionID'].value
			self.session = gSessionStore.getSession(sessionID)
			# IF session data was retrieved:
			print("sessionID:" + sessionID)
			if self.session:
				# yay! save/use it.
				pass
			else:
				# create a new session object, save/use it.
				sessionID = gSessionStore.createSession()
				self.session = gSessionStore.getSession(sessionID)
				# store the session ID in a cookie
				self.cookie['sessionID'] = sessionID
			# ELSE:
		else:
			# create a new session object, save/use it.
			sessionID = gSessionStore.createSession()
			self.session = gSessionStore.getSession(sessionID)
			print("New Session id is:" + sessionID)
			# store the session ID in a cookie
			self.cookie['sessionID'] = sessionID


	def load_cookie(self):
		if "Cookie" in self.headers:
			self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
			#print(self.cookie)
		else:
			self.cookie = cookies.SimpleCookie()


	def send_cookie(self):
		for morsel in self.cookie.values():
			self.send_header("Set-Cookie", morsel.OutputString())



		


def run():
	listen = ('127.0.0.1', 8080)
	server = HTTPServer(listen, GameServer)

	print ("Listening for the user")
	server.serve_forever()
####php -S localhost:9090###



run()