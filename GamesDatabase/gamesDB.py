import sqlite3



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class GamesDB:

	def __init__(self):
		self.connection = sqlite3.connect("games.db")
		self.connection.row_factory = dict_factory
		self.cursor = self.connection.cursor()

	def __del__(self):
		self.connection.close()

	def getGames(self):
		self.cursor.execute("SELECT * FROM games;")
		gamesList = self.cursor.fetchall()
		print("getting the collection")
		return gamesList

	def retrieveGame(self, data):
		######make sure data is in a list######
		#print (data)
		self.cursor.execute("SELECT * FROM games WHERE id= ? ;", [data])
		game = self.cursor.fetchall()
		print (game)
		return game

	def createGame(self, data):
		#print(data['title'][0])
		self.cursor.execute("INSERT INTO games (title, genre, console, multiplayer, rating, online) VALUES (?, ?, ?, ?, ?, ?)", (data['title'][0], data['genre'][0], data['console'][0], data['multiplayer'][0], data['rating'][0], data['online'][0]))
		self.connection.commit()
		return

	def killGames(self):
		self.cursor.execute("DELETE FROM games")
		return

	def deleteGame(self, data):
		self.cursor.execute("DELETE FROM games WHERE id = ? ", [data])
		self.connection.commit()
		print ("deleted game", data)
		return

	def updateGame(self, data, gameID):
		#Fix where clause?
		self.cursor.execute("UPDATE games SET title= ?, genre = ?, console = ?, rating = ?, multiplayer = ?, online = ?  WHERE id = ?", (data['title'][0], data['genre'][0], data['console'][0], data['rating'][0], data['multiplayer'][0], data['online'][0], gameID))
		self.connection.commit()
		return

	def getIDs(self):
		self.cursor.execute("SELECT id FROM games")
		idList = self.cursor.fetchall()
		#print (idList)
		return idList

	def createUser(self, data, password):
		self.cursor.execute("INSERT INTO users (userName, encryptedPassword, fName, lName, age) VALUES (?, ?, ?, ?, ?)", (data['userName'][0], password, data['fName'][0], data['lName'][0], data['age'][0]))
		self.connection.commit()
		return

	def getNames(self):
		self.cursor.execute("SELECT * FROM users")
		names = self.cursor.fetchall()
		return names

	def getPassword(self, name):
		self.cursor.execute("SELECT encryptedPassword FROM users WHERE userName = ?", [name])
		word = self.cursor.fetchall()
		return word

	def checkID(self):
		self.cursor.execute("SELECT id FROM users")
		word = self.cursor.fetchall()
		return word

