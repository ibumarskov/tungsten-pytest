import requests

from introspect_data import IntrospectData, NodeStatus, BgpPeerInfoData, \
    XmppPeerInfoData


class AnalyticClient:
    def __init__(self, ip, port=9081, base_url='analytics', protocol='http'):
        self.ip = ip
        self.port = port
        self.base_url = base_url
        self.protocol = protocol

    @property
    def url(self):
        return "{proto}://{ip}:{port}/{base_url}".format(
            proto=self.protocol, ip=self.ip, port=self.port,
            base_url=self.base_url)

    def send_get(self, uri):
        response = requests.get("{url}/{uri}".format(url=self.url,
                                                     uri=uri))
        response.raise_for_status()
        return response

    def send_post(self, uri, data, async_query=False):
        url = "{url}/{uri}".format(url=self.url, uri=uri)
        headers = {'Content-Type': 'application/json'}
        if async_query:
            headers.update({'Expect': '202-accepted'})
        response = requests.post(url, data)
        response.raise_for_status()
        return response

    def get_uve_types(self):
        response = self.send_get('uve-types')
        return response.json()

    def get_tables(self, table=None):
        uri = 'tables'
        if table:
            uri += '/{}'.format(table)
        response = self.send_get(uri)
        return response.json()

    def get_queries(self):
        response = self.send_get('queries')
        return response.json()

    def get_alarms(self):
        response = self.send_get('alarms')
        return response.content

    def get_uve_stream(self):
        response = self.send_get('uve-stream')
        return response.content

    # User Visible Entity (UVE) objects
    def get_uves(self, uve_type=None):
        uri = 'uves'
        if uve_type:
            uri += '/{}'.format(uve_type)
        response = self.send_get(uri)
        return response.json()

    # UVE storage-pools objects
    def get_uve_storage_pool(self, storage_pool=None):
        uri = 'storage-pools'
        if storage_pool:
            uri = uri[:-1]+'/{}'.format(storage_pool)
        return self.get_uves(uri)

    def get_uves_storage_pools(self):
        return self.get_uve_storage_pool()

    # UVE xmpp-peers objects
    def get_uve_xmpp_peer(self, xmpp_peer=None):
        uri = 'xmpp-peers'
        if xmpp_peer:
            uri = uri[:-1]+'/{}'.format(xmpp_peer)
        return self.get_uves(uri)

    def get_uves_xmpp_peers(self):
        return self.get_uve_xmpp_peer()

    def get_XmppPeer(self, bgp_peer):
        data = self.get_uve_xmpp_peer(bgp_peer)
        return XmppPeer(data)

    # UVE storage-clusters objects
    def get_uve_storage_cluster(self, storage_cluster=None):
        uri = 'storage-clusters'
        if storage_cluster:
            uri = uri[:-1] + '/{}'.format(storage_cluster)
        return self.get_uves(uri)

    def get_uves_storage_clusters(self):
        return self.get_uve_storage_cluster()

    # UVE service-instances objects
    def get_uve_service_instance(self, service_instance=None):
        uri = 'service-instances'
        if service_instance:
            uri = uri[:-1] + '/{}'.format(service_instance)
        return self.get_uves(uri)

    def get_uves_service_instances(self):
        return self.get_uve_service_instance()

    # UVE analytic-nodes objects
    def get_uve_analytics_node(self, analytics_node=None):
        uri = 'analytics-nodes'
        if analytics_node:
            uri = uri[:-1]+'/{}'.format(analytics_node)
        return self.get_uves(uri)

    def get_uves_analytics_nodes(self):
        return self.get_uve_analytics_node()

    def get_AnalyticNode(self, analytics_node):
        data = self.get_uve_analytics_node(analytics_node)
        return AnalyticNode(data)

    # UVE control-nodes objects
    def get_uve_control_node(self, control_node=None):
        uri = 'control-nodes'
        if control_node:
            uri = uri[:-1] + '/{}'.format(control_node)
        return self.get_uves(uri)

    def get_uves_control_nodes(self):
        return self.get_uve_control_node()

    def get_ControlNode(self, control_node):
        data = self.get_uve_control_node(control_node)
        return ControlNode(data)

    # UVE tags objects
    def get_uve_tag(self, tag=None):
        uri = 'tags'
        if tag:
            uri = uri[:-1] + '/{}'.format(tag)
        return self.get_uves(uri)

    def get_uves_tags(self):
        return self.get_uve_tag()

    # UVE virtual-machines objects
    def get_uve_virtual_machine(self, virtual_machine=None):
        uri = 'virtual-machines'
        if virtual_machine:
            uri = uri[:-1] + '/{}'.format(virtual_machine)
        return self.get_uves(uri)

    def get_uves_virtual_machines(self):
        return self.get_uve_virtual_machine()

    # UVE user-defined-log-statistics objects
    def get_uve_user_defined_log_statistic(self,
                                           user_defined_log_statistic=None):
        uri = 'user-defined-log-statistics'
        if user_defined_log_statistic:
            uri = uri[:-1] + '/{}'.format(user_defined_log_statistic)
        return self.get_uves(uri)

    def get_uves_user_defined_log_statistics(self):
        return self.get_uve_user_defined_log_statistic()

    # UVE servers objects
    def get_uve_server(self, server=None):
        uri = 'servers'
        if server:
            uri = uri[:-1] + '/{}'.format(server)
        return self.get_uves(uri)

    def get_uves_servers(self):
        return self.get_uve_server()

    # UVE firewall-rules objects
    def get_uve_firewall_rule(self, firewall_rule=None):
        uri = 'firewall-rules'
        if firewall_rule:
            uri = uri[:-1] + '/{}'.format(firewall_rule)
        return self.get_uves(uri)

    def get_uves_firewall_rules(self):
        return self.get_uve_firewall_rule()

    # UVE storage-disks objects
    def get_uve_storage_disk(self, storage_disk=None):
        uri = 'storage-disks'
        if storage_disk:
            uri = uri[:-1] + '/{}'.format(storage_disk)
        return self.get_uves(uri)

    def get_uves_storage_disks(self):
        return self.get_uve_storage_disk()

    # UVE service-chains objects
    def get_uve_service_chain(self, service_chain=None):
        uri = 'service-chains'
        if service_chain:
            uri = uri[:-1] + '/{}'.format(service_chain)
        return self.get_uves(uri)

    def get_uves_service_chains(self):
        return self.get_uve_service_chain()

    # UVE config-nodes objects
    def get_uve_config_node(self, config_node=None):
        uri = 'config-nodes'
        if config_node:
            uri = uri[:-1] + '/{}'.format(config_node)
        return self.get_uves(uri)

    def get_uves_config_nodes(self):
        return self.get_uve_config_node()

    def get_ConfigNode(self, config_node):
        data = self.get_uve_config_node(config_node)
        return ConfigNode(data)

    # UVE generators objects
    def get_uve_generator(self, generator=None):
        uri = 'generators'
        if generator:
            uri = uri[:-1] + '/{}'.format(generator)
        return self.get_uves(uri)

    def get_uves_generators(self):
        return self.get_uve_generator()

    # UVE bgp-peers objects
    def get_uve_bgp_peer(self, bgp_peer=None):
        uri = 'bgp-peers'
        if bgp_peer:
            uri = uri[:-1]+'/{}'.format(bgp_peer)
        return self.get_uves(uri)

    def get_uves_bgp_peers(self):
        return self.get_uve_bgp_peer()

    def get_BgpPeer(self, bgp_peer):
        data = self.get_uve_bgp_peer(bgp_peer)
        return BgpPeer(data)

    # UVE database-nodes objects
    def get_uve_database_node(self, database_node=None):
        uri = 'database-nodes'
        if database_node:
            uri = uri[:-1]+'/{}'.format(database_node)
        return self.get_uves(uri)

    def get_uves_database_nodes(self):
        return self.get_uve_database_node()

    def get_DatabaseNode(self, database_node):
        data = self.get_uve_database_node(database_node)
        return DatabaseNode(data)

    # UVE virtual-machine-interfaces objects
    def get_uve_virtual_machine_interface(self,
                                          virtual_machine_interface=None):
        uri = 'virtual-machine-interfaces'
        if virtual_machine_interface:
            uri = uri[:-1]+'/{}'.format(virtual_machine_interface)
        return self.get_uves(uri)

    def get_uves_virtual_machine_interfaces(self):
        return self.get_uve_virtual_machine_interface()

    # UVE firewall-policys objects - omg, policYs !
    def get_uve_firewall_policy(self, firewall_policy=None):
        uri = 'firewall-policys'
        if firewall_policy:
            uri = uri[:-1]+'/{}'.format(firewall_policy)
        return self.get_uves(uri)

    def get_uves_firewall_policys(self):
        return self.get_uve_firewall_policy()

    # UVE service-groups objects
    def get_uve_service_group(self, service_group=None):
        uri = 'service-groups'
        if service_group:
            uri = uri[:-1]+'/{}'.format(service_group)
        return self.get_uves(uri)

    def get_uves_service_groups(self):
        return self.get_uve_service_group()

    # UVE virtual-networks objects
    def get_uve_virtual_network(self, virtual_network=None):
        uri = 'virtual-networks'
        if virtual_network:
            uri = uri[:-1]+'/{}'.format(virtual_network)
        return self.get_uves(uri)

    def get_uves_virtual_networks(self):
        return self.get_uve_virtual_network()

    # UVE projects objects
    def get_uve_project(self, project=None):
        uri = 'projects'
        if project:
            uri = uri[:-1]+'/{}'.format(project)
        return self.get_uves(uri)

    def get_uves_projects(self):
        return self.get_uve_project()

    # UVE prouters objects
    def get_uve_prouter(self, prouter=None):
        uri = 'prouters'
        if prouter:
            uri = uri[:-1]+'/{}'.format(prouter)
        return self.get_uves(uri)

    def get_uves_prouters(self):
        return self.get_uve_prouter()

    # UVE logical-interfaces objects
    def get_uve_logical_interface(self, logical_interface=None):
        uri = 'logical-interfaces'
        if logical_interface:
            uri = uri[:-1]+'/{}'.format(logical_interface)
        return self.get_uves(uri)

    def get_uves_logical_interfaces(self):
        return self.get_uve_logical_interface()

    # UVE dns-nodes objects
    def get_uve_dns_node(self, dns_node=None):
        uri = 'dns-nodes'
        if dns_node:
            uri = uri[:-1]+'/{}'.format(dns_node)
        return self.get_uves(uri)

    def get_uves_dns_nodes(self):
        return self.get_uve_dns_node()

    # UVE vrouters objects
    def get_uve_vrouter(self, vrouter=None):
        uri = 'vrouters'
        if vrouter:
            uri = uri[:-1]+'/{}'.format(vrouter)
        return self.get_uves(uri)

    def get_uves_vrouters(self):
        return self.get_uve_vrouter()

    # UVE address-groups objects
    def get_uve_address_group(self, address_group=None):
        uri = 'address-groups'
        if address_group:
            uri = uri[:-1]+'/{}'.format(address_group)
        return self.get_uves(uri)

    def get_uves_address_groups(self):
        return self.get_uve_address_group()

    # UVE application-policy-sets objects
    def get_uve_application_policy_set(self, application_policy_set=None):
        uri = 'application-policy-sets'
        if application_policy_set:
            uri = uri[:-1]+'/{}'.format(application_policy_set)
        return self.get_uves(uri)

    def get_uves_application_policy_sets(self):
        return self.get_uve_application_policy_set()

    # UVE storage-osds objects
    def get_uve_storage_osd(self, storage_osd=None):
        uri = 'storage-osds'
        if storage_osd:
            uri = uri[:-1]+'/{}'.format(storage_osd)
        return self.get_uves(uri)

    def get_uves_storage_osds(self):
        return self.get_uve_storage_osd()

    # UVE routing-instances objects
    def get_uve_routing_instance(self, routing_instance=None):
        uri = 'routing-instances'
        if routing_instance:
            uri = uri[:-1]+'/{}'.format(routing_instance)
        return self.get_uves(uri)

    def get_uves_routing_instances(self):
        return self.get_uve_routing_instance()

    # UVE physical-interfaces objects
    def get_uve_physical_interface(self, physical_interface=None):
        uri = 'physical-interfaces'
        if physical_interface:
            uri = uri[:-1]+'/{}'.format(physical_interface)
        return self.get_uves(uri)

    def get_uves_physical_interfaces(self):
        return self.get_uve_physical_interface()

    # UVE kubernetes-manager-nodes objects
    def get_uve_kubernetes_manager_node(self, kubernetes_manager_node=None):
        uri = 'kubernetes-manager-nodes'
        if kubernetes_manager_node:
            uri = uri[:-1]+'/{}'.format(kubernetes_manager_node)
        return self.get_uves(uri)

    def get_uves_kubernetes_manager_nodes(self):
        return self.get_uve_kubernetes_manager_node()

    # UVE loadbalancers objects
    def get_uve_loadbalancer(self, loadbalancer=None):
        uri = 'loadbalancers'
        if loadbalancer:
            uri = uri[:-1]+'/{}'.format(loadbalancer)
        return self.get_uves(uri)

    def get_uves_loadbalancers(self):
        return self.get_uve_loadbalancer()


