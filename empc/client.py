import requests
import json

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
            r = requests.get(url, verify=False, timeout=timeout)
            if r.status_code == 200:
                # Must use vars to convert case-insensitive dict to dict
                response = {'port': port,
                            'url': url,
                            'headers': headers_to_dict(r.headers),
                            'body': r.text}
                responses.append(response)
        except (ConnectionError, requests.exceptions.ConnectionError) as ex:
            # This is typically connection refused, because there
            # is no HTTP service running on the port we queried.
            pass
    return responses

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
    r = requests.post(url, page)
    data = {}
    try:
        data = json.loads(r.text)
    except BaseException as ex:
        data['error'] = ex.message
    return data
