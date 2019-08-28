import logging
import pytest

from tungsten_tests.helpers import utils
from tungsten_tests.helpers import waiters

logger = logging.getLogger()


@pytest.mark.functional
class TestMVPN(object):

    vm1_cmp1_name = utils.rand_name(object.__name__ + "-vm1cmp1")
    vm2_cmp1_name = utils.rand_name(object.__name__ + "-vm2cmp1")
    vm1_cmp2_name = utils.rand_name(object.__name__ + "-vm1cmp2")
    vm1_cmp1 = None
    vm2_cmp1 = None
    vm1_cmp2 = None

    @pytest.fixture(scope='module')
    def setup(self, config, os_clients, cleanup, upload_images,
              create_flavors, router_attach_subnet, create_sg):
        nics = [{'net-id': config.os_net_id}]

        # TO DO: deploy instance on different hosts

        TestMVPN.vm1_cmp1 = os_clients.nova.servers.create(
            self.vm1_cmp1_name, config.os_ubuntu_img_id,
            config.os_ubuntu_flavor_id, nics=nics
        )
        cleanup(waiters.wait_for_instance_termination, os_clients.nova,
                self.vm1_cmp1.id)
        cleanup(os_clients.nova.servers.delete, self.vm1_cmp1.id)

        TestMVPN.vm2_cmp1 = os_clients.nova.servers.create(
            self.vm2_cmp1_name, config.os_ubuntu_img_id,
            config.os_ubuntu_flavor_id, nics=nics
        )
        cleanup(waiters.wait_for_instance_termination, os_clients.nova,
                self.vm2_cmp1.id)
        cleanup(os_clients.nova.servers.delete, self.vm2_cmp1.id)

        # TestMVPN.vm1_cmp2 = os_clients.nova.servers.create(
        #     self.vm1_cmp2_name, config.os_ubuntu_img_id,
        #     config.os_ubuntu_flavor_id, nics=nics
        # )
        # cleanup(waiters.wait_for_instance_termination, os_clients.nova,
        #         self.vm1_cmp2.id)
        # cleanup(os_clients.nova.servers.delete, self.vm1_cmp2.id)
        waiters.wait_instance_status(os_clients.nova, self.vm1_cmp1.id)
        waiters.wait_instance_status(os_clients.nova, self.vm2_cmp1.id)
        # waiters.wait_instance_status(os_clients.nova, self.vm1_cmp2.id)

    def test_mvpn_same_vn_same_node(self, os_clients, cleanup, setup):
        logger.info("VM 1 is {}".format(self.vm1_cmp1.id))
        pass

    def test_mvpn_same_vn_diff_nodes(self, os_clients, cleanup, setup):
        logger.info("VM 2 is {}".format(self.vm2_cmp1.id))
        pass
