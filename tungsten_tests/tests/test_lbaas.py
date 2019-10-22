import logging
import pytest
import time

from tungsten_tests.helpers import common
from tungsten_tests.helpers import utils

logger = logging.getLogger()


@pytest.mark.functional
class TestLBaaS(object):
    """Check LBaaS functional with neutron LBaaS v2 api (Deprecated since
    OpenStack Queens)."""

    name_prefix = 'tft_TestLBaaS'
    vm_list = []
    vm_client = {
        'name': utils.rand_name(name_prefix + "-vm_client"),
        'id': None,
        'ip': None,
        'floating_ip': None
    }
    vm_list.append(vm_client)
    vm1 = {
        'name': utils.rand_name(name_prefix + "-vm1"),
        'id': None,
        'ip': None,
        'floating_ip': None
    }
    vm_list.append(vm1)
    vm2 = {
        'name': utils.rand_name(name_prefix + "-vm2"),
        'id': None,
        'ip': None,
        'floating_ip': None
    }
    vm_list.append(vm2)
    vm3 = {
        'name': utils.rand_name(name_prefix + "-vm3"),
        'id': None,
        'ip': None,
        'floating_ip': None
    }
    vm_list.append(vm3)

    loadbalancer = {
        "name": "",
        "description": "Created by TFT (TungstenFabric Tests)",
        "admin_state_up": True,
        "project_id": "",
        "vip_subnet_id": "",
        "provider": "",
    }
    listener = {
        "name": "",
        "description": "TFT listener",
        "admin_state_up": True,
        "loadbalancer_id": "",
        "protocol": "",
        "protocol_port": "",
    }
    pool = {
        "name": "",
        "description": "TFT pool",
        "admin_state_up": True,
        "listener_id": "",
        "lb_algorithm": "",
        "protocol": "",
    }
    member1 = {
        "name": vm1['name'],
        "weight": "1",
        "admin_state_up": True,
        "subnet_id": "",
        "address": "",
        "protocol_port": "",
    }
    member2 = {
        "name": vm2['name'],
        "weight": "1",
        "admin_state_up": True,
        "subnet_id": "",
        "address": "",
        "protocol_port": "",
    }
    member3 = {
        "name": vm3['name'],
        "weight": "1",
        "admin_state_up": True,
        "subnet_id": "",
        "address": "",
        "protocol_port": "",
    }
    healthmonitor = {
        "name": "",
        "admin_state_up": True,
        "pool_id": "",
        "type": "",
        "delay": 15,
        "timeout": 14,
        "max_retries": 3,
    }
    cmd_http = "for i in {{1..{num}}}; do curl {vip}/hostname; done"
    cmd_tcp = "for i in {{1..{num}}}; do ssh-keyscan -p 22 -t ssh-rsa {vip} " \
              "2>/dev/null; done"

    @pytest.fixture(scope='class')
    def setup(self, os_init_setup, config, os_clients, os_actions_class):

        # Create VMs
        for vm in TestLBaaS.vm_list:
            instance = os_actions_class.create_instance(vm['name'])
            vm['id'] = instance.id

        # Wait while instances are being deployed
        for vm in TestLBaaS.vm_list:
            os_actions_class.wait_instance_status(vm['id'])

        # Assign floating ip
        for vm in TestLBaaS.vm_list:
            fip = os_actions_class.associate_fip(vm['id'])
            vm['ip'] = fip['floatingip']['fixed_ip_address']
            vm['floating_ip'] = fip['floatingip']['floating_ip_address']
        TestLBaaS.member1['address'] = TestLBaaS.vm1['ip']
        TestLBaaS.member2['address'] = TestLBaaS.vm2['ip']
        TestLBaaS.member3['address'] = TestLBaaS.vm3['ip']

        # Wait for cloud init
        for vm in TestLBaaS.vm_list:
            with common.ssh_connect(vm['floating_ip'],
                                    pkey=config.os_private_key) as ssh_client:
                common.wait_for_cloud_init(ssh_client)

        # Update LB objects
        TestLBaaS.loadbalancer["project_id"] = config.os_project_id
        TestLBaaS.loadbalancer["vip_subnet_id"] = config.os_subnet_id
        TestLBaaS.loadbalancer["provider"] = config.os_lb_provider
        TestLBaaS.member1["subnet_id"] = config.os_subnet_id
        TestLBaaS.member2["subnet_id"] = config.os_subnet_id
        TestLBaaS.member3["subnet_id"] = config.os_subnet_id

    def test_lbaas_http(self, setup, os_actions, ssh_connect):
        """Check loadbalancing of HTTP traffic using RoundRobin algorithm"""
        loadbalancer = TestLBaaS.loadbalancer.copy()
        listener = TestLBaaS.listener.copy()
        pool = TestLBaaS.pool.copy()
        member1 = TestLBaaS.member1.copy()
        member2 = TestLBaaS.member2.copy()

        loadbalancer['name'] = "tft_lbaas_http"
        tft_lb = os_actions.create_loadbalancer(loadbalancer)
        vip = tft_lb['loadbalancer']['vip_address']

        listener['name'] = "tft_listener_http"
        listener['loadbalancer_id'] = tft_lb['loadbalancer']['id']
        listener['protocol'] = "HTTP"
        listener['protocol_port'] = "80"
        tft_listener = os_actions.create_listener(listener)

        pool["name"] = "tft_pool_http"
        pool["listener_id"] = tft_listener['listener']['id']
        pool["lb_algorithm"] = "ROUND_ROBIN"
        pool["protocol"] = "HTTP"
        tft_pool = os_actions.create_lbaas_pool(pool)

        member1["protocol_port"] = "80"
        member2["protocol_port"] = "80"
        os_actions.create_lbaas_member(tft_pool['pool']['id'], member1)
        os_actions.create_lbaas_member(tft_pool['pool']['id'], member2)

        # Establish SSH connection
        vm_c = ssh_connect(TestLBaaS.vm_client['floating_ip'])

        # Check LB
        member_num = 2
        req_num = member_num * 3
        stdin, stdout, stderr = vm_c.exec_command(
            TestLBaaS.cmd_http.format(num=req_num, vip=vip)
        )
        out = stdout.read()
        logger.debug("VM output:\n{}".format(out))
        stat = utils.parser_lb_responses(out, req_num, member_num)
        logger.info("LB response statistics:\n{}".format(stat))

    def test_lbaas_tcp(self, setup, os_actions, ssh_connect):
        """Check loadbalancing of TCP traffic (SSH) using Least Connections
        algorithm"""
        loadbalancer = TestLBaaS.loadbalancer.copy()
        listener = TestLBaaS.listener.copy()
        pool = TestLBaaS.pool.copy()
        member1 = TestLBaaS.member1.copy()
        member2 = TestLBaaS.member2.copy()

        loadbalancer['name'] = "tft_lbaas_tcp"
        tft_lb = os_actions.create_loadbalancer(loadbalancer)
        vip = tft_lb['loadbalancer']['vip_address']

        listener['name'] = "tft_listener_tcp"
        listener['loadbalancer_id'] = tft_lb['loadbalancer']['id']
        listener['protocol'] = "TCP"
        listener['protocol_port'] = "22"
        tft_listener = os_actions.create_listener(listener)

        pool["name"] = "tft_pool_tcp"
        pool["listener_id"] = tft_listener['listener']['id']
        pool["lb_algorithm"] = "LEAST_CONNECTIONS"
        pool["protocol"] = "TCP"
        tft_pool = os_actions.create_lbaas_pool(pool)

        member1["protocol_port"] = "22"
        member2["protocol_port"] = "22"
        os_actions.create_lbaas_member(tft_pool['pool']['id'], member1)
        os_actions.create_lbaas_member(tft_pool['pool']['id'], member2)

        # Establish SSH connection
        vm_c = ssh_connect(TestLBaaS.vm_client['floating_ip'])

        # Check LB
        member_num = 2
        req_num = member_num * 3
        stdin, stdout, stderr = vm_c.exec_command(
            TestLBaaS.cmd_tcp.format(num=req_num, vip=vip)
        )
        out = stdout.read()
        logger.debug("VM output:\n{}".format(out))
        stat = utils.parser_lb_responses(out, req_num, member_num)
        logger.info("LB response statistics:\n{}".format(stat))

    def test_scale_pool(self, setup, os_actions, os_clients, ssh_connect):
        """Check scaling of loadbalancer pool"""
        loadbalancer = TestLBaaS.loadbalancer.copy()
        listener = TestLBaaS.listener.copy()
        pool = TestLBaaS.pool.copy()
        member1 = TestLBaaS.member1.copy()
        member2 = TestLBaaS.member2.copy()
        member3 = TestLBaaS.member3.copy()

        loadbalancer['name'] = "tft_scale_pool"
        tft_lb = os_actions.create_loadbalancer(loadbalancer)
        vip = tft_lb['loadbalancer']['vip_address']

        listener['name'] = "tft_listener_http"
        listener['loadbalancer_id'] = tft_lb['loadbalancer']['id']
        listener['protocol'] = "HTTP"
        listener['protocol_port'] = "80"
        tft_listener = os_actions.create_listener(listener)

        pool["name"] = "tft_pool_http"
        pool["listener_id"] = tft_listener['listener']['id']
        pool["lb_algorithm"] = "ROUND_ROBIN"
        pool["protocol"] = "HTTP"
        tft_pool = os_actions.create_lbaas_pool(pool)

        member1["protocol_port"] = "80"
        member2["protocol_port"] = "80"
        member3["protocol_port"] = "80"
        member = os_clients.neutron.create_lbaas_member(
            tft_pool['pool']['id'], {"member": member1}
        )
        logger.info("Member '{}' is added to pool '{}'"
                    "".format(member['member']['name'],
                              tft_pool['pool']['id']))

        # Establish SSH connection
        vm_c = ssh_connect(TestLBaaS.vm_client['floating_ip'])

        # Check LB
        member_num = 1
        req_num = member_num * 3
        stdin, stdout, stderr = vm_c.exec_command(
            TestLBaaS.cmd_http.format(num=req_num, vip=vip)
        )
        out = stdout.read()
        logger.debug("VM output:\n{}".format(out))
        stat = utils.parser_lb_responses(out, req_num, member_num)
        logger.info("LB response statistics:\n{}".format(stat))

        # Add pool members
        os_actions.create_lbaas_member(tft_pool['pool']['id'], member2)
        os_actions.create_lbaas_member(tft_pool['pool']['id'], member3)

        time.sleep(5)
        # Check LB
        member_num = 3
        req_num = member_num * 3
        stdin, stdout, stderr = vm_c.exec_command(
            TestLBaaS.cmd_http.format(num=req_num, vip=vip)
        )
        out = stdout.read()
        logger.debug("VM output:\n{}".format(out))
        stat = utils.parser_lb_responses(out, req_num, member_num)
        logger.info("LB response statistics:\n{}".format(stat))

        # Remove pool members
        os_clients.neutron.delete_lbaas_member(
            member['member']['id'], tft_pool['pool']['id']
        )
        logger.info("Member '{}' is removed from pool '{}'"
                    "".format(member1['name'],
                              tft_pool['pool']['id']))

        time.sleep(5)
        # Check LB
        member_num = 2
        req_num = member_num * 3
        stdin, stdout, stderr = vm_c.exec_command(
            TestLBaaS.cmd_http.format(num=req_num, vip=vip)
        )
        out = stdout.read()
        logger.debug("VM output:\n{}".format(out))
        stat = utils.parser_lb_responses(out, req_num, member_num)
        logger.info("LB response statistics:\n{}".format(stat))

    def test_multi_listeners(self, setup, os_actions, ssh_connect):
        """Check loadbalancer with several listeners"""
        loadbalancer = TestLBaaS.loadbalancer.copy()
        listener1 = TestLBaaS.listener.copy()
        listener2 = TestLBaaS.listener.copy()
        pool1 = TestLBaaS.pool.copy()
        pool2 = TestLBaaS.pool.copy()
        member1_1 = TestLBaaS.member1.copy()
        member1_2 = TestLBaaS.member2.copy()
        member2_1 = TestLBaaS.member1.copy()
        member2_2 = TestLBaaS.member2.copy()

        loadbalancer['name'] = "tft_loadbalancer"
        tft_lb = os_actions.create_loadbalancer(loadbalancer)
        vip = tft_lb['loadbalancer']['vip_address']

        listener1['name'] = "tft_listener_http"
        listener1['loadbalancer_id'] = tft_lb['loadbalancer']['id']
        listener1['protocol'] = "HTTP"
        listener1['protocol_port'] = "80"
        tft_listener1 = os_actions.create_listener(listener1)

        pool1["name"] = "tft_pool_http"
        pool1["listener_id"] = tft_listener1['listener']['id']
        pool1["lb_algorithm"] = "ROUND_ROBIN"
        pool1["protocol"] = "HTTP"
        tft_pool1 = os_actions.create_lbaas_pool(pool1)

        listener2['name'] = "tft_listener_tcp"
        listener2['loadbalancer_id'] = tft_lb['loadbalancer']['id']
        listener2['protocol'] = "TCP"
        listener2['protocol_port'] = "22"
        tft_listener2 = os_actions.create_listener(listener2)

        pool2["name"] = "tft_pool_tcp"
        pool2["listener_id"] = tft_listener2['listener']['id']
        pool2["lb_algorithm"] = "LEAST_CONNECTIONS"
        pool2["protocol"] = "TCP"
        tft_pool2 = os_actions.create_lbaas_pool(pool2)

        member1_1["protocol_port"] = "80"
        member1_2["protocol_port"] = "80"
        member2_1["protocol_port"] = "22"
        member2_2["protocol_port"] = "22"
        os_actions.create_lbaas_member(tft_pool1['pool']['id'], member1_1)
        os_actions.create_lbaas_member(tft_pool1['pool']['id'], member1_2)
        os_actions.create_lbaas_member(tft_pool2['pool']['id'], member2_1)
        os_actions.create_lbaas_member(tft_pool2['pool']['id'], member2_2)

        # Establish SSH connection
        vm_c = ssh_connect(TestLBaaS.vm_client['floating_ip'])

        member_num = 2
        req_num = member_num * 3

        # Check listener1
        stdin, stdout, stderr = vm_c.exec_command(
            TestLBaaS.cmd_http.format(num=req_num, vip=vip)
        )
        out = stdout.read()
        logger.debug("VM output:\n{}".format(out))
        stat = utils.parser_lb_responses(out, req_num, member_num)
        logger.info("LB response statistics:\n{}".format(stat))

        # Check listener2
        stdin, stdout, stderr = vm_c.exec_command(
            TestLBaaS.cmd_tcp.format(num=req_num, vip=vip)
        )
        out = stdout.read()
        logger.debug("VM output:\n{}".format(out))
        stat = utils.parser_lb_responses(out, req_num, member_num)
        logger.info("LB response statistics:\n{}".format(stat))

    def test_health_monitor_http(self, setup, os_actions, ssh_connect):
        """Check HTTP health monitor"""
        # Health check is carried out by HA proxy, so we don't need to
        # create OS health monitor
        loadbalancer = TestLBaaS.loadbalancer.copy()
        listener = TestLBaaS.listener.copy()
        pool = TestLBaaS.pool.copy()
        member1 = TestLBaaS.member1.copy()
        member2 = TestLBaaS.member2.copy()
        member3 = TestLBaaS.member3.copy()

        loadbalancer['name'] = "tft_lb_http"
        tft_lb = os_actions.create_loadbalancer(loadbalancer)
        vip = tft_lb['loadbalancer']['vip_address']

        listener['name'] = "tft_listener_http"
        listener['loadbalancer_id'] = tft_lb['loadbalancer']['id']
        listener['protocol'] = "HTTP"
        listener['protocol_port'] = "80"
        tft_listener = os_actions.create_listener(listener)

        pool["name"] = "tft-pool-http"
        pool["listener_id"] = tft_listener['listener']['id']
        pool["lb_algorithm"] = "ROUND_ROBIN"
        pool["protocol"] = "HTTP"
        tft_pool = os_actions.create_lbaas_pool(pool)

        member1["protocol_port"] = "80"
        member2["protocol_port"] = "80"
        member3["protocol_port"] = "80"
        os_actions.create_lbaas_member(tft_pool['pool']['id'], member1)
        os_actions.create_lbaas_member(tft_pool['pool']['id'], member2)
        os_actions.create_lbaas_member(tft_pool['pool']['id'], member3)

        # Establish SSH connection
        vm_c = ssh_connect(TestLBaaS.vm_client['floating_ip'])
        vm_1 = ssh_connect(TestLBaaS.vm1['floating_ip'])

        # Check LB
        member_num = 3
        req_num = member_num * 3
        stdin, stdout, stderr = vm_c.exec_command(
            TestLBaaS.cmd_http.format(num=req_num, vip=vip)
        )
        out = stdout.read()
        logger.debug("VM output:\n{}".format(out))
        stat = utils.parser_lb_responses(out, req_num, member_num)
        logger.info("LB response statistics:\n{}".format(stat))

        # Disable HTTP service on one pool member
        cmd = "sudo systemctl stop apache2 && systemctl status apache2"
        stdin, stdout, stderr = vm_1.exec_command(cmd)
        out = stdout.read()
        logger.debug("VM1 output:\n{}".format(out))

        # Check LB with non-working member
        member_num = 2
        req_num = member_num * 3
        stdin, stdout, stderr = vm_c.exec_command(
            TestLBaaS.cmd_http.format(num=req_num, vip=vip)
        )
        out = stdout.read()
        logger.debug("VM output:\n{}".format(out))
        stat = utils.parser_lb_responses(out, req_num, member_num)
        logger.info("LB response statistics:\n{}".format(stat))
