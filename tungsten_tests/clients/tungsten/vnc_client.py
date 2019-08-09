from vnc_api.vnc_api import VncApi


class ContrailEnvClient:
    def __init__(self, conf_file, **kwargs):
        self.vnc_lib = VncApi(conf_file=conf_file, **kwargs)

    def list_virtual_networks(self):
        vn_list = self.vnc_lib.resource_list('virtual-network', detail=True)
        return vn_list

    def list_config_nodes(self):
        cfg_node_list = self.vnc_lib.resource_list('config-node', detail=True)
        return cfg_node_list

    def list_bgp_routers(self):
        bgp_router_list = self.vnc_lib.resource_list('bgp-router', detail=True)
        return bgp_router_list

    def get_bgp_router(self, id):
        return self.vnc_lib._object_read('bgp-router', id=id)
