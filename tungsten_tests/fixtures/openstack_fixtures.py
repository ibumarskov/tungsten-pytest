import ipaddress
import logging
import pytest

import neutronclient.common.exceptions

from tungsten_tests.clients.os_clients import OpenStackClientManager
from tungsten_tests.helpers.common import download_file
from tungsten_tests.settings import TFT_UBUNTU_IMG_URL, TFT_IMAGE_PATH

logger = logging.getLogger()


@pytest.fixture(scope='session')
def os_clients(config):
    return OpenStackClientManager(
        auth_url=config.os_auth_url, username=config.os_username,
        password=config.os_password, project_name=config.os_project_name,
        user_domain_name=config.os_user_domain_name,
        project_domain_name=config.os_project_domain_name,
        endpoint_type=config.os_endpoint_type)


@pytest.fixture(scope='session')
def upload_images(config, os_clients):
    # Check if image is present
    for image in os_clients.glance.images.list():
        if image.name == config.os_ubuntu_img_name:
            config.os_ubuntu_img_id = image.id
            logger.info("Image {} was found. Image id is {}".format(
                config.os_ubuntu_img_name, config.os_ubuntu_img_id))
    if not config.os_ubuntu_img_id:
        logger.info("Image {} wasn't found.".format(config.os_ubuntu_img_name))
        file_path = download_file(TFT_UBUNTU_IMG_URL, TFT_IMAGE_PATH)
        image = os_clients.glance.images.create(name=config.os_ubuntu_img_name,
                                                disk_format='qcow2',
                                                container_format='bare',
                                                visibility='public')
        os_clients.glance.images.upload(image.id, open(file_path, 'rb'))
        config.os_ubuntu_img_id = image.id
        logger.info("Image {} is uploaded. Image id is {}".format(
            config.os_ubuntu_img_name, config.os_ubuntu_img_id))
    yield
    # Cleanup
    logger.info("Delete image {}".format(config.os_ubuntu_img_id))
    # os_clients.glance.images.delete(config.os_ubuntu_img_id)


@pytest.fixture(scope='session')
def create_flavors(config, os_clients):
    # Check if flavors exist
    for flavor in os_clients.nova.flavors.list():
        if flavor.name == config.os_ubuntu_flavor_name:
            config.os_ubuntu_flavor_id = flavor.id
            logger.info("Flavor {} was found. Flavor id is {}".format(
                config.os_ubuntu_flavor_name, config.os_ubuntu_flavor_id))
    if not config.os_ubuntu_flavor_id:
        logger.info("Flavor {} wasn't found."
                    "".format(config.os_ubuntu_flavor_name))
        flavor = os_clients.nova.flavors.create(
            name=config.os_ubuntu_flavor_name,
            ram=512, vcpus=1, disk=1,
            is_public=True)
        config.os_ubuntu_flavor_id = flavor.id
        logger.info("Flavor {} is created. Falvor id is {}".format(
            config.os_ubuntu_flavor_name, config.os_ubuntu_flavor_id))
    yield
    # Cleanup
    logger.info("Delete flavor {}".format(config.os_ubuntu_flavor_id))
    os_clients.nova.flavors.delete(config.os_ubuntu_flavor_id)


@pytest.fixture(scope='session')
def create_network(config, os_clients):
    # Check if network exist
    networks = os_clients.neutron.list_networks()
    for net in networks['networks']:
        if net['name'] == config.os_net_name:
            config.os_net_id = net['id']
            logger.info("Network {} was found. Network id is {}".format(
                config.os_net_name, config.os_net_id))
    if not config.os_net_id:
        logger.info("Network {} wasn't found.".format(config.os_net_name))
        network = {
            'name': config.os_net_name,
            'admin_state_up': True
        }
        net = os_clients.neutron.create_network({'network': network})
        config.os_net_id = net['network']['id']
        logger.info("Network {} is created. Network id is {}".format(
            config.os_net_name, config.os_net_id))
    yield
    # Cleanup
    logger.info("Delete network {}".format(config.os_net_id))
    os_clients.neutron.delete_network(config.os_net_id)


@pytest.fixture(scope='session')
def create_subnet(config, os_clients, create_network):
    # Check if subnet exist
    subnets = os_clients.neutron.list_subnets(network_id=config.os_net_id)
    for subnet in subnets['subnets']:
        if subnet['name'] == config.os_subnet_name:
            config.os_subnet_id = subnet['id']
            logger.info("Subnet {} was found. Subnet id is {}".format(
                config.os_subnet_name, config.os_subnet_id))
    if not config.os_subnet_id:
        logger.info("Subnet {} wasn't found.".format(config.os_subnet_name))
        ipv4_net = ipaddress.IPv4Network(unicode(config.os_subnet_cidr))
        ip_range = list(ipv4_net.hosts())
        subnet = {
            'name': config.os_subnet_name,
            'network_id': config.os_net_id,
            'ip_version': 4,
            'cidr': config.os_subnet_cidr,
            'allocation_pools': [{'start': str(ip_range[10]),
                                  'end': str(ip_range[-1])}]
        }
        subnet = os_clients.neutron.create_subnet({'subnet': subnet})
        config.os_subnet_id = subnet['subnet']['id']
        logger.info("Subnet {} is created. Subnet id is {}".format(
            config.os_subnet_name, config.os_subnet_id))
    yield
    # Cleanup
    logger.info("Delete subnet {}".format(config.os_subnet_id))
    os_clients.neutron.delete_subnet(config.os_subnet_id)


