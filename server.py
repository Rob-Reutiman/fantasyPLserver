import cherrypy
from library import _fpl_database
from controller import Controller

def start_service():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    fplDB = _fpl_database()

    fplController = Controller(fplDB=fplDB) 

    dispatcher.connect('get data', '/', controller=fplController, action = 'GET_ALL', conditions=dict(method=['GET']))

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