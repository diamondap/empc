import subprocess
import platform
import re


class NetworkInterface:
    "Contains information about one of the system's network interfaces."
    def __init__(self):
        self.mac_address = None
        self.ip4_address = None
        self.ip6_address = None
        self.name = None
        self.gateway = None
        self.is_default = False


class NetConfig:
    """
    Returns information about the sytem's network interfaces.
    """

    def __init__(self):
        self.os_type = None

    @classmethod
    def get_instance(self):
        """
        Returns an instance of a NetConfig class suitable for the current
        operating system.
        """
        os_type = platform.system()
        if os_type == 'Darwin':
            return NetConfigMac()
        elif os_type == 'Linux':
            return NetConfigLinux()
        elif os_type == 'Windows':
            return NetConfigWindows()
        else:
            raise NotImplementedError("No support for OS %s".format(os_type))

    def sys_command(self, command):
        """
        Executes a system command and returns two values. The first is the
        return value of the command (an integer). The second is the output
        of the command as a list of strings.
        """
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        output = []
        for line in p.stdout.readlines():
            output.append(str(line, 'utf-8'))
        retval = p.wait()
        return retval, output



class NetConfigMac(NetConfig):

    """
    Collects network configuration info on Mac OSX
    """

    def __init__(self):
        self.os_type = platform.system()

    def get_config(self):
        """
        Returns all the network configuration information we need. This is
        the only method you need to call.
        """
        network_interfaces = self.parse_interfaces(self.get_raw_interfaces())
        name, gateway = self.parse_default_gateway(self.get_raw_gateway())
        self.flag_default_interface(name, gateway, network_interfaces)
        return network_interfaces

    def get_raw_interfaces(self):
        """
        Returns the output of the shell command 'ifconfig' as a list of
        lines.
        """
        retval, output = self.sys_command('ifconfig')
        if retval != 0:
            raise ChildProcessError("get_raw_interfaces had unexpected "
                                    "exit value of %d".format(retval))
        return output

    def get_raw_gateway(self):
        """
        Returns the output of the shell command 'route -n get default'
        as a list of lines.
        """
        retval, output = self.sys_command('route -n get default')
        if retval != 0:
            raise ChildProcessError("get_raw_gateway had unexpected "
                                    "exit value of %d".format(retval))
        return output

    def parse_default_gateway(self, config):
        """
        Extracts the default gateway IP address and interface name from
        the output of 'route -n get default'. Returns two strings: the
        interface name and the IP4 address of the gateway.
        """
        gateway = None
        name = None
        for line in config:
            line = line.strip()
            if line.startswith('gateway:'):
                gateway = line.split(' ')[1].strip()
            elif line.startswith('interface:'):
                name = line.split(' ')[1].strip()
        return name, gateway

    def flag_default_interface(self, name, gateway, network_interfaces):
        """
        Given the interface name and gateway IP4 address of the default
        gateway, this sets the is_default flag and the ip4_address of the
        interface that provides access to the default gateway.
        """
        for interface in network_interfaces:
            if interface.name == name:
                interface.gateway = gateway
                interface.is_default = True
                return interface

    def parse_interfaces(self, config):
        """
        Parses the output of ifconfig and returns a list of NetworkInterface
        objects.
        """
        network_interfaces = []
        current_interface = None
        for line in config:
            match = re.match('(\w+): flags', line)
            if match:
                current_interface = NetworkInterface()
                current_interface.name = match.group(1)
                network_interfaces.append(current_interface)
                continue
            try:
                first, last = line.strip().split(' ', 1)
                if first == 'ether':
                    current_interface.mac_address = last.strip()
                elif (first == 'inet6' and 'scopeid' not in last
                      and 'temporary' not in last):
                    current_interface.ip6_address = last.split(' ')[0].strip()
                elif first == 'inet':
                    current_interface.ip4_address = last.split(' ')[0].strip()
            except Exception as ex:
                #print(line)
                pass
        return network_interfaces
