import cherrypy
from library import _fpl_database
from controller import Controller

def start_service():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    fplDB = _fpl_database()

    fplController = Controller(fplDB=fplDB) 

    dispatcher.connect('get all data', '/', controller=fplController, action = 'GET_ALL', conditions=dict(method=['POST']))
    dispatcher.connect('get player data', '/players/', controller=fplController, action = 'GET_PLAYERS', conditions=dict(method=['POST']))
    dispatcher.connect('get team data', '/teams/', controller=fplController, action = 'GET_TEAMS', conditions=dict(method=['POST']))
    dispatcher.connect('get fixture data', '/fixtures/', controller=fplController, action = 'GET_FIXTURES', conditions=dict(method=['POST']))
    dispatcher.connect('create account', '/create/', controller=fplController, action = 'CREATE_ACCOUNT', conditions=dict(method=['POST']))
    dispatcher.connect('login', '/auth/', controller=fplController, action = 'AUTHENTICATE', conditions=dict(method=['POST']))
    dispatcher.connect('featured players', '/featured/', controller=fplController, action='GET_FEATURED', conditions=dict(method=['POST']))

    # CORS related options connections
    dispatcher.connect('movie_key_options', '/movies/:movie_id', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('movie_options', '/movies/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('reset_key_options', '/reset/:movie_id', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('reset_options', '/reset/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('rating_options', '/ratings/:movie_id', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))

    conf = {

      'global': {
        'server.thread_pool': 5,
        'server.socket_host': '127.0.0.1',
	      'server.socket_port': 3000,
	    },

	    '/': {
	      'request.dispatch': dispatcher,
	    }
    }

    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

# class for CORS
class optionsController:
    def OPTIONS(self, *args, **kwargs):
        return ""

# function for CORS
def CORS(self):
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"



if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS) # CORS
    start_service()