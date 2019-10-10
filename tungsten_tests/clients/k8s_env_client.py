from kubernetes import client, config


class K8sEnvClient:
    def __init__(self, kubeconfig, mcpconfig):
        self.config = config.load_kube_config(config_file=kubeconfig)
        self.CoreV1Api = client.CoreV1Api()
        self.AppsV1Api = client.AppsV1Api()
        self.CustomObjectsApi = client.CustomObjectsApi()

        self.osdpl = {
            'name': mcpconfig.k8s_osdpl_name,
            'namespace': mcpconfig.k8s_osdpl_namespace,
            'plural': mcpconfig.k8s_osdpl_plural,
            'group': mcpconfig.k8s_osdpl_group,
            'version': mcpconfig.k8s_osdpl_version
        }
        self.TFOperator = {
            'name': mcpconfig.k8s_tfoperator_name,
            'namespace': mcpconfig.k8s_tfoperator_namespace,
            'plural': mcpconfig.k8s_tfoperator_plural,
            'group': mcpconfig.k8s_tfoperator_group,
            'version': mcpconfig.k8s_tfoperator_version
        }
        self.TFAnalytic = {
            'name': 'tf-analytics',
            'namespace': mcpconfig.k8s_tfoperator_namespace,
            'plural': 'tfanalytics',
            'group': 'analytics.tf.mirantis.com',
            'version': mcpconfig.k8s_tfoperator_version
        }
        self.TFConfig = {
            'name': 'tf-config',
            'namespace': mcpconfig.k8s_tfoperator_namespace,
            'plural': 'tfconfigs',
            'group': 'config.tf.mirantis.com',
            'version': mcpconfig.k8s_tfoperator_version
        }
        self.TFControl = {
            'name': 'tf-control',
            'namespace': mcpconfig.k8s_tfoperator_namespace,
            'plural': 'tfcontrols',
            'group': 'control.tf.mirantis.com',
            'version': mcpconfig.k8s_tfoperator_version
        }
        self.TFVrouter = {
            'name': 'tf-vrouter',
            'namespace': mcpconfig.k8s_tfoperator_namespace,
            'plural': 'tfvrouters',
            'group': 'vrouter.tf.mirantis.com',
            'version': mcpconfig.k8s_tfoperator_version
        }
        self.helmbundle_plural = 'helmbundles'

    def get_namespaced_deployment(self, name, **kwargs):
        if 'namespace' not in kwargs:
            namespace = self.TFOperator['namespace']
        return self.AppsV1Api.read_namespaced_deployment(name, namespace,
                                                         **kwargs)

    def get_pods(self):
        obj = self.CoreV1Api.list_pod_for_all_namespaces(watch=False)
        return obj

    def get_osdpl(self):
        obj = self.CustomObjectsApi.get_namespaced_custom_object(
            self.osdpl['group'], self.osdpl['version'],
            self.osdpl['namespace'], self.osdpl['plural'], self.osdpl['name']
        )
        return obj

    def _get_namespaced_custom_object(self, obj_dict):
        obj = self.CustomObjectsApi.get_namespaced_custom_object(
            obj_dict['group'], obj_dict['version'], obj_dict['namespace'],
            obj_dict['plural'], obj_dict['name']
        )
        return obj

    def get_tf_operator(self):
        return self._get_namespaced_custom_object(self.TFOperator)

    def get_tf_analytic(self):
        return self._get_namespaced_custom_object(self.TFAnalytic)

    def get_tf_config(self):
        return self._get_namespaced_custom_object(self.TFConfig)

    def get_tf_control(self):
        return self._get_namespaced_custom_object(self.TFControl)

    def get_tf_vrouter(self):
        return self._get_namespaced_custom_object(self.TFVrouter)

    def list_namespaced_helmbundles(self):
        obj = self.CustomObjectsApi.list_namespaced_custom_object(
            self.osdpl['group'], self.osdpl['version'],
            self.osdpl['namespace'], self.helmbundle['plural']
        )
        return obj

    def list_osdpl_helmbndls(self):
        helmbndls = self.list_namespaced_helmbundles()
        f_helmbndls = filter(lambda x:
                             x['metadata']['ownerReferences'][0]['name']
                             == self.osdpl['name'], helmbndls['items'])
        helmbndls['items'] = list(f_helmbndls)
        return helmbndls