class AnalyticNode(IntrospectData):
    def __init__(self, obj):
        super(AnalyticNode, self).__init__(obj)
        self.NodeStatus = \
            self._wrap_in_list(NodeStatus, self.obj['NodeStatus'])


class ControlNode(IntrospectData):
    def __init__(self, obj):
        super(ControlNode, self).__init__(obj)
        self.NodeStatus = \
            self._wrap_in_list(NodeStatus, self.obj['NodeStatus'])


class ConfigNode(IntrospectData):
    def __init__(self, obj):
        super(ConfigNode, self).__init__(obj)
        self.NodeStatus = \
            self._wrap_in_list(NodeStatus, self.obj['NodeStatus'])


class DatabaseNode(IntrospectData):
    def __init__(self, obj):
        super(DatabaseNode, self).__init__(obj)
        self.NodeStatus = \
            self._wrap_in_list(NodeStatus, self.obj['NodeStatus'])


class BgpPeer(IntrospectData):
    def __init__(self, obj):
        super(BgpPeer, self).__init__(obj)
        self.BgpPeerInfoData = BgpPeerInfoData(self.obj['BgpPeerInfoData'])


class XmppPeer(IntrospectData):
    def __init__(self, obj):
        super(XmppPeer, self).__init__(obj)
        self.XmppPeerInfoData = XmppPeerInfoData(self.obj['XmppPeerInfoData'])
