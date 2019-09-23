import logging
import time
import ipaddress

from novaclient.exceptions import NotFound

from tungsten_tests.clients.os_clients import OpenStackClientManager
from tungsten_tests.config import MCPConfig
from tungsten_tests.helpers import exceptions
from tungsten_tests.settings import TFT_CLOUD_INIT

logger = logging.getLogger()


class OpenStackActions(object):
    def __init__(self, os_clients, config, cleanup):
        isinstance(os_clients, OpenStackClientManager)
        self.os_clients = os_clients
        isinstance(config, MCPConfig)
        self.config = config
        self.cleanup = cleanup

    def _allocate_fip(self, ext_net_id):
        # TO DO: apply filter with tenant_id in request
        fips = self.os_clients.neutron.list_floatingips(filter)
        # Filter unused fips
        for fip in fips['floatingips']:
            if fip['status'] == 'DOWN' and \
                    fip['tenant_id'] == self.config.os_project_id:
                return self.os_clients.neutron.show_floatingip(
                    fip['id'])
        body = {
            'floating_network_id': ext_net_id
        }
        fip = self.os_clients.neutron.create_floatingip(
            {'floatingip': body}
        )
        return fip

    def associate_fip(self, instance_id, net_id=None):
        fip = self._allocate_fip(self.config.os_ext_net_id)
        interfaces = self.os_clients.nova.servers.interface_list(instance_id)
        if not net_id:
            net_id = self.config.os_net_id
        for i in interfaces:
            if i.net_id == net_id:
                body = {
                    "port_id": i.port_id
                }
                return self.os_clients.neutron.update_floatingip(
                    fip['floatingip']['id'], {'floatingip': body})
        raise exceptions.InterfaceNotFoundException(
            instance_id=instance_id, net_id=self.config.os_net_id)

    def return_floating_ip(self, instance_id, net_name=None):
        if not net_name:
            net_name = self.config.os_net_name
        vm = self.os_clients.nova.servers.get(instance_id)
        ips = vm.addresses[net_name]
        for ip in ips:
            if ip['OS-EXT-IPS:type'] == 'floating':
                return ip['addr']

    def return_az_hosts(self):
        availability_zones = self.os_clients.nova.availability_zones.list()
        for az in availability_zones:
            if az.zoneName == self.config.os_az:
                return az.hosts

    def create_instance(self, name, security_groups=None, key_name=None,
                        nics=None, **kwargs):
        if not security_groups:
            security_groups = [self.config.os_sg_name]
        if not key_name:
            key_name = self.config.os_keypair_id
        if not nics:
            nics = [{'net-id': self.config.os_net_id}]
        if 'userdata' not in kwargs:
            with open(TFT_CLOUD_INIT) as f:
                userdata = f.read()

        vm = self.os_clients.nova.servers.create(
            name, self.config.os_ubuntu_img_id,
            self.config.os_ubuntu_flavor_id,
            security_groups=security_groups, userdata=userdata,
            key_name=key_name, nics=nics, **kwargs
        )
        logger.info("VM '{}' is created. VM ID: {}".format(name,
                                                           vm.id))
        # Cleanup
        self.cleanup(self.wait_for_instance_termination, vm.id)
        self.cleanup(self.os_clients.nova.servers.delete, vm.id)
        return vm

    def create_network(self, name):
        network = {
            'name': name,
            'admin_state_up': True
        }
        net = self.os_clients.neutron.create_network({'network': network})
        net_id = net['network']['id']
        logger.info("Network '{}' is created. Network ID: {}".format(name,
                                                                     net_id))
        # Cleanup
        self.cleanup(
            self.os_clients.neutron.delete_network, net_id
        )
        return net

    def create_subnet(self, net_id, name, cidr):
        ipv4_net = ipaddress.IPv4Network(unicode(cidr))
        ip_range = list(ipv4_net.hosts())
        subnet = {
            'name': name,
            'network_id': net_id,
            'ip_version': 4,
            'cidr': cidr,
            'allocation_pools': [{'start': str(ip_range[10]),
                                  'end': str(ip_range[-1])}]
        }
        subnet = self.os_clients.neutron.create_subnet({'subnet': subnet})
        subnet_id = subnet['subnet']['id']
        logger.info("Subnet '{}' is created. Subnet ID: {}".format(name,
                                                                   subnet_id))
        # Cleanup
        self.cleanup(
            self.os_clients.neutron.delete_subnet, subnet['subnet']['id']
        )
        return subnet

    def router_attach_subnet(self, router_id, subnet_id):
        interface = {
            "subnet_id": subnet_id
        }
        resp = self.os_clients.neutron.add_interface_router(router_id,
                                                            interface)
        port_id = resp['port_id']
        logger.info("Port '{}' was attached to router '{}'"
                    "".format(port_id, router_id))
        # Cleanup
        self.cleanup(
            self.os_clients.neutron.remove_interface_router,
            router_id, interface
        )

    def wait_instance_status(self, instance_id, status='ACTIVE',
                             timeout=60, interval=1, raise_on_error=True):
        vm = self.os_clients.nova.servers.get(instance_id)
        vm_status = old_status = vm.status
        start_time = int(time.time())
        while True:
            t = time.time() - start_time
            if vm_status != old_status:
                logger.info(
                    'State transition "{}" ==> "{}" after {} second wait'
                    ''.format(old_status, vm_status, t))
                old_status = vm_status

            if vm_status == 'ERROR' and raise_on_error:
                logger.error(
                    "Instance {} status is {}".format(vm.id, vm_status))
                raise exceptions.BuildErrorException(server_id=vm.id)
            if status == 'BUILD' and vm_status != 'UNKNOWN':
                return True
            if vm_status == status:
                logger.info('Achived "{}" state after {} second wait'
                            ''.format(vm_status, t))
                return True

            timed_out = int(time.time()) - start_time >= timeout
            if timed_out:
                logger.error("Server {server_id} failed to reach {status} "
                             "status within the required time ({timeout} s)."
                             "".format(server_id=vm.id, status=status,
                                       timeout=timeout))
                logger.error("Current status: {}.".format(vm.status))
                raise exceptions.TimeoutException
            time.sleep(interval)
            vm = self.os_clients.nova.servers.get(instance_id)
            vm_status = vm.status

    def wait_for_instance_termination(self, instance_id, timeout=60,
                                      interval=1):
        start_time = int(time.time())
        try:
            vm = self.os_clients.nova.servers.get(instance_id)
        except NotFound:
            return True
        vm_status = old_status = vm.status
        while True:
            t = time.time() - start_time
            if vm_status != old_status:
                logger.info(
                    'State transition "{}" ==> "{}" after {} second wait'
                    ''.format(old_status, vm_status, t))
                old_status = vm_status

            if vm_status == 'ERROR':
                logger.error("Instance {} failed to delete and is in {} status"
                             "".format(vm.id, vm_status))
                raise exceptions.BuildErrorException(instance_id=vm.id)

            timed_out = int(time.time()) - start_time >= timeout
            if timed_out:
                logger.error("Server {server_id} failed to delete within the "
                             "required time ({timeout} s)."
                             "".format(server_id=vm.id, timeout=timeout))
                logger.error("Current status: {}.".format(vm.status))
                raise exceptions.TimeoutException
            time.sleep(interval)
            try:
                vm = self.os_clients.nova.servers.get(instance_id)
            except NotFound:
                return True
            vm_status = vm.status
