import logging
import pytest

from tungsten_tests.helpers import common
from tungsten_tests.helpers import utils

logger = logging.getLogger()


@pytest.mark.functional
class TestMcast(object):
    """Simple check of multicast traffic"""

    name_prefix = 'TestMcast'
    vm_list = []
    vm1 = {
        'name': utils.rand_name(name_prefix + "-vm1cmp1"),
        'id': None,
        'ip': None,
        'floating_ip': None
    }
    vm_list.append(vm1)
    vm2 = {
        'name': utils.rand_name(name_prefix + "-vm2cmp1"),
        'id': None,
        'ip': None,
        'floating_ip': None
    }
    vm_list.append(vm2)
    vm3 = {
        'name': utils.rand_name(name_prefix + "-vm1cmp2"),
        'id': None,
        'ip': None,
        'floating_ip': None
    }
    vm_list.append(vm3)
    loss_rate = 1

    @pytest.fixture(scope='class')
    def setup(self, os_init_setup, config, os_clients, os_actions_class):
        hosts = os_actions_class.return_az_hosts()
        if len(hosts) < 2:
            pytest.skip("Not enough hosts")
        host_list = []
        for host in hosts:
            host_list.append(host)
        az_host1 = config.os_az + ":" + host_list[0]
        az_host2 = config.os_az + ":" + host_list[1]

        # Create VMs
        vm1 = os_actions_class.create_instance(
            TestMcast.vm1['name'], availability_zone=az_host1)
        TestMcast.vm1['id'] = vm1.id

        vm2 = os_actions_class.create_instance(
            TestMcast.vm2['name'], availability_zone=az_host1)
        TestMcast.vm2['id'] = vm2.id

        vm3 = os_actions_class.create_instance(
            TestMcast.vm3['name'], availability_zone=az_host2)
        TestMcast.vm3['id'] = vm3.id

        # Wait while instances are being deployed
        for vm in TestMcast.vm_list:
            os_actions_class.wait_instance_status(vm['id'])

        # Assign floating ip
        for vm in TestMcast.vm_list:
            fip = os_actions_class.associate_fip(vm['id'])
            vm['ip'] = fip['floatingip']['fixed_ip_address']
            vm['floating_ip'] = fip['floatingip']['floating_ip_address']

        # Wait for cloud init
        for vm in TestMcast.vm_list:
            with common.ssh_connect(vm['floating_ip'],
                                    pkey=config.os_private_key) as ssh_client:
                common.wait_for_cloud_init(ssh_client)

    def test_mcast_same_vn_same_node(self, setup, ssh_connect):
        """
        Check multicast traffic when source and receiver are located in
        same network (subnet) and same compute.
        """
        mcast = '224.1.1.1'
        cmd_srv = 'iperf -s -u -B '+mcast+' -t 5'
        cmd_clt = 'iperf -c '+mcast+' -u -t 3'
        vm1_c = ssh_connect(TestMcast.vm1['floating_ip'])
        vm2_c = ssh_connect(TestMcast.vm2['floating_ip'])
        stdin1, stdout1, stderr1 = vm1_c.exec_command(cmd_srv)
        stdin2, stdout2, stderr2 = vm2_c.exec_command(cmd_clt)
        out1 = stdout1.read()
        out2 = stdout2.read()
        logger.info("VM1 output:\n{}".format(out1))
        logger.info("VM2 output:\n{}".format(out2))
        res = utils.parser_iperf_output(out1, udp=True)
        utils.check_iperf_res(res)

    def test_mcast_same_vn_diff_nodes(self, setup, ssh_connect):
        """
        Check multicast traffic when source and receiver are located in
        same network (subnet) but on different computes.
        """
        mcast = '224.1.1.2'
        cmd_srv = 'iperf -s -u -B ' + mcast + ' -t 5'
        cmd_clt = 'iperf -c ' + mcast + ' -u -t 3'
        vm1_c = ssh_connect(TestMcast.vm1['floating_ip'])
        vm3_c = ssh_connect(TestMcast.vm3['floating_ip'])
        stdin1, stdout1, stderr1 = vm1_c.exec_command(cmd_srv)
        stdin2, stdout2, stderr2 = vm3_c.exec_command(cmd_clt)
        out1 = stdout1.read()
        out2 = stdout2.read()
        logger.info("VM1 output:\n{}".format(out1))
        logger.info("VM3 output:\n{}".format(out2))
        res = utils.parser_iperf_output(out1, udp=True)
        utils.check_iperf_res(res)
