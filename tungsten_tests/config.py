import ConfigParser


class MCPConfig(object):
    def __init__(self, conf):
        cfgparser = ConfigParser.ConfigParser()
        cfgparser.read(conf)

        # K8s
        self.k8s_kubeconfig = cfgparser.get('k8s', 'kubeconfig')

        # K8s OpenStack deployment
        self.k8s_osdpl_name = cfgparser.get('k8s_osdpl', 'name')
        self.k8s_osdpl_namespace = cfgparser.get('k8s_osdpl', 'namespace')
        self.k8s_osdpl_group = cfgparser.get('k8s_osdpl', 'group')
        self.k8s_osdpl_version = cfgparser.get('k8s_osdpl', 'version')

        # TungstenFabric
        self.tf_srv_ip = cfgparser.get('tungsten', 'WEB_SERVER')
        self.tf_srv_port = cfgparser.get('tungsten', 'WEB_PORT')
        self.tf_auth_type = cfgparser.get('tungsten', 'AUTHN_TYPE')
        self.tf_auth_proto = cfgparser.get('tungsten', 'AUTHN_PROTOCOL')
        self.tf_auth_srv = cfgparser.get('tungsten', 'AUTHN_SERVER')
        self.tf_auth_port = cfgparser.get('tungsten', 'AUTHN_PORT')
        self.tf_auth_url = cfgparser.get('tungsten', 'AUTHN_URL')
        self.tf_auth_tenant = cfgparser.get('tungsten', 'AUTHN_TENANT')
        self.tf_auth_user = cfgparser.get('tungsten', 'AUTHN_USER')
        self.tf_auth_pwd = cfgparser.get('tungsten', 'AUTHN_PASSWORD')
        self.tf_nal_ip = cfgparser.get('tungsten', 'ANALYTIC_IP')
        self.tf_nal_port = cfgparser.getint('tungsten', 'ANALYTIC_PORT')
