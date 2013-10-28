import json
from datetime import tzinfo, timedelta, datetime
from bottle import get, post, route, run, static_file, response
from os.path import realpath, abspath, join, normpath, dirname
from empc.netconfig import NetConfig, NetworkInterface
import empc.client as client
import empc.models as models
from empc.log import logger

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

    # responses is a list of RouterResponse objects
    responses = client.find_potential_routers(interfaces)
    routers = []
    for router_response in responses:
        id_response = client.identify_page(router_response)
        print(id_response['router'])
        routers.append(id_response['router'])
        #logger.info("Looks like a {0} {1}".format(
        #    router.manufacturer, router.model))
    #data = {'routers': models.to_dict_list(routers) }
    response.set_header('Content-Type', 'application/json')
    return json.dumps({'routers': routers})

@get('/auto_login')
def auto_login():
    return client.auto_login(1)

def start(host, port):
    run(host=host, port=port, debug=True, reloader=True)
