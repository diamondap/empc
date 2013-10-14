import json
from datetime import tzinfo, timedelta, datetime
from bottle import get, post, route, run, static_file, response
import requests
from empc.netconfig import NetConfig, NetworkInterface
from os.path import realpath, abspath, join, normpath, dirname

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
    found_gateway = False
    for i in interfaces:
        if i.is_default:
            found_gateway = True
            r = requests.get("http://{0}".format(i.gateway))
            return r.text
    if found_gateway:
        return "Can't get response from router"
    else:
        return "Can't find gateway"

def start(host, port):
    run(host=host, port=port, debug=True, reloader=True)
