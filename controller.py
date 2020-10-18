import cherrypy
import json
from library import _fpl_database

class Controller(object):
  
  def __init__(self, fplDB=None):
    if fplDB is None:
      self.fplDB = _fpl_database()
    else:
      self.fplDB = fplDB

    self.fplDB.loadTemplate()

  def GET_ALL(self): 
    return json.dumps({
      "players": self.fplDB.players,
      "teams": self.fplDB.teams,
      "fixtures": self.fplDB.fixtures,
    })

  def GET_PLAYERS(self): 
    return json.dumps({"players": self.fplDB.players})

  def GET_PLAYER_BY_NAME(self):
    pass
  
  def GET_TEAMS(self): 
    return json.dumps({"teams": self.fplDB.teams})
  
  def GET_FIXTURES(self): 
    return json.dumps({"fixtures": self.fplDB.fixtures})