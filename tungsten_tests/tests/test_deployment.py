import itertools
import logging

from tungsten_tests.helpers.analytic_data import BgpPeerInfoData, \
    XmppPeerInfoData, NodeStatus

logger = logging.getLogger()


class TestEnvironment(object):

    def test_osdpl(self, k8s_client):
        osdpl = k8s_client.get_osdpl()
        assert osdpl['metadata']['name'] == 'osh-dev'

    def test_bgp_peering_control_nodes(self, tf_analytic):
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
                print msg.format(node, module_id, state)
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some services are failed"

    def test_status_config_nodes(self, tf_analytic):
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
                print msg.format(node, module_id, state)
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some services are failed"

    def test_status_database_nodes(self, tf_analytic):
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
                print msg.format(node, module_id, state)
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some services are failed"
