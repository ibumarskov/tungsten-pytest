import ConfigParser


class MCPConfig(object):
    def __init__(self, conf):
        cfgparser = ConfigParser.ConfigParser()
        cfgparser.read(conf)

        # K8s TungstenFabric operator
        self.k8s_tfoperator_name = cfgparser.get('k8s_tfoperator', 'name')
        self.k8s_tfoperator_namespace = \
            cfgparser.get('k8s_tfoperator', 'namespace')
        self.k8s_tfoperator_plural = cfgparser.get('k8s_tfoperator', 'plural')
        self.k8s_tfoperator_group = cfgparser.get('k8s_tfoperator', 'group')
        self.k8s_tfoperator_version = \
            cfgparser.get('k8s_tfoperator', 'version')

        # TungstenFabric (vnc_api)
        self.tf_srv_ip = cfgparser.get('tungsten', 'CONFIG_API_SERVER')
        self.tf_srv_port = cfgparser.get('tungsten', 'CONFIG_API_PORT')
        self.tf_auth_type = cfgparser.get('tungsten', 'AUTHN_TYPE')
        self.tf_auth_proto = cfgparser.get('tungsten', 'AUTHN_PROTOCOL')
        self.tf_auth_srv = cfgparser.get('tungsten', 'AUTHN_SERVER')
        self.tf_auth_port = cfgparser.get('tungsten', 'AUTHN_PORT')
        self.tf_auth_url = cfgparser.get('tungsten', 'AUTHN_URL')
        self.tf_auth_tenant = cfgparser.get('tungsten', 'AUTHN_TENANT')
        self.tf_auth_user = cfgparser.get('tungsten', 'AUTHN_USER')
        self.tf_auth_pwd = cfgparser.get('tungsten', 'AUTHN_PASSWORD')
        self.tf_analytic_srv_ports = {'alarm-gen': 5995,
                                      'api': 8090,
                                      'collector': 8089,
                                      'query-engine': 8091,
                                      'snmp': 5920,
                                      'topology': 5921}
        self.tf_control_srv_ports = {'control': 8083,
                                     'named': None,
                                     'dns': 8092}
        self.tf_config_srv_ports = {"api": None,
                                    "devicemgr": None,
                                    "schema": 8087,
                                    "svc-monitor": 8088}
        self.tf_vrouter_ports = {"agent": 8085}

        # OpenStack
        self.os_auth_url = cfgparser.get('openstack', 'auth_url')
        self.os_username = cfgparser.get('openstack', 'admin_username')
        self.os_password = cfgparser.get('openstack', 'admin_password')
        self.os_project_name = cfgparser.get('openstack', 'admin_project_name')
        self.os_user_domain_name = cfgparser.get('openstack',
                                                 'admin_user_domain_name')
        self.os_project_domain_name = cfgparser.get(
            'openstack', 'admin_project_domain_name')
        self.os_endpoint_type = cfgparser.get('openstack', 'endpoint_type')

        # Common OS setup
        self.os_project_id = None
        self.os_ubuntu_img_name = 'tft_ubuntu_img'
        self.os_ubuntu_img_id = None
        self.os_ubuntu_flavor_name = 'tft_ubuntu_flavor'
        self.os_ubuntu_flavor_id = None
        self.os_ext_net_name = 'public'
        self.os_ext_net_id = None
        self.os_net_name = 'tft-network'
        self.os_net_id = None
        self.os_subnet_name = 'tft-subnet'
        self.os_subnet_cidr = '192.168.200.0/24'
        self.os_sg_name = 'tft-sg'
        self.os_sg_id = None
        self.os_subnet_id = None
        self.os_router_name = 'tft-router'
        self.os_router_id = None
        self.os_port_name = 'tft-port'
        self.os_port_id = None
        self.os_keypair_name = 'tft-keypair'
        self.os_keypair_id = None
        self.os_private_key = None
        self.os_az = None
        self.os_lb_provider = 'opencontrail'
        # Test's specific data
        self.mcast_cidr = '192.168.201.0/24'
