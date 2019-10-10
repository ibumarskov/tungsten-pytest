import itertools
import logging
import pytest

from tungsten_tests.helpers.analytic_data import BgpPeerInfoData, \
    XmppPeerInfoData, NodeStatus

logger = logging.getLogger()


@pytest.mark.smoke
class TestDeployment(object):
    """Check that all services are deployed and configured properly."""

    @pytest.fixture(params=["alarm-gen", "api", "collector", "query-engine",
                            "snmp", "topology"])
    def tf_analytic_services(self, request):
        service = request.param
        yield service

    def test_tf_analytic_operator(self, k8s_client, tf_analytic_services):
        """Check Tungsten operator deploys analytics alarm-gen service"""
        tf_operator = k8s_client.get_tf_operator()
        tf_analytic = k8s_client.get_tf_analytic()

        # Check owner
        owner = tf_analytic['metadata']['ownerReferences'][0]['name']
        if not owner == k8s_client.TFOperator['name']:
            raise Exception("Owner of TFAnalytic operator mismatch: {} != {}"
                            "".format(owner, k8s_client.TFOperator['name']))

        # Check specs
        service = tf_analytic_services
        name = k8s_client.TFAnalytic['name']
        analytic_spec = tf_operator['spec'][name]
        if analytic_spec[service].viewitems() >= \
                tf_analytic['spec'][service].viewitems():
            raise Exception("Some specs were't translated from TFOperator to "
                            "TFAnalytic\n TFOperator specs:\n{}\n TFAnalytic "
                            "specs:\n{}\n"
                            "".format(analytic_spec[service],
                                      tf_analytic['spec'][service]))

        # Check deployment replica
        deployment = k8s_client.get_namespaced_deployment(
            name + '-' + service)
        if deployment.spec.replicas != analytic_spec[service]['replicas']:
            raise Exception("Deployment {} has incorrect replica number: {}\n"
                            "Operator spec replica number: {}"
                            "".format(deployment['metadata']['name'],
                                      deployment.spec.replicas,
                                      analytic_spec['replicas'])
                            )

        # TO DO: check service inside container

    @pytest.fixture(params=["api", "devicemgr", "schema", "svc-monitor"])
    def tf_config_services(self, request):
        service = request.param
        yield service

    def test_tf_config_operator(self, k8s_client, tf_config_services):
        """Check Tungsten operator deploys config related services"""
        tf_operator = k8s_client.get_tf_operator()
        tf_config = k8s_client.get_tf_config()

        # Check owner
        owner = tf_config['metadata']['ownerReferences'][0]['name']
        if not owner == k8s_client.TFOperator['name']:
            raise Exception("Owner of TFConfig operator mismatch: {} != {}"
                            "".format(owner, k8s_client.TFOperator['name']))

        # Check specs
        service = tf_config_services
        name = k8s_client.TFConfig['name']
        config_spec = tf_operator['spec'][name]
        if config_spec[service].viewitems() >= \
                tf_config['spec'][service].viewitems():
            raise Exception("Some specs were't translated from TFOperator to "
                            "TFConfig\n TFOperator specs:\n{}\n TFConfig "
                            "specs:\n{}\n"
                            "".format(config_spec[service],
                                      tf_config['spec'][service]))

        # Check deployment replica
        deployment = k8s_client.get_namespaced_deployment(
            name + '-' + service)
        if deployment.spec.replicas != config_spec[service]['replicas']:
            raise Exception("Deployment {} has incorrect replica number: {}\n"
                            "Operator spec replica number: {}"
                            "".format(deployment['metadata']['name'],
                                      deployment.spec.replicas,
                                      config_spec['replicas'])
                            )

        # TO DO: check service inside container

    @pytest.fixture(params=["control", "named", "dns"])
    def tf_control_services(self, request):
        service = request.param
        yield service

    def test_tf_control_operator(self, k8s_client, tf_control_services):
        """Check Tungsten operator deploys config related services"""
        tf_operator = k8s_client.get_tf_operator()
        tf_control = k8s_client.get_tf_control()

        # Check owner
        owner = tf_control['metadata']['ownerReferences'][0]['name']
        if not owner == k8s_client.TFOperator['name']:
            raise Exception("Owner of TFConfig operator mismatch: {} != {}"
                            "".format(owner, k8s_client.TFOperator['name']))

        # Check specs
        service = tf_control_services
        name = k8s_client.TFControl['name']
        config_spec = tf_operator['spec'][name]
        if config_spec[service].viewitems() >= \
                tf_control['spec'][service].viewitems():
            raise Exception("Some specs were't translated from TFOperator to "
                            "TFControl\n TFOperator specs:\n{}\n TFControl "
                            "specs:\n{}\n"
                            "".format(config_spec[service],
                                      tf_control['spec'][service]))

        # Check deployment replica
        deployment = k8s_client.get_namespaced_deployment(
            name + '-' + service)
        if deployment.spec.replicas != config_spec[service]['replicas']:
            raise Exception("Deployment {} has incorrect replica number: {}\n"
                            "Operator spec replica number: {}"
                            "".format(deployment['metadata']['name'],
                                      deployment.spec.replicas,
                                      config_spec['replicas'])
                            )

        # TO DO: check service inside container

    @pytest.fixture(params=["agent"])
    def tf_vrouter_services(self, request):
        service = request.param
        yield service

    def test_tf_vrouter_operator(self, k8s_client, tf_vrouter_services):
        """Check Tungsten operator deploys config related services"""
        tf_operator = k8s_client.get_tf_operator()
        tf_vrouter = k8s_client.get_tf_vrouter()

        # Check owner
        owner = tf_vrouter['metadata']['ownerReferences'][0]['name']
        if not owner == k8s_client.TFOperator['name']:
            raise Exception("Owner of TFConfig operator mismatch: {} != {}"
                            "".format(owner, k8s_client.TFOperator['name']))

        # Check specs
        service = tf_vrouter_services
        name = k8s_client.TFVrouter['name']
        config_spec = tf_operator['spec'][name]
        if config_spec[service].viewitems() >= \
                tf_vrouter['spec'][service].viewitems():
            raise Exception("Some specs were't translated from TFOperator to "
                            "TFVrouter\n TFOperator specs:\n{}\n TFVrouter "
                            "specs:\n{}\n"
                            "".format(config_spec[service],
                                      tf_vrouter['spec'][service]))

        # Check deployment replica
        deployment = k8s_client.get_namespaced_deployment(
            name + '-' + service)
        if deployment.spec.replicas != config_spec[service]['replicas']:
            raise Exception("Deployment {} has incorrect replica number: {}\n"
                            "Operator spec replica number: {}"
                            "".format(deployment['metadata']['name'],
                                      deployment.spec.replicas,
                                      config_spec['replicas'])
                            )

        # TO DO: check service inside container

    def test_bgp_peering_control_nodes(self, tf_analytic):
        """Check bgp peering between all control nodes."""
        bgp_peers = tf_analytic.get_uves_bgp_peers()
        # TO DO: get list of NTW nodes from tungsten operator
        ntw_nodes = ['ntw01', 'ntw02', 'ntw03']
        msg = "Check BGP peering {}, State: {}"
        errors = []
        for c in itertools.combinations(ntw_nodes, 2):
            conn = False
            for peer_name in map(lambda x: x['name'], bgp_peers):
                if c[0] in peer_name and c[1] in peer_name:
                    peer = tf_analytic.get_uve_bgp_peer(peer_name)
                    data = BgpPeerInfoData(peer)
                    state = data.state_info
                    conn = True
                    print(msg.format(c, state))
                    if not state == 'Established':
                        errors.append(msg.format(c, state))
                    break
            if conn is False:
                print(msg.format(c, "Unknown"))
                errors.append(msg.format(c, "Unknown"))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some BGP peering sessions are failed"

    def test_xmpp_peering_vrouters(self, tf_analytic):
        """Check xmpp peering between vrouters (compute nodes)."""
        xmpp_peers = tf_analytic.get_uves_xmpp_peers()
        # TO DO: get list of NTW nodes from tungsten operator
        ntw_nodes = ['ntw01', 'ntw02', 'ntw03']
        # TO DO: get list of CMP nodes or vrouter pods from tungsten operator
        cmp_nodes_ip = ['10.11.1.1', '10.11.1.2']
        msg = "Check XMPP peering {}, State: {}"
        errors = []
        for c in itertools.product(ntw_nodes, cmp_nodes_ip):
            conn = False
            for peer_name in map(lambda x: x['name'], xmpp_peers):
                if c[0] in peer_name and c[1] in peer_name:
                    peer = tf_analytic.get_uve_xmpp_peer(peer_name)
                    data = XmppPeerInfoData(peer)
                    state = data.state_info
                    conn = True
                    print(msg.format(c, state))
                    if not state == 'Established':
                        errors.append(msg.format(c, state))
                    break
            if conn is False:
                print(msg.format(c, "Unknown"))
                errors.append(msg.format(c, "Unknown"))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some XMPP peering sessions are failed"

    def test_list_analytics_nodes(self, tf_analytic):
        """Check amount of analytic nodes."""
        # TO DO: get list of Analytic nodes from tungsten operator
        env_nodes = ['nal01', 'nal02', 'nal03']
        tf_nodes = map(lambda n: n['name'],
                       tf_analytic.get_uves_analytics_nodes())
        errors = []
        for node in env_nodes:
            if node not in tf_nodes:
                errors.append("Analytic node {} not found".format(node))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some analytic nodes not found"

    def test_list_config_nodes(self, tf_analytic):
        """Check amount of config nodes."""
        # TO DO: get list of Config nodes from tungsten operator
        env_nodes = ['ntw01', 'ntw02', 'ntw03']
        tf_nodes = map(lambda n: n['name'],
                       tf_analytic.get_uves_config_nodes())
        errors = []
        for node in env_nodes:
            if node not in tf_nodes:
                errors.append("Config node {} not found".format(node))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some config nodes not found"

    def test_list_database_nodes(self, tf_analytic):
        """Check amount of database nodes."""
        # TO DO: get list of Database nodes from tungsten operator
        env_nodes = ['nal01', 'nal02', 'nal03', 'ntw01', 'ntw02', 'ntw03']
        tf_nodes = map(lambda n: n['name'],
                       tf_analytic.get_uves_database_nodes())
        errors = []
        for node in env_nodes:
            if node not in tf_nodes:
                errors.append("Database node {} not found".format(node))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some database nodes not found"

    def test_status_analytics_nodes(self, tf_analytic):
        """Check status of analytic nodes."""
        # TO DO: get list of Analytics nodes from tungsten operator
        env_nodes = ['nal01', 'nal02', 'nal03']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        for node in env_nodes:
            nal_node = tf_analytic.get_uve_analytics_node(node)
            data = NodeStatus(nal_node)
            for process in data.get_process_status:
                module_id = NodeStatus.module_id(process)
                state = NodeStatus.state(process)
                print(msg.format(node, module_id, state))
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some services are failed"

    def test_status_config_nodes(self, tf_analytic):
        """Check status of config nodes."""
        # TO DO: get list of Config nodes from tungsten operator
        env_nodes = ['ntw01', 'ntw02', 'ntw03']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        for node in env_nodes:
            conf_node = tf_analytic.get_uve_config_node(node)
            data = NodeStatus(conf_node)
            for process in data.get_process_status:
                module_id = NodeStatus.module_id(process)
                state = NodeStatus.state(process)
                print(msg.format(node, module_id, state))
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some services are failed"

    def test_status_database_nodes(self, tf_analytic):
        """Check status of database nodes."""
        # TO DO: get list of Database nodes from tungsten operator
        env_nodes = ['nal01', 'nal02', 'nal03', 'ntw01', 'ntw02', 'ntw03']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        for node in env_nodes:
            db_node = tf_analytic.get_uve_database_node(node)
            data = NodeStatus(db_node)
            for process in data.get_process_status:
                module_id = NodeStatus.module_id(process)
                state = NodeStatus.state(process)
                print(msg.format(node, module_id, state))
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some services are failed"
