import json
from datetime import tzinfo, timedelta, datetime
from bottle import get, post, route, run, static_file, response
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

    # html = "<p>Found {0} interfaces</p>".format(len(interfaces))
    # for i in interfaces:
    #     html += "<p>Interface {0}</p>".format(i.name)
    #     html += "<ul>"
    #     for prop, value in vars(i).items():
    #         html += "<li>{0} = {1}</li>".format(prop, value)
    #     html += "</ul>"
    # return html

def start(host, port):
    run(host=host, port=port, debug=True, reloader=True)
