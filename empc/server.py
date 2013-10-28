import json
from datetime import tzinfo, timedelta, datetime
from bottle import get, post, route, run, static_file, response
from os.path import realpath, abspath, join, normpath, dirname
from empc.netconfig import NetConfig
import empc.client as client
from empc import models
from empc.log import logger

this_dir = dirname(realpath(__file__))
resource_dir = abspath(normpath(join(this_dir, '..', 'resources')))
last_ping = None
net_state = None

@route('/static/<filename>')
def static(filename):
    return static_file(filename, root=resource_dir)

@get('/ping')
def ping():
    last_ping = datetime.utcnow()
    data = {'last_ping': last_ping.isoformat() }
    return data

@get('/')
def index():
    return static_file('index.html', root=resource_dir)

@get('/netinfo')
def netinfo():
    interfaces = NetConfig.get_instance().get_config()
    router = find_router(interfaces)
    global net_state
    net_state = models.NetState(interfaces=interfaces,
                                router=router)
    response.set_header('Content-Type', 'application/json')
    print(net_state.to_json())
    return net_state.to_json()

def find_router(interfaces):
    """
    Note that this returns only the first router. We're checking only
    for the default gateway on the default interface, so there should
    be only one.
    """
    responses = client.find_potential_routers(interfaces)
    for router_response in responses:
        id_response = client.identify_page(router_response)
        router_dict = id_response['router']
        return models.Router(**router_dict)

@get('/auto_login')
def auto_login():
    return client.auto_login(1)

def start(host, port):
    run(host=host, port=port, debug=True, reloader=True)
