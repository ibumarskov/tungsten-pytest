import logging
import time

import novaclient.exceptions

from tungsten_tests.helpers import exceptions

logger = logging.getLogger()


def wait_instance_status(nova_client, instance_id, status='ACTIVE', timeout=60,
                         interval=1, raise_on_error=True):
    vm = nova_client.servers.get(instance_id)
    vm_status = old_status = vm.status
    start_time = int(time.time())
    while True:
        t = time.time() - start_time
        if vm_status != old_status:
            logger.info('State transition "{}" ==> "{}" after {} second wait'
                        ''.format(old_status, vm_status, t))
            old_status = vm_status

        if vm_status == 'ERROR' and raise_on_error:
            logger.error("Instance {} status is {}".format(vm.id, vm_status))
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
        vm = nova_client.servers.get(instance_id)
        vm_status = vm.status


def wait_for_instance_termination(nova_client, instance_id, timeout=60,
                                  interval=1):
    start_time = int(time.time())
    try:
        vm = nova_client.servers.get(instance_id)
    except novaclient.exceptions.NotFound:
        return True
    vm_status = old_status = vm.status
    while True:
        t = time.time() - start_time
        if vm_status != old_status:
            logger.info('State transition "{}" ==> "{}" after {} second wait'
                        ''.format(old_status, vm_status, t))
            old_status = vm_status

        if vm_status == 'ERROR':
            logger.error("Instance {} failed to delete and is in {} status"
                         "".format(vm.id, vm_status))
            raise exceptions.BuildErrorException(server_id=vm.id)

        timed_out = int(time.time()) - start_time >= timeout
        if timed_out:
            logger.error("Server {server_id} failed to delete within the "
                         "required time ({timeout} s)."
                         "".format(server_id=vm.id, timeout=timeout))
            logger.error("Current status: {}.".format(vm.status))
            raise exceptions.TimeoutException
        time.sleep(interval)
        try:
            vm = nova_client.servers.get(instance_id)
        except novaclient.exceptions.NotFound:
            return True
        vm_status = vm.status
