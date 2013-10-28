import unittest
import empc.client as client
from empc.netconfig import NetworkInterface

class ClientTest(unittest.TestCase):

    def setUp(self):
        self.test_host = 'httpbin.org'
        self.mock_interfaces = [
            NetworkInterface(is_default=False, gateway='192.168.99.1'),
            NetworkInterface(is_default=True, gateway='httpbin.org'),
            NetworkInterface(is_default=False, gateway='10.11.12.24')]

    # Several tests run against httpbin.org. This function tests
    # common response data from that server.
    def assert_responses(self, responses):
        self.assertEqual(2, len(responses))
        # Response from port 80
        response = responses[0]
        self.assertEqual('http://httpbin.org', response.url)
        self.assertEqual(80, response.port)
        self.assertTrue(len(response.headers) > 3)
        self.assertTrue(len(response.body) > 1000)
        # Response from port 443
        response = responses[1]
        self.assertEqual('https://httpbin.org', response.url)
        self.assertEqual(443, response.port)
        self.assertTrue(len(response.headers) > 3)
        self.assertTrue(len(response.body) > 1000)


    def test_find_http_service(self):
        responses = client.find_http_service(self.test_host)
        self.assert_responses(responses)

    def test_find_potential_routers(self):
        responses = client.find_potential_routers(self.mock_interfaces)
        self.assert_responses(responses)


    #TODO: test_identify_page
