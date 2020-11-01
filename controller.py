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


  def GET_FEATURED(self):
    data = json.loads(cherrypy.request.body.read().decode('utf-8'))
    response = {"result": "success"}

    if not isValidUser(data["username"], data["password"]):
      response["result"] = "error"
      response["body"] = "User not authenticated"
      return json.dumps(response)

    featured_fwd = {"computedRanking": 0}
    featured_mid = {"computedRanking": 0}
    featured_def = {"computedRanking": 0}
    featured_gkp = {"computedRanking": 0}

    for player in self.fplDB.players:
      # if forward
      if player["position"] == 4:
        computedRanking = (player["ict_position_rank"] * 4) + (player["form"] * 2) + (player["ppg"] * 3)
        if computedRanking > featured_fwd["computedRanking"]:
          featured_fwd = player
          featured_fwd["computedRanking"] = computedRanking

      # if midfielder
      if player["position"] == 3:
        computedRanking = (player["ict_position_rank"] * 4) + (player["form"] * 2) + (player["ppg"] * 3)
        if computedRanking > featured_mid["computedRanking"]:
          featured_mid = player
          featured_mid["computedRanking"] = computedRanking
 
      # if defender
      if player["position"] == 2:
        computedRanking = (player["ict_position_rank"] * 4) + (player["form"] * 2) + (player["ppg"] * 3)
        if computedRanking > featured_def["computedRanking"]:
          featured_def = player
          featured_def["computedRanking"] = computedRanking

      # if goalie
      if player["position"] == 1:
        computedRanking = (player["ict_position_rank"] * 4) + (player["form"] * 2) + (player["ppg"] * 3)
        if computedRanking > featured_fwd["computedRanking"]:
          featured_gkp = player
          featured_gkp["computedRanking"] = computedRanking

    response["featured_fwd"] = featured_fwd
    response["featured_mid"] = featured_mid
    response["featured_def"] = featured_def
    response["featured_gkp"] = featured_gkp

    import pprint
    pprint.pprint(response)

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