import unittest
import platform
from tests import load_fixture
from empc.netconfig import NetConfig, NetworkInterface


class NetConfigTest(unittest.TestCase):

    def test_get_instance(self):
        self.assertEqual(platform.system(), NetConfig.get_instance().os_type)

    def test_sys_command(self):
        pass


class NetConfigMacTest(unittest.TestCase):

    def setUp(self):
        self.net_config = NetConfig.get_instance()

    def test_get_config(self):
        interfaces = self.net_config.get_config()
        self.assertTrue(len(interfaces) > 0)
        self.assertIsInstance(interfaces[0], NetworkInterface)
        found_default = False
        for i in interfaces:
            if i.is_default:
                found_default = True
                self.assertIsNotNone(i.gateway)
        self.assertTrue(found_default)

    def test_get_raw_interfaces(self):
        output = self.net_config.get_raw_interfaces()
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) > 0)

    def test_get_raw_gateway(self):
        output = self.net_config.get_raw_gateway()
        self.assertIsInstance(output, list)
        self.assertTrue(len(output) > 0)

    def test_parse_default_gateway(self):
        config = load_fixture('route_n_get_default_mac.txt').split("\n")
        name, gateway = self.net_config.parse_default_gateway(config)
        self.assertEqual('en0', name)
        self.assertEqual('216.30.180.1', gateway)

    def test_flag_default_interface(self):
        config = load_fixture('ifconfig_mac.txt').split("\n")
        interfaces = self.net_config.parse_interfaces(config)
        default_interface = self.net_config.flag_default_interface(
            "en0", "216.30.180.1", interfaces)
        self.assertEqual("en0", default_interface.name)
        self.assertEqual("216.30.180.1", default_interface.gateway)

    def test_parse_interfaces(self):
        config = load_fixture('ifconfig_mac.txt').split("\n")
        interfaces = self.net_config.parse_interfaces(config)
        self.assertIsInstance(interfaces, list)
        self.assertEqual(6, len(interfaces))
        self.assertEqual('lo0', interfaces[0].name)
        self.assertEqual('127.0.0.1', interfaces[0].ip4_address)
        self.assertEqual('::1', interfaces[0].ip6_address)

        self.assertEqual('en0', interfaces[3].name)
        self.assertEqual('16:22:a3:c9:e2:1c', interfaces[3].mac_address)
        self.assertEqual('216.29.144.16', interfaces[3].ip4_address)
        self.assertEqual('2144:f9c0:10:1001:124a:f3f1:fe90:e5e8',
                         interfaces[3].ip6_address)
