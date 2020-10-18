import cherrypy
import json
from library import _fpl_database

class Controller(object):
  
  def __init__(self, fplDB=None):
    if fplDB is None:
      self.fplDB = _fpl_database()
    else:
      self.fplDB = _fpl_database

    self.fplDB.loadTemplate()

  def GET_ALL(self): 
    return json.dumps(self.fplDB)