from os import path

from kubernetes import client, config


class K8sEnvClient(object):
    def __init__(self, kubeconfig):
        if path.exists(kubeconfig):
            self.config = config.load_kube_config(config_file=kubeconfig)
        else:
            # In case when tests are run from k8s cluster
            self.config = config.load_incluster_config()
        self.client = client
        self.CoreV1Api = self.client.CoreV1Api()
        self.AppsV1Api = self.client.AppsV1Api()
        self.CustomObjectsApi = self.client.CustomObjectsApi()


class K8sTFOperator(K8sEnvClient):
    def __init__(self, kubeconfig, name, namespace, plural, group, version):
        super(K8sTFOperator, self).__init__(kubeconfig)
        self.name = name
        self.namespace = namespace
        self.plural = plural
        self.group = group
        self.version = version
        self.obj = self.CustomObjectsApi.get_namespaced_custom_object(
            self.group, self.version, self.namespace, self.plural, self.name
        )


class K8sTFAnalytic(K8sEnvClient):
    def __init__(self, kubeconfig, name, namespace, plural, group, version):
        super(K8sTFAnalytic, self).__init__(kubeconfig)
        self.name = name
        self.namespace = namespace
        self.plural = plural
        self.group = group
        self.version = version
        self.obj = self.CustomObjectsApi.get_namespaced_custom_object(
            self.group, self.version, self.namespace, self.plural, self.name
        )

    @property
    def service(self):
        services = self.obj['spec']['api']['services']
        service_name = services[0]['metadata']['name']
        return self.CoreV1Api.read_namespaced_service(
            service_name, self.obj['metadata']['namespace']
        )

    @property
    def service_port_api(self):
        port_name = 'api'
        for port in self.service.spec.ports:
            if port.name == port_name:
                return port


class K8sTFConfig(K8sEnvClient):
    def __init__(self, kubeconfig, name, namespace, plural, group, version):
        super(K8sTFConfig, self).__init__(kubeconfig)
        self.name = name
        self.namespace = namespace
        self.plural = plural
        self.group = group
        self.version = version
        self.obj = self.CustomObjectsApi.get_namespaced_custom_object(
            self.group, self.version, self.namespace, self.plural, self.name
        )


class K8sTFControl(K8sEnvClient):
    def __init__(self, kubeconfig, name, namespace, plural, group, version):
        super(K8sTFControl, self).__init__(kubeconfig)
        self.name = name
        self.namespace = namespace
        self.plural = plural
        self.group = group
        self.version = version
        self.obj = self.CustomObjectsApi.get_namespaced_custom_object(
            self.group, self.version, self.namespace, self.plural, self.name
        )


class K8sTFVrouter(K8sEnvClient):
    def __init__(self, kubeconfig, name, namespace, plural, group, version):
        super(K8sTFVrouter, self).__init__(kubeconfig)
        self.name = name
        self.namespace = namespace
        self.plural = plural
        self.group = group
        self.version = version
        self.obj = self.CustomObjectsApi.get_namespaced_custom_object(
            self.group, self.version, self.namespace, self.plural, self.name
        )
