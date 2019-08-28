import logging
import pytest

from tungsten_tests.helpers import utils

logger = logging.getLogger()


@pytest.mark.functional
class TestMVPN(object):

    vm1 = {
        'name': utils.rand_name(object.__name__ + "-vm1cmp1"),
        'id': None,
        'ip': None,
        'floating_ip': None
    }
    vm2 = {
        'name': utils.rand_name(object.__name__ + "-vm2cmp1"),
        'id': None,
        'ip': None,
        'floating_ip': None
    }
    vm3 = {
        'name': utils.rand_name(object.__name__ + "-vm1cmp2"),
        'id': None,
        'ip': None,
        'floating_ip': None
    }

    @pytest.fixture(scope='module')
    def setup(self, config, os_clients, os_actions, cleanup, upload_images,
              create_flavors, router_attach_subnet, create_sg, create_keypair):
        # TO DO: deploy instance on different hosts
        vm1 = os_actions.create_instance(TestMVPN.vm1['name'])
        TestMVPN.vm1['id'] = vm1.id

        vm2 = os_actions.create_instance(TestMVPN.vm2['name'])
        TestMVPN.vm2['id'] = vm2.id

        vm3 = os_actions.create_instance(TestMVPN.vm3['name'])
        TestMVPN.vm3['id'] = vm3.id

        # Wait while instances are being deployed
        os_actions.wait_instance_status(TestMVPN.vm1['id'])
        os_actions.wait_instance_status(TestMVPN.vm2['id'])
        os_actions.wait_instance_status(TestMVPN.vm3['id'])

        # Assign floating ip
        fip = 'floatingip'
        vm1_fip = os_actions.associate_fip(TestMVPN.vm1['id'])
        TestMVPN.vm1['ip'] = vm1_fip[fip]['fixed_ip_address']
        TestMVPN.vm1['floating_ip'] = vm1_fip[fip]['floating_ip_address']

        vm2_fip = os_actions.associate_fip(TestMVPN.vm2['id'])
        TestMVPN.vm2['ip'] = vm2_fip[fip]['fixed_ip_address']
        TestMVPN.vm2['floating_ip'] = vm2_fip[fip]['floating_ip_address']

        vm3_fip = os_actions.associate_fip(TestMVPN.vm3['id'])
        TestMVPN.vm3['ip'] = vm3_fip[fip]['fixed_ip_address']
        TestMVPN.vm3['floating_ip'] = vm3_fip[fip]['floating_ip_address']
        pass

    def test_mvpn_same_vn_same_node(self, setup, ssh_connect):
        logger.info("VM 1: {}".format(TestMVPN.vm1))
        vm1_cmp1_c = ssh_connect(TestMVPN.vm1['floating_ip'])
        stdin1, stdout1, stderr1 = vm1_cmp1_c.exec_command('cat /etc/hostname')
        out = stdout1.read()
        logger.info(out)
