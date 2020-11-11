import cherrypy
from library import _fpl_database
from controller import Controller

# class for CORS
class optionsController:
    def OPTIONS(self, *args, **kwargs):
        return ""

# function for CORS
def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = '*'
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

def start_service():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    fplDB = _fpl_database()

    fplController = Controller(fplDB=fplDB)

    dispatcher.connect('get all data', '/', controller=fplController, action = 'GET_ALL', conditions=dict(method=['POST']))
    dispatcher.connect('get player data', '/auth/', controller=fplController, action = 'AUTHENTICATE', conditions=dict(method=['POST']))
    dispatcher.connect('get player data', '/players/', controller=fplController, action = 'GET_PLAYERS', conditions=dict(method=['POST']))
    dispatcher.connect('get team data', '/teams/', controller=fplController, action = 'GET_TEAMS', conditions=dict(method=['POST']))
    dispatcher.connect('get fixture data', '/fixtures/', controller=fplController, action = 'GET_FIXTURES', conditions=dict(method=['POST']))
    dispatcher.connect('create account', '/create/', controller=fplController, action = 'CREATE_ACCOUNT', conditions=dict(method=['POST']))
    dispatcher.connect('featured players', '/featured/', controller=fplController, action='GET_FEATURED', conditions=dict(method=['POST']))

    # CORS related options connections
    dispatcher.connect('all', '/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('players', '/auth/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('players', '/players/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('teams', '/teams/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('fixture', '/fixtures/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('create account', '/create/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('featured', '/featured/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))


    conf = {

      'global': {
        'server.thread_pool': 5,
        'server.socket_host': '127.0.0.1',
	      'server.socket_port': 8000,
	    },

	    '/': {
	      'request.dispatch': dispatcher,
        'tools.CORS.on':True,
	    }
    }

    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS) # CORS
    start_service()