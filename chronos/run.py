import os
import logging

from paste.httpserver import serve
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
import pyramid.events
from pyramid.exceptions import NotFound
from pyramid.httpexceptions import HTTPFound
import sqlite3


from chronos import controllers
from chronos import db


logging.basicConfig()
log = logging.getLogger(__file__)

here = os.path.dirname(os.path.abspath(__file__))



@pyramid.events.subscriber(pyramid.events.ApplicationCreated)
def application_created_subscriber(event):
    log.warn('Initializing database...')
    f = open(os.path.join(here, 'schema.sql'), 'r')
    stmt = f.read()
    settings = event.app.registry.settings
    db = sqlite3.connect(settings['sqlite_path'])
    db.executescript(stmt)
    db.commit()
    f.close()


@pyramid.events.subscriber(pyramid.events.NewRequest)
def new_request_subscriber(event):
    request = event.request
    settings = request.registry.settings
    db_factory = db.Factory(settings['sqlite_path'])
    request.db = db_factory.create()
    request.add_finished_callback(close_db_connection)


def close_db_connection(request):
    request.db.close()


if __name__ == '__main__':
    # configuration settings
    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['sqlite_path'] = os.path.join(here, 'chronos.db')
    settings['mako.directories'] = os.path.join(here, 'templates')

    controller = controllers.Controller()

    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_route('index', '/')
    config.add_route('graph', '/graph')
    config.add_static_view('static', os.path.join(here, 'static'))
    config.scan()
    # serve app
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0')
