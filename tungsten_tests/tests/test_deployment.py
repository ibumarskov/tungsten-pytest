import itertools
import logging
import pytest

from tungsten_tests.clients.tungsten.introspect_client import IntrospectClient

logger = logging.getLogger()


@pytest.mark.smoke
class TestDeployment(object):
    """Check that all services are deployed and configured properly."""

    @pytest.fixture(params=["api", "collector", "nodemgr",
                            "alarm-gen", "alarmnodemgr",
                            "query-engine", "dbnodemgr",
                            "snmp", "topology", "snmpnodemgr"])
    def tf_analytic_services(self, request):
        service = request.param
        yield service

    def test_tf_analytic_cr_specs(self, tf_analytic_services, k8s_tf_operator,
                                  k8s_tf_analytic):
        """Verify TFAnalytic CR's specs"""

        # Check owner
        owner = k8s_tf_analytic.obj['metadata']['ownerReferences'][0]['name']
        if owner != k8s_tf_operator.name:
            raise Exception("Owner of TFAnalytic operator mismatch: {} != {}"
                            "".format(owner, k8s_tf_operator.name))

        # Check specs of Analytic CR
        service = tf_analytic_services
        name = k8s_tf_analytic.name
        tfop_analytic_spec = k8s_tf_operator.obj['spec'][name]
        if service not in k8s_tf_analytic.obj['spec']:
            raise Exception(
                "Spec for {} service was't found in TFAnalytic CR.".format(
                    service))
        if service not in tfop_analytic_spec:
            pytest.skip("Specs for {} service isn't defined (default values "
                        "are used).".format(name))
        if tfop_analytic_spec[service].viewitems() >= \
                k8s_tf_analytic.obj['spec'][service].viewitems():
            raise Exception("Some specs were't translated from TFOperator to "
                            "TFAnalytic\n TFOperator specs:\n{}\n TFAnalytic "
                            "specs:\n{}\n"
                            "".format(tfop_analytic_spec[service],
                                      k8s_tf_analytic.obj['spec'][service]))

    def test_tf_analytic_ds_specs(self, tf_analytic_services, k8s_client,
                                  k8s_tf_analytic):
        """Verify Daemon Set specs of TFAnalytic controller"""

        # Check deployment set image
        service = tf_analytic_services
        name = k8s_tf_analytic.name
        if service in ["api", "collector", "nodemgr"]:
            ds_name = name
        elif service in ["alarm-gen", "alarmnodemgr"]:
            ds_name = name + '-alarm'
        elif service in ["query-engine", "dbnodemgr"]:
            ds_name = name + '-database'
        elif service in ["snmp", "topology", "snmpnodemgr"]:
            ds_name = name + '-snmp'
        else:
            ds_name = name + '-' + service

        ds = k8s_client.AppsV1Api.read_namespaced_daemon_set(
            ds_name, k8s_tf_analytic.namespace)

        image = None
        for c in ds.spec.template.spec.containers:
            if c.name == service:
                image = c.image
                break

        analytic_srv_spec = k8s_tf_analytic.obj['spec'][service]
        spec_image = analytic_srv_spec['containers'][0]['image']
        if image != spec_image:
            raise Exception("Deployment set {} has incorrect image: {}\n"
                            "Operator spec image: {}"
                            "".format(ds['metadata']['name'],
                                      image,
                                      spec_image))

    @pytest.fixture(params=["api", "devicemgr", "svc-monitor", "schema",
                            "nodemgr"])
    def tf_config_services(self, request):
        service = request.param
        yield service

    def test_tf_config_cr_specs(self, tf_config_services, k8s_tf_operator,
                                k8s_tf_config):
        """"Verify TFConfig CR's specs"""

        # Check owner
        owner = k8s_tf_config.obj['metadata']['ownerReferences'][0]['name']
        if owner != k8s_tf_operator.name:
            raise Exception("Owner of TFConfig operator mismatch: {} != {}"
                            "".format(owner, k8s_tf_operator.name))

        # Check specs of Analytic CR
        service = tf_config_services
        name = k8s_tf_config.name
        tfop_config_spec = k8s_tf_operator.obj['spec'][name]
        if service not in k8s_tf_config.obj['spec']:
            raise Exception(
                "Spec for {} service was't found in TFConfig CR.".format(
                    service))
        if service not in tfop_config_spec:
            pytest.skip("Specs for {} service isn't defined (default values "
                        "are used).".format(name))
        if tfop_config_spec[service].viewitems() >= \
                k8s_tf_config.obj['spec'][service].viewitems():
            raise Exception("Some specs were't translated from TFOperator to "
                            "TFConfig\n TFOperator specs:\n{}\n TFConfig "
                            "specs:\n{}\n"
                            "".format(tfop_config_spec[service],
                                      k8s_tf_config.obj['spec'][service]))

    def test_tf_config_ds_specs(self, tf_config_services, k8s_client,
                                k8s_tf_config):
        """Verify Daemon Set specs of TFConfig controller"""

        # Check deployment set image
        services = [tf_config_services]
        name = k8s_tf_config.name
        ds_name = name

        ds = k8s_client.AppsV1Api.read_namespaced_daemon_set(
            ds_name, k8s_tf_config.namespace)

        for service in services:
            image = None
            for c in ds.spec.template.spec.containers:
                if c.name == service:
                    image = c.image
                    break

            config_srv_spec = k8s_tf_config.obj['spec'][tf_config_services]
            spec_image = None
            for c in config_srv_spec['containers']:
                if c['name'] == service:
                    spec_image = c['image']
                    break
            if image != spec_image or image is None:
                raise Exception("Deployment set {} has incorrect image: {}\n"
                                "Operator spec image: {}"
                                "".format(ds['metadata']['name'],
                                          image,
                                          spec_image))

    @pytest.fixture(params=["control", "dns", "nodemgr"])
    def tf_control_services(self, request):
        service = request.param
        yield service

    def test_tf_control_cr_specs(self, tf_control_services, k8s_tf_operator,
                                 k8s_tf_control):
        """Verify TFControl CR's specs"""

        # Check owner
        owner = k8s_tf_control.obj['metadata']['ownerReferences'][0]['name']
        if owner != k8s_tf_operator.name:
            raise Exception("Owner of TFConfig operator mismatch: {} != {}"
                            "".format(owner, k8s_tf_operator.name))

        # Check specs of TFControl
        service = tf_control_services
        name = k8s_tf_control.name
        tfop_control_spec = k8s_tf_operator.obj['spec'][name]
        if service not in k8s_tf_control.obj['spec']:
            raise Exception(
                "Spec for {} service was't found in TFControl CR.".format(
                    service))
        if service not in tfop_control_spec:
            pytest.skip("Specs for {} service isn't defined (default values "
                        "are used).".format(name))
        if tfop_control_spec[service].viewitems() >= \
                k8s_tf_control.obj['spec'][service].viewitems():
            raise Exception("Some specs were't translated from TFOperator to "
                            "TFControl\n TFOperator specs:\n{}\n TFControl "
                            "specs:\n{}\n"
                            "".format(tfop_control_spec[service],
                                      k8s_tf_control.obj['spec'][service]))

    def test_tf_control_ds_specs(self, tf_control_services, k8s_client,
                                 k8s_tf_control):
        """Verify Daemon Set specs of TFControl controller"""

        # Check deployment set image
        if tf_control_services == 'dns':
            services = ["dns", "named"]
        else:
            services = [tf_control_services]
        name = k8s_tf_control.name
        ds_name = name

        ds = k8s_client.AppsV1Api.read_namespaced_daemon_set(
            ds_name, k8s_tf_control.namespace)

        for service in services:
            image = None
            for c in ds.spec.template.spec.containers:
                if c.name == service:
                    image = c.image
                    break

            control_srv_spec = k8s_tf_control.obj['spec'][tf_control_services]
            spec_image = None
            for c in control_srv_spec['containers']:
                if c['name'] == service:
                    spec_image = c['image']
                    break
            if image != spec_image or image is None:
                raise Exception("Deployment set {} has incorrect image: {}\n"
                                "Operator spec image: {}"
                                "".format(ds['metadata']['name'],
                                          image,
                                          spec_image))

    @pytest.fixture(params=["agent", "nodemgr"])
    def tf_vrouter_services(self, request):
        service = request.param
        yield service

    def test_tf_vrouter_cr_specs(self, tf_vrouter_services, k8s_tf_operator,
                                 k8s_tf_vrouter):
        """Verify TFVrouter CR's specs"""

        # Check owner
        owner = k8s_tf_vrouter.obj['metadata']['ownerReferences'][0]['name']
        if owner != k8s_tf_operator.name:
            raise Exception("Owner of TFConfig operator mismatch: {} != {}"
                            "".format(owner, k8s_tf_operator.name))

        # Check specs of TFVrouter
        service = tf_vrouter_services
        name = k8s_tf_vrouter.name
        tfop_vrouter_spec = k8s_tf_operator.obj['spec'][name]
        if service not in k8s_tf_vrouter.obj['spec']:
            raise Exception(
                "Spec for {} service was't found in TFVrouter CR.".format(
                    service))
        if service not in tfop_vrouter_spec:
            pytest.skip("Specs for {} service isn't defined (default values "
                        "are used).".format(name))
        if tfop_vrouter_spec[service].viewitems() >= \
                k8s_tf_vrouter.obj['spec'][service].viewitems():
            raise Exception("Some specs were't translated from TFOperator to "
                            "TFVrouter\n TFOperator specs:\n{}\n TFVrouter "
                            "specs:\n{}\n"
                            "".format(tfop_vrouter_spec[service],
                                      k8s_tf_vrouter.obj['spec'][service]))

    def test_tf_vrouter_ds_specs(self, tf_vrouter_services, k8s_client,
                                 k8s_tf_vrouter):
        """Verify Daemon Set specs of TFVrouter controller"""

        # Check deployment set image
        services = [tf_vrouter_services]
        name = k8s_tf_vrouter.name
        ds_name = name + "-agent"

        ds = k8s_client.AppsV1Api.read_namespaced_daemon_set(
            ds_name, k8s_tf_vrouter.namespace)

        for service in services:
            image = None
            for c in ds.spec.template.spec.containers:
                if c.name == service:
                    image = c.image
                    break

            vrouter_srv_spec = k8s_tf_vrouter.obj['spec'][tf_vrouter_services]
            spec_image = None
            for c in vrouter_srv_spec['containers']:
                if c['name'] == service:
                    spec_image = c['image']
                    break
            if image != spec_image or image is None:
                raise Exception("Deployment set {} has incorrect image: {}\n"
                                "Operator spec image: {}"
                                "".format(ds['metadata']['name'],
                                          image,
                                          spec_image))

    @pytest.fixture(params=["job", "web"])
    def tf_webui_services(self, request):
        service = request.param
        yield service

    def test_tf_webui_cr_specs(self, tf_webui_services, k8s_tf_operator,
                               k8s_tf_webui):
        """Verify TFWebUI CR's specs"""

        # Check owner
        owner = k8s_tf_webui.obj['metadata']['ownerReferences'][0]['name']
        if owner != k8s_tf_operator.name:
            raise Exception("Owner of TFConfig operator mismatch: {} != {}"
                            "".format(owner, k8s_tf_operator.name))

        # Check specs of TFWebUI
        service = tf_webui_services
        name = k8s_tf_webui.name
        tfop_vrouter_spec = k8s_tf_operator.obj['spec'][name]
        if service not in k8s_tf_webui.obj['spec']:
            raise Exception(
                "Spec for {} service was't found in TFWebUI CR.".format(
                    service))
        if service not in tfop_vrouter_spec:
            pytest.skip("Specs for {} service isn't defined (default values "
                        "are used).".format(name))
        if tfop_vrouter_spec[service].viewitems() >= \
                k8s_tf_webui.obj['spec'][service].viewitems():
            raise Exception("Some specs were't translated from TFOperator to "
                            "TFWebUI\n TFOperator specs:\n{}\n TFWebUI "
                            "specs:\n{}\n"
                            "".format(tfop_vrouter_spec[service],
                                      k8s_tf_webui.obj['spec'][service]))

    def test_tf_webui_ds_specs(self, tf_webui_services, k8s_client,
                               k8s_tf_webui):
        """Verify Daemon Set specs of TFWebUI controller"""

        # Check deployment set image
        services = [tf_webui_services]
        name = k8s_tf_webui.name
        ds_name = name

        ds = k8s_client.AppsV1Api.read_namespaced_daemon_set(
            ds_name, k8s_tf_webui.namespace)

        for service in services:
            image = None
            for c in ds.spec.template.spec.containers:
                if c.name == service:
                    image = c.image
                    break

            webui_srv_spec = k8s_tf_webui.obj['spec'][tf_webui_services]
            spec_image = None
            for c in webui_srv_spec['containers']:
                if c['name'] == service:
                    spec_image = c['image']
                    break
            if image != spec_image or image is None:
                raise Exception("Deployment set {} has incorrect image: {}\n"
                                "Operator spec image: {}"
                                "".format(ds['metadata']['name'],
                                          image,
                                          spec_image))

    def test_list_analytics_nodes(self, tf):
        """Verify all analytic nodes deployed by TF operator were added to
        Tungsten configuration.
        """
        # TO DO: Get list of Analytic nodes from k8s deployment
        env_nodes = ['nal01', 'nal02', 'nal03']
        # Get list of Analytic nodes from tungsten configuration
        tf_nodes = map(lambda n: n.display_name, tf.list_analytics_node)

        logger.info("k8s nodes: {}".format(env_nodes))
        logger.info("TF nodes: {}".format(tf_nodes))
        # Comparison
        node_present = True
        for node in env_nodes:
            if node not in tf_nodes:
                node_present = False
                logger.error("Analytic node {} isn't present in TF "
                             "configuration.".format(node))
        assert node_present, "Some analytic nodes weren't found"

    def test_list_config_nodes(self, tf):
        """Verify all config nodes deployed by TF operator were added to
        Tungsten configuration.
        """
        # TO DO: Get list of Config nodes from k8s deployment
        env_nodes = ['ntw01', 'ntw02', 'ntw03']
        # Get list of Analytic nodes from tungsten configuration
        tf_nodes = map(lambda n: n.display_name, tf.list_config_node)

        logger.info("k8s nodes: {}".format(env_nodes))
        logger.info("TF nodes: {}".format(tf_nodes))
        # Comparison
        node_present = True
        for node in env_nodes:
            if node not in tf_nodes:
                node_present = False
                logger.error("Config node {} isn't present in TF "
                             "configuration.".format(node))
        assert node_present, "Some config nodes weren't found"

    def test_list_database_nodes(self, tf):
        """Verify all config nodes deployed by TF operator were added to
        Tungsten configuration.
        """
        # TO DO: Get list of Database nodes from k8s deployment
        env_nodes = ['nal01', 'nal02', 'nal03', 'ntw01', 'ntw02', 'ntw03']
        # Get list of Database nodes from tungsten configuration
        tf_nodes = map(lambda n: n.display_name, tf.list_database_node)

        logger.info("k8s nodes: {}".format(env_nodes))
        logger.info("TF nodes: {}".format(tf_nodes))
        # Comparison
        node_present = True
        for node in env_nodes:
            if node not in tf_nodes:
                node_present = False
                logger.error("Database node {} isn't present in TF "
                             "configuration.".format(node))
        assert node_present, "Some database nodes weren't found"

    def test_list_vrouter_nodes(self, tf):
        """Verify all vrouter nodes deployed by TF operator were added to
        Tungsten configuration.
        """
        # TO DO: Get list of Database nodes from k8s deployment
        env_nodes = ['cmp1', 'cmp2']
        # Get list of Database nodes from tungsten configuration
        tf_nodes = map(lambda n: n.display_name, tf.list_vrouter_router)

        logger.info("k8s nodes: {}".format(env_nodes))
        logger.info("TF nodes: {}".format(tf_nodes))
        # Comparison
        node_present = True
        for node in env_nodes:
            if node not in tf_nodes:
                node_present = False
                logger.error("vRouter (compute) node {} isn't present in TF "
                             "configuration.".format(node))
        assert node_present, "Some vRouter nodes weren't found"

    def test_introspect_analytic_services(self, config, tf_analytic_services):
        """Verify status of analytics services via introspect."""
        # TO DO: get list of Control nodes from tungsten operator
        env_nodes = ['10.11.0.227']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        port = config.tf_analytic_srv_ports[tf_analytic_services]
        for node in env_nodes:
            ic = IntrospectClient(ip=node, port=port)
            ns = ic.get_NodeStatusUVEList()
            state = ns.NodeStatusUVE[0].NodeStatus[0].ProcessStatus[0].state
            module_id = \
                ns.NodeStatusUVE[0].NodeStatus[0].ProcessStatus[0].module_id
            logger.info(msg.format(node, module_id, state))
            if state != "Functional":
                errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Service isn't functional"

    def test_introspect_control_services(self, config, tf_control_services):
        """Verify status of control services via introspect."""
        # TO DO: get list of Control nodes from tungsten operator
        env_nodes = ['10.11.0.224', '10.11.0.225', '10.11.0.226']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        port = config.tf_control_srv_ports[tf_control_services]
        if tf_control_services == 'named' and port is None:
            pytest.skip("Named service doesn't have an introspect.")
        for node in env_nodes:
            ic = IntrospectClient(ip=node, port=port)
            ns = ic.get_NodeStatusUVEList()
            state = ns.NodeStatusUVE[0].NodeStatus[0].ProcessStatus[0].state
            module_id = \
                ns.NodeStatusUVE[0].NodeStatus[0].ProcessStatus[0].module_id
            logger.info(msg.format(node, module_id, state))
            if state != "Functional":
                errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Service isn't functional"

    def test_introspect_config_services(self, config, tf_config_services):
        """Verify status of config services via introspect."""
        # TO DO: get list of Control nodes from tungsten operator
        env_nodes = ['10.11.0.224']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        port = config.tf_config_srv_ports[tf_config_services]
        if port is None:
            pytest.xfail("Port for introspect is Unknown.")
        for node in env_nodes:
            ic = IntrospectClient(ip=node, port=port)
            ns = ic.get_NodeStatusUVEList()
            for status_uve in ns.NodeStatusUVE:
                state = status_uve.NodeStatus[0].ProcessStatus[0].state
                module_id = \
                    status_uve.NodeStatus[0].ProcessStatus[0].module_id
                logger.info(msg.format(node, module_id, state))
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Contrail-dns service isn't functional"

    def test_introspect_vrouter_services(self, config, tf_vrouter_services):
        """Verify status of control services via introspect."""
        # TO DO: get list of Control nodes from tungsten operator
        env_nodes = ['10.11.1.1', '10.11.1.2']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        port = config.tf_control_srv_ports[tf_vrouter_services]
        for node in env_nodes:
            ic = IntrospectClient(ip=node, port=port)
            ns = ic.get_NodeStatusUVEList()
            state = ns.NodeStatusUVE[0].NodeStatus[0].ProcessStatus[0].state
            module_id = \
                ns.NodeStatusUVE[0].NodeStatus[0].ProcessStatus[0].module_id
            logger.info(msg.format(node, module_id, state))
            if state != "Functional":
                errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Service isn't functional"

    def test_status_analytics_nodes(self, tf_analytic):
        """Verify status of analytic nodes via analytic."""
        # TO DO: Get list of Analytics nodes from k8s deployment
        env_nodes = ['nal01', 'nal02', 'nal03']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        for node in env_nodes:
            data = tf_analytic.get_AnalyticNode(node)
            for process in data.NodeStatus[0].ProcessStatus:
                module_id = process.module_id
                state = process.state
                logger.info(msg.format(node, module_id, state))
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some services are failed"

    def test_status_control_nodes(self, tf_analytic):
        """Verify status of control nodes via analytic."""
        # TO DO: get list of Control nodes from tungsten operator
        env_nodes = ['ntw01', 'ntw02', 'ntw03']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        for node in env_nodes:
            data = tf_analytic.get_ControlNode(node)
            for process in data.NodeStatus[0].ProcessStatus:
                module_id = process.module_id
                state = process.state
                logger.info(msg.format(node, module_id, state))
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some services are failed"

    def test_status_config_nodes(self, tf_analytic):
        """Verify status of config nodes via analytic."""
        # TO DO: get list of Config nodes from tungsten operator
        env_nodes = ['ntw01', 'ntw02', 'ntw03']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        for node in env_nodes:
            data = tf_analytic.get_ConfigNode(node)
            for process in data.NodeStatus[0].ProcessStatus:
                module_id = process.module_id
                state = process.state
                logger.info(msg.format(node, module_id, state))
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some services are failed"

    def test_status_database_nodes(self, tf_analytic):
        """Verify status of database nodes via analytic."""
        # TO DO: get list of Database nodes from tungsten operator
        env_nodes = ['nal01', 'nal02', 'nal03', 'ntw01', 'ntw02', 'ntw03']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        for node in env_nodes:
            data = tf_analytic.get_DatabaseNode(node)
            for process in data.NodeStatus[0].ProcessStatus:
                module_id = process.module_id
                state = process.state
                logger.info(msg.format(node, module_id, state))
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some services are failed"

    def test_status_vrouter_nodes(self, tf_analytic):
        """Verify status of vrouters via analytic."""
        # TO DO: Get list of vRouter nodes from k8s deployment
        env_nodes = ['cmp1', 'cmp2']
        msg = "Node: {}, Module: {} Status: {}"
        errors = []
        for node in env_nodes:
            data = tf_analytic.get_vRouter(node)
            for process in data.NodeStatus[0].ProcessStatus:
                module_id = process.module_id
                state = process.state
                logger.info(msg.format(node, module_id, state))
                if state != "Functional":
                    errors.append(msg.format(node, module_id, state))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some services are failed"

    def test_bgp_peering_control_nodes(self, tf_analytic):
        """Verify bgp peering between all control nodes."""
        bgp_peers = tf_analytic.get_uves_bgp_peers()
        # TO DO: get list of NTW nodes from tungsten operator
        ntw_nodes = ['ntw01', 'ntw02', 'ntw03']
        msg = "Check BGP peering {}, State: {}"
        errors = []
        for c in itertools.combinations(ntw_nodes, 2):
            conn = False
            for peer_name in map(lambda x: x['name'], bgp_peers):
                if c[0] in peer_name and c[1] in peer_name:
                    bgp_peer = tf_analytic.get_BgpPeer(peer_name)
                    state = bgp_peer.BgpPeerInfoData.PeerStateInfo.state
                    conn = True
                    logger.info(msg.format(c, state))
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
        """Verify xmpp peering between vrouters (compute nodes)."""
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
                    xmpp_peer = tf_analytic.get_XmppPeer(peer_name)
                    state = xmpp_peer.XmppPeerInfoData.PeerStateInfo.state
                    conn = True
                    logger.info(msg.format(c, state))
                    if not state == 'Established':
                        errors.append(msg.format(c, state))
                    break
            if conn is False:
                print(msg.format(c, "Unknown"))
                errors.append(msg.format(c, "Unknown"))
        if len(errors) != 0:
            logger.error(errors)
            assert False, "Some XMPP peering sessions are failed"
