import cherrypy
import json
from library import _fpl_database

def isValidUser(username, password):

  f = open("users.txt", "r")

  for line in f:
    u, p = line.split()
    if username == u and password == p:
      return True

  return False

class Controller(object):
  
  def __init__(self, fplDB=None):
    if fplDB is None:
      self.fplDB = _fpl_database()
    else:
      self.fplDB = fplDB

    self.fplDB.loadTemplate()

  # GET METHODS

  def GET_ALL(self): 

    data = json.loads(cherrypy.request.body.read().decode('utf-8'))
    response = {"result": "success"}

    if isValidUser(data["username"], data["password"]):
      response["players"] = self.fplDB.players
      response["teams"] = self.fplDB.teams
      response["fixtures"] = self.fplDB.fixtures
    else:
      response["result"] = "error"
      response["body"] = "User not authenticated."

    return json.dumps(response)

  def GET_PLAYERS(self): 

    data = json.loads(cherrypy.request.body.read().decode('utf-8'))
    response = {"result": "success"}

    if isValidUser(data["username"], data["password"]):
      response["players"] = self.fplDB.players
    else:
      response["result"] = "error"
      response["body"] = "User not authenticated."

    return json.dumps(response)
  
  def GET_TEAMS(self): 

    data = json.loads(cherrypy.request.body.read().decode('utf-8'))
    response = {"result": "success"}

    if isValidUser(data["username"], data["password"]):
      response["teams"] = self.fplDB.teams
    else:
      response["result"] = "error"
      response["body"] = "User not authenticated."

    return json.dumps(response)
  
  def GET_FIXTURES(self): 
    data = json.loads(cherrypy.request.body.read().decode('utf-8'))
    response = {"result": "success"}

    if isValidUser(data["username"], data["password"]):
      response["fixtures"] = self.fplDB.fixtures
    else:
      response["result"] = "error"
      response["body"] = "User not authenticated."

    return json.dumps(response)

  # POST METHODS

  def CREATE_ACCOUNT(self):

    data = json.loads(cherrypy.request.body.read().decode('utf-8'))

    f = open("users.txt", "a")
    f.write(data["username"] + " " + data["password"] + "\n")

    return json.dumps({"result": "success"})

  def AUTHENTICATE(self):

    data = json.loads(cherrypy.request.body.read().decode('utf-8'))

    if isValidUser(data["username"], data["password"]):
      return json.dumps({"result": "success"})
      
    return json.dumps({"result": "error", "body": "Invalid user/password combo."})