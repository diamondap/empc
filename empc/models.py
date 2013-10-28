import json

# Everything in here is tested in em/tests/unit/libs/http_test.py
# since those classes actually implement these methods.
class JsonSerializable:
    """
    This base class provides methods to serialize relatively
    simple objects to and from JSON. Note that it does not
    handle nested objects, datetimes, or other complex objects.
    It's only for really simple cases!
    """

    @classmethod
    def from_json(self, json_string):
        data = json.loads(json_string)
        return self(**data)

    def to_json(self):
        return json.dumps(self.__dict__)

def list_to_json(items):
    """
    Converts a list of JsonSerializable objects to JSON.
    """
    return json.dumps(to_dict_list(items))

def list_from_json(json_string, klass):
    """
    Converts a JSON string to a list of items of class klass.
    This assumes you're working with very simple objects of
    type JsonSerializable.
    """
    object_list = []
    dictionaries = json.loads(json_string)
    for dictionary in dictionaries:
        object_list.append(klass(**dictionary))
    return object_list

def to_dict_list(items):
    """
    Converts a list of JsonSerializable objects to a list of dictionaries.
    """
    dictionaries = []
    for item in items:
        if not isinstance(item, JsonSerializable):
            raise ValueError('Items must of type JsonSerializable')
        dictionaries.append(item.__dict__)
    return dictionaries


class RouterRequest(JsonSerializable):
    """
    This class contains information about HTTP requests that the client will
    have to send to the router.
    """
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.method = kwargs.get('method')
        self.headers = kwargs.get('headers')
        self.data = kwargs.get('data')

    def __str__(self):
        return "RouterRequest {0} {1}".format(self.method, self.url)


class RouterResponse(JsonSerializable):
    """
    This class contains information about an HTTP response that our remote
    client received and then passed back to the server.
    """

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.method = kwargs.get('method')
        self.status_code = kwargs.get('status_code')
        self.port = kwargs.get('port')
        self.headers = kwargs.get('headers')
        self.body = kwargs.get('body')

    @classmethod
    def from_http_response(self, response, method, url, port):
        # Convert special headers class to a regular dictionary.
        # Note that all header names will be lower-case.
        headers = {}
        for header in response.headers:
            headers[header] = response.headers[header]
        return RouterResponse(url=url,
                              method=method,
                              status_code=response.status_code,
                              port=port,
                              headers=headers,
                              body=response.text)

    def __str__(self):
        return "RouterResponse {0} {1}".format(self.method, self.url)


class Router(JsonSerializable):

    def __init__(self, *args, **kwargs):
        self.manufacturer = kwargs.get('manufacturer')
        self.model = kwargs.get('model')
        self.auth_protocol = kwargs.get('auth_protocol')
        self.protocol = kwargs.get('protocol')
        self.port = kwargs.get('port')
        self.firmware_version = kwargs.get('firmware_version')
        self.firmware_major = kwargs.get('firmware_major')
        self.firmware_minor = kwargs.get('firmware_minor')
        self.firmware_point = kwargs.get('firmware_point')
        self.firmware_date = kwargs.get('firmware_date')
        self.ip_address = None
        self.mac_address = None
        self.base_url = None
