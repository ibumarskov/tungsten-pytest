from cinderclient import client as cinder_client
from glanceclient import client as glance_client
from heatclient import client as heat_client
from keystoneauth1 import identity
from keystoneauth1 import session
from keystoneclient import client as keystone_client
from neutronclient.v2_0 import client as neutron_client
from novaclient import client as nova_client


class OpenStackClientManager(object):
    """Manager that provides access to the official python clients for
    calling various OpenStack APIs.
    """

    CINDERCLIENT_VERSION = 3
    GLANCECLIENT_VERSION = 2
    HEATCLIENT_VERSION = 1
    KEYSTONECLIENT_VERSION = (3,)
    NEUTRONCLIENT_VERSION = 2
    NOVACLIENT_VERSION = 2

    def __init__(self, auth_url=None, username=None, password=None,
                 project_name=None, user_domain_name='Default',
                 project_domain_name='Default', endpoint_type='public',
                 cert=False, **kwargs):
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.project_name = project_name
        self.user_domain_name = user_domain_name
        self.project_domain_name = project_domain_name
        self.endpoint_type = endpoint_type
        self.cert = cert
        self.kwargs = kwargs

        # Lazy clients
        self._auth = None
        self._compute = None
        self._network = None
        self._volume = None
        self._image = None
        self._orchestration = None

    @classmethod
    def _get_auth_session(cls, auth_url=None, username=None, password=None,
                          project_name=None, user_domain_name='Default',
                          project_domain_name='Default', cert=None):
        if None in (username, password, project_name):
            print(username, password, project_name)
            msg = ("Missing required credentials for identity client. "
                   "username: {username}, password: {password}, "
                   "tenant_name: {project_name}").format(
                username=username,
                password=password,
                project_name=project_name)
            raise Exception(msg)

        if cls.KEYSTONECLIENT_VERSION[0] == 2:
            auth_url = "{}/{}".format(auth_url, "v2.0/")
            auth = identity.v2.Password(auth_url=auth_url,
                                        username=username,
                                        password=password,
                                        tenant_name=project_name)
        elif cls.KEYSTONECLIENT_VERSION[0] == 3:
            auth_url = "{}/{}".format(auth_url, "v3/")
            auth = identity.v3.Password(auth_url=auth_url,
                                        username=username,
                                        password=password,
                                        project_name=project_name,
                                        user_domain_name=user_domain_name,
                                        project_domain_name=project_domain_name
                                        )
        else:
            msg = ("Unsupported Keystone client version. "
                   "KEYSTONECLIENT_VERSION is {}"
                   "".format(cls.KEYSTONECLIENT_VERSION))
            raise Exception(msg)
        auth_session = session.Session(auth=auth, verify=cert)
        return auth_session

    @classmethod
    def get_keystone_client(cls, auth_url=None, username=None, password=None,
                            project_name=None, user_domain='Default',
                            project_domain='Default', cert=None, **kwargs):
        session = cls._get_auth_session(auth_url=auth_url,
                                        username=username,
                                        password=password,
                                        project_name=project_name,
                                        user_domain_name=user_domain,
                                        project_domain_name=project_domain,
                                        cert=cert)
        return keystone_client.Client(version=cls.KEYSTONECLIENT_VERSION,
                                      session=session, **kwargs)

    @classmethod
    def get_nova_client(cls, auth_url=None, username=None, password=None,
                        project_name=None, user_domain='Default',
                        project_domain='Default', cert=None, **kwargs):
        session = cls._get_auth_session(auth_url=auth_url,
                                        username=username,
                                        password=password,
                                        project_name=project_name,
                                        user_domain_name=user_domain,
                                        project_domain_name=project_domain,
                                        cert=cert)
        return nova_client.Client(version=cls.NOVACLIENT_VERSION,
                                  session=session, **kwargs)

    @classmethod
    def get_neutron_client(cls, auth_url=None, username=None, password=None,
                           project_name=None, user_domain='Default',
                           project_domain='Default', cert=None, **kwargs):
        session = cls._get_auth_session(auth_url=auth_url,
                                        username=username,
                                        password=password,
                                        project_name=project_name,
                                        user_domain_name=user_domain,
                                        project_domain_name=project_domain,
                                        cert=cert)
        return neutron_client.Client(session=session, **kwargs)

    @classmethod
    def get_cinder_client(cls, auth_url=None, username=None, password=None,
                          project_name=None, user_domain='Default',
                          project_domain='Default', cert=None, **kwargs):
        session = cls._get_auth_session(auth_url=auth_url,
                                        username=username,
                                        password=password,
                                        project_name=project_name,
                                        user_domain_name=user_domain,
                                        project_domain_name=project_domain,
                                        cert=cert)
        return cinder_client.Client(version=cls.CINDERCLIENT_VERSION,
                                    session=session, **kwargs)

    @classmethod
    def get_glance_client(cls, auth_url=None, username=None, password=None,
                          project_name=None, user_domain='Default',
                          project_domain='Default', cert=None, **kwargs):
        session = cls._get_auth_session(auth_url=auth_url,
                                        username=username,
                                        password=password,
                                        project_name=project_name,
                                        user_domain_name=user_domain,
                                        project_domain_name=project_domain,
                                        cert=cert)
        return glance_client.Client(version=cls.GLANCECLIENT_VERSION,
                                    session=session, **kwargs)

    @classmethod
    def get_heat_client(cls, auth_url=None, username=None, password=None,
                        project_name=None, user_domain='Default',
                        project_domain='Default', cert=None, **kwargs):
        session = cls._get_auth_session(auth_url=auth_url,
                                        username=username,
                                        password=password,
                                        project_name=project_name,
                                        user_domain_name=user_domain,
                                        project_domain_name=project_domain,
                                        cert=cert)
        return heat_client.Client(version=str(cls.GLANCECLIENT_VERSION),
                                  session=session, **kwargs)

    @property
    def keystone(self):
        if self._auth is None:
            self._auth = self.get_keystone_client(
                self.auth_url, self.username, self.password, self.project_name,
                self.user_domain_name, self.project_domain_name, self.cert
            )
        return self._auth

    @property
    def nova(self):
        if self._compute is None:
            self._compute = self.get_nova_client(
                self.auth_url, self.username, self.password, self.project_name,
                self.user_domain_name, self.project_domain_name, self.cert,
                endpoint_type=self.endpoint_type
            )
        return self._compute

    @property
    def neutron(self):
        if self._network is None:
            self._network = self.get_neutron_client(
                self.auth_url, self.username, self.password, self.project_name,
                self.user_domain_name, self.project_domain_name, self.cert,
                interface=self.endpoint_type
            )
        return self._network

    @property
    def cinder(self):
        if self._volume is None:
            self._volume = self.get_cinder_client(
                self.auth_url, self.username, self.password, self.project_name,
                self.user_domain_name, self.project_domain_name, self.cert,
                endpoint_type=self.endpoint_type
            )
        return self._volume

    @property
    def glance(self):
        # TO DO: add endpoint type support
        if self._image is None:
            self._image = self.get_glance_client(
                self.auth_url, self.username, self.password, self.project_name,
                self.user_domain_name, self.project_domain_name, self.cert
            )
        return self._image

    @property
    def heat(self):
        if self._orchestration is None:
            self._orchestration = self.get_heat_client(
                self.auth_url, self.username, self.password, self.project_name,
                self.user_domain_name, self.project_domain_name, self.cert,
                endpoint_type=self.endpoint_type
            )
        return self._orchestration
