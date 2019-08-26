from kubernetes import client, config


class K8sEnvClient:
    def __init__(self, kubeconfig, osdpl_name, osdpl_namespace,
                 osdpl_group='lcm.mirantis.com', osdpl_version='v1alpha1'):
        self.config = config.load_kube_config(config_file=kubeconfig)
        self.v1 = client.CoreV1Api()
        self.v1alpha1 = client.CustomObjectsApi()
        self.osdpl_name = osdpl_name
        self.osdpl_namespace = osdpl_namespace
        self.osdpl_plural = 'openstackdeployments'
        self.osdpl_group = osdpl_group
        self.osdpl_version = osdpl_version
        self.helmbundle_plural = 'helmbundles'

    def get_pods(self):
        obj = self.v1.list_pod_for_all_namespaces(watch=False)
        return obj

    def get_osdpl(self):
        obj = self.v1alpha1.get_namespaced_custom_object(
            self.osdpl_group, self.osdpl_version, self.osdpl_namespace,
            self.osdpl_plural, self.osdpl_name)
        return obj

    def list_namespaced_helmbundles(self):
        obj = self.v1alpha1.list_namespaced_custom_object(
            self.osdpl_group, self.osdpl_version, self.osdpl_namespace,
            self.helmbundle_plural)
        return obj

    def list_osdpl_helmbndls(self):
        helmbndls = self.list_namespaced_helmbundles()
        f_helmbndls = filter(lambda x:
                             x['metadata']['ownerReferences'][0]['name']
                             == self.osdpl_name, helmbndls['items'])
        helmbndls['items'] = list(f_helmbndls)
        return helmbndls
