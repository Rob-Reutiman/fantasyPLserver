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


    conf = {

      'global': {
        'server.thread_pool': 5,
        'server.socket_host': '127.0.0.1',
	      'server.socket_port': 53075,
	    },

	    '/': {
	      'request.dispatch': dispatcher,
	    }
    }

    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)


if __name__ == '__main__':
    start_service()