from bottle import get, post, route, run
from empc.netconfig import NetConfig, NetworkInterface

@get('/')
def index():
    return "This is the index page."

@get('/netinfo')
def netinfo():
    interfaces = NetConfig.get_instance().get_config()
    html = "<p>Found {0} interfaces</p>".format(len(interfaces))
    for i in interfaces:
        html += "<p>Interface</p>"
        html += "<ul>"
        for prop, value in vars(i).items():
            html += "<li>{0} = {1}</li>".format(prop, value)
        html += "</ul>"
    return html

def start():
    run(host='localhost', port=9932, debug=True, reloader=True)
