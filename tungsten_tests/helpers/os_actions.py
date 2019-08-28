import logging
import time

import novaclient.exceptions

from tungsten_tests.config import MCPConfig
from tungsten_tests.helpers import exceptions
from tungsten_tests.clients.os_clients import OpenStackClientManager

logger = logging.getLogger()


class OpenStackActions(object):
    def __init__(self, os_clients, config, cleanup):
        isinstance(os_clients, OpenStackClientManager)
        self.os_clients = os_clients
        isinstance(config, MCPConfig)
        self.config = config
        self.cleanup = cleanup

    def _allocate_fip(self, ext_net_id):
        fips = self.os_clients.neutron.list_floatingips()
        # Filter unused fips
        for fip in fips['floatingips']:
            if fip['status'] != 'DOWN':
                fips['floatingips'].remove(fip)
        if len(fips['floatingips']) == 0:
            body = {
                'floating_network_id': ext_net_id
            }
            fip = self.os_clients.neutron.create_floatingip(
                {'floatingip': body}
            )
        else:
            fip = self.os_clients.neutron.show_floatingip(
                fips['floatingips'][0]['id']
            )
        return fip

    def associate_fip(self, instance_id):
        fip = self._allocate_fip(self.config.os_ext_net_id)
        interfaces = self.os_clients.nova.servers.interface_list(instance_id)
        for i in interfaces:
            if i.net_id == self.config.os_net_id:
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

    def create_instance(self, name, *args, **kwargs):
        nics = [{'net-id': self.config.os_net_id}]
        vm = self.os_clients.nova.servers.create(
            name, self.config.os_ubuntu_img_id,
            self.config.os_ubuntu_flavor_id,
            security_groups=[self.config.os_sg_name],
            key_name=self.config.os_keypair_id, nics=nics
        )
        # Cleanup
        self.cleanup(self.wait_for_instance_termination, vm.id)
        self.cleanup(self.os_clients.nova.servers.delete, vm.id)
        return vm

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
        except novaclient.exceptions.NotFound:
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
            except novaclient.exceptions.NotFound:
                return True
            vm_status = vm.status
