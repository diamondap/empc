import requests

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
                            'headers': vars(r.headers),
                            'body': r.text}
                responses.append(response)
        except (ConnectionError, requests.exceptions.ConnectionError) as ex:
            # This is typically connection refused, because there
            # is no HTTP service running on the port we queried.
            pass
    return responses


def find_potential_routers(interfaces):
    default_interfaces = [i for i in interfaces if i.is_default == True]
    responses = []
    for i in default_interfaces:
        responses = responses + find_http_service(i.gateway)
    return responses
