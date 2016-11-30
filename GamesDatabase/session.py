import base64, os

class SessionStore:

        def __init__(self):
                self.sessionData = {}
                return

        def createSession(self):
                newSessionId = self.generateSessionId()
                self.sessionData[newSessionId] = {}
                print(self.sessionData)
                return newSessionId
 
        def getSession(self, sessionId):
                if sessionId in self.sessionData:
                        return self.sessionData[sessionId]
                else:
                        return None
 
        def generateSessionId(self):
                r = os.urandom(32)
                return base64.b64encode(r).decode("utf-8")


# Session {
# 	1233: {
# 		userId: 1
# 	}
# 	23444: {
# 		userId: 2
# 	}
# }