import requests
import json

router_client = requests.Session()
em_client = requests.Session()

def find_http_service(host_name_or_ip, timeout=1.0):
    """
    This function tries to locate an HTTP interface at the given host name
    or IP address. It returns a list of dictionaries containing information
    about successful responses. Each dictionary has the following keys:

    * port     - The port number of the HTTP service on the remote host.
    * url      - The URL that generated the response.
    * headers  - The HTTP response headers.
    * body     - The HTTP response body.
    """
    responses = []
    ports = [80, 443, 8000, 8080, 8888]
    for port in ports:
        if port == 443:
            url = "https://{0}".format(host_name_or_ip)
        elif port == 80:
            url = "http://{0}".format(host_name_or_ip)
        else:
            url = "http://{0}:{1}".format(host_name_or_ip, port)
        try:
            r = router_client.get(url, verify=False, timeout=timeout)
            if r.status_code == 200:
                responses.append(response_to_dict(r, url, port))
        except (ConnectionError, requests.exceptions.ConnectionError) as ex:
            # This is typically connection refused, because there
            # is no HTTP service running on the port we queried.
            pass
    return responses

def response_to_dict(response, url, port):
    """
    Convert an HttpResponse object to a simple dictionary that can be
    easily converted to and from JSON.
    """
    return {'port': port,
            'url': url,
            'headers': headers_to_dict(response.headers),
            'body': response.text}

def headers_to_dict(headers):
    """
    Converts response headers collection, which is a special
    case-insensitive dict, to a normal dict.
    """
    hdict = {}
    for header in headers.keys():
        hdict[header] = headers[header]
    return hdict

def find_potential_routers(interfaces):
    """
    Returns a list of dictionaries with information about potential routers.
    Each dict includes keys 'port', 'url', 'body' and 'headers'. The values
    are all strings, except for headers, which is a dict.
    """
    default_interfaces = [i for i in interfaces if i.is_default == True]
    responses = []
    for i in default_interfaces:
        responses = responses + find_http_service(i.gateway)
    return responses

def identify_page(page):
    """
    Sends a page to EM server so EM can identify the type of router.
    """
    url = "http://localhost:8080/api/v1/identify_router"
    r = em_client.post(url, page)
    response_data = {}
    try:
        response_data = json.loads(r.text)
    except BaseException as ex:
        response_data['error'] = ex.message
    return response_data

def auto_login(router_id):
    """
    Try to automatically log in to the router. This works only on routers
    that have bad security, such as MediaLink routers that send the password
    in the login page HTML.
    """
    url = "http://localhost:8080/api/v1/creds_request/{0}/".format(router_id)
    r = em_client.get(url)
    creds_response = {}
    try:
        creds_response = json.loads(r.text)
    except BaseException as ex:
        return {'error': ex.message}

    if creds_response and creds_response[0]:
        creds = creds_response[0]
        r = router_client.get('http://192.168.1.1' + creds['url'])
        data = response_to_dict(r, creds['url'], 80)
        url = "http://localhost:8080/api/v1/login_request/{0}/".format(router_id)
        r = em_client.post(url, data)
        print(r.text)
        login_request = json.loads(r.text)
        r = router_client.post('http://192.168.1.1' + login_request.url,
                               login_request.data)
        return {'html': r.text}
    else:
        return {'error': 'This router does not support auto-login.'}
