import json
from datetime import tzinfo, timedelta, datetime
from bottle import get, post, route, run, static_file, response
from os.path import realpath, abspath, join, normpath, dirname
from empc.netconfig import NetConfig, NetworkInterface
import empc.client as client

this_dir = dirname(realpath(__file__))
resource_dir = abspath(normpath(join(this_dir, '..', 'resources')))
last_ping = None

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
    data = []
    for i in interfaces:
        data.append(vars(i))
    response.set_header('Content-Type', 'application/json')
    return json.dumps(data)

@get('/find_router')
def find_router():
    interfaces = NetConfig.get_instance().get_config()
    #interfaces = [NetworkInterface(is_default=True, gateway='httpbin.org')]
    responses = client.find_potential_routers(interfaces)
    data = {'found_router': False, 'routers': []}
    for r in responses:
        data['found_router'] = True
        router = {'url': r['url'], 'port': r['port']}
        data['routers'].append(router)
    return data

def start(host, port):
    run(host=host, port=port, debug=True, reloader=True)
