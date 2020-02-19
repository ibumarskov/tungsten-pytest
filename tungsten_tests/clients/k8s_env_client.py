from kubernetes import client, config


class K8sEnvClient(object):
    def __init__(self, kubeconfig):
        if kubeconfig:
            self.config = config.load_kube_config(config_file=kubeconfig)
        else:
            # In case when tests are run from k8s cluster
            self.config = config.load_incluster_config()
        self.client = client
        self.CoreV1Api = self.client.CoreV1Api()
        self.AppsV1Api = self.client.AppsV1Api()
        self.CustomObjectsApi = self.client.CustomObjectsApi()

    def filter_pods_by_owner_refence(self, namespace, kind, name):
        pods = self.CoreV1Api.list_namespaced_pod(namespace)
        filtered_pods = []
        for pod in pods.items:
            for owner in pod.metadata.owner_references:
                if owner.kind == kind and owner.name == name:
                    filtered_pods.append(pod)
                    break
        return filtered_pods


class K8sCustomObject(K8sEnvClient):
    def __init__(self, kubeconfig, name, namespace, plural, group, version):
        super(K8sCustomObject, self).__init__(kubeconfig)
        self.name = name
        self.namespace = namespace
        self.plural = plural
        self.group = group
        self.version = version
        self.obj = self.CustomObjectsApi.get_namespaced_custom_object(
            self.group, self.version, self.namespace, self.plural, self.name
        )

    def filter_pods_by_owner_refence(self, kind, name):
        return super(K8sCustomObject, self).filter_pods_by_owner_refence(
            self.namespace, kind, name)

    def read_namespaced_endpoints(self, name, **kwargs):
        return self.CoreV1Api.read_namespaced_endpoints(name, self.namespace,
                                                        **kwargs)

    def read_namespaced_service(self, name, **kwargs):
        return self.CoreV1Api.read_namespaced_service(name, self.namespace,
                                                      **kwargs)
