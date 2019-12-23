from vnc_api.vnc_api import VncApi


class ContrailEnvClient:
    def __init__(self, username, password, tenant_name, api_server_host,
                 api_server_port, auth_host, auth_port, auth_protocol,
                 auth_url, auth_type, **kwargs):
        self.vnc_lib = VncApi(
            username=username, password=password, tenant_name=tenant_name,
            api_server_host=api_server_host, api_server_port=api_server_port,
            auth_host=auth_host, auth_port=auth_port,
            auth_protocol=auth_protocol, auth_url=auth_url,
            auth_type=auth_type, **kwargs)

    @property
    def list_analytics_node(self):
        return self.vnc_lib.resource_list('analytics-node', detail=True)

    @property
    def list_config_node(self):
        return self.vnc_lib.resource_list('config-node', detail=True)

    @property
    def list_database_node(self):
        return self.vnc_lib.resource_list('database-node', detail=True)

    @property
    def list_vrouter_router(self):
        return self.vnc_lib.resource_list('virtual-router', detail=True)

    @property
    def list_virtual_networks(self):
        return self.vnc_lib.resource_list('virtual-network', detail=True)

    @property
    def list_bgp_routers(self):
        return self.vnc_lib.resource_list('bgp-router', detail=True)

    def get_analytics_node(self, id):
        return self.vnc_lib._object_read('analytics-node', id=id)

    def get_bgp_router(self, id):
        return self.vnc_lib._object_read('bgp-router', id=id)
