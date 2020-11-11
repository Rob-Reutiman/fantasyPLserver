import cherrypy
import json
from library import _fpl_database

def isValidUser(users, username, password):

  u = users.get(username)

  if u is None:
    return "new"
  if password == u["password"]:
    return "valid"

  return "wrong"

class Controller(object):
  
  def __init__(self, fplDB=None):
    if fplDB is None:
      self.fplDB = _fpl_database()
    else:
      self.fplDB = fplDB

    self.fplDB.loadTemplate()

  # GET METHODS

  def AUTHENTICATE(self):
    data = json.loads(cherrypy.request.body.read().decode('utf-8'))

    result = isValidUser(self.fplDB.users, data["username"], data["password"])

    if result == "valid":
      return json.dumps({"result": "success"})

    if result == "wrong":
      return json.dumps({"result": "error", "body": "Invalid user/password combo."})

    self.fplDB.users[data["username"]] = {
      "password": data["password"],
      "team": {
        "GKs": ["", ""],
        "DEFs": ["", "", "", "", ""],
        "MIDs": ["", "", "", "", ""],
        "FWDs": ["", "", ""]
      }
    }

    return json.dumps({"result": "success"})
      
  def GET_ALL(self): 

    response = {"result": "success"}

    response["players"] = self.fplDB.players
    response["teams"] = self.fplDB.teams
    response["fixtures"] = self.fplDB.fixtures

    return json.dumps(response)

  def GET_PLAYERS(self): 

    response = {"result": "success"}
    response["players"] = self.fplDB.players

    return json.dumps(response)

  def GET_FEATURED(self):
    response = {"result": "success"}

    featured_fwd = {"computedRanking": 0}
    featured_mid = {"computedRanking": 0}
    featured_def = {"computedRanking": 0}
    featured_gkp = {"computedRanking": 0}

    for player in self.fplDB.players:
      # if forward
      if int(player["position"]) == 4:
        computedRanking = (float(player["form"]) * 2) + (float(player["ppg"]) * 3) / (int(player["ict_position_rank"]))
        if computedRanking > featured_fwd["computedRanking"]:
          featured_fwd = player
          featured_fwd["computedRanking"] = computedRanking

      # if midfielder
      if int(player["position"]) == 3:
        computedRanking = (float(player["form"]) * 2) + (float(player["ppg"]) * 3) / (int(player["ict_position_rank"]))
        if computedRanking > featured_mid["computedRanking"]:
          featured_mid = player
          featured_mid["computedRanking"] = computedRanking
 
      # if defender
      if int(player["position"]) == 2:
        computedRanking = (float(player["form"]) * 2) + (float(player["ppg"]) * 3) / (int(player["ict_position_rank"]))
        if computedRanking > featured_def["computedRanking"]:
          featured_def = player
          featured_def["computedRanking"] = computedRanking

      # if goalie
      if int(player["position"]) == 1:
        computedRanking = (float(player["form"]) * 2) + (float(player["ppg"]) * 3) / (int(player["ict_position_rank"]))
        if computedRanking > featured_fwd["computedRanking"]:
          featured_gkp = player
          featured_gkp["computedRanking"] = computedRanking

    response["featured_fwd"] = featured_fwd
    response["featured_mid"] = featured_mid
    response["featured_def"] = featured_def
    response["featured_gkp"] = featured_gkp

    return json.dumps(response)

  def GET_TEAMS(self): 

    response = {"result": "success"}

    response["teams"] = self.fplDB.teams

    return json.dumps(response)
  
  def GET_FIXTURES(self): 
    response = {"result": "success"}

    response["fixtures"] = self.fplDB.fixtures

    return json.dumps(response)

  def GET_USER_TEAM(self): 
    data = json.loads(cherrypy.request.body.read().decode('utf-8'))

    username = data["username"]
    u = self.fplDB.users.get(username)

    response = {"result": "success"}
    response["team"] = u["team"]

    return json.dumps(response)

  def UPDATE_USER_TEAM(self): 
    data = json.loads(cherrypy.request.body.read().decode('utf-8'))

    response = {"result": "success"}
    username = data["username"]
    self.fplDB.users[username]["team"] = data["team"]

    print(self.fplDB.users[username])

    return json.dumps(response)