@pytest.fixture(scope='session')
def create_sg(config, os_clients):
    # Check if security group exist
    sgs = os_clients.neutron.list_security_groups()
    for sg in sgs['security_groups']:
        if sg['name'] == config.os_sg_name:
            config.os_sg_id = sg['id']
            logger.info("Security group {} was found. SG id is {}".format(
                config.os_subnet_name, config.os_subnet_id))
            break
    if not config.os_sg_id:
        logger.info("Security group {} wasn't found.".format(
            config.os_subnet_name))
        sg_body = {
            'name': config.os_sg_name
        }
        sg = os_clients.neutron.create_security_group(
            {'security_group': sg_body}
        )
        config.os_sg_id = sg['security_group']['id']
        logger.info("Security group {} is created. SG id is {}".format(
            config.os_subnet_name, config.os_subnet_id))

    # Add security group rules
    sg_rules = [{
        "direction": "ingress",
        "ethertype": "IPv4",
        "protocol": "icmp",
        "security_group_id": config.os_sg_id
    }, {
        "direction": "ingress",
        "port_range_min": "0",
        "ethertype": "IPv4",
        "port_range_max": "65535",
        "protocol": "udp",
        "security_group_id": config.os_sg_id
    }, {
        "direction": "ingress",
        "port_range_min": "0",
        "ethertype": "IPv4",
        "port_range_max": "65535",
        "protocol": "tcp",
        "security_group_id": config.os_sg_id
    }, {
        "direction": "ingress",
        "ethertype": "IPv6",
        "protocol": "icmp",
        "security_group_id": config.os_sg_id
    }, {
        "direction": "ingress",
        "port_range_min": "0",
        "ethertype": "IPv6",
        "port_range_max": "65535",
        "protocol": "tcp",
        "security_group_id": config.os_sg_id
    }, {
        "direction": "ingress",
        "port_range_min": "0",
        "ethertype": "IPv6",
        "port_range_max": "65535",
        "protocol": "udp",
        "security_group_id": config.os_sg_id
    }]

    for rule in sg_rules:
        try:
            os_clients.neutron.create_security_group_rule(
                {'security_group_rule': rule}
            )
        except neutronclient.common.exceptions.Conflict as e:
            logger.warning("{}".format(e))
    yield
    # Cleanup
    logger.info("Delete security group {}".format(config.os_sg_id))
    os_clients.neutron.delete_security_group(config.os_sg_id)


@pytest.fixture(scope='session')
def get_external_net(config, os_clients):
    if not config.os_ext_net_id:
        net = os_clients.neutron.list_networks(name=config.os_ext_net_name)
        if len(net['networks']) == 1:
            if not net['networks'][0]['router:external']:
                raise Exception("Network {} isn't external"
                                "".format(config.os_ext_net_name))
            else:
                config.os_ext_net_id = net['networks'][0]['id']
        elif len(net['networks']) > 1:
            raise Exception("Can't determine external network {}. Was found "
                            "several networks with such name: {}"
                            "".format(config.os_ext_net_name, net['networks']))
        else:
            raise Exception("Can't find external network {}"
                            "".format(config.os_ext_net_name))


@pytest.fixture(scope='session')
def create_router(config, os_clients, get_external_net):
    # Check if router exist
    routers = os_clients.neutron.list_routers()
    for router in routers['routers']:
        if router['name'] == config.os_router_name:
            ext_gw_net = router['external_gateway_info']['network_id']
            if ext_gw_net != config.os_ext_net_id:
                raise Exception("Incorrect gateway network: {}. Should be: {}"
                                "".format(ext_gw_net, config.os_ext_net_id))
            config.os_router_id = router['id']
            logger.info("Router {} was found. Router id is {}".format(
                config.os_router_name, config.os_router_id))
    if not config.os_router_id:
        logger.info("Router {} wasn't found.".format(config.os_router_name))
        external_gateway_info = {
            'network_id': config.os_ext_net_id
        }
        router = {
            'name': config.os_router_name,
            'admin_state_up': True,
            'external_gateway_info': external_gateway_info
        }
        router = os_clients.neutron.create_router({'router': router})
        config.os_router_id = router['router']['id']
        logger.info("Router {} is created. Router id is {}".format(
            config.os_router_name, config.os_router_id))
    yield
    # Cleanup
    logger.info("Delete router {}".format(config.os_router_id))
    os_clients.neutron.delete_router(config.os_router_id)


@pytest.fixture(scope='session')
def router_attach_subnet(config, os_clients, create_subnet, create_router):
    # Check if port is attached
    ports = os_clients.neutron.list_ports(device_id=config.os_router_id)
    for port in ports['ports']:
        if port['name'] == config.os_port_name:
            net_id = port['network_id']
            if port['network_id'] != config.os_net_id:
                raise Exception("Incorrect port network: {}. Should be: {}"
                                "".format(net_id, config.os_net_id))
            config.os_port_id = port['id']
            logger.info("Port {} was found. Port id is {}".format(
                config.os_port_name, config.os_port_id))
    if not config.os_port_id:
        logger.info("Port {} wasn't found.".format(config.os_port_name))
        interface = {
            "subnet_id": config.os_subnet_id
        }
        resp = os_clients.neutron.add_interface_router(config.os_router_id,
                                                       interface)
        config.os_port_id = resp['port_id']
        port = {
            "name": config.os_port_name
        }
        os_clients.neutron.update_port(config.os_port_id, {'port': port})
        logger.info("Port {}:{} was attached to router {}:{}".format(
            config.os_port_name, config.os_port_id, config.os_router_name,
            config.os_router_id))
    yield
    # Cleanup
    logger.info("Detach port {}".format(config.os_port_id))
    os_clients.neutron.remove_interface_router(config.os_router_id, interface)
